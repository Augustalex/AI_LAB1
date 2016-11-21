"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
from random import Random

from datetime import time

import util
from game import Directions


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
    return [s, s, w, s, w, w, s, w]


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

    return graphSearch(problem, util.Stack())


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return graphSearch(problem, util.Queue())


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    return graphSearch(problem, util.PriorityQueueWithFunction(lambda n : n.pathCost))


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    return graphSearch(problem, util.PriorityQueueWithFunction(lambda n: n.pathCost))


class Node:
    """
    Class for Nodes to store attributes.
    Nodes can be placed in a data structure.
    """

    def __init__(self, state, parent=None, action=None, pathCost=0):
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

        self.action = action
        self.state = state
        self.parent = parent
        self.pathCost = pathCost

    def __str__(self):
        return str(self.state)

    def expandNode(self, problem):
        return [Node(successor, self, action, self.pathCost + stepCost)
                for (successor, action, stepCost) in problem.getSuccessors(self.state)]


def graphSearch(problem, fringe):
    """
    Returns a sequence of moves according to the generic search algorithm
    if a solution is found, faile otherwise.
    :param fringe:
    :param problem:
    :return:
    """
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    closed = {}
    fringe.push(Node(problem.getStartState()))
    while fringe:
        if fringe.isEmpty():
            return None
        node = fringe.pop()
        if problem.isGoalState(node.state):
            path = []
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path.reverse()
            return path
        if node.state not in closed:
            closed[node.state] = True

            for fringeElement in node.expandNode(problem):
                fringe.push(fringeElement)

    print "Hello from the outside //Adelle"
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
