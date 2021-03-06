import random
import copy
from matplotlib import pyplot as plt 
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from queue import Queue as queue

class edge:

    def __init__(self, var1, var2, nactionsx, nactionsy):
        """
        Constructor for the edge class
        :param var1: the (index of the) first decision variable
        :param var2: the (index of the) second decision variable
        :param nactionsx: the number of possible values for var1
        :param nactionsy: the number of possible values for var1
        """
        self.rewards = [] #table with the local rewards
        self.x = var1
        self.y = var2
        for i in range(nactionsx):
            rew = []
            for j in range(nactionsy):
                rew.append( random.random() )
            self.rewards.append(rew)

    def localReward(self, xval, yval):
        """
        Return the local reward for this edge given the values of the connected decision variables
        :param xval: value of the first decision variable
        :param yval: value of the second decision variable
        :return: the local reward
        """
        return self.rewards[xval][yval]


class coordinationGraph:

    def __init__(self, noNodes, pEdge, noActions, seed=42):
        """
        Constructor for the coordination graph class. It generates a random graph based on a seed.

        :param noNodes: The number of vertices in the graph. Each vertex represents a decision variable.
        :param pEdge: the probability that an edge will be made
        :param noActions: the number of possible values (integers between 0 and noActions) for the decision variables
        :param seed: the pre-set seed for the random number generator
        """
        random.seed(seed)
        self.nodesAndConnections = dict() #for each node, a list of nodes it is connected to
        self.edges = dict() #A dictionary of tuples (of two decision variables) to an object of the edge class
        for i in range(noNodes): #First make sure that the entire graph is connected (connecting all nodes to the next one)
            if i == 0:
                self.nodesAndConnections[i] = [i + 1]
                self.nodesAndConnections[i+1] = [i]
                eddy = edge(i, i+1, noActions, noActions)
                self.edges[(i,i+1)] = eddy
            elif i <noNodes-1:
                self.nodesAndConnections[i].append(i + 1)
                self.nodesAndConnections[i + 1] = [i]
                eddy = edge(i, i + 1, noActions, noActions)
                self.edges[(i, i + 1)] = eddy
        tuplist = [(x, y) for x in range(noNodes) for y in range(x + 2, noNodes)]
        for t in tuplist: #Then, for each possible edge, randomly select which exist and which do not
            r = random.random()
            if r < pEdge:
                self.nodesAndConnections[t[0]].append(t[1])
                self.nodesAndConnections[t[1]].append(t[0])
                self.edges[t] = edge(t[0], t[1], noActions, noActions)
        #For reasons of structure, finally, let's sort the connection lists for each node
        for connections in self.nodesAndConnections.values():
            connections.sort()

    def evaluateSolution(self, solution):
        """
        Evaluate a solution from scratch; by looping over all edges.

        :param solution: a list of values for all decision variables in the coordination graph
        :return: the reward for the given solution.
        """
        result = 0
        for i in range(len(solution)):
            for j in self.nodesAndConnections[i]:
                if(j>i):
                    result += self.edges[(i,j)].localReward(solution[i], solution[j])
        return result

    def evaluateChange(self, oldSolution, variableIndex, newValue):
        """
        :param oldSolution: The original solution
        :param variableIndex: the index of the decision variable that is changing
        :param newValue: the new value for the decision variable
        :return: The difference in reward between the old solution and the new solution (with solution[variableIndex] set to newValue)
        """
        delta = 0
        
        newSolution = copy.deepcopy(oldSolution)
        # Call evaluate solution on the initial solution, to get the reward for that solution
        oldSolutionVal = self.evaluateSolution(newSolution)
        
        # Change the old solution to the new solution
        newSolution[variableIndex] = newValue

        # Call evaluate solution on the new solution, to get the reward for that solution
        newSolutionVal = self.evaluateSolution(newSolution)

        delta = newSolutionVal - oldSolutionVal
        return delta

    def randomSol(self):
        solution = []
        for i in range(0, len(self.nodesAndConnections)):
            solution.append(random.randint(0,nActs-1))
        return solution


def randomKeysToQueue(coordinationGraph):
    """
    :param coordinationGraph: the coordination graph to randomise the keys of
    :return: a shuffled queue of keys
    """
    temp = []
    q = queue()
    for key in coordinationGraph.nodesAndConnections.keys():
        temp.append(key)

    random.shuffle(temp)
    for item in temp:
        q.put(item)

    return q

def localSearch4CoG(coordinationGraph, initialSolution):
    """
    :param coordinationGraph: the coordination graph to optimise for
    :param initialSolution: an initial solution for the coordination graph
    :return: a new solution (a local optimum)
    """
    
    vars = randomKeysToQueue(coordinationGraph)

    while not vars.empty():
        # Get the first edge index in the queue
        i = vars.get()

        # For every possible solution, check if it increases the local reward at the edge index
        for ai in range(0,3):
            delta = coordinationGraph.evaluateChange(initialSolution, i, ai)
            
            if delta > 0:
                # If the reward is higher, set the initial solution's solution to the new solution
                initialSolution[i] = ai

                # Make a new queue, so that all keys can be checked again
                vars = randomKeysToQueue(coordinationGraph)

                break

    return initialSolution

def multiStartLocalSearch4CoG(coordinationGraph, noIterations):
    """
    :param coordinationGraph: the coordination graph to optimise for
    :param noIterations:  the number of times local search is run
    :return: the best local optimum found and its reward
    """
    solution = None
    reward = float("-inf")
   
    for i in range(0, noIterations):
        currentSolution = localSearch4CoG(coordinationGraph, coordinationGraph.randomSol())
        currentReward = coordinationGraph.evaluateSolution(currentSolution)
        if currentReward > reward:
            reward = currentReward
            solution = currentSolution
        
    return solution, reward


def iteratedLocalSearch4CoG(coordinationGraph, pChange, noIterations):
    """
    :param coordinationGraph: the coordination graph to optimise for
    :param pChange: the perturbation strength, i.e., when mutating the solution, the probability for the value of a given
                    decision variable to be set to a random value.
    :param noIterations:  the number of iterations
    :return: the best local optimum found and its reward
    """

    solution = None
    reward = float("-inf")

    for i in range(0, noIterations):
            currentSolution = localSearch4CoG(coordinationGraph, coordinationGraph.randomSol())
            currentReward = coordinationGraph.evaluateSolution(currentSolution)

            for index in currentSolution:
                r = random.random()
                if r < pChange:
                    currentSolution[index] = random.randint(0,3)
                
            if currentReward > reward:
                reward = currentReward
                solution = currentSolution

    return solution, reward

nVars = 50
nActs = 3
cog = coordinationGraph(nVars,1.5/nVars,nActs)

### 5.2
print("Running 5.2...", end="")
lsVals = []
count = 50
for i in range(0, count):
    seed = random.randint(0, 10000)
    cogn = coordinationGraph(nVars, 1.5/nVars, nActs, seed)
    rndSol = cogn.randomSol()
    localSol = localSearch4CoG(cogn, rndSol)
    rew = cogn.evaluateSolution(localSol)
    lsVals.append(rew)
plt.title("5.2 - Histogram of rewards found via local search")
plt.ylabel("Count")
plt.xlabel("Local Reward")
plt.hist(x=lsVals, bins=50)
plt.show()
print(" ...DONE!")    


### 5.3 - Script to run iterated local search 'tries' times.
print("Running 5.3...")
bestNum = float("-inf")
bestSol = None
tries = 10
bpch = float("-inf")
print("Attempting Iterated local search {} times...".format(tries), end="")
for i in range(1, tries+1):
    pc = 1/i
    aSol,aReward = iteratedLocalSearch4CoG(cog, pc, 10)
    if(aReward > bestNum):
        bestNum = aReward
        bestSol = aSol
        bpch = pc
print("Done!")
print("Best Reward: {}\nWith pChange: {}".format(bestNum, bpch))


### 5.5
print("Running 5.5...", end="")
count=50
ilsVals = []
mlsVals = []
bestIlsRew = float("-inf")
bestMlsRew = float("-inf")
cogn = coordinationGraph(nVars, 1.5/nVars, nActs)
for i in range(0, count):
    rndSol = cogn.randomSol()

    mlsSol, mlsRew = multiStartLocalSearch4CoG(cogn, 10)
    ilsSol, ilsRew = iteratedLocalSearch4CoG(cogn, random.randint(1, 1000)/1000, 10)
    
    if(mlsRew > bestMlsRew):
        bestMlsRew = mlsRew
    if(ilsRew > bestIlsRew):
        bestIlsRew = ilsRew


    mlsVals.append(bestIlsRew)
    ilsVals.append(bestMlsRew)

plt.title("5.5 - Plot of highest quality/reward as a function of the iteration")
xInfo = list(range(1,count+1))

plt.plot(xInfo,ilsVals, label="Iterated Local Search")
plt.plot(xInfo,mlsVals, label="Multi Start Local Search")

plt.xlabel("Iteration")
plt.ylabel("Best Quality/Reward")
plt.xlim(1, 10)

plt.legend()
plt.show()
print(" ...DONE!")


