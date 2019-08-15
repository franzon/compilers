import ply.lex as lex

reserved = {
    'se': 'SE',
    'então': 'ENTAO',
    'senão': 'SENAO',
    'fim': 'FIM',
    'repita': 'REPITA',
    'até': 'ATE',
    'leia': 'LEIA',
    'escreva': 'ESCREVA',
    'retorna': 'RETORNA',
    'flutuante': 'FLUTUANTE',
    'inteiro': 'INTEIRO'
}

tokens = [
    'IDENTIFICADOR',
    'FLUTUANTE_LITERAL',
    'INTEIRO_LITERAL',

    'DOIS_PONTOS',
    'VIRGULA',
    'ATRIBUICAO',

    'IGUAL',
    'DIFERENTE',
    'MENOR',
    'MENOR_IGUAL',
    'MAIOR',
    'MAIOR_IGUAL',

    'E',
    'OU',
    'NAO',

    'ADICAO',
    'SUBTRACAO',
    'MULTIPLICACAO',
    'DIVISAO',

    'ABRE_PARENTESES',
    'FECHA_PARENTESES',
    'ABRE_COLCHETES',
    'FECHA_COLCHETES',

    'COMENTARIO'
] + list(reserved.values())


def t_COMENTARIO(t):
    r'\{[^\}]*[^\{]*\}'
    contador = t.value.count("\n")
    t.lexer.lineno += contador


def t_IDENTIFICADOR(t):
    r'[a-zA-Z_záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ][a-zA-Z_0-9záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t


def t_FLUTUANTE_LITERAL(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


def t_INTEIRO_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_DOIS_PONTOS = r':'
t_VIRGULA = r','
t_ATRIBUICAO = r':='
t_IGUAL = r'='
t_DIFERENTE = r'<>'
t_MENOR = r'<'
t_MENOR_IGUAL = r'<='
t_MAIOR = r'>'
t_MAIOR_IGUAL = r'>='
t_E = r'\&\&'
t_OU = r'\|\|'
t_NAO = r'!'
t_ADICAO = r'\+'
t_SUBTRACAO = r'\-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'\/'
t_ABRE_PARENTESES = r'\('
t_FECHA_PARENTESES = r'\)'
t_ABRE_COLCHETES = r'\['
t_FECHA_COLCHETES = r'\]'


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Caractere inválido: '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
