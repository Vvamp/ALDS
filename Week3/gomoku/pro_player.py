import random
import datetime
import game
import random_player
import pprint
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

class Node:
    def __init__(self, parent, board, N=0, Q=0, children=[]):
        self.parent = parent
        self.board = board
        self.N = N
        self.Q = Q
        self.children=children


class Tree:
    def __init__(self, root):
        self.root = root
    

class gom_player():
    """
    This is an agent class for the game 'go-moku', written by Vincent van Setten.
    """
    def id(self):
        """
        Returns this class's ID
        """
        return "PRO-PLAYER # Vincent van Setten, V2C"

    def __init__(self, black_=True):
        self.black = black_
        self.ply = 1

    def print_player(self):
        """
        Prints the gom_player information.
        Prints the id and what colour the player is.
        """
        player_colour = "Black"
        if self.black is not True:
            player_colour = "White"
        print("-- ProPlayer by Vvamp --\nID: {}\nColour: {}\n\n".format(self.id(), player_colour))

    def isFullyExpanded(self, n):
        if len(self.getPossibleMoves(n.board)) == len(n.children):
            return True
        return False

    def getPossibleMoves(self, state):
        dummyGame = game.gomoku_game(board_=state, ply_= self.ply)
        return dummyGame.valid_moves()

    def findSpotToExpand(self, n):
        if len(n.children) == 0:
            return n
        
        if not self.isFullyExpanded(n):
            dummyGame = game.gomoku_game(board_=n.board, ply_=self.ply)
            dummyGame.move(random.choice(self.getPossibleMoves(n.board)))
            nP = Node(n, dummyGame.current_board())
            n.children.append(nP)
            return nP 

        nP = max(n.children, n.q)
        return self.findSpotToExpand(nP)
        
    def rollout(self, n):
        dummyGame2 = game.gomoku_game(board_=n.board, ply_=self.ply)
        i = 0
        while len(self.getPossibleMoves(dummyGame2.current_board())) >= 1:
            print(i)
            a = random.choice(self.getPossibleMoves(dummyGame2.current_board()))
            dummyGame2.move(a)
            nP = Node(n, dummyGame2.current_board())
            n = nP
            i+=1
            print("Moves: ", len(self.getPossibleMoves(dummyGame2.current_board())))
            if(i % 500 == 0):
                prettyboard(dummyGame2.board)
        return dummyGame2.check_win(dummyGame2.previous_move)

    def checkPly(self, board):
        count = 0
        for x in board:
            for y in x:
                if(y != 0):
                    count += 1
        return count


    def move(self, board, last_move, valid_moves, max_time_to_move_ms=1000):
        """This is the most important method: the agent will get:
        1) the current state of the board
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximimum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        # max_time_to_move_datetime = datetime.datetime.now() + datetime.timedelta(milliseconds=max_time_to_move_ms)
        # while datetime.datetime.now() < max_time_to_move_datetime:
        #     self.valid_moves = valid_moves
        #     nLeaf = self.findSpotToExpand(board)
        #     val = self.rollout(nLeaf)
        #     self.backupVal(nLeaf, val)
        self.ply = self.checkPly(board)
        nRoot = Node(None, board)
        nLeaf = self.findSpotToExpand(nRoot)

        val = self.rollout(nLeaf)
        print(val)
        # self.tree = Tree(nRoot)
        self.valid_moves = valid_moves
        self.current_board = board

        return "h"


# Initialize vince_player object with default colour(black)
vincents_player = gom_player()

# Print vince_player object info
vincents_player.print_player()

class GameDummy:
	def __init__(self, children):
		self.children = children 



# gameDummy = GameDummy(["a", "b"])

# print(vincents_player.move(gameDummy, "up", ["up", "left", "right"]))



game2 = game.gomoku_game()
player = random_player.random_dummy_player()
move1= player.move(game2.current_board(), game2.previous_move, game2.valid_moves())

game2.move(move1)
move2=vincents_player.move(game2.current_board(), game2.previous_move, game2.valid_moves())
game2.move(move2)
move2=player2.move(game2.current_board(), game2.previous_move, game2.valid_moves())
game2.move(move2)
# prettyboard(game2.current_board())


b = []
g = []
# # Using a custom board works when creating my own
# # However,when using the current_board(), it doesn't do anything with the board. it remains empty, as if it doesn't move.
for i in range(19):
    g.append([0] * 19)  #
import copy
c = copy.deepcopy(game2.current_board())
for x in c:
    o = []
    for y in x:
        # for z in y:
        if y == 1:
            o.append(1)
        elif y == 2:
            o.append(2)
        elif y == 0:
            o.append(0)
    b.append(copy.deepcopy(o))
print(type(b))
print(type(c))
game3 = game.gomoku_game(board_=b, ply_=game2.ply)
print('==========')
# prettyboard(b)
print('==========')

# game3 = game.gomoku_game(board_=b)
i=0
# while(i<100):
#     game3.move(player.move(game3.current_board(), game3.previous_move, game3.valid_moves()))
#     i+=1
print("OM: {}".format(game2.previous_move))
move2=player2.move(game3.current_board(), game2.previous_move, game2.valid_moves())
game3.move(move2)
print("OM: {}".format(game3.previous_move))

move2=player2.move(game3.current_board(), game3.previous_move, game3.valid_moves())
game3.move(move2)
print("OM: {}".format(game3.previous_move))

move2=player2.move(game3.current_board(), game3.previous_move, game3.valid_moves())
game3.move(move2)
prettyboard(game3.cur7rent_board())

print('============')
# pprint.pprint(g)
print('=============')
# pprint.pprint(b)