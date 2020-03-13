import random
import copy
import gomoku
import mcts
import time
from pprint import pprint

class pro_player:

    def __init__(self, black_=True, ply_=1, game=None, root=None):
        self.black   = black_
        self.ply     = ply_
        self.game    = game
        self.n_root  = root

    def new_game(self, black_):
        self.black = black_

        if black_:
            self.ply = 1

        else:
            self.ply = 2

        if self.n_root is None:
            self.game   = gomoku.gomoku_game(ply_=self.ply)                # Create a new game    

    def move(self, board, last_move, valid_moves, max_time_to_move=1000):

        # start_time = time.time_ns()
        
        if self.ply is 1:
            self.n_root = mcts.MCTS_Node(state=self.game, valid_moves=valid_moves)                  # Create the root node
            self.game.move(valid_moves[0])
            return valid_moves[0]

        elif self.ply is 2:
            self.game.move(last_move)
            self.n_root = mcts.MCTS_Node(state=self.game, valid_moves=valid_moves)                  # Create the root node

        else:
            self.game.move(last_move)
            self.n_root = self.n_root.new_root(last_move)
            # self.n_root.moves = self.game.valid_moves()

        for i in range(100):                                                        # <<<<< !!!! Change to 'out of time' loop
            n_leaf = self.FindSpotToExpand( self.n_root )
            val    = self.rollout( n_leaf )
            self.BackupValue( n_leaf, val )

        # pprint(gomoku.prettyboard(self.game.board))
        # print(self.black)

        best = self.n_root.uct().current

        # print(best)
        # print("===>", self.ply, "\n")

        self.game.move(last_move)
        # self.n_root = self.n_root.new_root(last_move)
        self.ply += 2

        return best


    def FindSpotToExpand(self, node):

        if node.is_terminal():                                                          # Check if game finished
            return node

        if not node.is_fully_expanded():                                                # Is fully expanded?
            action       = random.choice(node.moves)
            node.moves.remove(action)

            new_moves = copy.deepcopy(node.moves)

            new_state    = node.move(action)
            new_node     = mcts.MCTS_Node(state=new_state[0], valid_moves=new_moves, parent=node, current=action)
            node.children.append(new_node)
            
            return new_node

        new_node = node.uct()

        return self.FindSpotToExpand(new_node)


    def rollout(self, node):

        score = 0

        while node.state is not None:
            
            action             = node.rollout_policy()                                  # Generate random action by using the rollout policy
            new_state, result  = node.move(action)                                      # Peform the action, return the new state and result if excist
            node.state         = new_state                                              # Change the state of the node with the new state

            score = result

        return score


    def BackupValue(self, node, value):
        
        while node is not None:

            node.n += 1                                                                 # Increment the number of visits

            try:                                                                        # Get the current ply that is equal to the node
                game_ply = node.state.ply

            except AttributeError:
                game_ply = node.parent.state.ply + 1

            if self.is_oppponent(game_ply):                                             # Check if ply is opponent,
                node.q = node.q - value                                                 # If True: Minimize value

            else:
                node.q = node.q + value

            node = node.parent
            

    def is_oppponent(self, ply):

        is_even = (ply % 2) is 0                                                        # Check if ply is an even number

        if is_even and not self.black:                                                  # If ply is even and opponent is white,
            return True                                                                 # Return True

        elif not is_even and self.black:                                                # If ply is not even and opponent is black,
            return True                                                                 # Return True

        return False                                                                    # Return False if ply is not from the opponent


    def id(self):
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "Gomoku TA - Justin van Ziel"

    