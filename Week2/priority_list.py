# Data structure chosen: List
# Reason: It's easy to use, flexible and it's easy to read.
# Time complexity: 
#   - queue()		=	O(1) 
#	- dequeue()		=	O(n)
#	- contains()	=	O(n)
#	- remove()		=	O(n)
# TODO: Waarom koos ik voor een list(researched/resource-wise)

# Works as of 3-12-2019
import math
class PriorityNode:
	def __init__(self, data, priority):
		self.data = data 
		self.priority = priority


class PriorityList:
	"""
	A priority queue, implemented by using a list of 'Priority Node' objects.
	"""
	def __init__(self):
		"""
		Initializes the priority queue object.
		"""
		self.data = []

	def queue(self, v, p):
		"""
		Adds a new element in the priority queue with data 'v' and priority 'p'
		"""
		newNode = PriorityNode(v, p)
		self.data.append(newNode)

	def dequeue(self):
		"""
		Returns the element with the highest priority from the priority queue and removes it.
		If there are multiple elements with the same priority, the first one encountered gets removed.
		"""
		largestNode = None

		if(len(self.data) <= 0):
			return -math.inf

		for i in range(0, len(self.data)):
			if i == 0:
				largestNode = self.data[i]
			else:
				if largestNode.priority < self.data[i].priority:
					largestNode = self.data[i]

		self.data.remove(largestNode)
		return largestNode.data

	def contains(self, v):
		"""
		If the priority queue contains the value 'v', returns true.
		If all the items have been checked and the value hasn't been found, it returns false.
		"""
		for node in self.data:
			if node.data == v:
				return True
		return False

	def remove(self, v):
		"""
		Removes every element with value 'v' in the priority queue.
		"""
		indicesToRemove = []

		for i in range(0, len(self.data)):
			if self.data[i].data == v:
				indicesToRemove.append(i)

		indicesToRemove.sort(reverse=True)

		for index in indicesToRemove:
			del(self.data[index])
			
	def print(self):
		"""
		Outputs all current elements in the priority queue.
		"""
		print("{", end="")
		for node in self.data:
			# print("Item - Value: {} Priority: {}".format(node.data, node.priority))
			print("[{}, {}], ".format(node.data, node.priority), end="")
		print("}\n")


# Test
_list = PriorityList()

_list.queue(5, 1)
_list.queue(8, 2)
_list.queue(5, 3)
_list.queue(5, 4)
_list.queue(5, 9)
if _list.dequeue() != 5:
	raise Exception("Highest priority number is not 5!")

_list.remove(5)

if _list.contains(2) is False and _list.contains(8) is True and _list.contains(5) is False:
	print("All tests passed! Hooray!")
else:
	_list.print()

	print("List should not contain 2: ", end="")
	if _list.contains(2):
		print("INCORRECT")
	else:
		print("CORRECT")

	print("List should contains 8: ", end="")
	if _list.contains(8):
		print("CORRECT")
	else:
		print("INCORRECT")

	print("List should not contain 5: ", end="")
	if _list.contains(5):
		print("INCORRECT")
	else:
		print("CORRECT")
	raise Exception("--- One or more tests failed, check the results above ---")

