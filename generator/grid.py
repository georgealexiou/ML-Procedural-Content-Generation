import random
import string
from sys import path
import helper
import format_grid
from argparse import ArgumentParser

alphabet = string.ascii_uppercase + string.ascii_lowercase

def create(size):
    grid = Grid(size)
    formatted = helper.init(size)
    if(formatted == ''):
        format_grid.gen(size, grid)
    else:
        print(formatted)

# grid[y][x]
class Grid:
    def __init__(self, size):
        self.size = size
        self.nodes = [['.']*size for _ in range(size)]
        self.filled = [['']*size for _ in range(size)]
        self.colors = 0
        self.letter_used = 0

    ''' Returns all neighbouring points of a point p '''
    def get_neighbours(self, p):
        neighbours = []
        neighbours.append((p[0],p[1]+1))
        neighbours.append((p[0],p[1]-1))
        neighbours.append((p[0]+1,p[1]))
        neighbours.append((p[0]-1,p[1]))

        return neighbours

    ''' Returns all empty slots in a grid '''
    def get_empty_spots(self):
        empty = []
        
        for y, row in enumerate(self.filled):
            for x, item in enumerate(row):
                if item == '':
                    empty.append((x,y))
        
        return empty

    ''' Returns all empty points that can be reached from a point '''
    def get_empty_neighbours(self, p):
        neighbours = self.get_neighbours(p)
        available = []

        for item in neighbours:
            if -1 in item or self.size in item:
                continue

            if self.filled[item[0]][item[1]] == '':
                available.append(item)

        return available

    ''' Returns all possible positions for the second endpoint given the first'''
    def get_possible_p2(self, p):
        all_available = []
        all_available.append(p)

        i = 0
        while (i <= len(all_available) - 1):
            all_available += self.get_empty_neighbours(all_available[i])
            res = []
            [res.append(x) for x in all_available if x not in res]
            all_available = res
            i += 1
        
        res.remove(p)

        return res

    ''' Generates two new endpoints to be added to the grid '''
    def generate_pair(self):
        empty_spots = self.get_empty_spots()
        
        possible_p2 = []
        i = 0
        while(len(possible_p2) < 1 and i <= 5):
            p1 = random.choice(empty_spots)
            possible_p2 = self.get_possible_p2(p1)
            i += 1

        if(len(possible_p2) < 2):
            return None, None

        p2 = random.choice(possible_p2)

        while (p1 == p2 or p2 in self.get_neighbours(p1)):
            p2 = random.choice(possible_p2)

        self.colors += 1

        return p1, p2

    def create_path(self, p1, p2):
        node = path_gen.Node(self, None, '', p1, p2)
        grid = node.aStar()
        return grid

    def generate_grid(self):
        while self.get_empty_spots() != None:
            p1, p2 = self.generate_pair()
            self.create_path(p1, p2)

            tobreak = True
            for i in self.get_empty_spots():
                if(len(self.get_empty_neighbours(i)) >= 3):
                    tobreak = False

            if tobreak:
                break
                    

    ''' Generates two new endpoints to be added to the grid '''
    def fix(self):
        empty = self.get_empty_spots()
        for i in empty:
            for j in self.get_neighbours(i):
                # extend path
                if(self.nodes[j[0]][j[1]].isalnum()):
                    self.nodes[i[0]][i[1]] = self.nodes[j[0]][j[1]] 
                    self.nodes[j[0]][j[1]] = '.'
                    break #check other neighbours

parser = ArgumentParser(description='Run Generator')
parser.add_argument('size', metavar='N', type = int, nargs='*')
arguments = parser.parse_args()

create(arguments.size[0])
