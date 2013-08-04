import sympy
from sympy.matrices import *
import random
import math

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
        return tuple(v)
    else:
        return None

def energy(x):
	if x == None: return 0
	else: return max(abs(max(x)),abs(min(x)))

def neighbor(facet):
	"Return a random neighbor -- one coordinate of one vertex is changed."
	ret = [list(x) for x in facet]
	N = len(facet)
	M = len(facet[0])
	i,j = random.randrange(N),random.randrange(M)
	ret[i][j] = 1 - ret[i][j]
	return ret

def temp(r):
	return 100*(1-r)
	

def prob(e1,e2,T):
	if e2 > e1: return 1
	else: return math.exp((e2-e1)/T)

def record(facet,N,x):
	f = open("facet"+str(N)+","+str(energy(x)),"w")
	for v in facet:
		f.write(str(v))
		f.write("\n")
	f.write(str(x))
	f.write("\n")
	f.close()

def retrieve(dim,norm):
	f = open("facet%d,%d" % (dim,norm))
	facet = []
	for line in f:
		facet.append(eval(line))
	return facet[:-1] #ignore the normal vector

def anneal(facet):
	s, E = facet, energy(normalvector(facet))
	sbest, Ebest = s, E
	Eseen = set([0,E])
	k = 0 # total iterations
	kmax = 5000
	while k < kmax:
		snew = neighbor(s)
		x = normalvector(s)
		Enew = energy(x)
		if Enew not in Eseen:
			Eseen.add(Enew)
			record(snew,len(snew),x)
		if Enew > Ebest:
			sbest, s = snew, s
			Ebest, E = Enew, Enew
			print k,Enew,Ebest,"***"
		elif prob(E,Enew,temp(float(k)/kmax)) > random.random():
			s, E = snew, Enew
			print k,Enew,Ebest,"*"
		else:
			print k,Enew,Ebest
		k += 1

import sys
if len(sys.argv) == 2:
	N = int(sys.argv[1])
	facet = [[random.randrange(2) for x in range(N)] for y in range(N)]
	anneal(facet)
elif len(sys.argv) == 3:
	N, E = int(sys.argv[1]), int(sys.argv[2])
	facet = retrieve(N,E)
	anneal(facet)
