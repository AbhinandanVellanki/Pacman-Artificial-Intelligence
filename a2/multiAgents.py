from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
    
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        foodis= math.inf
        for f in newFood.asList():
            dis=manhattanDistance(f, newPos)
            if dis<foodis:
                foodis=dis
        if len(newFood.asList())==0:
            foodis=math.inf
        ghostdis=math.inf
        for g in newGhostStates:
            dis=manhattanDistance(g.getPosition(), newPos)
            if dis<ghostdis:
                ghostdis=dis
        if ghostdis==0:
            ghostdis=1
        eval=successorGameState.getScore()-1/ghostdis+1/foodis+sum(newScaredTimes)
        return eval
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def getAction(self, gameState):
        """
          #Returns the minimax action from the current gameState using self.depth and self.evaluationFunction.          

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        if gameState.isWin() or gameState.isLose() or self.depth==0:
            return self.evaluationFunction(gameState)
        nextactions=gameState.getLegalActions(0)
        max=-999
        if len(nextactions)==0:
            return Directions.STOP
        for a in nextactions:
            nextstate=gameState.generateSuccessor(0,a)
            vals=self.minimizer(nextstate,1,self.depth)
            if vals>max:
                max,action=vals,a
        return action
                
    def minimizer(self, gameState, num, depth):
        if gameState.isWin() or gameState.isLose() or depth==0:
            return self.evaluationFunction(gameState)
        nextactions=gameState.getLegalActions(num)
        minival=999
        for a in nextactions:
            nextstate=gameState.generateSuccessor(num, a)
            if gameState.getNumAgents()==num+1:
                val=self.maximizer(nextstate, depth-1)
                if minival>val:
                    minival=val
            else:
                val=self.minimizer(nextstate, num+1, depth)
                if minival>val:
                    minival=val
        return minival 
        
    def maximizer(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth==0:
            return self.evaluationFunction(gameState)
        maxival=-999
        nextactions=gameState.getLegalActions(0)
        for a in nextactions:
            nextstate=gameState.generateSuccessor(0,a)
            val=self.minimizer(nextstate,1,depth)
            if maxival<val:
                maxival=val
        return maxival
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        if gameState.isWin() or gameState.isLose() or self.depth==0:
            return self.evaluationFunction(gameState)
        v=-9999
        ap=-9999
        bt=9999
        nextactions=gameState.getLegalActions(0)
        if len(nextactions)==0:
            return Directions.STOP
        for a in nextactions:
            nextstate=gameState.generateSuccessor(0, a)
            val=self.getminval(nextstate, self.depth, 1, ap, bt)
            if val>bt:
                return a
            if val>ap:
                ap=val
            if val>v:
                v, action=val,a
        return action
    
    def getmaxval(self, gameState, depth, num, ap, bt):
        if gameState.isWin() or gameState.isLose() or len(gameState.getLegalActions(0))==0 or depth==0:
            return self.evaluationFunction(gameState)
        v=-99999
        nextactions=gameState.getLegalActions(0)
        for a in nextactions:
            nextstate=gameState.generateSuccessor(num,a)
            v=max(v,self.getminval(nextstate, depth, 1, ap, bt))
            if v>bt:
                return v
            ap=max(ap,v)
        return v
    
    def getminval(self, gameState,depth,num, ap,bt):
        if gameState.isWin() or gameState.isLose() or len(gameState.getLegalActions(num))==0 or depth==0:
            return self.evaluationFunction(gameState)
        v=99999
        nextactions=gameState.getLegalActions(num)
        for a in nextactions:
            nextstate=gameState.generateSuccessor(num,a)
            if num+1==gameState.getNumAgents():
                v=min(v,self.getmaxval(nextstate, depth-1,0, ap, bt))
                if v<ap:
                    return v
                bt=min(bt,v)
            else:
                v=min(v,self.getminval(nextstate, depth,num+1, ap, bt))
                if v < ap:
                    return v
                bt=min(bt,v)
        return v
                
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        if gameState.isWin() or gameState.isLose() or self.depth==0:
            return self.evaluationFunction(gameState)
        v=-999
        nextactions=gameState.getLegalActions(0)
        if len(nextactions)==0:
            return Directions.STOP
        for a in nextactions:
            nextstate=gameState.generateSuccessor(0,a)
            val=self.expect(nextstate,1,0)
            if val>v:
                v, action=val, a
        return action
    
    def expect(self, gameState, num, depth):
        if depth==self.depth or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        val=0
        nextactions=gameState.getLegalActions(num)
        if len(nextactions)==0:
            val=self.evaluationFunction(gameState)
        else:
            for a in nextactions:
                if num+1==gameState.getNumAgents():
                    val+=self.getmaxival(gameState.generateSuccessor(num,a),depth+1,0)
                else:
                    val+=self.expect(gameState.generateSuccessor(num,a),num+1, depth)
            val/=len(nextactions)
        return val
    
    def getmaxival(self, gameState, depth, num):
        if depth == self.depth or gameState.isLose() or gameState.isWin():
              return self.evaluationFunction(gameState)
        nextactions=gameState.getLegalActions(num)
        if len(nextactions)==0:
            val=self.evaluationFunction(gameState)
        else:
            val=float('-inf')
            for a in nextactions:
                score=self.expect(gameState.generateSuccessor(num,a), num+1, depth)
                if score>val:
                    val=score
        return val
            
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: if current state is goal state return positive high value
      if no more food left return positive high value
      if pacman is at same position as any ghost, return negative high value
      else, return current score + reciprocal of sum of distances to all food-recirprocal of sum of distances to ghosts+total scared time of ghosts 
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return 99999
    foodpos=currentGameState.getFood().asList()
    if len(foodpos)==0:
        return 99999
    foodis=sum(manhattanDistance(f,currentGameState.getPacmanPosition())for f in foodpos)
    ghost=currentGameState.getGhostStates()
    ghostsc=0
    totscaredtime=0
    for g in ghost:
        scaredtime=g.scaredTimer
        pos=g.getPosition()
        if pos==currentGameState.getPacmanPosition():
            return -999999
        dis=manhattanDistance(pos, currentGameState.getPacmanPosition())
        if dis!=0:
            ghostsc+=float(1/(dis+scaredtime))
        totscaredtime+=scaredtime
    return currentGameState.getScore()+1/foodis-ghostsc+1/len(foodpos)+totscaredtime
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

