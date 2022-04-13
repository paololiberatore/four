#!/usr/bin/env python3
#
# check whether two formulae are equivalent

import logic
import sys
import os


if len(sys.argv) <= 2 or sys.argv[1] == '-h':
    print('args: formula formula')
else:
    if not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
        print('X')
        sys.exit(0)
    f = logic.formula(*set(open(sys.argv[1]).read().split()))
    g = logic.formula(*set(open(sys.argv[2]).read().split()))
    if logic.equivalent(f, g):
        print('-')
        sys.exit(0)
    else:
        print('NON EQUIVALENT')
        sys.exit(1)

