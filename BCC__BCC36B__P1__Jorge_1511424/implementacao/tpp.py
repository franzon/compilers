#!/usr/bin/env python3

import sys
import os
import argparse
# import lexer
import tpp_parser

parser = argparse.ArgumentParser(description='Compilador da linguagem TPP')
parser.add_argument('source', type=str, help='Arquivo de entrada')

args = parser.parse_args()

arq = open(args.source, 'r', encoding='utf-8')
data = arq.read()
arq.close()

# tppLexer = lexer.TppLexer()
# tppLexer.input_data(data)

# tppLexer.print_tokens()

tppParser = tpp_parser.TppParser()
tppParser.input_data(data)
tppParser.build_graph()
