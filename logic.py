# propositional logic functions

# print with a certain level of nesting

maxlevel = 2
def printinfo(level, *s):
    if level <= maxlevel:
        if level > 1:
            print(' ' * (8 * (level - 1) - 1), end = '')
        for e in s:
            if e == '\\nonl':
                break;
            print(e, end = ' ')
        else:
            print()


# make a list of literals out of a string

def literalset(s):
    all = set()
    sign = ''
    variable = None
    for c in s:
        if c == '-':
            sign = '-'
        elif c == '&':
            variable = c
        elif variable != None and c == ';':
            all |= {sign + variable + c}
            variable = None
            sign = ''
        elif variable != None:
            variable += c
        else:
            all |= {sign + c}
            sign = ''
    return all


# make a clause from a list or string

def clause(s):
    if isinstance(s, list):
        return frozenset(s)
    elif s == '()':
        return frozenset()
    elif '->' in s:
        p = s.split('->')
        h = literalset(p[1])
        b = {'-' + l for l in literalset(p[0])}
        return frozenset(b | h)
    else:
        return frozenset(literalset(s))


# parse a formula

def formula(*l):
    f = set()
    for c in l:
        if '=' in c:
            p = c.split('=')
            f |= {clause(p[0] + '->' + p[1])} | {clause(p[1] + '->' + p[0])}
        else:
            f |= {clause(c)}
    return f


# from clause to string

def clausetostring(clause, pretty = False, parsable = False):
    if pretty:
        return ''.join({l[1:] for l in clause if l[0] == '-'}) + '->' + \
               ''.join({l for l in clause if l[0] != '-'})
    elif parsable:
        if clause:
            return ''.join(clause)
        else:
            return '()'
    else:
        return '(' + ' '.join(clause) + ')'


# from formula to string

def formulatostring(formula, label = None, pretty = False, parsable = False):
    s = label + ' ' if label else ''
    s += ' '.join(clausetostring(c, pretty,parsable) for c in formula)
    return s


# print a clause

def clauseprint(clause, label = None, pretty = False, parsable = False):
    s = label + ' ' if label else ''
    print(s + clausetostring(clause, pretty, parsable))


# print a formula

def formulaprint(formula, label = None, pretty = False, parsable = False):
    print(formulatostring(formula, label, pretty, parsable))


# size of a formula: occurrencies of variables

def formulasize(a):
    return sum([len(x) for x in a])


# variables, positive and negative literals of a clause or formula

def positive(c):
    return {l for l in c if l[0] != '-'}

def negative(c):
    return {l[1:] for l in c if l[0] == '-'}

def variable(c):
    return positive(c) | negative(c)

def positives(f):
    return {x for c in f for x in positive(c)}

def negatives(f):
    return {x for c in f for x in negative(c)}

def variables(f):
    return {x for c in f for x in variable(c)}


# negation of a literal

def negate(l):
    return '-' + l if l[0] != '-' else l[1:]


# literals of a literal or a set

def literals(v):
    if isinstance(v, set):
        return {l for x in v for l in literals(x)}
    else:
        return {v, negate(v)}


# check whether a clause contains a variable in a set

def present(v, c):
    return v & variable(c) != set()


# check whether a clause is a tautology

def tautology(c):
    for l in c:
        if '-' + l in c:
            return True
    return False


# remove tautologies from a formula

def detautologize(s):
    return {c for c in s if not tautology(c)}


# unit and non-unit clauses of a formula

def unit(f):
    u = set()
    m = set()
    for c in f:
        if len(c) == 1:
            u |= c
        else:
            m |= {c}
    return u,m


# resolve two clauses; emptyset if they don't resolve or resolve to a tautology

def resolve(a, b):
    for x in a:
        for y in b:
            if x == '-' + y or '-' + x == y:
                r = a.difference([x]).union(b.difference([y]))
                return set() if tautology(r) else set({r})
    return set()


# minimal (not containing others) clauses of a formula

def minimal(new, old = set()):
    res = set()
    for c in new:
        for d in new | old:
            if d < c:
                break
        else:
            res |= {c}
    for c in old:
        for d in new:
            if d < c:
                break
        else:
            res |= {c}
    return res


# prime implicates: repeatedly minimize the resolution closure

def close(s):
    r = set()
    n = s.copy()
    while n != r:
        r = n.copy()
        for a in r:
           for b in r:
               n |= resolve(a, b)
        n = minimal(n)
    return n


# check equivalence

def equivalent(s, r):
    return close(detautologize(s)) == close(detautologize(r))


