import random
import gomoku
import copy
import time
import math


class random_dummy_player:
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """

    def __init__(self, black_=False):
        """Constructor for the player."""
        self.black = black_
        self.firstMoveInMiddle = black_
        print("player " + str(self.id()) +
              " is color black: " + str(self.black))

    def new_game(self, black_, game=None):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_

    def move(self, board, last_move, valid_moves, max_time_to_move=1000):
        """This is the most important method: the agent will get:
        1) the current state of the board
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximimum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        return random.choice(valid_moves)

    def id(self):
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "Random move AI"


class Monte_Carlo_Search_Tree_Node:
    """ implementation of a monte carlo search tree with the gomoku game"""

    def __init__(self, game=None, timesVisited=0, last_move=None, parentNode=None):
        """This constructor needs the following params
        1) game, a gomoku game 
        2) the number of times this node was visisted
        3) optional, the move that was made in this node's game
        4) optional, the parent node which made this node"""
        self.game = game
        self.last_move = last_move
        self.children = []
        self.parentNode = parentNode
        self.value = 0
        self.timesVisited = timesVisited
        self.finished = False
        if last_move is not None:
            self.checkIfFinished()

    def print_MCST_node(self):
        """function to print all info from the node"""
        gomoku.prettyboard(self.game.board)
        print("last move: " + str(self.last_move))
        print("finished: " + str(self.finished))
        print("UCT Value: " + str(self.value))
        print("times visited: " + str(self.timesVisited))
        print("nr of children: " + str(len(self.children)))
        if self.parentNode is not None:
            print("has parent: True")
        else:
            print("has parent: False")

    def expandThisNodeWithAllValidMoves(self, valid_moves):
        """This makes all the children with a possible valid move on the board for this node.
        1) an array with all the valid_moves that are possible"""

        for move in valid_moves:
            temp_game = gomoku.gomoku_game(
                board_=self.game.current_board(), ply_=copy.deepcopy(self.game.ply))
            temp_game.move(move)
            childNode = Monte_Carlo_Search_Tree_Node(
                temp_game, 0, copy.deepcopy(move), self)
            self.children.append(childNode)
        return

    def whichPlayerWasThisTurn(self):
        """Function to check which player's turn it was on this node's gamestate"""
        if self.game.ply % 2 == 1:
            return 1
        else:
            return 2

    def checkIfFinished(self):
        """Function to update the finished variable with a bool. It will turn true when the game was won, or when the there were no more valid moves left on this state"""
        self.finished = self.game.check_win(self.last_move)
        if not self.finished:
            self.finished = len(self.children) == len(self.game.valid_moves())


def calculateUTC(n, parentN, q, c=1/math.sqrt(2)):
    """This function is my implementation (and understanding) of the UTC value calculation
    1) n, the number of times the child node was visited
    2) parentN, the number of times the parent of the child node was visited
    3) q, the value (wins and loses) of the child node
    4) optional, c, the constant you want to calculate the UTC with. This is some black magic and I cannot explain it. But change this value to get other results """
    return (q/n) + c * (math.sqrt(math.log2(parentN)/n))

# deze functie is raar, Diederik vragen? Hoe werkt dit? wat is finished? Maar vooral, wat is de "not yet explored move (reader)" en waar komt die vandaan???
# DEZE IS SOWIESO VERKEERD, MET DIEDERIK BESPREKEN!!!!!
def findSpotToExpand(node):
    print("find spot to expand begin")
    valid_moves = node.game.valid_moves()
    if node.finished or len(node.children) >= len(valid_moves):
        print("node was finished so stop find spot to expand")
        return node
    if len(node.children) < len(valid_moves):
        print("node had less children than valid moves length so continue")
        nextValidMove = valid_moves[len(node.children)]
        gomoku.prettyboard(node.game.board)
        print("oldply: " + str(node.game.ply))
        newGame = gomoku.gomoku_game(board_=node.game.current_board(), ply_=node.game.ply)
        print("newply: " + str(newGame.ply))
        print(newGame.move(nextValidMove))
        print("newply: " + str(newGame.ply))
        new_node = Monte_Carlo_Search_Tree_Node(newGame, 0, nextValidMove, node)
        node.children.append(new_node)
        return new_node

    print("find spot to expand in het stuk waarvan ik denk dat ie daar nooit komt")
    max_uct = -100000
    nodeWithBestUCT = None
    for child in node.children:
        print("find spot to expand for loop door children")
        som = calculateUTC(child.timesVisited, node.timesVisited, child.value)
        if som > max_uct:
            max_uct = som
            nodeWithBestUCT = child
    return findSpotToExpand(nodeWithBestUCT)


def rollout(node):
    print("rollout begin")
    tempNode = copy.deepcopy(node)
    won = False
    while not won and len(tempNode.game.valid_moves()) > 0:
      #  print("rollout while loop")
        validMoves = tempNode.game.valid_moves()
        move = random.choice(validMoves)
        succeeded, won = tempNode.game.move(move)
    # hoe doe ik dit winnen en verliezen???? zo goed???
    if len(validMoves) == 0 and not won:
        return 0
    if tempNode.game.ply % 2 == 1:
        return 1
    else:
        return -1


def backupValue(node, val):
    print("backupvalue begin")
    while node is not None:
        print("backupvalue while loop")
        node.timesVisited += 1
        if node.game.ply %2 == 0:
            node.value = node.value - val
        else:
            node.value = node.value + val
        node = node.parentNode


def monte_carlo_tree_search(board, ply, move, move_time):
    """This function is my implementation (and understanding) of algorithm 20 of the ALDS reader.
    1) game, a gomoku game object from where you want to start searching
    2) move, a valid move
    3) move_time, the time the algorithm has to explore """
    # create the start time, make a new "root" node with the move played
    print("monte carlo tree search begin")
    startTime = time.time_ns()
    new_game = gomoku.gomoku_game(
        board_= board, ply_=copy.deepcopy(ply))
    gomoku.prettyboard(new_game.board)
    print(new_game.ply)
    rootNode = Monte_Carlo_Search_Tree_Node(new_game, 0, copy.deepcopy(move)) #create the rootnode with gamestate s0
    # go into the loop
    c = 0
    while True:
        c+=1
        print("monte carlo tree search while loop: "+str(ply)+",  iter: "+str(c))
        if time.time_ns() - startTime >= move_time*10000000 - 500: #check if out of time, else break
            break
        leaf = findSpotToExpand(rootNode) #find spot to expand and put in leaf variable
        val = rollout(leaf) #put rollout in val
        backupValue(leaf, val) # back up the values through the tree
        print("rn_ch: "+str(len(rootNode.children)))

    # check which players turn it is to ensure that the algorithm searches for the node with the value that is good for the player whos turn it is. i.e. if the white player
    # starts searching for a uct value that is positive, he will in fact make moves that are good for the black player
    # the node that is going to contain the best move (last_move) the game should make
    print(len(rootNode.children))
    nodeWithMoveToMake = rootNode.children[0]
    # take the first child as benchmark
    print(len(rootNode.children))
    max_value = rootNode.children[0].value / rootNode.children[0].timesVisited
    for child in rootNode.children:
        som = child.value/child.timesVisited
        if som > max_value:
            max_value = som
            nodeWithMoveToMake = child
    return nodeWithMoveToMake


class Good_Player:
    """This class specifies a player that uses a monte carlo tree search algorithm to make moves.
    """

    def __init__(self, main_game, black_=True):
        """Constructor for the player.
        1) main (first) gomoku game reference reference
        2) wether it is black or not"""
        self.main_game = main_game
        self.black = black_
        self.rootNode = None #Monte_Carlo_Search_Tree_Node(copy.deepcopy(main_game))

    def new_game(self, black_, game=None):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_
        print("player " + str(self.id()) +
              " is color black: " + str(self.black))
        self.main_game=game

    def move(self, board, last_move, valid_moves, max_time_to_move=1000):
        """This is the most important method: the agent will get:
        1) the current state of the board
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximimum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        choice = random.choice(valid_moves)
        #hier zometeen de functies van het tree searchen
        gomoku.prettyboard(board)
        print(self.main_game.ply)
        self.rootNode = monte_carlo_tree_search(board, self.main_game.ply, choice,max_time_to_move)
        return  self.rootNode.last_move

    def id(self):
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "Oscar Kromhout"
