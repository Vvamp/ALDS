# Works as of 3-12-2019
import random
def partition(a, lo, hi):
	"""
	Move all values smaller than the index higher to the left and return the index of the last change(basically our pivot)
	"""
	pivot = a[hi]
	print(f"Pivot: {pivot}")
	i = lo
	for j in range(lo, hi):
		if a[j] <= pivot:
			a[i],a[j] = a[j],a[i] 
			i+=1

	a[i],a[hi] = a[hi],a[i]
	return i


def quick_sort(a, lo, hi):
	"""
	Sort array 'a' via quick sort
	"""
	if lo >= hi:
		return a

	p = partition(a, lo, hi)	# Attempt to sort array and return current pivot
	a = quick_sort(a, lo, p-1) 	# Partition values left of current pivot
	a = quick_sort(a, p+1, hi)	# Partition values right of current pivot
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


#Feedback: comments

