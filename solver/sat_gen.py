from functools import reduce
from datetime import datetime
import operator
import itertools

import helper

L = 1
R = 2
T = 4
B = 8
LR = L | R
TB = T | B
TL = T | L
TR = T | R
BL = B | L
BR = B | R
SWAP = {L: R, R: L, T: B, B: T}
VECTORS = [(L, 0, -1), (R, 0, 1), (T, -1, 0), (B, 1, 0)]
POS_TYPES = [LR, TB, TL, TR, BL, BR]
PATH = {LR: '─', TB: '│', TL: '┘', TR: '└', BL: '┐', BR: '┌'}

color_count = 0
size = 0

'''unused'''
def old_gen(grid):
    col = 0

    #generate endpoints
    for pair in grid.points:
        col +=1
        grid.e1.append('E1|{color}|{path_pos}|{position}'.format(color = col, path_pos = 1, position = pair[0]))

        curr_e2 = []
        for i in range(2, grid.size * grid.size + 1):
            curr_e2.append('E2|{color}|{path_pos}|{position}'.format(color = col, path_pos = i, position = pair[1]))

        grid.e2.append(curr_e2)

    #generate non endpoints
    for i in range(1, grid.size * grid.size + 1):
        endpoints = grid.get_endpoints()
        if i not in endpoints:
            curr_ne = []
            for c in range(1, grid.colors + 1):
                curr_c = []
                for p in range(2, grid.size * grid.size):
                    curr_c.append('x|{color}|{path_pos}|{position}'.format(color = c, path_pos = p, position = i))

                curr_ne.append(curr_c)


''' Generate all SAT Variables and CNF Clauses using for use with pycosat'''
def cnf(grid, colors):

    start = datetime.now()
    
    #helper method that liks sat variavle to 
    def get_colors(i, j, color):
        return (i*len(grid) + j)*len(colors) + color + 1

    #amount of color (path) variables to be made
    get_colors_count = len(colors) * len(grid)**2

    clauses = generate_clauses(grid, colors)
    pos_vars, num_pos_vars = generate_path_vars(grid, get_colors_count)
    pos_clauses = generate_path_clauses(grid, colors, pos_vars)
    num_vars = get_colors_count + num_pos_vars
    clauses = clauses + pos_clauses

    return get_colors, pos_vars, num_vars, clauses, (datetime.now() - start).total_seconds()

''' Generate all path variables'''
def generate_path_vars(grid, start_var):
    pos_vars = dict()
    num_pos_vars = 0

    for x, y, node in helper.flatten(grid):
        #if a node is not an endnode we create the appropreate sat variables
        if not node.isalnum():
            neighbor_bits = (pos_bit for (pos_bit, _, _) in colorable_adjacent(len(grid), x, y))
            cell_flags = reduce(operator.or_, neighbor_bits, 0)
            pos_vars[x, y] = dict()

            for code in POS_TYPES:
                if cell_flags & code == code:
                    num_pos_vars += 1
                    pos_vars[x, y][code] = start_var + num_pos_vars

    return pos_vars, num_pos_vars

''' Generate all clauses'''
def generate_clauses(grid, colors):
    clauses = []

    for x, y, node in helper.flatten(grid):
        if node.isalnum():
            # Each endpoint has a predefined colour
            clauses.append([get_colors(x, y, colors[node], len(grid), len(colors))])

            # Each node cannot be more than one color
            for other_color in range(len(colors)):
                if other_color != colors[node]:
                    clauses.append([-get_colors(x, y, other_color, len(grid), len(colors))])

            # Every non endpoint has exactly two neighbours of the same color
            neighbours = [get_colors(ni, nj, colors[node], len(grid), len(colors)) for _, ni, nj in colorable_adjacent(len(grid), x, y)]
            clauses.append(neighbours)
            clauses.extend(((-a, -b) for (a, b) in itertools.combinations(neighbours, 2)))

        else:
            # Same colored neighbours of a node must be the same either paths or endpoints
            clauses.append([get_colors(x, y, color, len(grid), len(colors)) for color in range(len(colors))])
            cell_get_colors = (get_colors(x, y, color, len(grid), len(colors)) for color in range(len(colors)))
            clauses.extend(((-a, -b) for (a, b) in itertools.combinations(cell_get_colors, 2)))


    return clauses

''' Generate extra path clauses'''
def generate_path_clauses(grid, colors, pos_vars):

    pos_clauses = []
    color_count = len(colors)

    for x, y, node in helper.flatten(grid):

        if not node.isalnum():

            # Each node has a specific position in a path (determined by the path var)
            cell_pos_dict = pos_vars[(x, y)]
            cell_pos_vars = cell_pos_dict.values()
            pos_clauses.append(cell_pos_vars)
            pos_clauses.extend(((-a, -b) for (a, b) in itertools.combinations(cell_pos_dict, 2)))

            for color in range(color_count):
                color_1 = get_colors(x, y, color, len(grid), color_count)
                for pos_bit, n_i, n_j in get_adjacent(x, y):

                    color_2 = get_colors(n_i, n_j, color, len(grid), color_count)

                    for pos_type, pos_var in cell_pos_dict.items():
                        
                        # Path variables determine which neighbours are of the same color
                        if pos_type & pos_bit:
                            pos_clauses.append([-pos_var, -color_1, color_2])
                            pos_clauses.append([-pos_var, color_1, -color_2])

                        # All other path variables must have a different color
                        elif helper.is_valid(len(grid), n_i, n_j):
                            pos_clauses.append([-pos_var, -color_1, -color_2])

    return pos_clauses

def get_colors(x, y, color, size, color_count):
    return (x*size + y)*color_count + color + 1

def get_adjacent(x, y):
    return ((pos_bit, x+delta_i, y+delta_j) for (pos_bit, delta_i, delta_j) in VECTORS)

#uses get_adjacent to return adjacent nodes that are valid (in the grid and can be colored)
def colorable_adjacent(size, x, y):
    return ((pos_bit, ni, nj) for (pos_bit, ni, nj) in get_adjacent(x, y) if helper.is_valid(size, ni, nj))
