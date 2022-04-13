#!/usr/bin/env python3
#
# forget by nondeterministic linear resolution

import logic
import os
import sys


# advance linear resolution by resolving the center clause

def replace(other, clause, line, vars, formula):
    print('# line =', '[' + logic.formulatostring(line) + ']')
    print('#', logic.clausetostring(clause), '*', end = ' ')
    print(logic.clausetostring(other), end = ' ')
    # print(v + ' ' + logic.clausetostring(other), end = ' ')
    result = logic.resolve(clause, other)
    if not result:
        print('==>', 'T     tautology')
        return
    generated = next(iter(result))
    print('==>', logic.clausetostring(generated), end = ' ')
    if other not in formula and not generated < clause:
        print('    not subclause', end = ' ')
	# s-linear resolution
	# print()
        # print('#T=' + str(len(generated) + len(clause)))
        # return
    for previous in line:
        if previous <= generated:
            print('    subsumed')
            print('#T=' + str(logic.formulasize(line)))
            return
    nline = {previous for previous in line if not generated < previous}
    nline = nline | result
    print()
    print('#T=' + str(logic.formulasize(line)))

    linear(generated, nline, vars, formula)


# linear resolution

def linear(clause, line, vars, formula):
    print('# center:', logic.clausetostring(clause))
    lits = logic.literals(vars)

    toreplace = logic.variable(clause) & set(vars)
    if not toreplace:
        print(logic.clausetostring(clause, parsable = True))
        return

    # a-ordering resolution
    toreplace = min(toreplace)

    l = logic.negate(min(clause & logic.literals(toreplace)))
    print('# literal:', l)
    candidates = {c for c in formula | line if l in c}
    print('# candidates:', logic.formulatostring(candidates))
    print('#T=' + str(logic.formulasize(formula) + logic.formulasize(line)))
    print('#M=' + str(logic.formulasize(line)))
    for other in candidates:
        replace(other, clause, line, vars, formula)


# forget by nondeterministic s-linear resolution

def forget(vars, formula):
    formula = logic.minimal(logic.detautologize(formula))
    logic.formulaprint(formula, '# minimized:')

    for c in formula:
        print('####')
        linear(c, set(), vars, formula)


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
    print('\tlinear.py [-t] testfile.py')
    print('\tlinear.py -c vars clause clause...' )
    print('\tlinear.py -f vars file' )
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

