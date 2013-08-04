#!/usr/bin/python
import random

def randgrid(n,p):
	grid = [0]*n
	for x in range(n):
		grid[x] = [0]*n
		for y in range(n):
			grid[x][y] = [0]*n
			for z in range(n):
				if random.random()<p:
					grid[x][y][z]=1
	return grid

import copy

def neighbors(previous,x,y,z):
	total=0
	n = len(previous)
	# previous[x][y][z]==0, so we can simplify by including previous[x][y][z]
	# as a possible neighbor instead of excluding.
	total += sum( [previous[a][y][z] for a in range(n)] )
	total += sum( [previous[x][a][z] for a in range(n)] )
	total += sum( [previous[x][y][a] for a in range(n)] )
	return total

def advance(grid,threshold):
	previous = copy.copy(grid)
	n = len(grid)
	altered = False
	for x in range(n):
		for y in range(n):
			for z in range(n):
				if previous[x][y][z] == 1: continue
				elif neighbors(previous,x,y,z) >= threshold:
					grid[x][y][z] = 1
					altered = True
	return altered

def spans(grid,threshold):
	while advance(grid,threshold):
		pass
	n=len(grid)
	for x in range(n):
		for y in range(n):
			for z in range(n):
				if grid[x][y][z]==0:
					return False
	return True

def prob(n,p,threshold,k):
	successes=0.
	for i in range(k):
		grid=randgrid(n,p)
		if spans(grid,threshold):
			successes+=1
	return successes/k
			
