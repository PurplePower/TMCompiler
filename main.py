from ply import lex
from ply import yacc
import lex_rules
import yacc_rules

if __name__ == '__main__':

    with open('src.txt', 'r') as f:
        text = f.read()

    lexer = lex.lex(module=lex_rules)
    parser = yacc.yacc(module=yacc_rules)
    parser.parse(text)

    sm = yacc_rules.mn.sm

    for s in sm.states:
        print(f'{s}')

    # convert to tm script

    script = ''


    def sym(x):
        return 1 if x == 1 else '_'  # convert all 0 to _ (blank)


    action_convert = {
        'left': 'l', 'right': 'r',
        'write 1': sym(1), 'write 0': sym(0),
        None: '*'
    }

    for state in sm.states:
        script += f'; state {state.name}\n'
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