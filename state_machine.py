from typing import List


class Transition:
    """
    An edge of a state going out.

    """

    def __init__(self, x, next_state, act=None):
        self.x = x
        self.next_state = next_state
        self.act = act

    def __str__(self):
        return f'{self.x}: {self.act or ""} -> {self.next_state.name}'


class State:
    def __init__(self, name):
        self.name = name
        self.label = None
        self.transitions = {}  # dict of input: Transition

    def __str__(self):
        s = f'state {self.name}: label {self.label}, {len(self.transitions)} transitions\n'
        for x, t in self.transitions.items():
            s += str(t) + '\n'
        return s

    def add_transition(self, x, next_state, act):
        self.transitions[x] = Transition(x, next_state, act)

    def add_transitions(self, transitions):
        self.transitions.update(transitions)


class StateMachine:
    def __init__(self):
        self.states: List[State] = []
        self.state_count = 0
        self.end_state = None

    def add_state(self):
        state = State(self.state_count)
        self.state_count += 1
        self.states.append(state)
        return state

    pass
