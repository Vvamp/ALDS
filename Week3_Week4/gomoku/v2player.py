import random
import time
import copy
import gomoku
import multiprocessing
import numpy as np
from typing import Tuple

import math


class Node:
    def __init__(self, parent, game: gomoku.GameState, last_move: gomoku.Move):
        self.parent = parent  # Parent
        self.game = game  # Current game state
        self.last_move = last_move  # Last move
        self.valid_moves = self.getValidMoves()
        self.children = []  # Posisible moves
        self.N = 0  # Number of visits
        self.Q = 0  # Number of points(wins + 0.5*draws)

    def isTerminal(self):
        """
        Checks if the game has finished
        """
        if len(self.valid_moves) == 0 or self.game == None:
            return True
        else:
            return False

    def getValidMoves(self):
        """
        Returns the current valid moves for the game statea
        """
        self.valid_moves = gomoku.valid_moves(self.game)
        return self.valid_moves

    def findBestChild(self):
        """
        Find best child with the function provided in the reader
        """
        if len(self.children) == 0:
            return self
        bestUCT = 0
        bestChild = self.children[0]
        c = 1 / math.sqrt(2)  # might be optimizable (the value)
        for child in self.children:
            current_uct = child.Q / child.N + c * math.sqrt(
                math.log2(child.parent.N) / child.N
            )
            if current_uct > bestUCT:
                bestChild = child
                bestUCT = current_uct
        return bestChild

    def isFullyExpanded(self):
        """
        Check if the node is fully expanded - aka every valid move has a bide
        """
        return len(self.valid_moves) == len(
            self.children
        )  # If my valid moves == my children, I am fully expanded(For each move, there is a child)


def backupValue(gameresult, node):
    """Calculate N and Q for each node from 'node' until root

    Args:
        gameresult (int): Result of node's game
        node (Node): The node to start calculating from
    """
    # print("Backing up value from: ", node, " with res: ", gameresult)
    myTurn = True  # Always my turn when I start

    # Calculate from bottom node to top what the Q and N are per node
    while node is not None:
        node.N += 1
        if myTurn:
            myTurn = False
            node.Q = node.Q - gameresult
        else:
            myTurn = True
            node.Q = node.Q + gameresult
        node = node.parent


def rollout(node: Node) -> int:
    """Play random moves until the game ends and return a reward(1 if win, 0 if loss, 0.5 if draw)


    Args:
        node (Node): The node to rollout from

    Returns:
        int: The game result
    """
    # print("Rollout: ", node)
    s_node = copy.deepcopy(node)
    result = 0
    # Play until the last node was played and the game ends
    if s_node == None:
        # print("Node was none in rollout!")
        return 0

    while not s_node.isTerminal():
        a = random.choice(s_node.valid_moves)  # Choose a random move

        newGame = copy.deepcopy(s_node.game)
        valid, result, newGame = gomoku.move(newGame, a)

        # If for some reason the move was invalid, just ignore it and try another move
        if not valid:
            continue

        newNode = Node(s_node, newGame, a)  # Store the new move in a node
        s_node = newNode  # Make the current node the new node

        # If I win, return immediately
        if result:
            return result

    # Return if win or loss
    return result


def findSpotToExpand(node, valid_moves):
    """
    Finds a new child(a new gamestate associated with a move) for the current node.
    Alternatively, if all children are already given, calculate the children for the best child.
    """
    # print("Find spot to expand: ", node, " valid moves: ", valid_moves)
    # If node is terminal(game finished), return current node
    if node.isTerminal():
        # print("Node terminal in findspottoexpand: ", node)
        return node

    if not node.isFullyExpanded():
        # Create a new child node with a random valid move and add it to the current node's children
        new_gamestate = copy.deepcopy(node.game)
        new_gamestate_move = random.choice(node.valid_moves)

        valid, win, ngs = gomoku.move(new_gamestate, new_gamestate_move)
        if type(ngs) != gomoku.GameState and type(ngs) != tuple:
            print(type(ngs))
            print("Error in findspottoexpand!")
            return node
        newChild = Node(node, ngs, new_gamestate_move)
        node.children.append(newChild)

        # Return the new child
        # print("Returning newchild: ", newChild)
        return newChild

    # print("FSTE > Node is fully expanded. Finding best child and calling that")
    # If the node is already expanded, find the best child of this node and expand that one
    newNode = node.findBestChild()
    # print("FSTE > Best child: ", newNode)
    return findSpotToExpand(
        newNode, gomoku.valid_moves(newNode.game)
    )  # Find a new one with the list of valid moves


def worker_task(rootNode, valid_moves):
    newLeaf = findSpotToExpand(rootNode, valid_moves)
    gameresult = rollout(newLeaf)
    backupValue(gameresult, newLeaf)
    return


class vvamp_player:
    def __init__(self, black_=True):
        """Constructor for the player."""
        self.black = black_

    def new_game(self, black_):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_
        if not black_:
            self.play = 2

    def move(self, state, last_move, max_time_to_move=1000):
        """This is the most important method: the agent will get:
        1) the current state of the state
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximimum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        valid_moves = gomoku.valid_moves(state)
        time_deadline = time.time() + (
            max_time_to_move * 1 / 1000
        )  # Deadline is 99% of the time to move in ms in ns. Can be optimized

        board = state[0]
        ply = state[1]

        # If only 1 move is possible, do that move
        if len(valid_moves) == 1:
            return valid_moves[0]

        currentGame = copy.deepcopy(state)  # Current game board
        rootNode = Node(
            None, currentGame, last_move
        )  # Current Rootnode(active gamestate)
        cRound = 0
        pool = multiprocessing.Pool(4)
        time_deadline = time.time + max_time_to_move/1--  # Example deadline

        while time.time() < time_deadline:
            # Submit a new task
            pool.apply_async(worker_task, args=(rootNode, valid_moves))

            # You may want to check here if it's time to stop submitting new tasks
            if time.time() >= time_deadline:
                break

        pool.close()
        pool.join()

        # If the best child is invalid for some reason, just use a random valid move
        # With the new code it should always be valid, but just in case
        bestChild = rootNode.findBestChild()
        if not bestChild.last_move in valid_moves:
            print("Chosen best child move is invalid")
            return valid_moves[0]

        self.play += 2
        return bestChild.last_move

    def id(self):
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "V-Player v2 - By Vvamp#0001"
