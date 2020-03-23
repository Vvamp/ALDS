# Works as of 3-12-2019

def find(lst, x):
	if len(lst) == 0:
		return -1
	
	if lst[-1] == x:
		return len(lst)-1

	return find(lst[:-1], x)


lst = [5, 2, 8, 3, 10]

print("The index of '3' should be '3' and is " + str(find(lst, 3)))