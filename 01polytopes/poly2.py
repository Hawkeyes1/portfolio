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
    A = Matrix(facet)
    vs = A.nullspace()
    if len(vs) == 1:
        v = tointeger(vs[0])
        v = [abs(x) for x in v]
        v.sort()
        return tuple(v)
    else:
        return None

def brutesearch(n):
    cube = list(list(x) for x in itertools.product([0,1],repeat=n) if 1 in x)
    results = set([])
    for k in range(1,n+1):
        top = [1]*k + [0]*(n-k)
        rest = [x for x in cube if sum(x) <= k]
        results = set.union(results,set(normalvector(list(f)+[top]) for f in itertools.combinations(rest,n-2)))
    results = [x for x in results if x != None]
    results.sort()
    results.reverse()
    return results

import sys
n = int(sys.argv[1])
if n == 1: 
    print "Version optimized for n >= 2; inaccurate for n = 1."
    sys.exit(0)
for x in brutesearch(n):
    print x
