from perc import *
from sys import argv
# call this as python print_results.py n p k theta
n = float(argv[1])
p = float(argv[2])
k = float(argv[3])
theta = float(argv[4])


print "Calculating spanning probability for n,p,k,theta = ",n,p,k,theta
print "Format: a,prob(n,a*p,k,theta)"
a = 0
prev1=0
prev2=0
curr=0
while (min(curr,prev1,prev2) < .99):
	curr = prob(n,a*p,k,theta)
	print a,curr
	a += 0.1
	prev1,prev2 = prev2,curr
	


