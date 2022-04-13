#!/usr/bin/env python3
#
# forget by resolving out variables (variable elimination, davis-putnam)

import logic
import sys


# remove a variable from a formula by resolving it out

def resolveout(x, f):
    print('# formula ' + logic.formulatostring(f))
    print('# resolve out ' + x)
    p = {c for c in f if x in c}
    n = {c for c in f if logic.negate(x) in c}
    r = set()
    t = 1
    for c in p:
        for d in n:
           s = logic.resolve(c, d)
           r |= s
           t = t + logic.formulasize(r)
    print('#T=' + str(t))
    print('#M=' + str(logic.formulasize(f) + logic.formulasize(r)))
    return f - p - n | r


# remove a sequence of variables from a formula

def forget(v, f):
    f = logic.minimal(logic.detautologize(f))
    for x in v:
        f = resolveout(x, f)
    logic.formulaprint(f, parsable = True)


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
    print('\teliminate.py [-t] testfile.py')
    print('\teliminate.py -c vars clause clause...' )
    print('\teliminate.py -f vars formula')
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

