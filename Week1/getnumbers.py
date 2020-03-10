# Works as of 3-12-2019

def getNumbers(s):
	numbers = []
	currentNumber = -1
	for char in s:
		if char >= '0' and char <= '9':
			if currentNumber == -1:
				currentNumber = 0

			if currentNumber % 10 == 0:
				currentNumber = int(char)
			else:
				currentNumber *= 10
				currentNumber += int(char)
		else:
			if currentNumber > -1:
				numbers.append(currentNumber)
			currentNumber = -1
	return numbers

text = "een123zin45 6met-632meerdere+7777getallen"
print("getNumbers > \"" + text + "\" \nReturns -> " + str(getNumbers(text)))