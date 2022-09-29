from ply import lex
from ply import yacc
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import lex_rules
import yacc_rules
import Manager

if __name__ == '__main__':

    filename = 'src/min.txt'

    with open(filename, 'r') as f:
        text = f.read()

    lexer = lex.lex(module=lex_rules)
    parser = yacc.yacc(module=yacc_rules)
    parser.parse(text)

    sm = yacc_rules.mn.sm

    for s in sm.states:
        print(f'{s}')

    # convert to tm script of 5-tuples
    # simulated at https://morphett.info/turing/turing.html

    script = ''


    def sym(x):
        return 1 if x == 1 else '_'  # convert all 0 to _ (blank)


    action_convert = {
        'left': 'l', 'right': 'r',
        'write 1': sym(1), 'write 0': sym(0),
        None: '*',
        'halt': 'h'
    }

    with open(filename, 'r') as f:
        text = f.readlines()

    mn = Manager.mn

    for state in sm.states:
        script += f'; state {state.name}'
        lineno = mn.get_state_lineno(state)
        if lineno:
            script += f' # line {lineno}\t{text[lineno - 1]}'
        else:
            script += '\n'
        for x, t in state.transitions.items():
            if t.act == 'left' or t.act == 'right':
                script += f'{state.name} {sym(x)} * {action_convert[t.act]} {t.next_state.name}\n'
            elif t.act == 'halt':
                continue  # skip it
            else:
                script += f'{state.name} {sym(x)} {action_convert[t.act]} * {t.next_state.name}\n'

        script += '\n'

    with open('script.txt', 'w') as f:
        f.write(script)

    print('Parse done!')

    ##################
    # plot as a graph

    # net = Network(notebook=False, directed=True, height='2000px')
    # net.add_nodes(
    #     [s.name for s in sm.states],
    #     title=[f'{s.name}' for s in sm.states],
    #     label=[f'line {mn.get_state_lineno(s)}' for s in sm.states],
    #     y=[float(s.name) * 90 for s in sm.states]
    # )
    # for n in net.nodes:
    #     n.update({'physics': False})
    # for s in sm.states:
    #     for x, t in s.transitions.items():
    #         net.add_edge(s.name, t.next_state.name, label=f'{t.x}: {action_convert[t.act]}'.upper())
    #
    # net.show_buttons(filter_=['physics', 'nodes', 'edge'])
    # net.show('tm.html')
