donotanalyze(
    'unit clauses, true',
    'bc',
    'a', '-e',
    'a->b', 'b->c', 'c->d', 'ae'
)

donotanalyze(
    'unit clauses, false',
    'bc',
    'a', '-e',
    'a->b', 'b->c', 'c->d', 'd->e'
)

analyze(
    'unit clauses, undetermined',
    'bc',
    'a',
    'a->b', 'b->c', 'c->d', 'ef'
)
