#!/usr/bin/env python3

import sys
import os
from parser2 import parser, Node

# program_name = sys.argv[1]
f = open(os.path.join(os.path.dirname(__file__), '../codes/test.tpp'))
result = parser.parse(f.read())
f.close()


def imprimir(node, i):
    print(' ' * i, node)

    if node.value is not None:
        if node.value is Node:
            imprimir(node.value, i+1)
        else:
            for n in node.value:
                imprimir(n, i+1)


imprimir(result, 0)
