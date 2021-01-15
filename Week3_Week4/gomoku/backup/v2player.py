import random
import time
import copy
import gomoku
import math

class Node:
    def __init__(self, parent, game, last_move):
        self.parent = parent        # Parent
        self.game = game            # Current game
        self.last_move = last_move  # Last move
        self.valid_moves = self.game.valid_moves()
        self.children = []          # Posisible moves
        self.N = 0                  # Number of visits
        self.Q = 0                  # Number of points(wins + 0.5*draws)

    def isTerminal(self):
        """
        Checks if the game has finished
        """
        if len(self.getValidMoves()) == 0 or self.game == None:
            return True 
        else:
            return False
    
    def getValidMoves(self):
        """
        Returns the current valid moves for the game statea
        """
        self.valid_moves = self.game.valid_moves() 
        return self.valid_moves

    def showChildren(self, bc):
        # print(f"Valid Moves: {len(self.valid_moves)}")
        # print(f"Best Child: p:{bc.Q} LM:{bc.last_move}")
        # print("All Children:")
        # for child in self.children:
        #     print(f"- p:{child.Q} LM:{child.last_move}")
        gomoku.prettyboard(self.game.board)
        print(len(self.game.valid_moves()))
        print("--")
        

    def findBestChild(self):
        """
        Find best child with the function provided in the reader
        """
        bestUCT = 0
        bestChild = self.children[0] 
        c = 1 / math.sqrt(2) 
        for child in self.children:
            current_uct = child.Q / child.N + c * math.sqrt(math.log2(child.parent.N) / child.N)
            if current_uct > bestUCT:
                bestChild = child 
                bestUCT = current_uct
        # print("Trying to find best child. Best Child: {}\nChildren:{}".format(bestChild, self.children))
        self.showChildren(bestChild)
        return bestChild
            
        
    def isFullyExpanded(self):
        """
        Check if the node is fully expanded - aka every valid move has a bide 
        """
        return (len(self.valid_moves) == len(self.children)) # If my valid moves == my children, I am fully expanded(For each move, there is a child)


def backupValue(gameresult, node):
    myTurn=True # Always my turn when I start
   
   # Calculate from bottom node to top what the Q and N are per node
    while node is not None:
        node.N+=1
        if myTurn:
            myTurn=False
            node.Q = node.Q - gameresult
        else:
            myTurn=True 
            node.Q = node.Q + gameresult
        node = node.parent
    
def rollout(node):
    """
    Play random moves until the game ends and return a reward(1 if win, 0 if loss, 0.5 if draw)
    """
    #TODO: check if game was a tie
    s_node = copy.deepcopy(node)
    result = 0

    # Play until the last node was played and the game ends
    while not s_node.isTerminal():
        a = random.choice(s_node.getValidMoves()) # Choose a random move

        newGame = copy.deepcopy(s_node.game)
        valid,result = newGame.move(a) # Move chosen move on board

        # If for some reason the move was invalid, just ignore it and try another move
        if not valid:
            continue 
          

        newNode = Node(s_node, newGame, a)    # Store the new move in a node
        s_node = newNode    # Make the current node the new node

        # If I win, return immediately
        if(result):
            return result 

    # Return if win or loss
    return result



def findSpotToExpand(node):
    """
    Finds a new child(a new gamestate associated with a move) for the current node. 
    Alternatively, if all children are already given, calculate the children for the best child.
    """
    # If node is terminal(game finished), return current node
    if node.isTerminal():
        return node 

    if not node.isFullyExpanded():
        # Create a new child node with a random valid move and add it to the current node's children
        new_gamestate = copy.deepcopy(node.game)
        new_gamestate_move = random.choice(node.getValidMoves())
        new_gamestate.move(new_gamestate_move)

        newChild = Node(node, new_gamestate, new_gamestate_move)    
        node.children.append(newChild)

        # Return the new child
        return newChild 
    
    # If the node is already expanded, find the best child of this node and expand that one
    newNode = node.findBestChild()
    findSpotToExpand(newNode)

class vvamp_player:
    def __init__(self, black_=True):
        """Constructor for the player."""
        self.black = black_
        self.play = 1

    def new_game(self, black_):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_
        if(not black_):
            self.play = 2
            
    def move(self, board, last_move, max_time_to_move=1000):
        """This is the most important method: the agent will get:
        1) the current state of the board
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximimum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        valid_moves = gomoku.valid_moves(board)
        time_deadline = time.time() + (max_time_to_move*0.90/1000) # Deadline is 99% of the time to move in ms in ns. Can be optimized

        # If only 1 move is possible, do that move
        if(len(valid_moves) == 1):
            return valid_moves[0]


        currentGame = gomoku.gomoku_game(19, copy.deepcopy(board), self.play)      # Current game board
        rootNode = Node(None, currentGame, last_move)               # Current Rootnode(active gamestate)

        while(time.time() < time_deadline):
            ## Calculate new move
            newLeaf = findSpotToExpand(rootNode)

            ## Play until game ends for that move
            gameresult = rollout(newLeaf)

            ## Calculate score for that move
            backupValue(gameresult, newLeaf)




        # Find best child

        #-- Met de code hieronder zou die als die een fout maakt, alsnog een slimme keuze moeten maken. Dit was tijdelijke code, maar maakt hem ook dommer?
        # bestChild = None
        # while len(rootNode.children) != 0:
        #     bestChild = rootNode.findBestChild()
        #     if not bestChild.last_move in valid_moves:
        #         rootNode.children.remove(bestChild)
        #         print("Current best child move is invalid")
        #     else:
        #         break
        
        # if not bestChild.last_move in valid_moves:
        #     print("Chosen best child move is invalid")
        #     return valid_moves[0]

        # If the best child is invalid for some reason, just use a random valid move
        bestChild = rootNode.findBestChild()
        if not bestChild.last_move in valid_moves:
                print("Chosen best child move is invalid")
                return valid_moves[0]





        print("Supplied Valid Moves: {}".format(len(valid_moves)))
        print("Simulated Valid Moves: {}".format(len(currentGame.valid_moves())))
        gomoku.prettyboard(currentGame.board)

        self.play += 2
        return bestChild.last_move

    def id(self):
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "V-Player v2 - By Vvamp#0001"