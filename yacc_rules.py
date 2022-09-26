import ply.yacc as yacc
from lex_rules import tokens
from state_machine import StateMachine
import Manager

mn = Manager.mn

start = 'program'


def p_error(p):
    print(f'Syntax error!')


def p_empty(p):
    'empty :'
    pass


def p_program(p):
    'program : stmt_seq'
    # handle ending state
    mn.program_end()

    p[0] = p[1]


def p_stmt_seq(p):
    """stmt_seq : stmt_seq stmt
                | empty
    """
    if p[1] is not None:
        p[0] = p[2]
    else:
        p[0] = None


def p_stmt(p):
    """stmt : action
            | while_stmt
            | if_stmt
            | goto_stmt
            | labelled_stmt
    """
    if p[1]['type'] == 'action' and 'state' not in p[1]:
        # action as a single stmt, create state for it
        # not a labelled action, labelled already created at stmt:action
        state = mn.add_stmt_state(p.lineno(1))
        act = p[1]['action']
        if act != 'halt':
            mn.delay_transition(0, act, state)
            mn.delay_transition(1, act, state)
        p[1].update(state=state)

    mn.last_state = p[1]['state']

    p[0] = p[1]


def p_action(p):
    """action   : LEFT
                | RIGHT
                | WRITE SYMBOL
                | HALT
    """
    # action as a single stmt created at stmt : action rule
    act = p[1]
    if act == 'write':
        act += ' ' + str(p[2])

    p[0] = {'type': 'action', 'action': act}
    p.set_lineno(0, p.lineno(1))


def p_label(p):
    """label : ID"""
    p[0] = p[1]
    p.set_lineno(0, p.lineno(1))


def p_labelled_stmt(p):
    """labelled_stmt : label ':' stmt"""
    label = p[1]
    mn.define_label(label, p.lineno(1))
    mn.associate_label(label, p[3]['state'])
    p[0] = p[3]
    p[0].update(labelled=True)


def p_while_stmt(p):
    """while_stmt : WHILE '(' SYMBOL ')' action"""
    state = mn.add_stmt_state(p.lineno(1))
    sym = p[3]
    state.add_transition(sym, state, p[5]['action'])  # the loop

    # transition to exit loop set later
    mn.delay_transition(mn.reverse_symbol(sym), None, state)

    p[0] = {'state': state, 'type': 'while_stmt'}


def p_goto_stmt(p):
    """goto_stmt : GOTO label"""
    state = mn.add_stmt_state(p.lineno(1))
    label = p[2]
    mn.connect_jumps(0, None, state, label)  # unconditional jump
    mn.connect_jumps(1, None, state, label)  # unconditional jump too

    p[0] = {'state': state, 'type': 'goto_stmt', 'goto_label': label}


def p_if_stmt(p):
    """if_stmt  : IF '(' SYMBOL ')' action
                | IF '(' SYMBOL ')' GOTO label
    """
    state = mn.add_stmt_state(p.lineno(1))
    sym = p[3]
    if isinstance(p[5], dict):  # action
        mn.delay_transition(sym, p[5]['action'], state)
        mn.delay_transition(mn.reverse_symbol(sym), None, state)
    else:
        mn.connect_jumps(sym, None, state, p[6])
        mn.delay_transition(mn.reverse_symbol(sym), None, state)

    p[0] = {'state': state, 'type': 'if_stmt'}
