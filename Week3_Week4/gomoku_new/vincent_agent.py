from basePlayer import basePlayer
import random
from gomoku import Move, GameState
from GmUtils import GmUtils
import time, copy, math

# TOdo: I still don't win
# Todo: memoization. Don't throw away any nodes with more plays than the current ply. Try to find the current node and continue with that as root node(as some nodes will already be finished)
# 2 - Root
# 4 - Children of children

nodes = 0


class Node:
    def __init__(self, gameState, isBlack: bool, lastMove, isPlayer: bool, parent=None):
        self.parent = parent
        self.gameState = gameState
        self.lastMove = lastMove
        self.isBlack = isBlack
        self.isPlayer = isPlayer
        self.children = set()
        self.explored_moves = set()
        self.N = 0  # Number of visits
        self.valid_moves = None
        self.Q = 0  # Accrued points: wins + 0.5*draws
        global nodes
        nodes += 1

    def isTerminal(self):
        return len(self.get_valid_moves()) == 0

    def getUct(self):
        c = 1 / math.sqrt(2)  # TODO: Play with value
        uct = self.Q / self.N + c * math.sqrt(math.log2(self.parent.N) / self.N)
        return uct

    def get_valid_moves(self):
        if self.valid_moves == None:
            self.valid_moves = set(
                GmUtils.getValidMoves(self.gameState[0], self.gameState[1])
            )
        return self.valid_moves

    def get_unexplored_moves(self):
        return self.valid_moves - self.explored_moves

    def addChildNode(self, newChild):
        if self.valid_moves == None:
            self.get_valid_moves()
        self.children.add(newChild)
        self.explored_moves.add(newChild.lastMove)


def findSpotToExpand(root_node: Node):
    valid_moves = root_node.get_valid_moves()
    if len(valid_moves) == 0:
        return root_node

    unexplored_moves = valid_moves - root_node.explored_moves
    if len(unexplored_moves) == 0:
        best_child = max(root_node.children, key=lambda child: child.getUct())

        return findSpotToExpand(best_child)

    # Get random child
    newMove = random.choice(tuple(unexplored_moves))
    newState = copy.deepcopy(root_node.gameState)
    GmUtils.addMoveToBoard(newState[0], newMove, not root_node.isBlack)
    newNode = Node(
        newState, not root_node.isBlack, newMove, not root_node.isPlayer, root_node
    )
    root_node.addChildNode(newNode)

    return newNode


def rollout(leaf_node: Node):
    lastMove = None
    isPlayer = leaf_node.isPlayer
    isBlack = leaf_node.isBlack
    gameState = copy.deepcopy(leaf_node.gameState)
    currentNode = leaf_node
    valid_moves = currentNode.get_valid_moves()

    if len(valid_moves) == 0:
        currentNode.get_valid_moves()
    while len(valid_moves) != 0:
        valid_moves = currentNode.get_valid_moves()

        if len(valid_moves) == 0:
            break
        isPlayer = not isPlayer
        isBlack = not isBlack
        lastMove = random.choice(tuple(valid_moves))
        newState = copy.deepcopy(currentNode.gameState)
        GmUtils.addMoveToBoard(newState[0], lastMove, isBlack)
        newNode = Node(newState, isBlack, lastMove, isPlayer, currentNode)
        currentNode.addChildNode(newNode)
        valid_moves = currentNode.get_valid_moves()
        currentNode = newNode

    winnerExists = GmUtils.isWinningMove(lastMove, gameState[0])
    if winnerExists == False:
        return 0.5  # Tied

    return GmUtils.isWinningMove(lastMove, gameState[0]) and isPlayer


def backupValue(game_result, leaf_node: Node):
    while leaf_node is not None:
        leaf_node.N += 1
        if not leaf_node.isPlayer:
            leaf_node.Q = leaf_node.Q - game_result
        else:
            leaf_node.Q = leaf_node.Q + game_result
        leaf_node = leaf_node.parent


class VincentAgent(basePlayer):
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """

    def __init__(self, black_: bool = True):
        """Constructor for the player."""
        self.black = black_

    def new_game(self, black_: bool):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_

    def move(
        self, state: GameState, last_move: Move, max_time_to_move: int = 1000
    ) -> Move:
        """This is the most important method: the agent will get:
        1) the current state of the game
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        global nodes
        nodes = 0
        # If only 1 move is possible, automatically do that move
        valid_moves = GmUtils.getValidMoves(state[0], state[1])
        if len(valid_moves) == 1:
            return valid_moves[0]

        nRoot = Node(state, not self.black, last_move, False)  # Node x

        time_deadline = (
            time.time() + (max_time_to_move * 0.5) / 1000
        )  # Deadline is 99% of the time to move in ms in ns. Can be optimized

        while time.time() < time_deadline:
            ## Calculate new move
            newLeaf = findSpotToExpand(nRoot)
            if time.time() >= time_deadline:
                break
            ## Play until game ends for that move
            val = rollout(newLeaf)
            if time.time() >= time_deadline:
                break

            ## Calculate score for that move
            backupValue(val, newLeaf)

        best_move: Node = max(
            nRoot.children, key=lambda child: child.Q / max(child.N, 1)
        )
        # print("Did best move:", best_move.lastMove, "out of", len(nRoot.children),"/",len(valid_moves), "and total nodes:", nodes)
        return best_move.lastMove

    def id(self) -> str:
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "Vincent van Setten (1734729)"
