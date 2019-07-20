import ply.lex as lex

reserved = {
    'se': 'SE',
    'entao': 'ENTAO',
    'senao': 'SENAO',
    'fim': 'FIM',
    'repita': 'REPITA',
    'ate': 'ATE',
    'leia': 'LEIA',
    'escreva': 'ESCREVA',
    'retorna': 'RETORNA'
}

tokens = [
    'COLLON',
    'SEMICOLLON',
    'COMMA',

    'ASSIGN',

    'LESSER',
    'GREATER',
    'LESSER_EQUALS',
    'GREATER_EQUALS',
    'EQUALS',
    'NOT_EQUALS',

    'PLUS',
    'MINUS',
    'TIMES',
    'DIVISION',

    'AND',
    'OR',
    'NOT',

    'ID',

    'INTEGER',
    'FLOAT',

    'SQUARE_BRACKET_L',
    'SQUARE_BRACKET_R',
    'PARENTESIS_L',
    'PARENTESIS_R'
] + list(reserved.values())


t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVISION = r'\/'

t_INTEGER = r'\d+'

t_PARENTESIS_L = r'\('
t_PARENTESIS_R = r'\)'


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

data = '3 + (3*4) - 2'
lexer.input(data)

tokens = [t for t in lexer]

print(tokens)
