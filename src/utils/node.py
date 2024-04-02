class TreeNode:
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.children = []
        self.depth = depth

        # A* algorithm attributes
        self.f = 0
        self.g = 0
        self.h = 0

        # Monte Carlo Tree Search attributes
        self.wins = 0.0
        self.visits = 0.0
        self.ressq = 0.0
        self.sputc = 0.0

    def __lt__(self, other):
        return self.f < other.f

    def add_child(self, child_node):
        """
            Add a child node to the current node
        """

        self.children.append(child_node)
        child_node.parent = self

    # used for MCST
    def SetWeight(self, weight):
        """
            Set the weight of the node
        """
        self.weight = weight

    def AppendChild(self, child):

        """
            Append a child to the node
        """
        
        self.children.append(child)
        child.parent = self

    def IsEqual(self, Node):
        if(self.state == Node.state):
            return True
        else:
            return False