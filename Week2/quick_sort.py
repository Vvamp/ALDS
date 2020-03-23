# Works as of 3-12-2019
import random
def partition(a, lo, hi):
	pivot = a[hi]
	i = lo
	for j in range(lo, hi):
		if a[j] <= pivot:
			a[i],a[j] = a[j],a[i] 
			i+=1

	a[i],a[hi] = a[hi],a[i]
	return i


def quick_sort(a, lo, hi):
	if lo >= hi:
		return a 

	p = partition(a, lo, hi)
	a = quick_sort(a, lo, p-1)
	a = quick_sort(a, p+1, hi)
	return a

# Testing

# Generate a random list with random, probably unsorted, numbers
l = []
for i in range (0, 5+random.randint(0, 10)):
	l.append(random.randint(0, 200))

print("Unsorted array: {}".format(l))
print("\n")

# Store sorted list in x
x = quick_sort(l, 0, len(l)-1)

print("Sorted array: {}".format(x))


# explanations! 