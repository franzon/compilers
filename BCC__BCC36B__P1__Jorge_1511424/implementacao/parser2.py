import ply.yacc as yacc
from lexer import tokens


class Node:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return '[{}] {}'.format(self.type, self.value)


def p_fator(p):
    '''fator : numero'''
    p[0] = Node('fator', p[1])


def p_numero_1(p):
    '''numero : INTEIRO_LITERAL'''

    p[0] = Node('inteiro', p[1])


def p_numero_2(p):
    '''numero : FLUTUANTE_LITERAL'''

    p[0] = Node('flutuante', p[1])


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()
