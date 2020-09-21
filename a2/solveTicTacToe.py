#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser
import numpy as np

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)
    
    def transferStringToInt(self, aBoard):
        for i in range(0, 3):
            for j in range(0, 3):
                if aBoard[i][j] != 'X':
                    aBoard[i][j] = int(0)
        return aBoard
    
    def getboards(self, board):
        boards=[board]
        temp=board
        for i in range(3):
            newboard=self.rotate(board)
            boards.append(newboard)
            board=newboard
        boards.append(self.fliphoriz(temp))
        boards.append(self.flipvert(temp))
        return boards
        
    def rotateBoard(self, board):
        t = copy.deepcopy(board)
        for i in range(3):
            newBoard = copy.deepcopy(t)
            newBoard[0][0] = t[2][0]
            newBoard[0][1] = t[1][0]
            newBoard[0][2] = t[0][0]
            newBoard[1][0] = t[2][1]
            newBoard[1][2] = t[0][1]
            newBoard[2][0] = t[2][2]
            newBoard[2][1] = t[1][2]
            newBoard[2][2] = t[0][2]
        return newBoard

    def fliphoriz(self, Board):
        npar = np.array(Board)
        npar = np.fliplr(npar)
        board = npar.tolist()
        board = self.transferStringToInt(board)
        return board
    
    def flipvert(self, Board):
        npar = np.array(Board)
        npar = np.flipud(npar)
        board = npar.tolist()
        board = self.transferStringToInt(board)
        return board
               
    def giveval(self, nextboard, gameRules):
        b=[[['X',0,'X'],[0,0,0],[0,0,0]],[['X',0,0],[0,'X',0],[0,0,0]],[['X',0,0],[0,0,'X'],[0,0,0]],[[0,'X',0],[0,'X',0],[0,0,0]],[['X','X',0],['X',0,0],[0,0,0]],[[0,'X',0],['X',0,'X'],[0,0,0]],[['X','X',0],[0,'X','X'],[0,0,0]],[['X','X',0],[0,'X',0],['X',0,0]],[['X','X',0],[0,0,'X'],['X',0,0]],[['X','X',0],[0,0,0],['X','X',0]],[['X','X',0],[0,0,0],['X',0,'X']],[['X',0,'X'],[0,'X',0],[0,'X',0]],[['X',0,0],[0,'X','X'],[0,'X',0]],[['X','X',0],['X',0,'X'],[0,0,'X']],[['X','X',0],['X',0,'X'],[0,'X',0]]]
        c=[[[0,0,0],[0,0,0],[0,0,0]]]
        c2=[[[0,0,0],[0,'X',0],[0,0,0]]]
        ad=[[['X','X',0],[0,0,0],[0,0,0]]]
        a=[[['X',0,0],[0,0,0],[0,0,'X']],[[0,'X',0],['X',0,0],[0,0,0]],[[0,'X',0],[0,0,0],[0,'X',0]],[['X','X',0],[0,0,0],['X',0,0]],[['X',0,'X'],[0,'X',0],[0,0,0]],[['X',0,'X'],[0,0,0],[0,'X',0]],[['X',0,0],[0,'X','X'],[0,0,0]],[['X','X',0],['X','X',0],[0,0,0]],[['X','X',0],['X',0,'X'],[0,0,0]],[['X','X',0],['X',0,0],[0,0,'X']],[['X','X',0],[0,0,0],[0,'X','X']],[['X',0,'X'],[0,0,0],['X',0,'X']],[[0,'X',0],['X',0,'X'],[0,'X',0]],[['X','X',0],[0,'X','X'],['X',0,0]],[['X','X',0],[0,0,'X'],['X','X',0]],[['X','X',0],[0,0,'X'],['X',0,'X']],[['X','X',0],['X',0,'X'],[0,'X','X']]]
        ab=[[['X','X',0],[0,'X',0],[0,0,0]],[['X',0,'X'],[0,0,0],['X',0,0]],[[0,'X',0],['X','X',0],[0,0,0]],[['X','X',0],[0,0,'X'],[0,'X',0]],[['X','X',0],[0,0,'X'],[0,0,'X']]]
        d=[[['X','X',0],[0,0,'X'],[0,0,0]], [['X','X',0],[0,0,0],[0,'X',0]], [['X','X',0],[0,0,0],[0,0,'X']]]
        one=[[['X',0,0],[0,0,0],[0,0,0]], [[0,'X',0],[0,0,0],[0,0,0]], [['X',0,0],[0,0,'X'],[0,'X',0]]]
        
        #print(nextboard)
        
        if nextboard in b:
            return 'b'
        elif nextboard in c:
            return 'c'
        elif nextboard in c2:
            return 'c2'
        elif nextboard in ad:
            return 'ad'
        elif nextboard in a:
            return 'a'
        elif nextboard in ab:
            return 'ab'
        elif nextboard in one:
            return 1
        elif nextboard in d:
            return 'd'
        else:
            return 'z'
        
    
    def getvals(self, board, GameRules):
        new_board=copy.deepcopy(board)
        arr_1 = new_board[:3]
        arr_2 = new_board[3:6]
        arr_3 = new_board[6:]
        new_board = [arr_1,arr_2,arr_3]
        for i in range(3):
            for j in range(3):
                if new_board[i][j]:
                    new_board[i][j]='X'
                else:
                    new_board[i][j] = 0
        board=new_board
        #print(board)
        for i in range(0, 4):
            board = self.rotateBoard(board)
            testBoard = copy.deepcopy(board)
            for j in range(0, 3):
                if j == 1:
                    testBoard = self.fliphoriz(board)
                    val=self.giveval(testBoard, GameRules)
                    if val=='z': continue
                    return val
                elif j == 2:
                    testBoard = self.flipvert(board)
                    val=self.giveval(testBoard, GameRules)
                    if val=='z': continue
                    return val
                
    def score(self,boards, gameRules):
        score=1
        #print(boards)
        a=""
        for b in boards:
            val=self.getvals(b, gameRules)
            if val==1 or not val: continue
            a+=val
        if a in ['c2','cc','a','bb','b2' ,'bc','cb']:
            return 1000

        return score
            
class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        
    def getAction(self, gameState, gameRules):
        nextactions=gameState.getLegalActions(gameRules)
        maxscore=-9999
        for a in nextactions:
            nextstate=gameState.generateSuccessor(a)
            #print(nextstate.boards)
            score=gameState.score(nextstate.boards, gameRules)
            if score>maxscore:
                maxscore, action=score, a
        return action        


class randomAgent():
    
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
