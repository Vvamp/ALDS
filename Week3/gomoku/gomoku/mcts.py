import time
import gomoku
import random
import numpy as np
from pprint import pprint

class MCTS_Node:

    def __init__(self, state=None, valid_moves=None, parent=None, current=None):

        self.state      = state                     # State of the game, board
        self.moves      = valid_moves               # Get current valid moves
        self.current    = current
        self.parent     = parent                    # Parent of the node
        self.children   = []                        # Children of the node
        self.n          = 1                         # Number of visits
        self.q          = 1                         # Win-Lose values


    def move(self, action):

        new_game = gomoku.gomoku_game(board_=self.state.current_board(), ply_=self.state.ply)
        ok, win  = new_game.move(action)

        if ok and not win:                          # If the move is ok and we didn't won yet, return the game state
            return new_game, action
        
        return None, self.calc_score( ok, win )     # If the condition isn't met change the state to 'None' and calculate the score


    def calc_score(self, ok, win):

        if not ok:                                  # Disqualified? Return 0
            return 0

        elif win:                                   # Won the game? Return 1
            return 1

        elif len(self.moves) is 0:                  # Out of moves (draw)? Return 0.5
            return 0.5

        return 0                                    # Return None if no condition is met


    def is_fully_expanded(self):                    # Are there any moves left?
        return len(self.moves) is 0


    def rollout_policy(self):                       # Perform a random rollout policy
        return random.choice(self.moves)

    
    def results(self):
        return self.q


    def new_root(self, last_move):

        for c in self.children:

            if last_move == c.current:
                return c
        
        return self


    def uct(self, c_param=1.3):              # Get the best node according to UCT value

        choices_weights = [
            (c.results() / c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]

        return self.children[np.argmax(choices_weights)]

    def best_child(self):

        pro_child = self.children[0]

        for c in self.children[1:]:
            
            if( c.q / c.n ) > (pro_child.q / pro_child.n):
                pro_child = c

        return pro_child

    def is_terminal(self):                          # Check if game has finished

        if self.state is None:
            return True

        return False
