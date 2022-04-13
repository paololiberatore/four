forget
======

Four programs for forgetting variables from propositional formulae.

The commandline arguments are the same for all four. They are shown by option
``-h``. The variables to forget and the formula can be given either as a Python
program (``-t``, the default), as the variables and the clauses (``-c``) or as
the variables and a file containing the formula (``-f``).

```
	close.py [-t] testfile.py
	close.py -c ab 'ab->c' 'de=fg' 'adf' 
	close.py -f ab file.txt
```

Clause `abc` is `a OR b OR c`. A variable is either a single character or an
html entity like ``&string;``

close.py
--------

Forget by repeatedly resolving clauses and removing the subsumed ones, and
finally removing the clauses containing the variables to forget.

eliminate.py
------------

Forget by resolving out each variable to forget: Davis-Putnam applied to the
variables to forget only.

linear.py
---------

Forget by s-linear resolution: choose a clause and keep resolving it with a
clause of the formula or a clause previusly generated, the latter only if the
result subsumes the clause. Resolve only on the variables to forget, stop when
none is left.

backtrack.py
------------

Forget by backtracking with unit propagation over the variables to forget.



test
====

equivalence.py
--------------

Check whether two formulae are equivalent.

generate.py
-----------

Generate a random formula.

run
---

Iteratively build a random formula, calls the four forgetting programs and
check the equivalence of their results.

square
------

Test formulae within a certain number of variables, variables to forget and
clauses.



time and memory self-reporting
==============================

Lines in the output:

#T=x
	x units of time have been spent; the total running time is their sum

#M=x
	program is currently using x units of memory; the required memory is
	the maximal value

Time and memory are the asymptotic measure of the best way to do certain
operations, not the actual time or number of instructions executed. For
example, if a certain operation can be done in linear time, the reported time
may be the size of the formula even if the program itself implements that in
quadratic time.


