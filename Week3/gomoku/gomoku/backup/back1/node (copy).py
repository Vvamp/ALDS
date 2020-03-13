import random
import time

class Node:

    def __init__(self, parent=None):

        self.parent     = parent
        self.children   = []
        self.n          = 0                         # Number of visits
        self.q          = 0                         # Win-Lose values


    def best_child(self):
        return True

    def is_terminal(self):
        return False

    def is_fully_expanded(self):
        return True

class MCTS:

    def __init__(self, board, last_move, valid_moves, max_time_to_move):
        
        self.board          = board
        self.last_move      = last_move
        self.valid_moves    = valid_moves
        self.max_time       = max_time_to_move

    def mcts(self, game_state):

        n_root = Node(game_state)

        while time.time_ns < self.max_time:
            
            n_leaf = self.FindSpotToExpand( n_root )
            val    = self.rollout( n_leaf )
            self.BackupValue( n_leaf, val )

        return n_root.best_child()

    def FindSpotToExpand(self, node):

        if node.is_terminal():
            return node

        if not node.is_fully_expanded(self.board, self.valid_moves): #<<< check for valid move ? pop from the valid list?
            new_node = Node(node)   #? empty node with 'root' as parent
            node.children.append(new_node)
            return new_node

        new_node = node.best_child()
        return self.FindSpotToExpand(new_node)

    def rollout(self, node):
        return 1

    def BackupValue(self, node, value):
        return
