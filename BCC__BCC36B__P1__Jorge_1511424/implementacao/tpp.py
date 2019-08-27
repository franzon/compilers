#!/usr/bin/env python3

import sys
import os
import argparse
import lexer

parser = argparse.ArgumentParser(description='Compilador da linguagem TPP')
parser.add_argument('source', type=str, help='Arquivo de entrada')

args = parser.parse_args()

arq = open(args.source, 'r', encoding='utf-8')
data = arq.read()
arq.close()

tppLexer = lexer.TppLexer()
tppLexer.input_data(data)

tppLexer.print_tokens()

# # program_name = sys.argv[1]
# f = open(os.path.join(os.path.dirname(__file__), '../codes/test.tpp'))
# result = parser.parse(f.read())
# f.close()


# def imprimir(node, i):
#     print(' ' * i, node)

#     if node.value is not None:
#         if node.value is Node:
#             imprimir(node.value, i+1)
#         else:
#             for n in node.value:
#                 imprimir(n, i+1)


# imprimir(result, 0)
