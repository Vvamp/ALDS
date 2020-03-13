import random
import time
import copy
import itertools
import math
import json

class gomokuSimulation:
    """This class specifies the game dynamics of the gomoku game
    implementing the tournaments rules as on https://www.jijbent.nl/spelregels/go-moku.php"""
    def __init__(self, bsize_=19, board_=None):
        if(board_ is None):
            self.board = []
        else:
            self.board = board_
        self.ply=1
        self.bsize = bsize_
        self.previous_move = None
        rclist = list(range(bsize_))
        self.empty = list(itertools.product(rclist,rclist))
        assert self.bsize%2 == 1
        for i in range(bsize_):
            self.board.append([0]*bsize_) #Not repeating the list because of the pointers

    def current_board(self):
        """Returns a deep copy of the board, making it harder for agents to state of the board by accident."""
        return self.board

    def check_win(self, last_move):
        """This method checks whether the last move played wins the game.
        The rule for winning is: /exactly/ 5 stones line up (so not 6 or more),
        horizontally, vertically, or diagonally."""
        color = self.board[last_move[0]][last_move[1]]
        #check up-down
        number_ud = 1
        if(last_move[1]<self.bsize-1):
            lim1 = last_move[1]+1
            lim2 = last_move[1]+6 if last_move[1]+6<self.bsize else self.bsize
            for i in range(lim1, lim2):
                if self.board[last_move[0]][i] == color:
                    number_ud += 1
                else:
                    break
        if (last_move[1] > 0):
            lim2 = last_move[1] - 5 if last_move[1]-5 > 0 else 0
            for i in reversed(range(lim2, last_move[1])):
                if self.board[last_move[0]][i] == color:
                    number_ud += 1
                else:
                    break
        if number_ud == 5:
            return True
        #check left - right
        number_lr = 1
        if (last_move[0] < self.bsize - 1):
            lim1 = last_move[0] + 1
            lim2 = last_move[0] + 6 if last_move[0] + 6 < self.bsize else self.bsize
            for i in range(lim1, lim2):
                if self.board[i][last_move[1]] == color:
                    number_lr += 1
                else:
                    break
        if (last_move[0] > 0):
            lim2 = last_move[0] - 5 if last_move[0] - 5 > 0 else 0
            for i in reversed(range(lim2, last_move[0])):
                if self.board[i][last_move[1]] == color:
                    number_lr += 1
                else:
                    break
        if number_lr == 5:
            return True
        #check lower left - upper right
        number_diag = 1
        xlim = last_move[0] - 1
        ylim = last_move[1] - 1
        while (xlim>=0 and ylim>=0):
            if self.board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim-1
            ylim = ylim-1
        xlim = last_move[0] + 1
        ylim = last_move[1] + 1
        while (xlim<self.bsize and ylim<self.bsize):
            if self.board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim + 1
            ylim = ylim + 1
        if number_diag == 5:
            return True
        #check lower right - upper left
        number_diag = 1
        xlim = last_move[0] + 1
        ylim = last_move[1] - 1
        while (xlim <self.bsize and ylim >= 0):
            if self.board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim + 1
            ylim = ylim - 1
        xlim = last_move[0] - 1
        ylim = last_move[1] + 1
        while (xlim >= 0 and ylim < self.bsize):
            if self.board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim - 1
            ylim = ylim + 1
        if number_diag == 5:
            return True
        return False

    def move(self, move_tuple):
        """Performs the provided move. The move is a tuple of an x and y position on the board."""
        if move_tuple[0]<0 or move_tuple[0]>=self.bsize or move_tuple[1]<0 or move_tuple[1]>=self.bsize:
            return False, False
        if self.board[move_tuple[0]][move_tuple[1]] == 0:
 #           if self.ply in [1,3]:
 #               if move_tuple not in self.valid_moves() :
 #                   return False, False
            place = 2 if self.ply%2 else 1
            self.board[move_tuple[0]][move_tuple[1]] = place
            self.ply += 1
            self.empty.remove(move_tuple)
            self.previous_move = move_tuple
            return True, self.check_win(move_tuple)
        else:
            return False, False


class node:
    def __init__(self, position = None, posibleChildNodes = None ,gameBoard = None, parentNode = None,  childNodes = [], numberOfVisits = 0, QValue = 0):
        self.position = position
        self.posibleChildNodes = posibleChildNodes
        self.gameBoard = gameBoard
        self.parentNode = parentNode
        self.childNodes = childNodes
        self.numberOfVisits = numberOfVisits
        self.QValue = QValue
        self.movesTested = []
        
        
    def expand(self, validMoves):
        if len(self.posibleChildNodes) != 0:    
            newPosition = self.posibleChildNodes.pop()  
            newGameBoard = json.loads(json.dumps(self.gameBoard))  
            newPosibleChildren = json.loads(json.dumps(validMoves))
            random.shuffle(newPosibleChildren)
            newChildNode = node(newPosition, newPosibleChildren, newGameBoard, self,  [])
            if len(self.posibleChildNodes) is 0:
                newChildNode.QValue = 1
                newChildNode.numberOfVisits = 1
                self.childNodes.append(newChildNode)
                return
            newChildNode.rollout()
            newChildNode.gameBoard = newGameBoard
            self.childNodes.append(newChildNode)
            return
        else:
            expandedChildNode = self.bestChildToDiscover()
            return expandedChildNode.expand(expandedChildNode.posibleChildNodes)


    def rollout(self):
        myTurn = True
        simulationGameBoard = json.loads(json.dumps(self.gameBoard))
        simulationGame = gomokuSimulation(19, simulationGameBoard)
        self.movesTested.append(self.posibleChildNodes.pop()) 
        while simulationGame.move((self.movesTested[len(self.movesTested) -1][0], self.movesTested[len(self.movesTested) -1][1]))[1] != True:
                myTurn = not myTurn
                self.movesTested.append(self.posibleChildNodes.pop())
        if myTurn is True:
            self.backTrack(1)
        else:
            self.backTrack(0)
        self.posibleChildNodes = self.posibleChildNodes + self.movesTested
        self.movesTested.clear()
        return


    def backTrack(self, gameResult):
        self.numberOfVisits = self.numberOfVisits + 1
        self.QValue = self.QValue + gameResult
        updateParent = self.parentNode
        while updateParent != None:
            updateParent.numberOfVisits += 1
            updateParent.QValue += gameResult
            updateParent = updateParent.parentNode
        return



    def bestChildToDiscover(self):
        bestChildNode = self.childNodes[0]
        for i in self.childNodes[1:]:
            if i.calculateUCB() > bestChildNode.calculateUCB():
                bestChildNode = i
        return bestChildNode

    def bestChildToReturn(self):
        bestChildNode = self.childNodes[0]
        for i in self.childNodes[1:]:
            if (i.QValue / i.numberOfVisits) > (bestChildNode.QValue / bestChildNode.numberOfVisits):
                bestChildNode = i
        return bestChildNode

    def calculateUCB(self):
        return ((self.QValue / self.numberOfVisits) + (1 / math.sqrt(2)*(math.sqrt(math.log(self.parentNode.numberOfVisits / self.numberOfVisits)))))


class myGommokuAI:
    def __init__(self, black_=True):
        self.black = black_
        self.gameBoard = None
        self.baseNode = node([0,0])

    def new_game(self, black_):
        self.black = black_

    def move(self, board, lastMove, validMoves,  max_time_to_move=1000):
        if len(validMoves) is 1:
            self.baseNode = node(random.shuffle(validMoves))
            return validMoves[0]
        timeStart = time.time()    
        self.baseNode = node(lastMove, QValue=1, numberOfVisits=1)   
        self.baseNode.posibleChildNodes = json.loads(json.dumps(validMoves))   
        random.shuffle(self.baseNode.posibleChildNodes)  
        self.baseNode.gameBoard = json.loads(json.dumps(board))
        timeEnd = time.time()
        while (timeEnd - timeStart) < float(990/1000):
            self.baseNode.expand(validMoves)
            timeEnd = time.time()   
        returnNode = self.baseNode.bestChildToReturn()
        if((returnNode.position[0], returnNode.position[1]) in validMoves):
            return (returnNode.position[0], returnNode.position[1])
        else:
            return random.choice(validMoves)
    

    def id(self):
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "MatthiesBrouwer"