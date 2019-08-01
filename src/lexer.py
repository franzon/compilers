import ply.lex as lex

reserved = {
    'se': 'IF',
    'então': 'THEN',
    'senão': 'ELSE',
    'fim': 'END',
    'repita': 'REPEAT',
    'até': 'UNTIL',
    'leia': 'READ',
    'escreva': 'WRITE',
    'retorna': 'RETURN',
    'inteiro': 'INTEGER',
    'flutuante': 'FLOAT'
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

    'FLOAT_LITERAL',
    'INTEGER_LITERAL',

    'SQUARE_BRACKET_L',
    'SQUARE_BRACKET_R',
    'PARENTESIS_L',
    'PARENTESIS_R',

    'COMMENT'
] + list(reserved.values())


def t_COMMENT(t):
    r'\{[^\}]*[^\{]*\}'
    contador = t.value.count("\n")
    t.lexer.lineno += contador


def t_FLOAT_LITERAL(t):
    r'^ [+-]?\d+(?: \.\d*(?: [eE][+-]?\d+)?)?$'
    t.value = float(t.value)
    return t


def t_INTEGER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


t_COLLON = r':'
t_SEMICOLLON = r';'
t_COMMA = r','
t_ASSIGN = r':='
t_LESSER = r'<'
t_GREATER = r'>'
t_LESSER_EQUALS = r'<='
t_GREATER_EQUALS = r'>='
t_EQUALS = r'='
t_NOT_EQUALS = r'<>'
t_AND = r'\&\&'
t_OR = r'\|\|'
t_NOT = r'!'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVISION = r'\/'
t_SQUARE_BRACKET_L = r'\['
t_SQUARE_BRACKET_R = r'\]'
t_PARENTESIS_L = r'\('
t_PARENTESIS_R = r'\)'


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

arq = open('./tests/lexer_001.tpp')
lexer.input(arq.read())
arq.close()
tokens = [t for t in lexer]

for tok in tokens:
    print(tok)
