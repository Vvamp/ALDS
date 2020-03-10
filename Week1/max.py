# Works as of 3-12-2019

import math
def max(a):
	currentMax = -math.inf
	for i in range(0,len(a)):
		if a[i] > currentMax:
			currentMax = a[i]
	return currentMax


l = [4, 2, 252]
print(max(l))