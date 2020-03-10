# Works as of 3-12-2019
import random

classSize = 23
timesToLoop = 100
duplicates = 0

def checkDuplicates():
	birthdays = [] 
	for i in range(classSize):
		birthday = random.randint(1, 366)

		# If there was a birthday that already occured before, it's a duplicate -> return True
		if birthday in birthdays:
			return True
		birthdays.append(birthday)

	# If there were no duplicates, return true
	return False

for i in range(0, timesToLoop):
	if checkDuplicates():
		duplicates+=1

print("Approximated Chance: " + str(duplicates/timesToLoop*100) + '%')
