"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import update as update
import util
import Queue.py


class Node:
    """
    Class for Nodes to store attributes.
    Nodes can be placed in a data structure.
    """

    def __init__(self, state, parent = None, action=None, pathCost = None):
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 1

        self.action = action
        self.state = state
        self.parent = parent

    def __str__(self):
        return str(self.state)


def nodeTester():
    node1 = Node("node1")
    node2 = Node("node2", node1)
    node3 = Node("node3", node2)
    node4 = Node("node4", node3)
    printNodes(node4)

def printNodes(node):
    print "Printing out list of nodes:"
    while node:
        print node,
        node = node.getParent()
    #print

nodeTester()


class make_node:
    """
    Class for Nodes to store attributes.
    Nodes can be placed in a data structure.
    """


    def __init__(self, state, parent=None, action=None, path_cost=0):
        "Create a search tree Node, derived from a parent by an action."
        update(self, state=state, parent=parent, action=action,
               path_cost=path_cost, depth=0)
        if parent:
            self.depth = parent.depth + 1


    def __repr__(self):
        "returns a printable representation of the object."
        return "<Node %s>" % (self.state,)


    def path(self):
        "Create a list of nodes from the root to this node."
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        return result


    def expand_node(self, problem):
        "Return a list of nodes reachable from this node."
        return [make_node(next, self, act,
                     problem.path_cost(self.path_cost, self.state, act, next))
                for (act, next) in problem.successor(self.state)]


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




def graph_search(problem, fringe):
    """
    Returns a sequence of moves according to the generic search algorithm
	if a solution is found, faile otherwise.
    :param problem:
    :return:
    """
    from game import Directions
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())


    closed = {}
    fringe.append(make_node(problem.initial))
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state):
            return node
        if node.state not in closed:
            closed[node.state] = True
            fringe.extend(node.expand_node(problem))


    return None


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
    "*** YOUR CODE HERE ***"


    return graph_search(problem, Queue())


    util.raiseNotDefined()




def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()




def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()




def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0




def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


