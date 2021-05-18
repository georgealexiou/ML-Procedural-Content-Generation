import random

class Grid:

    def __init__(self, size):
        self.size = size
        self.nodes = [[None]*size]*size
        self.existing = []

    def add_connection (self, node, x, y):

        #if we want to add a connection we check adjacent
        if (node.type == "connection"):
            if(self.nodes[x][y].type == "connection" and self.nodes[x][y].name != node.name):
                self.break_adjacent_connection(x,y,self.nodes[x][y].name)

    #used for creating a pair of new colors
    def create_pair (self, node1, node2, x1, y1, x2, y2):
        check1 = self.nodes[x1][y1] == None or self.nodes[x1][y1].type != "connection"
        check2 = self.nodes[x2][y2] == None or self.nodes[x2][y2].type != "connection"

        if (check1 and check2):
            self.nodes[x1][y1] = node1
            self.nodes[x2][y2] = node2

    #used for moving a node in a new location (can only move point nodes)
    def move_node (self, x1, y1, x2, y2):
        prev = self.nodes[x1][y1]
        new = self.nodes[x2][y2]

        if(self.nodes[x1][y1].type == "point"):
            #if target node is empty -> move
            if (self.nodes[x2][y2] == None):
                self.nodes[x2][y2] = self.nodes[x1][y1]
                self.nodes[x1][y1] = None

            #elif target node is node of different color -> swap
            elif (self.nodes[x2][y2].type == "point" and self.nodes[x2][y2].name != self.nodes[x1][y1].name):
                temp = self.nodes[x1][y1]
                self.nodes[x1][y1] = self.nodes[x2][y2]
                self.nodes[x2][y2] = temp

            #elif target node is connection (solver) and -> swap and TODO break connection
            elif(self.nodes[x2][y2].type == "connection"):
                self.break_adjacent_connection(x2, y2, self.nodes[x2][y2].name)

    #breaks connection if node is inserted in that position
    def break_adjacent_connection(self, x, y, name):
        if (self.nodes[x-1][y].type == "connection"):
            self.remove_node(x-1, y)
            self.break_adjacent_connection(x-1, y, name)
        
        if (self.nodes[x+1][y].type == "connection"):
            self.remove_node(x+1, y)
            self.break_adjacent_connection(x+1, y, name)

        if (self.nodes[x][y-1].type == "connection"):
            self.remove_node(x, y-1)
            self.break_adjacent_connection(x, y-1, name)

        if (self.nodes[x][y+1].type == "connection"):
            self.remove_node(x, y+1)
            self.break_adjacent_connection(x, y+1, name)

    #unsafe removal of node
    def remove_node(self, x, y):
        self.nodes[x][y] == None

    def print_grid(self):
        return self.nodes

    def to_string(self):
        out = ""
        for i in self.nodes:
            for j in i:
                counter = 0
                if j != None:
                    if counter > 0:
                        out = out + counter
                        counter = 0

                    out = out + j.name
                else:
                    counter += 1

        return out

class Node:
    
    def __init__(self, name, node_type):
        self.name = name
        self.type = node_type

    def __str__():
        return self.name
    