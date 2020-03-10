# Works
m = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000] # possible banknotes

def moneyRec(j, i=12):
	"""
	Calculate the amount of combinations possible to reach number 'j', with the possible banknotes 'm'.
	Args:
		j	= amount to find
		i* 	= iterator	- Defaults to 12
		* optional 
	"""
	if moneyRec.matrix[j][i] == 0:
		if j >= m[i]:
			moneyRec.matrix[j][i] = moneyRec(j,i-1) + moneyRec(j-m[i],i)
		else:
			moneyRec.matrix[j][i] = moneyRec(j,i-1)

	return moneyRec.matrix[j][i]

# Enter an amount of money
correctValEntered = False
while correctValEntered is False:
	try:
		findMoney = int(input("Enter an amount of money: "))
		correctValEntered = True
	except:
		print("Please enter a valid number!")

# Create a matrix matrix filled with 0, where a[0, j] and a[i, 0] are set to 1
mat = [[0 for x in range(len(m))] for y in range(findMoney+1)] 
for i in range(0, findMoney+1):
	for j in range(0, len(m)):
		if i == 0 or j == 0:
			mat[i][j] = 1

# Set moneyRec.matrix to mat
setattr(moneyRec, 'matrix', mat)

# Calculate and show the possible combinations recursively
print("There are {} possible combinations to get to {} cents!".format(moneyRec(findMoney), findMoney))

