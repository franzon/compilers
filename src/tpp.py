#!/usr/bin/env python3

import sys
from parser import parser

program_name = sys.argv[1]
f = open(program_name)
result = parser.parse(f.read())
f.close()

print(result)
