import ply.lex as lex
import colorama

colorama.init()


class TppLexer(object):

    reserved = {
        'se': 'SE',
        'então': 'ENTAO',
        'senão': 'SENAO',
        'repita': 'REPITA',
        'até': 'ATE',
        'fim': 'FIM',
        'retorna': 'RETORNA',
        'leia': 'LEIA',
        'escreva': 'ESCREVA',
        'flutuante': 'FLUTUANTE',
        'inteiro': 'INTEIRO'
    }

    tokens = [

        'SOMA',
        'SUBTRACAO',
        'MULTIPLICACAO',
        'DIVISAO',

        'IGUALDADE',
        'DESIGUALDADE',
        'ATRIBUICAO',
        'MENOR',
        'MENOR_IGUAL',
        'MAIOR',
        'MAIOR_IGUAL',

        'VIRGULA',
        'DOIS_PONTOS',

        'ID',
        'NUM_INTEIRO',
        'NUM_PONTO_FLUTUANTE',
        'NUM_NOTACAO_CIENTIFICA',

        'E_LOGICO',
        'OU_LOGICO',
        'NEGACAO',

        'ABRE_PAR',
        'FECHA_PAR',
        'ABRE_COL',
        'FECHA_COL',

        'COMENTARIO'
    ] + list(reserved.values())

    t_DOIS_PONTOS = r':'
    t_VIRGULA = r','
    t_ATRIBUICAO = r':='
    t_IGUALDADE = r'='
    t_DESIGUALDADE = r'<>'
    t_MENOR = r'<'
    t_MENOR_IGUAL = r'<='
    t_MAIOR = r'>'
    t_MAIOR_IGUAL = r'>='
    t_E_LOGICO = r'\&\&'
    t_OU_LOGICO = r'\|\|'
    t_NEGACAO = r'!'
    t_SOMA = r'\+'
    t_SUBTRACAO = r'\-'
    t_MULTIPLICACAO = r'\*'
    t_DIVISAO = r'\/'
    t_ABRE_PAR = r'\('
    t_FECHA_PAR = r'\)'
    t_ABRE_COL = r'\['
    t_FECHA_COL = r'\]'

    t_ignore = ' \t'

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_COMENTARIO(self, t):
        r'{.*}'
        contador = t.value.count("\n")
        t.lexer.lineno += contador

    def t_ID(self, t):
        r'[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ_][0-9A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ_]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_NUM_PONTO_FLUTUANTE(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_NUM_NOTACAO_CIENTIFICA(self, t):
        r'\d+(\.?)[eE](-)?\d+'
        t.value = float(t.value)
        return t

    def t_NUM_INTEIRO(self, t):
        r'0|[1-9]\d*'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Caractere inválido: '%s'" % t.value[0])
        t.lexer.skip(1)

    def input_data(self, data):
        self.lexer.input(data)

    def print_tokens(self):
        count = 0
        for tok in self.lexer:
            print(colorama.Fore.BLUE, '[', tok.type, ']',
                  colorama.Style.RESET_ALL, ' ', tok.value, sep='')
            count += 1
        print('--------------')
        print('Número de tokens: ', count)
