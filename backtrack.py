#!/usr/bin/env python3
#
# forget by backtracking + unit propagation

import logic
import sys

# propagate model in formula on the forget variables

def propagate(model, formula, forget):
    unit = model

    while unit:
        logic.formulaprint(formula, '## formula:')
        print('## unit:', ' '.join(unit))

        opposite = {logic.negate(l) for l in model}
        print('## opposite:', ' '.join(opposite))

        unit = set()
        simplified = set()

        for clause in formula:
            print('## %20s' % logic.clausetostring(clause) , end = ' ')
            removed = frozenset({l for l in clause if l not in opposite})

            if removed & model:
                print('T')
                continue

            simplified |= {removed}
            if removed == clause:
                print('=', end = ' ')
            else:
                print(logic.clausetostring(removed), end = ' ')

            if len(removed) == 1 and logic.variables(removed) & forget:
                unit |= {*removed}
                print('    +', *removed, end = '')

            print()

        formula = simplified
        model |= unit

    print('## model:', ' '.join(model))
    logic.formulaprint(formula, '## formula:')

    if not formula:
        return True, model, formula
    if frozenset() in formula:
        return False, model, formula
    return None, model, formula


# backtracking with unit propagation

def dpll(model, unit, forget, formula):
    print('#######################')
    print('# model:', ' '.join(model))
    print('#T=' + str(logic.formulasize(formula)))
    print('#M=' + str(len(model)))

    r,model,formula = propagate(model, formula, forget)
    print('# propagate:', r)
    print('# model:', ' '.join(model))
    logic.formulaprint(formula, '# formula:')
    if r != None:
        return r

    for clause in formula:
        if len(clause) == 1:
            unit |= {next(iter(clause))}
            branch = next(iter(logic.variable(clause)))
            print('# first unit:', next(iter(clause)))
            break
    else:
        unset = logic.variables(formula) - logic.variables(model)
        pool = unset - forget
        if not pool:
            pool = unset
        print('# pool:', ' '.join(pool))
        branch = next(iter(pool))

    print('# branch:', branch)
    print('# unit:', ' '.join(unit))

    pos = dpll(model | {branch},       set(unit), forget - {branch}, formula)
    neg = dpll(model | {'-' + branch}, set(unit), forget - {branch}, formula)

    print('# finish:', branch)

    # both sat or both unsat: return that
    if pos == neg:
        print('# accordance')
        return pos

    # branching past the keep variables: do not generate a clause
    if branch in forget:
        print('# discordance beyond keep variables')
        return pos or neg

    model -= unit
    model |= {branch if pos == False else '-' + branch}
    print('# falsifying model:', ' '.join(model))
    clause = {logic.negate(l) for l in model if not logic.variables({l}) & forget}
    logic.clauseprint(clause, parsable = True)
    return pos or neg


# forget

def forget(v, f):
    k = logic.variables(f) - v
    print('# keep:', ' '.join(k))
    if not dpll(set(), set(), v, f):
        print('# UNSAT')
        print('()')


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
    print('\tbacktrack.py [-t] testfile.py')
    print('\tbacktrack.py -c vars clause clause...' )
    print('\tbacktrack.py -f vars file')
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

