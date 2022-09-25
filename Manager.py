from state_machine import StateMachine


class Manager:
    """
    A class for handling processing in tokenizing and parsing.

    """

    def __init__(self):
        self.sm = StateMachine()
        self.last_state = None

        # labels recording
        self.label_pos = {}  # label -> state, each label points to only one stmt
        self.labels = {}  # record all appeared labels, label -> defined line
        self.last_saw_label = None
        self.last_saw_label_line = 0

        # delayed non-label transitions
        self.delayed_transitions = []  # (x, act, src_state)

        # delayed label jump transitions
        self.delayed_jumps = {}  # label -> List of (x, act, src_state)

        # warnings and errors
        self.warnings = []
        self.errors = []

    ###############################################
    # label recording

    def associate_label(self, label, state):
        """
        Associate a label to a stmt's state.
        :param label:
        :param state:
        :return:
        """
        assert label not in self.label_pos  # assert appear once
        state.label = label
        self.label_pos[label] = state
        self._connect_delayed_jumps(label, state)

    def get_label(self, label):
        return self.label_pos[label]

    ###############################################
    # delay non-label transitions

    def delay_transition(self, x, act, src_state):
        self.delayed_transitions.append((x, act, src_state))

    def _connect_delayed_transitions(self, state):
        for x, act, src_state in self.delayed_transitions:
            src_state.add_transition(x, state, act)
        self.delayed_transitions.clear()

    ###############################################
    # delay label jumps

    def _delay_label_jump(self, x, act, src_state, label):
        t = self.delayed_jumps.get(label, [])
        t.append((x, act, src_state))
        self.delayed_jumps[label] = t

    def _connect_delayed_jumps(self, label, state):
        if label not in self.delayed_jumps:
            return
        t = self.delayed_jumps[label]
        for x, act, src_state in t:
            src_state.add_transition(x, state, act)
        self.delayed_jumps.pop(label)  # no more delay

    def connect_jumps(self, x, act, src_state, label):
        try:
            target_state = self.get_label(label)
            src_state.add_transition(x, target_state, act)
        except KeyError:
            self._delay_label_jump(x, act, src_state, label)

    ###############################################
    # state management

    def add_stmt_state(self):
        """
        Add a beginning state for a stmt. Also connect delayed transitions.
        :return: added state
        """
        s = self.sm.add_state()
        self._connect_delayed_transitions(s)
        return s

    def add_state(self):
        return self.sm.add_state()

    def program_end(self):
        def is_halt(s):
            return len(s.transitions) == 0

        if self.delayed_jumps:
            # there are jumps to undefined labels
            for lb, jmps in self.delayed_jumps:
                for x, act, src_state in jmps:
                    self.errors.append(
                        f'Jumps to undefined label {lb}: ({x}:{act}->{src_state.name})')
        if self.delayed_transitions:
            # an ending state must be added
            end = self.add_stmt_state()
            self.sm.end_state = end

        for w in self.warnings:
            print(f'[waring] {w}')

        if self.errors:
            for e in self.errors:
                print(f'[error] {e}')
            raise Exception('Parse error exists.')

    ###############################################
    # utils

    def reverse_symbol(self, sym):
        return (sym + 1) % 2


mn = Manager()  # shared across files
