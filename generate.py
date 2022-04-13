#!/usr/bin/env python3
#
# generate a random set of clauses

import random
import math
import sys



# generate long negative clauses and implications among pairs of variables

def generateequivalent1(vars, clauses):
    pos = [      str(chr(x)) for x in range(ord('a'), ord('a') + vars)]
    neg = ['-' + str(chr(x)) for x in range(ord('a'), ord('a') + vars)]
    for i in range(0, int(math.sqrt(vars)) + 1):
        for l in neg:
            if random.randint(0, 10) < 5:
                print(l, end = '')
        print()
    for x in pos:
        for i in range(0, int(math.sqrt(vars)) + 1):
            y = neg[random.randint(0, vars - 1)]
            print(y + x)

def generateequivalent2(vars, clauses):
    pos = [      str(chr(x)) for x in range(ord('a'), ord('a') + vars)]
    neg = ['-' + str(chr(x)) for x in range(ord('a'), ord('a') + vars)]
    for i in range(0, int(math.sqrt(vars)) + 1):
        for j in range(0, int(math.sqrt(vars)) + 1):
            l = neg[random.randint(0, vars - 1)]
            print(l, end = '')
        print()
    for x in pos:
        for i in range(0, int(math.sqrt(vars)) + 1):
            l = neg[random.randint(0, vars - 1)]
            print(l + x)

def generateequivalent3(vars, clauses):
    pos = [      str(chr(x)) for x in range(ord('a'), ord('a') + vars)]
    neg = ['-' + str(chr(x)) for x in range(ord('a'), ord('a') + vars)]
    nneg = set(neg)
    for i in range(0, int(math.sqrt(vars)) + 1):
        r = set()
        p = list(nneg)
        for j in range(0, int(math.sqrt(vars)) + 1):
            l = p[random.randrange(0, len(p))]
            print(l, end = '')
            r |= {l}
        nneg -= r
        print()
    for x in pos:
        for i in range(0, int(math.sqrt(vars)) + 1):
            y = neg[random.randrange(0, vars)]
            print(y + x)

generateequivalent = generateequivalent1


# generate clauses of three variables

def generate3(vars, clauses):
    pos = [      str(chr(x)) for x in range(ord('a'), ord('a') + vars)]
    neg = ['-' + str(chr(x)) for x in range(ord('a'), ord('a') + vars)]
    lit = pos + neg
    for c in range(0, clauses):
        len = 3
        clause = random.sample(lit, len)
        print(''.join(clause), end = ' ')
    print()



# generate clauses of 2, 3 and sqrt(vars+1) literals

def generate23sqrt(vars, clauses):
    pos = [      str(chr(x)) for x in range(ord('a'), ord('a') + vars)]
    neg = ['-' + str(chr(x)) for x in range(ord('a'), ord('a') + vars)]
    lit = pos + neg
    for c in range(0, clauses):
        len = random.randint(2, 4)
        if len == 4:
            len = int(math.sqrt(vars + 1))
        clause = random.sample(lit, len)
        print(''.join(clause), end = ' ')
    print()


# cmdline arguments

generate = generate3
idx = 1
if len(sys.argv) > idx and sys.argv[idx] == '-3':
    generate = generate3
    idx = idx + 1
elif len(sys.argv) > idx and sys.argv[idx] == '-23sqrt':
    generate = generate23sqrt
    idx = idx + 1
elif len(sys.argv) > idx and sys.argv[idx] == '-equiv':
    generate = generateequivalent
    idx = idx + 1

if len(sys.argv) <= idx or sys.argv[idx] == '-h':
    if len(sys.argv) <= idx or sys.argv[idx] != '-h':
        print('argument(s) missing')
    print('usage:')
    print('\tgenerate.py [-3|-23sqrt|-equiv] vars clauses')
else:
    vars = int(sys.argv[idx])
    clauses = int(sys.argv[idx + 1])
    generate(vars, clauses)

