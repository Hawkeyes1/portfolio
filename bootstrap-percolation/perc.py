#!/usr/bin/python
import random

def randgrid(n,p):
	grid = range(n)
	for x in range(n):
		grid[x] = [0]*n
	for x in range(n):
		for y in range(n):
			if random.random()<p:
				grid[x][y]=1
	return grid

import copy

def neighbors(previous,x,y):
	total=0
	n = len(previous)
	# previous[x][y]==0, so we can simplify by including previous[x][y]
	# as a possible neighbor instead of excluding.
	total += sum( [previous[x][a] for a in range(n)] )
	total += sum( [previous[a][y] for a in range(n)] )
	return total

def advance(grid,threshold=2):
	previous = copy.copy(grid)
	n = len(grid)
	altered = False
	for x in range(n):
		for y in range(n):
			if previous[x][y] == 1: continue
			elif neighbors(previous,x,y) >= threshold:
				grid[x][y] = 1
				altered = True
	return altered

def spans(grid,threshold=2):
	while advance(grid,threshold):
		pass
	n=len(grid)
	for x in range(n):
		for y in range(n):
			if grid[x][y]==0:
				return False
	return True

def prob(n,p,k=100,threshold=2):
	successes=0.
	for i in range(k):
		grid=randgrid(n,p)
		if spans(grid,threshold):
			successes+=1
	return successes/k
			
