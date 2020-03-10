import math
import pprint

def avgHairLength(x):
	total = len(x)
	if total <= 0:
		return 0
	sum = 0
	for element in x:
		sum+=element[1]
	
	return sum / total
    
def hairy(arr):
    result = []
    arrTups = []
    for i in range(0, len(arr)-1):
        for j in range(i+1, len(arr)-1):
            for k in range(j+1, len(arr)-1):
                tup = (arr[i], arr[j], arr[k])
                # rest = arr \ tup, without having another for loop
                arrTups.append(tup)

    for tup in arrTups:
        rest = arr[:]
        rest.remove(tup[0])
        rest.remove(tup[1])
        rest.remove(tup[2])
        relativeHair = avgHairLength(tup) - avgHairLength(rest)
        result.append((tup[0][0], tup[1][0], tup[2][0], relativeHair))

    return result

students = [("Vincent", 5), ("Caro", 40), ("Oscar", 6),("Vincent2", 5), ("Caro2", 40), ("Oscar2", 6)]

pprint.pprint(hairy(students))