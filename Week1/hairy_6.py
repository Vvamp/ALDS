#done
import math
import timeit
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


setup1= """from __main__ import hairy
from __main__ import students
st = students
"""

def hairy2(arr):
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
  

setup2="""from __main__ import hairy2
from __main__ import students
st = students
"""

students = [("Vincent", 5), ("Caro", 40), ("Oscar", 6),("Vincent", 5), ("Caro", 40), ("Oscar", 6)]


print("Hairy slow:")
print(timeit.timeit(stmt="hairy(students)", setup=setup1,number=100000))
print("Hairy fast:")
print(timeit.timeit(stmt="hairy2(students)", setup=setup2,number=100000))


print("Why should you measure multiple times? > Because timings can vary a lot. Measuring once could and probably will give you a wrong time. By measuring multiple times, you get a good average.")
print("Why do we use the Big-Oh notation instead of just timing algo-rithms? > Because timing is based on the specific computer and can depend heavily on a number of factors.")