import itertools

def memoize(f):
    cache = {}
    def g(*args):
        if args in cache:
            return cache[args]
        else:
            val = f(*args)
            cache[args] = val
            return val
    return g

@memoize
def partitions2(n,k):
    if n == 0:
        if k >= 0:
            return [[]]
        return []
    if n < 0:
        return []
    else:
        if k <= 0:
            return []
        return partitions2(n,k-1) + [[k]+x for x in partitions2(n-k,k)]
        return out

def partitions(n):
    return [tuple(x) for x in partitions2(n,n)]

@memoize
def children(p):
    out = []
    n = len(p)
    for i in range(n):
        out.append(p[:i])
        for j in range(1,p[i]):
            out.append(p[:i] + tuple(min(x,j) for x in p[i:]))
    return out

@memoize
def wins(p):
    if p == ():
        return True
    else:
        return any(not wins(q) for q in children(p))

def pp(p):
    out = ""
    for x in p:
        out += str(x)
    return out

for i in [7,8,9]:
    print "PARTITIONS OF", i
    W, L = [], []
    for p in partitions(i):
        if wins(p):
            W.append(p)
        else:
            L.append(p)
    W.reverse()
    L.reverse()
    print "WINS:",[pp(p) for p in W]
    print "LOSSES:",[pp(p) for p in L]
