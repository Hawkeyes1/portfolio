import itertools

import sys
v = eval(sys.argv[1])
N = len(v)

cube = itertools.product([0,1],repeat=N)

dots = {}
for a in cube:
    b = sum(a[i]*v[i] for i in range(N))
    if b in dots:
        dots[b].append(a)
    else:
        dots[b] = [a]

for b in dots:
    if len(dots[b]) >= N:
        dots[b].sort()
        print "x * %s = %d:" % (str(v),b)
        for x in dots[b]:
            print "\t",x
