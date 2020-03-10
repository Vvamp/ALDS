import random
import datetime


class nodeLeaf:
	def __init__(self, parent, N, Q,children=[None]):
		self.parent = parent
		self.N = N 
		self.Q = Q
		self.children = children
	
class Tree:
	def __init__(self, root):
		self.root = root
	


class vince_player():
	"""
	This is an agent class for the game 'go-moku', written by Vincent van Setten.
	It inherits from the "random_player" class.
	"""
	def id(self):
		"""
		Returns this class's ID
		"""
		return "vincent_player"

	def print_player(self):
		"""
		Prints the vince_player's information.
		Prints the id and what colour the player is.
		"""
		player_colour = "Black"
		if self.black is not True:
			player_colour = "White"
		print("-- vince_player object --\nID: {}\nColour: {}\n\n".format(self.id(), player_colour))

	def findSpotToExpand(self, n):
		if n.children is None:
			return n 
		else:
			n.children.append("o")
			return "h"
		
		
		
	def rollout(self, n):
		while 1:
			return random.choice(self.valid_moves)
	
	def backupVal(self, n, v):
		print("Leaf: {}\nValue: {}".format(n, v))
		pass

	def move(self, board, last_move, valid_moves, max_time_to_move_ms=1000):
		"""This is the most important method: the agent will get:
		1) the current state of the board
		2) the last move by the opponent
		3) the available moves you can play (this is a special service we provide ;-) )
		4) the maximimum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
		"""
		max_time_to_move_datetime = datetime.datetime.now() + datetime.timedelta(milliseconds=max_time_to_move_ms)
		while datetime.datetime.now() < max_time_to_move_datetime:
			self.valid_moves = valid_moves
			nLeaf = self.findSpotToExpand(board)
			val = self.rollout(nLeaf)
			self.backupVal(nLeaf, val)

		return "> Done"


# Initialize vince_player object with default colour(black)
vincents_player = vince_player()

# Print vince_player object info
vincents_player.print_player()

class GameDummy:
	def __init__(self, children):
		self.children = children 



gameDummy = GameDummy(["a", "b"])

print(vincents_player.move(gameDummy, "up", ["up", "left", "right"]))

