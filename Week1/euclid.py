# Works as of 3-12-2019

def calcGCD(p, q):
	if p < q:
		return calcGCD(q%p, p)

	if q == 0:
		return p
		
	if p == q:
		return p

	if p > q:
		return calcGCD(q, p%q)


print(calcGCD(8, 12))