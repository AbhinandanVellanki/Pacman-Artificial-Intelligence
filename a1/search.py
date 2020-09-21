"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import collections

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    frontier=util.Stack() 
    routes=util.Stack()
    if problem.isGoalState(problem.getStartState()):
        return []
    for child in problem.getSuccessors(problem.getStartState()):
        frontier.push(child)
        path=[]
        path.append(child[1])
        routes.push(path)
    
    exploredset=[]
    exploredset.append(problem.getStartState())
    while not frontier.isEmpty():
        node=frontier.pop()
        way=routes.pop()
        if(problem.isGoalState(node[0])):
            exploredset.clear()
            return way
        if node[0] not in exploredset:
            exploredset.append(node[0])
            for child in problem.getSuccessors(node[0]):
                frontier.push(child)
                path=way.copy()
                path.append(child[1])
                routes.push(path)
    util.raiseNotDefined()
    
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    from game import Directions
    frontier=util.Queue() 
    routes=util.Queue()
    if problem.isGoalState(problem.getStartState()):
        return []
    for child in problem.getSuccessors(problem.getStartState()):
        frontier.push(child)
        path=[]
        path.append(child[1])
        routes.push(path)
    
    exploredset=[]
    exploredset.append(problem.getStartState())
    while not frontier.isEmpty():
        node=frontier.pop()
        way=routes.pop()
        if(problem.isGoalState(node[0])):
            return way
        if node[0] not in exploredset:
            exploredset.append(node[0])
            for child in problem.getSuccessors(node[0]):
                frontier.push(child)
                path=way.copy()
                path.append(child[1])
                routes.push(path)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    frontier=util.PriorityQueue()
    routes=util.PriorityQueue()
    if problem.isGoalState(problem.getStartState()):
        return []
    for child in problem.getSuccessors(problem.getStartState()):
        frontier.push(child,child[2])
        path=[]
        path.append(child[1])
        routes.push(path, child[2])
    exploredset=[]
    exploredset.append(problem.getStartState())
    while frontier:
        node=frontier.pop()
        way=routes.pop()
        if(problem.isGoalState(node[0])):
            return way
        if node[0] not in exploredset:
            exploredset.append(node[0])
            for child in problem.getSuccessors(node[0]):
                frontier.push(child, problem.getCostOfActions(way)+child[2])
                path=way.copy()
                path.append(child[1])
                routes.push(path, problem.getCostOfActions(way)+child[2])         
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    frontier=util.PriorityQueue()
    routes=util.PriorityQueue()
    if problem.isGoalState(problem.getStartState()):
        return []
    for child in problem.getSuccessors(problem.getStartState()):
        frontier.push(child,child[2]+heuristic(child[0], problem))
        path=[]
        path.append(child[1])
        routes.push(path, child[2]+heuristic(child[0], problem))
    exploredset=[]
    exploredset.append(problem.getStartState())
    while frontier:
        node=frontier.pop()
        way=routes.pop()
        if(problem.isGoalState(node[0])):
            
            return way
        if node[0] not in exploredset:
            exploredset.append(node[0])
            for child in problem.getSuccessors(node[0]):
                frontier.push(child, problem.getCostOfActions(way)+child[2]+heuristic(child[0], problem))
                path=way.copy()
                path.append(child[1])
                routes.push(path, problem.getCostOfActions(way)+child[2]+heuristic(child[0], problem))     
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
