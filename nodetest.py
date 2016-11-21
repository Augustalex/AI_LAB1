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


def nodeTester():
    node1 = Node("node1")
    node2 = Node("node2", node1)
    node3 = Node("node3", node2)
    node4 = Node("node4", node3)
    node5 = Node("node5", node4)
    node6 = Node("node6", node5)
    printNodes(node6)

def printNodes(node):
    print "Printing out list of nodes:"
    while node:
        print node,
        node = node.parent
    #print

nodeTester()