# Works as of 3-12-2019
class myStack () :
	"""
	Class to make a stack
	EXAMPLE
	--------
	>>> stack = mystack ()
	"""
	def __init__ ( self ) :
		"""
		Constructor for Class myStack
		PARAMETERS
		------------
		self : self
		EXAMPLE
		--------
		>>> stack = mystack ()
		"""
		self.list = []
	def isEmpty ( self ) :
		"""
		Function to check is the stack is empty
		PARAMETERS
		------------
		self : self
		RETURN
		---------
		result : bool
		True if and only if the stack is empty .
		EXAMPLE
		--------
		>>> stack = mystack ()
		>>> stack.isEmpty ()
		True
		"""
		if not self.list:
			return True
		else:
			return False

	def push ( self , x ) :
		"""
		Function to push things to the stack
		PARAMETERS
		------------
		self : self
		x
		:
		The value you want to push onto the stack
		EXAMPLE
		--------
		>>> stack = myStack ()
		>>> stack.push (5)
		"""
		self.list.append(x)
		
	def pop ( self ) :
		"""
		Function to pop a value from the stack
		PARAMETERS
		------------
		self : self
		RETURN
		---------
		top :
		the top value of the stack
		EXAMPLE
		--------
		>>> stack = mystack ()
		>>> stack . push (15)
		>>> stack . push (5)
		>>> stack . pop ()
		5
		>>> stack . pop ()
		15
		"""
		item = self.list[len(self.list)-1]
		self.list.pop(len(self.list)-1)
		return item
	def peek ( self ) :
		"""
		Function to peek at the top variable on the stack .
		PARAMETERS
		------------
		self : self
		RETURN
		---------
		top :
		The value that is on the top of the stack
		EXAMPLE
		--------
		>>> stack = mystack ()
		>>> stack . push (15)
		>>> stack . push (5)
		>>> stack . peep ()
		5
		>>> stack . peep ()
		5
		"""
		return self.list[len(self.list)-1]


a = myStack()
testIsSuccessful = True

if a.isEmpty():
	print("Init > Stack is empty!")
else:
	testIsSuccessful = False
	print("Init > Stack is not empty!")
print("")

a.push(5)
a.push(10)
a.push(16)

if a.peek() is not 16:
	testIsSuccessful = False

print("Push Test > Answer should be '16'")
print("Push Test > Answer: " + str(a.peek()))
a.pop()
if a.peek() is not 10:
	testIsSuccessful = False

print("")
print("Pop Test > Answer should be '10'")
print("Pop Test > Answer: " + str(a.peek()))
print("")

if testIsSuccessful is True:
	print("Results > All tests passed!")
else:
	print("Results > One or more tests failed. :(")
print("-- Program Complete --")