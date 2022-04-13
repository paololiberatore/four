#!/usr/bin/env python3
#
# forget by iteratively minimized resolution closure (prime implicates)

import logic
import itertools
import sys


# prime implicates: repeatedly minimize the resolution closure

def close(s):
    s = logic.minimal(s)
    n = set()
    t = 0
    while n != s:
        g = set()
        for a in s:
           for b in s:
               r = logic.resolve(a, b)
               g |= r
               t = t + logic.formulasize(r)
        print('#T=' + str(t))
        n = s
        s = logic.minimal(g, n)
        print('#T=' + str(logic.formulasize(g) * logic.formulasize(s)))
        print('#M=' + str(logic.formulasize(s)), logic.formulatostring(s))
    return n


# forget by resolution closure

def forget(v, f):
    f = logic.minimal(logic.detautologize(f))
    a = close(f)
    r = {c for c in a if not logic.present(v, c)}
    logic.formulaprint(r, parsable = True)


# analyze a formula

def analyze(d, v, *s):
    print('##', d, '##')
    print('# first argument:', v)
    print('# other arguments:', ' '.join(s))
    e = logic.literalset(v)
    print('# forget:', ' '.join(e))
    f = logic.formula(*s)
    logic.formulaprint(f, '# formula:')
    r = forget(e, f)


# do not analyze a formula

def donotanalyze(d, result, *s):
    pass


# commandline arguments

if len(sys.argv) <= 1 or sys.argv[1] == '-h':
    if len(sys.argv) <= 1:
        print('no argument')
    print('usage:')
    print('\tclose.py [-t] testfile.py')
    print('\tclose.py -c vars clause clause...' )
    print('\tclose.py -f vars file')
    print('\t\tvars: abc')
    print('\t\tclause: ab->c, ab=c, abc (= a or b or c)')
elif sys.argv[1] == '-c':
    analyze('cmdline formula', *sys.argv[2:])
elif sys.argv[1] == '-f':
    f = set(open(sys.argv[3]).read().split())
    analyze(sys.argv[3], sys.argv[2], *f)
elif sys.argv[1] == '-t':
    exec(open(sys.argv[2]).read())
else:
    exec(open(sys.argv[1]).read())

