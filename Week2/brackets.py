#Works as of 3-12-2019

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
		if(len(self.list) <= 0):
			return -1
		return self.list[len(self.list)-1]


def Brackets(input, rules):
	exprBrackets = myStack()

	for char in expression:
		if char not in rules:
			print(f"Error > Invalid Input! Unknown character '{char}'.")
			return False
		else:
			# Check if character is any starting character and if it is, add it to the stack
			if char is rules[0] or char is rules[2] or char is rules[4]:
				exprBrackets.push(char)
			else:
				# If the character is not a starting character and thus an end character, remove the matching bracket
				# Matching bracket by checking if the current character to match is equal to the matching start character AND the exprbrackets is not empty
				bracketIndex = brackets.index(char)
				if exprBrackets.peek() is rules[bracketIndex-1] and exprBrackets.peek() != -1:
					exprBrackets.pop()
				else:
					return False

	if exprBrackets.isEmpty():
		return True
	else:
		return False



brackets = ['<', '>', '[', ']', '(' ,')']
expression = input("Expression > ")

if Brackets(expression, brackets):
	print("Valid expression!")
else:
	print("Error > Invalid expression!")

# Feedback fixed: Give the dictionary and input via parameters and return a bool

print("-- Program Complete --")