# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    #"*** YOUR CODE HERE ***"
    start = problem.getStartState()
    isGoal = problem.isGoalState(problem.getStartState())

    '''
    succs: [('B', '0:A->B', 1.0), ('C', '1:A->C', 2.0), ('D', '2:A->D', 4.0)]
    [((34, 15), 'South', 1), ((33, 16), 'West', 1)]
    '''


    startNode = sNode(start, None, 0, None)

    frontier = util.Stack()
    explored= []
    frontier.push(startNode)
    while not frontier.isEmpty():
        curr = frontier.pop()
        if problem.isGoalState(curr.state):
            return solution(curr)
        elif not curr.state in explored:
            explored.append(curr.state)
            for s in problem.getSuccessors(curr.state):
                st = s[0]
                if st not in explored:
                    frontier.push(sNode(s[0], s[1], s[2], curr))

    return False
            
def solution(node):
    sol = []
    while node.parent is not None:
        sol.append(node.action)
        node = node.parent
    sol.reverse()
    return sol



class sNode:
    parent = None
    action = None
    costFromParent = None
    state = None

    cumCost = 0

    def __init__(self, state, action, cost, parent, cumCost = None, aStarPrior = None):
        self.state = state
        self.action = action
        self.costFromParent = cost
        self.parent = parent
        self.cumCost = cumCost
        self.aStarPrior=aStarPrior

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    start = problem.getStartState()
    isGoal = problem.isGoalState(problem.getStartState())


    startNode = sNode(start, None, 0, None)

    frontier = util.Queue()
    explored= []
    frontier.push(startNode)
    while not frontier.isEmpty():
        curr = frontier.pop()
        if problem.isGoalState(curr.state):
            return solution(curr)
        elif not curr.state in explored:
            explored.append(curr.state)
            for s in problem.getSuccessors(curr.state):
                st = s[0]
                if st not in explored:
                    frontier.push(sNode(s[0], s[1], s[2], curr))

    return False

def uniformCostSearch(problem):

    start = problem.getStartState()
    isGoal = problem.isGoalState(problem.getStartState())


    startNode = sNode(start, None, 0, None, cumCost= 0)

    frontier = util.PriorityQueue()
    explored= []
    frontier.push((startNode), 0)
    while not frontier.isEmpty():
        curr = frontier.pop()
        if problem.isGoalState(curr.state):
            return solution(curr)
        elif not curr.state in explored:
            explored.append(curr.state)
            for s in problem.getSuccessors(curr.state):
                st = s[0]
                if st not in explored:
                    #construct node with cumCost = parent + cost and push at that priority
                    frontier.push(sNode(s[0], s[1], s[2], curr, cumCost= (curr.cumCost + s[2])), curr.cumCost + s[2])

    return False

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    isGoal = problem.isGoalState(problem.getStartState())


    startNode = sNode(start, None, 0, None, cumCost=0, aStarPrior = 0 + heuristic(start, problem))

    frontier = util.PriorityQueue()
    explored= []
    frontier.push((startNode), 0)
    while not frontier.isEmpty():
        curr = frontier.pop()
        if problem.isGoalState(curr.state):
            return solution(curr)
        elif not curr.state in explored:
            explored.append(curr.state)
            for s in problem.getSuccessors(curr.state):
                st = s[0]
                if st not in explored:
                    #construct node with cumCost = parent + cost and priority = cumcost + heuristic push at that priority
                    frontier.push(sNode(s[0], s[1], s[2], curr, cumCost= (curr.cumCost + s[2])), curr.cumCost + s[2] + heuristic(s[0], problem))

    return False


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
