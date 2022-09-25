import ply.lex as lex
import Manager

mn = Manager.mn

# reserved keywords
keywords = {
    'if': 'IF',
    'while': 'WHILE',
    'goto': 'GOTO',
    'left': 'LEFT',
    'right': 'RIGHT',
    'write': 'WRITE',
    'halt': 'HALT'
}

# tokens of a 0-1 TM
tokens = [
             'SYMBOL',
             'ID',

         ] + list(keywords.values())

t_ignore = ' \t'


def t_SYMBOL(t):
    r"0|1"
    t.value = int(t.value)
    return t


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = keywords.get(t.value, 'ID')
    return t


def t_COMMENT(t):
    r"[\#|//].*"
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


literals = ':()'


def t_lparen(t):
    r'\('
    t.type = '('
    return t


def t_rparen(t):
    r'\)'
    t.type = ')'
    return t


def t_error(t):
    print(f'Illegal token at {t.lexer.lineno}: {t.value}')
    t.lexer.skip()
