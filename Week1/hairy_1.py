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
    for i in range(0, len(arr)-1):
        for j in range(i+1, len(arr)-1):
            for k in range(j+1, len(arr)-1):
                tup = (arr[i], arr[j], arr[k])
                # rest = arr \ tup, without having another for loop
                rest = arr[:]
                rest.remove(arr[i])
                rest.remove(arr[j])
                rest.remove(arr[k])
                relativeHair = avgHairLength(tup) - avgHairLength(rest)
                xy = (tup[0][0], tup[1][0], tup[2][0], relativeHair)
                result.append(xy)

    return result

students = [("Vincent", 5), ("Caro", 40), ("Oscar", 6),("Vincent2", 5), ("Caro2", 40), ("Oscar2", 6)]

pprint.pprint(hairy(students))