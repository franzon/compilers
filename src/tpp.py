#!/usr/bin/env python3

import sys
from lexer import lexer


program_name = sys.argv[1]
f = open(program_name)
lexer.input(f.read())
f.close()


for tok in lexer:
    print(tok)
