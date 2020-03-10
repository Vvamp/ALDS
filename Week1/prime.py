# Works as of 3-12-2019

# 1. I'd check if it's divisable by any other number than itself or 1 by checking all solutions. Like below
def unresearchedPrime():
	primes = []
	for numToCheck in range(2, 1000):
		isPrime = True
		for i in range(0, numToCheck):
			if i > 1 and i != numToCheck:
				if numToCheck%i == 0:
					isPrime = False
					break
		if isPrime:
			primes.append(numToCheck)

	return primes

#print(unresearchedPrime())


#2. O(n^2)
#3 See below
import math 

def primeSieve(n):
	A = []
	for i in range(2, n):
		A.append(True)

	for i in range(2, int(math.sqrt(n))):
		if A[i-2] == True:
			for j in range(i**2, n, i):
				A[j-2] = False
	
	return A

# Print the results
x = 2
for num in primeSieve(1000):
	if num==True:
		print(str(x) + ", ")
	x+=1

#4 O(n log log n)