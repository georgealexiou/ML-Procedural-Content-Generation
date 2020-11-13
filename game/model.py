class Grid:

    def __init__(self, size):
        self.size = size
        self.nodes = [[]]
        self.existing_colors = []

    def add_node (self, node, x, y):
        if (node.type != "point"):
            if (self.nodes[x][y] == None): #what happens when adding connection to an existing connection node
                self.nodes[x][y] = node

    #used for creating a pair of new colors
    def create_pair (self, node1, node2, x1, y1, x2, y2):
        check1 = self.nodes[x1][y1] == None or self.nodes[x1][y1].type == "connection"
        check2 = self.nodes[x2][y2] == None or self.nodes[x2][y2].type == "connection"

        if (check1 and check2):
            self.nodes[x1][y1] = node1
            self.nodes[x2][y2] = node2

    def move_node (self, x1, y1, x2, y2):
        prev = self.nodes[x1][y1]
        new = self.nodes[x2][y2]
        
        #if target node is empty -> move
        if (self.nodes[x2][y2] == None):
            self.nodes[x2][y2] = self.nodes[x1][y1]
            self.nodes[x1][y1] = None

        #if target node is node of different color -> swap
        elif (self.nodes[x2][y2].type == "point" and self.nodes[x2][y2].color != self.nodes[x1][y1].color):
            temp = self.nodes[x1][y1]
            self.nodes[x1][y1] = self.nodes[x2][y2]
            self.nodes[x2][y2] = temp

        #if target node is connection (solver)
        elif (self.nodes[x2][y2].type == "connection"):
            self.nodes[x2][y2] = self.nodes[x1][y1]
            self.nodes[x1][y1] = None

    def to_string(self):
        print(self.nodes)

class Node:
    
    def __init__(self, name, color, node_type):
        self.label = color
        self.type = node_type
        self.color = self.determine_color()

    def determine_color():
        return ""
