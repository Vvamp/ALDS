import random
import time
import copy
import gomoku
import math

def findSpotToExpand(n):
    if n.hasFinished():
        return n
    # print("N not finished")


    if not n.isFullyExpanded():
        n_state = copy.deepcopy(n.gamestate)
        n_move = n.randomMove(n_state)
        n_state.move(n_move)
        n_node = TreeNode(n_state, n, n_move)
        n.children.append(n_node)
        return n_node 

    # print("N Fully Expanded ")
    n_node = n.bestChild()
    return findSpotToExpand(n_node)

def backupValue(n, value ):
    isMe = True
    while n is not None:
        n.N += 1
        if isMe: 
            n.Q = n.Q + value
        else:
            n.Q = n.Q - value
        isMe = not isMe
        n = n.parent
    

def rollout(n):
    result = 0 
    s = copy.deepcopy(n)
    while not s.isFullyExpanded() and boardFull(s.gamestate.current_board()) :
        a = s.randomMove(s.board)
        win,result = s.gamestate.move(a)

        # TODO: break when win or loss
        # TODO: Docstrings
        # TODO mail jorn
    return result

def boardFull(board):
    for row in board:
        for val in row:
            if(val==0):
                return False
    return True
    

def prettyboard(board):
    """
    Function to print the board to the standard out
    :param board: a d by d list representing the board, 0 being empty, 1 black stone, and 2 a white stone
    """
    for row in board:
        for val in row:
            if(val==0):
                print('- ',end='')
            elif(val==1):
                print('o ',end='')
            else:
                print('x ',end='')
        print()


class TreeNode:
    def __init__(self, gamestate=None, parent=None, lastMove=None):
        self.parent = parent
        self.gamestate = gamestate
        self.move=lastMove
        self.children = []
        self.valid_moves = self.checkValidMoves()
        self.N = 0
        self.Q = 0

    def checkValidMoves(self):
        return self.gamestate.valid_moves()

    def isFullyExpanded(self):
        # print("{} == {}".format(len(self.checkValidMoves()), len(self.children)))
        return len(self.checkValidMoves()) == len(self.children)
    

    def uct(self, c=1):
        return (self.Q/self.N) + c * (math.sqrt(math.log2(self.parent.N)/self.N))

    def bestChild(self):
        # Return best child
        highestVal = float("-inf")
        bChild = None
        for child in self.children:
                cVal = child.uct(1)
                if cVal > highestVal:
                    bChild = child 
                    highestVal = cVal
        return bChild


    def bestChildren(self):
        # Return a list of sorted best children

        bChildren = self.children
        bChildren.sort(key=lambda child: child.uct(1))
        # for child in self.children:
        #         cVal = child.uct(1)
        #         if cVal > highestVal:
        #             bChild = child 
        #             highestVal = cVal
        # return bChild
        return bChildren

    def hasFinished(self):
        if self.gamestate is None:
            return True
        return False

    
    def randomMove(self, board):
        return random.choice(board.valid_moves())

   



class vvamp_player:
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """
    def __init__(self, black_=True):
        """Constructor for the player."""
        self.black = black_
        self.ply = 1

    def new_game(self, black_):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_
        if(not black_):
            self.ply = 2


    def move(self, board, last_move, valid_moves, max_time_to_move=1000):
        """This is the most important method: the agent will get:
        1) the current state of the board
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximimum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        t = time.time()
        # print("Move > Start")
        if(len(valid_moves) == 1):
            return valid_moves[0]

        aGame = gomoku.gomoku_game(19, board, self.ply)
        root = TreeNode(aGame, None, last_move)
        # print("Move > Loop")
        while time.time() < t+(max_time_to_move*0.99/1000):
            # print("     Loop > Expand ")
            leaf = findSpotToExpand(root)
            # print("     Loop > Rollout ")
            val = rollout(leaf)
            # print("     Loop > Backup ")
            backupValue(leaf, val)

        bestChild = root.bestChild()
        self.ply += 2

        if not bestChild.move in valid_moves:
            # print("Move > move is invalid, finding new one")
            bestChildren = root.bestChildren()
            if(len(bestChildren) <= 1):
                if bestChildren[0] not in valid_moves:
                    raise IOError
            i=0
            while bestChild.move not in valid_moves:
                # print("Move > move {} is invalid".format(i))
                # print("{}/{}".format(len(bestChildren), i))
                bestChild = bestChildren[i]
                
                i+=1
                if(len(bestChildren) <= i):
                    # print("Move > No valid moves in best children!!!")
                    raise InterruptedError
        

        if bestChild.move in valid_moves:
            root.gamestate.move(bestChild.move)
            # print("Move > Done")   
            return bestChild.move
        else:
            # print("INVAL MOVE!")
            raise InterruptedError

    def id(self):
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "V-Player Vvamp#0001 -- -- -- -- WOOHOOOO ALDSSSS GOMOKUUUU"

