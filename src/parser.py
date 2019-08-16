import ply.yacc as yacc
from lexer import tokens


def p_programa(p):
    'programa: lista_declaracoes'
    p[0] = p[1]


def p_lista_declaracoes(p):
    '''lista_declaracoes: lista_declaracoes declaracao
                        | declaracao'''

    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = [p[1]]


def p_declaracao(p):
    '''declaracao: declaracao_variaveis
                 | inicializacao_variaveis
                 | declaracao_funcao'''

    p[0] = p[1]


def p_declaracao_variaveis(p):
    'declaracao_variaveis: tipo DOIS_PONTOS lista_variaveis'
    p[0] = ('declaracao_variaveis', p[1], p[3])


def p_inicializacao_variaveis(p):
    'inicializacao_variaveis: atribuicao'
    p[0] = p[1]


def p_lista_variaveis(p):
    '''lista_variaveis: lista_variaveis VIRGULA var
                      | var'''

    if len(p) == 4:
        p[0] = p[1] + p[3]
    else:
        p[0] = [p[1]]


def p_var(p):
    '''var: IDENTIFICADOR
          | IDENTIFICADOR indice'''

    if len(p) == 3:
        p[0] = ('var_array', p[1], p[2])
    else:
        p[0] = ('var', p[1])


def p_indice(p):
    '''indice: indice ABRE_COLCHETES expressao FECHA_COLCHETES
             | ABRE_COLCHETES expressao FECHA_COLCHETES'''

    if len(p) == 5:
        p[0] = ('indice [')


def p_numero(p):
    '''numero: INTEIRO_LITERAL
             | FLUTUANTE_LITERAL'''
    p[0] = p[1]


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()
