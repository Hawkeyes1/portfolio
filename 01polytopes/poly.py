import sympy
from sympy.matrices import *
import itertools

def tointeger(v):
    n = 1
    for k in v:
        n = sympy.core.numbers.ilcm(k.q,n)
    return list(k*n for k in v)

def abs(x):
    if x < 0: return -x
    return x

def normalvector(facet):
    A = Matrix([list(x) for x in facet])
    vs = A.nullspace()
    if len(vs) == 1:
        v = tointeger(vs[0])
        v = [abs(x) for x in v]
        v.sort()
        return tuple(v)
    else:
        return None

def brutesearch(dimension):
    cube = list(list(x) for x in itertools.product([0,1],repeat=dimension))
    results = set([])
    count = 0
    for f in itertools.combinations(cube,dimension-1):
        results.add(normalvector(f))
        count += 1
        print count
    results = [x for x in results if x != None]
    results.sort()
    results.reverse()
    return results

import sys
n = int(sys.argv[1])
for x in brutesearch(n):
    print x
