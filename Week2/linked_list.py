# Works as of 3-12-2019

class ListNode:
	def __init__(self, value, next=None):
		self.value = value 
		self.next = next
	
	def append(self, value):
		if self.next is None:
			self.next = ListNode(value)
		else:
			self.next.append(value)

	def min(self):
		if self.next is None:
			return self.value
		if self.next.min() < self.value:
			return self.next.min()
		else:
			return self.value

	def deleteRec(self, value, prev):
		if value == self.value:
			if self.next is None:
				prev.next = None
			else:
				prev.next = self.next
		if self.next is not None:
			self.next.deleteRec(value, self)

	def delete(self, value):
		if self.next is None:
			return
		
		self.next.deleteRec(value, self)

	def print(self):
		print(self.value)
		if self.next is not None:
			self.next.print()


x = ListNode(10)
x.append(5)
x.append(20)
x.append(50)
x.append(1)
x.append(2)
x.append(5)
print("Min val in linked list: {}".format(x.min()))
x.delete(5)
x.print()