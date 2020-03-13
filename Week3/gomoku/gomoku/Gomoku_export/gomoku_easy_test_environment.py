# Gomoku easy test environment  (by Marius Versteegen)

# FIRST, RUN THIS AT THE COMMAND PROMPT (to download the pygame library)
# python -m pip install -U pygame --user

# Tips + potentiele instinkers bij Gomoku
'''
    Deze voorbeeldcode heeft een aantal handige test-faciliteiten:
    - Via de klasse GmGameRules kun je de board afmetingen en het aantal stenen op een rij dat wint instellen.
    - Via een gui kun je zelf meespelen, als je een (of meerdere) human player toevoegt.

    * Begin met het implementeren van de pseusdocode voor een zuivere MontecarloPlayer.
    * Test die met een klein board (2x2) om de basis-algoritmen te debuggen
    * Gebruik de debugger, met breakpoints en de mogelijkheid om dingen tijdens zo'n breakpoint 
        aan te roepen, zoals self.printTree(node)
    * Gebruik ook de profiler (in plaats van timeit) om een goed overzicht te krijgen van waar de 
      rekentijd zit.
    * Herschrijf de functie isWinningMove zodanig dat het aantal op een rij dat wint instelbaar is.
      Stel het daarmee vervolgens in op 3 op een rij.
    * Maak het bord 3x3 en test het 3 op een rij spel.
    * Je kunt een enkele move onderzoeken door je board vooraf een bepaalde waarde te geven, zoals
      [[1,2,0],[2,0,0],[1,0,0]] # 0=empty, 1=zwart, 2=wit
    * Let op bij FindSpotToExpand: een winning node is ook een terminal node!
    * Maak een printNode en printTree functie, waardoor je snel een overzicht kunt krijgen van 
      een enkele node en haar kinderen of in het geval van printTree: de hele boom die er onder hangt.
      Print van elke node positie, N, Q en uct
    * Houd je Montecarlo-player klasse klein. Verhuis 2e orde utility functies naar een andere klasse
      met @staticmethod functies.
    * De beste move die je uiteindelijk selecteert is niet de move met de hoogste Q, maar de move met de hoogste Q/N
      (NB: de findspot to expand gebruikt daarentegen de uitkomst van de uct formule als criterium)
    * Je zult merken dat 5 op een rij op een 8x8 board met zuiver MontecarloPlayer als tegenstander nog goed
      werkt als die tegenstander zo'n 2 seconden de tijd heeft.
    * Om de effectiviteit van je heuristiek te testen zou je voorlopig op dat bord kunnen blijven testen,
      en kijken of je dankzij die heuristiek je rekentijd met een bepaalde factor kunt verkleinen-zonder dat het
      tegenspel slecht wordt.
'''

# TODO: start with Move Center

import random, sys, pygame, time, math, copy
from pygame.locals import *
from pygame.locals import KEYUP,QUIT,MOUSEBUTTONUP,K_ESCAPE

class GmGameRules():
    winningSeries=5
    BOARDWIDTH=19
    BOARDHEIGHT=19

# The Gomoku Game class
class GmGame():
    DIFFICULTY = 1 # how many moves to look ahead. (>2 is usually too much)
    
    SPACESIZE = 35 # size of the tokens and individual board spaces in pixels
    
    FPS = 30 # frames per second to update the screen
    WINDOWWIDTH = 1024 # width of the program's window, in pixels
    WINDOWHEIGHT = 768 # height in pixels
    
    XMARGIN = 0 # will be calculated at call of start()
    YMARGIN = 0
    
    BRIGHTBLUE = (0, 50, 255)
    LIGHTGRAY = (155, 150, 140)
    WHITE = (255, 255, 255)
    
    BGCOLOR = LIGHTGRAY
    TEXTCOLOR = WHITE
    
    BLACK = 1
    WHITE = 2
    EMPTY = 0
    MARKER = 3             # cannot be on board, but can be displayed
    HUMAN = 'human'        # WHITE player
    HUMAN2 = 'human2'      # BLACK player
    COMPUTER = 'computer'  # BLACK player
    
    BlackPlayer = ''
    WhitePlayer = ''
    
    GameType_HumanVsCpu = "HumanVsCpu"
    GameType_HumanVsHuman = "HumanVsHuman"
    
    # if you want to test an ai game maximally quickly, you could disable showIntermediateMoves
    def start(player1,player2,max_time_to_move, showIntermediateMoves=True):
        GmGame.XMARGIN = int((GmGame.WINDOWWIDTH - GmGameRules.BOARDWIDTH * GmGame.SPACESIZE) / 2)
        GmGame.YMARGIN = int((GmGame.WINDOWHEIGHT - GmGameRules.BOARDHEIGHT * GmGame.SPACESIZE) / 2)
        
        global FPSCLOCK, DISPLAYSURF, WHITETOKENIMG
        global BLACKTOKENIMG, BOARDIMG, ARROWIMG, ARROWRECT, HUMANWINNERIMG
        global COMPUTERWINNERIMG, WINNERRECT, TIEWINNERIMG, MARKERIMG
    
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((GmGame.WINDOWWIDTH, GmGame.WINDOWHEIGHT))
        pygame.display.set_caption('Gomoku')
    
        WHITETOKENIMG = pygame.image.load('4row_white_smaller.png')
        WHITETOKENIMG = pygame.transform.smoothscale(WHITETOKENIMG, (GmGame.SPACESIZE, GmGame.SPACESIZE))
        BLACKTOKENIMG = pygame.image.load('4row_black_smaller.png')
        BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (GmGame.SPACESIZE, GmGame.SPACESIZE))
        MARKERIMG = pygame.image.load('marker.png')
        MARKERIMG = pygame.transform.smoothscale(MARKERIMG, (GmGame.SPACESIZE, GmGame.SPACESIZE))
        BOARDIMG = pygame.image.load('gomoku_board.png')
        BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (GmGame.SPACESIZE, GmGame.SPACESIZE))
    
        HUMANWINNERIMG = pygame.image.load('4row_humanwinner.png')
        COMPUTERWINNERIMG = pygame.image.load('4row_computerwinner.png')
        # make the winner impage small, such that we can cramp it in the topleft
        HUMANWINNERIMG = pygame.transform.smoothscale(HUMANWINNERIMG, (5*GmGame.SPACESIZE, 2*GmGame.SPACESIZE))
        COMPUTERWINNERIMG = pygame.transform.smoothscale(COMPUTERWINNERIMG, (5*GmGame.SPACESIZE, 2*GmGame.SPACESIZE))
        TIEWINNERIMG = pygame.image.load('4row_tie.png')
        WINNERRECT = HUMANWINNERIMG.get_rect()
        #WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
        WINNERRECT.left=0
        WINNERRECT.top=0
    
        while True:
            player1.new_game(player1.black) # for convenience, I keep the color the same for each player.
            player2.new_game(player2.black)
            GmGame.runGame(player1,player2,max_time_to_move,showIntermediateMoves)
    
    def runGame(player1, player2, max_time_to_move, showIntermediateMoves,):
        last_move = None
        valid_moves = None
        
        # black goes first
        activePlayer = player1 if player1.black else player2 
        
        # Set up a blank board data structure.
        mainBoard = GmGame.getNewBoard()
    
        while True: # main game loop
            # I don't bother to fill valid_moves. My class bookkeeps that by itself.
            last_move = (column,row) = activePlayer.move(mainBoard, last_move, valid_moves, max_time_to_move)
            color = GmGame.getPlayerColor(activePlayer)
            
            if gomokuUtils.isValidMove(mainBoard, column, row):
                gomokuUtils.addMoveToBoard(mainBoard,last_move,color)
                if showIntermediateMoves: GmGame.drawBoardWithExtraTokens(mainBoard,column,row,GmGame.MARKER)
                
            if gomokuUtils.isWinningMove(last_move,mainBoard):
                if(activePlayer==player1):
                    winnerImg = HUMANWINNERIMG
                else:
                    winnerImg = COMPUTERWINNERIMG
                break
            elif GmGame.isBoardFull(mainBoard):
                # A completely filled board means it's a tie.
                winnerImg = TIEWINNERIMG
                if showIntermediateMoves: GmGame.drawBoardWithExtraTokens(mainBoard,last_move[0],last_move[1],GmGame.MARKER)
                break
            activePlayer = gomokuUtils.getNonActivePlayer(activePlayer,player1,player2)
            
            if showIntermediateMoves: 
                pygame.display.update()
                FPSCLOCK.tick()
    
        while True:
            # Keep looping until player clicks the mouse or quits.
            GmGame.drawBoardWithExtraTokens(mainBoard,last_move[0],last_move[1],GmGame.MARKER)
            DISPLAYSURF.blit(winnerImg, WINNERRECT)
            pygame.display.update()
            FPSCLOCK.tick()
            
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    return
    
    # token can be BLACK, WHITE or MARKER
    # x is row
    # y is col
    def drawToken(token,x,y):
        if token != None:
            spaceRect = pygame.Rect(0, 0, GmGame.SPACESIZE, GmGame.SPACESIZE)
            spaceRect.topleft = (GmGame.XMARGIN + (x * GmGame.SPACESIZE), GmGame.YMARGIN + (y * GmGame.SPACESIZE))
            if token == GmGame.WHITE:
                DISPLAYSURF.blit(WHITETOKENIMG, spaceRect)
            elif token == GmGame.BLACK:
                DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)
            elif token == GmGame.MARKER:
                DISPLAYSURF.blit(MARKERIMG, spaceRect)
                
    def drawBoard(board, extraToken=None):
        DISPLAYSURF.fill(GmGame.BGCOLOR)
    
        spaceRect = pygame.Rect(0, 0, GmGame.SPACESIZE, GmGame.SPACESIZE)
    
        # draw board under the tokens
        for x in range(GmGameRules.BOARDWIDTH):
            for y in range(GmGameRules.BOARDHEIGHT):
                spaceRect.topleft = (GmGame.XMARGIN + (x * GmGame.SPACESIZE), GmGame.YMARGIN + (y * GmGame.SPACESIZE))
                DISPLAYSURF.blit(BOARDIMG, spaceRect)
    
        # draw tokens
        for x in range(GmGameRules.BOARDWIDTH):
            for y in range(GmGameRules.BOARDHEIGHT):
                spaceRect.topleft = (GmGame.XMARGIN + (x * GmGame.SPACESIZE), GmGame.YMARGIN + (y * GmGame.SPACESIZE))
                if board[x][y] == GmGame.WHITE:
                    DISPLAYSURF.blit(WHITETOKENIMG, spaceRect)
                elif board[x][y] == GmGame.BLACK:
                    DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)
    
        # draw the extra token
        if extraToken != None:
            GmGame.drawToken(extraToken)
    
    def drawBoardWithExtraTokens(board,x=0,y=0,token1=None,token2=None):
        GmGame.drawBoard(board)
        if token1!=None:
          GmGame.drawToken(token1,-1,y)
          GmGame.drawToken(token1,x,-1)
    
        if token2!=None:
          GmGame.drawToken(token2,-1,y)
          GmGame.drawToken(token2,x,-1)
    
    def getNewBoard():
        board = []
        for x in range(GmGameRules.BOARDWIDTH):
            board.append([GmGame.EMPTY] * GmGameRules.BOARDHEIGHT)
        
        #board = [[0,2,2,2,2],[0,1,2,1,2],[0,2,1,2,1],[1,2,1,2,1],[2,1,2,1,2]]
        return board
    
    def isBoardFull(board):
        # Returns True if there are no empty spaces anywhere on the board.
        for x in range(GmGameRules.BOARDWIDTH):
            for y in range(GmGameRules.BOARDHEIGHT):
                if board[x][y] == GmGame.EMPTY:
                    return False
        return True
    
    def getPlayerColor(player_):
        return GmGame.BLACK if player_.black else GmGame.WHITE

class gomokuUtils():
    @staticmethod
    def getNonActivePlayer(activePlayer, player1, player2):
        return player1 if id(activePlayer)==id(player2) else player2
    
    @staticmethod
    def hasNeighbour(move,board):
        xmin=max(move[0]-1,0)
        ymin=max(move[1]-1,0)
        xmax=max(move[0]+2,GmGameRules.BOARDWIDTH) # upper bound excluded
        ymax=max(move[1]+2,GmGameRules.BOARDHEIGHT)
        for x in range(xmin,xmax):
            for y in range(ymin,ymax):
                if board[x][y]!=0 : 
                    return True
        return False
    
    @staticmethod
    def isWinningMove(last_move, board):
        """This method checks whether the last move played wins the game.
        The rule for winning is: /exactly/ 5 stones line up (so not 6 or more),
        horizontally, vertically, or diagonally."""
        bsize=len(board)
        assert(len(board[0])==bsize)    #verify the assumption made below.
        color = board[last_move[0]][last_move[1]]
        #check up-down
        number_ud = 1
        if(last_move[1]<bsize-1):
            lim1 = last_move[1]+1
            lim2 = last_move[1]+GmGameRules.winningSeries+1 if last_move[1]+GmGameRules.winningSeries+1<bsize else bsize
            for i in range(lim1, lim2):
                if board[last_move[0]][i] == color:
                    number_ud += 1
                else:
                    break
        if (last_move[1] > 0):
            lim2 = last_move[1] - GmGameRules.winningSeries if last_move[1]-GmGameRules.winningSeries > 0 else 0
            for i in reversed(range(lim2, last_move[1])):
                if board[last_move[0]][i] == color:
                    number_ud += 1
                else:
                    break
        if number_ud >= GmGameRules.winningSeries: # TODO: use == for gomoku (and >= for 5 in a row)
            return True
        #check left - right
        number_lr = 1
        if (last_move[0] < bsize - 1):
            lim1 = last_move[0] + 1
            lim2 = last_move[0] + GmGameRules.winningSeries+1 if last_move[0] + GmGameRules.winningSeries+1 < bsize else bsize
            for i in range(lim1, lim2):
                if board[i][last_move[1]] == color:
                    number_lr += 1
                else:
                    break
        if (last_move[0] > 0):
            lim2 = last_move[0] - GmGameRules.winningSeries if last_move[0] - GmGameRules.winningSeries > 0 else 0
            for i in reversed(range(lim2, last_move[0])):
                if board[i][last_move[1]] == color:
                    number_lr += 1
                else:
                    break
        if number_lr >= GmGameRules.winningSeries: # TODO: use == for gomoku (and >= for 5 in a row)
            return True
        #check lower left - upper right
        number_diag = 1
        xlim = last_move[0] - 1
        ylim = last_move[1] - 1
        while (xlim>=0 and ylim>=0):
            if board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim-1
            ylim = ylim-1
        xlim = last_move[0] + 1
        ylim = last_move[1] + 1
        while (xlim<bsize and ylim<bsize):
            if board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim + 1
            ylim = ylim + 1
        if number_diag >= GmGameRules.winningSeries: # TODO: use == for gomoku (and >= for 5 in a row)
            return True
        #check lower right - upper left
        number_diag = 1
        xlim = last_move[0] + 1
        ylim = last_move[1] - 1
        while (xlim <bsize and ylim >= 0):
            if board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim + 1
            ylim = ylim - 1
        xlim = last_move[0] - 1
        ylim = last_move[1] + 1
        while (xlim >= 0 and ylim < bsize):
            if board[xlim][ylim] == color:
                number_diag += 1
            else:
                break
            xlim = xlim - 1
            ylim = ylim + 1
        if number_diag >= GmGameRules.winningSeries: # TODO: use == for gomoku (and >= for 5 in a row)
            return True
        return False
    
    @staticmethod  
    def getRandomMove(board):
        # let's make a random move
        # First, make a list of all empty spots
        validMoves = []
        for col in range(GmGameRules.BOARDWIDTH):
            for row in range(GmGameRules.BOARDHEIGHT):
                if gomokuUtils.isValidMove(board, col, row):
                    validMoves.append((col,row))
    
        return random.choice(validMoves)

    @staticmethod
    def isValidMove(board, column, row):
        # Returns True if there is an empty space in the given column.
        # Otherwise returns False.
        return ((column >= 0) and (column < len(board)) and (row >= 0) and (row < len(board[0])) and (board[column][row] == 0))
    
    @staticmethod
    def createDictFromList(lst):
        dic={}
        for member in lst:
            dic[member]=1   # dummy value
        return dic

    @staticmethod
    def addMoveToBoard(board,move,color):
        board[move[0]][move[1]] = color

    @staticmethod
    def removeTokenFromBoard(board,move):
        board[move[0]][move[1]] = 0 # 0 must mean empty, for this.
        
    @staticmethod
    def shuffleList(lst):
        lstSize = len(lst)
        for i in range (0,lstSize):
            # Switch places with random other.
            #indexExchangeCandidate=random.randint(0,lstSize-1)
            indexExchangeCandidate=int(lstSize * random.random()) # 5 times faster. Could be even faster if we may assume that numpy can be used.
            
            tmp=lst[indexExchangeCandidate]
            lst[indexExchangeCandidate]=lst[i]
            lst[i]=tmp
            
    # precondition: make sure to add the move to the tempboard first.
    @staticmethod
    def addNeighbouringValidMovesToDic(dicValidMoves, move, tempboard):
        assert(tempboard[move[0]][move[1]]!=0)
        xmin=max(move[0]-1,0)
        ymin=max(move[1]-1,0)
        xmax=max(move[0]+2,GmGameRules.BOARDWIDTH) # upper bound excluded
        ymax=max(move[1]+2,GmGameRules.BOARDHEIGHT)
        for x in range(xmin,xmax):
            for y in range(ymin,ymax):
                if tempboard[x][y]==0 : 
                    dicValidMoves[(x,y)]=1    
            
    @staticmethod
    def printSimpleNode(getUctProvidingObject, node):
        print("pos:{},Q:{},N:{}".format(node.pos,node.Q,node.N))
        strIndent=" "
        for pos,child in node.children.items():
            print(strIndent+"pos:{},Q:{},N:{}".format(child.pos,child.Q,child.N))
            
    # print only the node and its direct children
    @staticmethod
    def printNode(getUctProvidingObject, node):
        part1 = node.Q/node.N
        print("pos:{},Q:{},N:{}".format(node.pos,node.Q,node.N)+",uct:{0:.2f}".format(getUctProvidingObject.getUct(node))+",Q/N:{0:.2f}".format(part1))
        strIndent=" "
        for pos,child in node.children.items():
            part1 = child.Q/child.N
            print(strIndent+"pos:{},Q:{},N:{}".format(child.pos,child.Q,child.N)+",uct:{0:.2f}".format(getUctProvidingObject.getUct(child))+"Q/N:{0:.2f}".format(part1))

    @staticmethod
    def printTree(getUctProvidingObject, node,indent=0):
        strIndent=" "*indent
        print(strIndent+"pos:{},Q:{},N:{}".format(node.pos,node.Q,node.N)+",uct:{0:.2f},Q/N:{0:.2f}".format(getUctProvidingObject.getUct(node),node.Q/node.N))
        for pos,child in node.children.items():
            getUctProvidingObject.printTree(getUctProvidingObject,child,indent+2)        
    

    def copyToTempBoard(self,board):
        if self.tempBoard==None:
            self.tempBoard=copy.deepcopy(board)
        else:
            # avoid reallocation
            nofCols = len(board)
            nofRows = len(board[0])
            for col in range(0,nofCols):
                for row in range(0,nofRows):
                    self.tempBoard[col][row]=board[col][row]

    def new_game(self, black_):
        self.reset(black_)

    def getValidMoves(board):
        # First, make a list of all empty spots
        validMoves = []
        for col in range(0,len(board)):
            for row in range(0,len(board[0])):
                if gomokuUtils.isValidMove(board, col, row):
                    validMoves.append((col,row))
        
        return validMoves


# This default base player does a randomn move
class basePlayer:
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """
    def __init__(self, black_=True):
        """Constructor for the player."""
        self.black = black_

    def new_game(self, black_):
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
        return "random_player"

class humanPlayer(basePlayer):
    def __init__(self, black_=True):
        self.black = black_
        
    def new_game(self, black_):
        self.black = black_

    def move(self, board, last_move, valid_moves, max_time_to_move=1000):   
        tokenx, tokeny = None, None
        while True:
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    tokenx, tokeny = event.pos
                    if GmGame.YMARGIN < tokeny < GmGame.WINDOWHEIGHT-GmGame.YMARGIN and GmGame.XMARGIN < tokenx < GmGame.WINDOWWIDTH - GmGame.XMARGIN:
                        # place it
                        column = int((tokenx - GmGame.XMARGIN) / GmGame.SPACESIZE)
                        row = int((tokeny - GmGame.YMARGIN) / GmGame.SPACESIZE)
                        #print("row:{},col:{}".format(row,column))
                        if gomokuUtils.isValidMove(board, column, row):
                            return (column,row)
                    tokenx, tokeny = None, None
    
            if last_move!=None:
                GmGame.drawBoardWithExtraTokens(board,last_move[0],last_move[1],GmGame.MARKER)
            else:
                GmGame.drawBoard(board)
          
            pygame.display.update()
            FPSCLOCK.tick()

    def id(self):
        return "Marius"

# player gives an implementation the basePlayer cl
class randomPlayer(basePlayer):
    def __init__(self, black_=True):
        self.black = black_
    
        self.max_move_time_ns   = 0
        self.start_time_ns      = 0

    def new_game(self, black_):
        self.black = black_

    def move(self, board, last_move, valid_moves, max_time_to_move=1000):
        self.max_move_time_ns   = 0.95 * max_time_to_move * 1000000 # ms to ns
        self.start_time_ns      = time.time_ns()
        
        return gomokuUtils.getRandomMove(board)

    def id(self):
        return "Marius"


random.seed(0) # voor reproduceerbare debugging

aiPlayer1 = randomPlayer(black_=False)
#aiPlayer2 = pureMontecarloPlayer(black_=False)
#aiPlayer2 = heuristicalMontecarloPlayer1(black_=False)
humanPlayer1 = humanPlayer(black_=True)
humanPlayer2 = humanPlayer(black_=False)

# change the rules for testing
# reasonable combinations for pureMontecarlo are: w=8,h=8,series=5, rollouts(in move = 8000 / time=4s)
GmGameRules.BOARDWIDTH=3
GmGameRules.BOARDHEIGHT=3
GmGameRules.winningSeries=3
GmGame.start(player1=humanPlayer1,player2=aiPlayer1,max_time_to_move=4000,showIntermediateMoves=True) # don't speciry an aiPlayer for Human vs Human games
