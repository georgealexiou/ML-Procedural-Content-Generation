from functools import reduce
from datetime import datetime
import operator

import helper

L = 1
R = 2
T = 4
B = 8

DELTAS = [(L, 0, -1),
          (R, 0, 1),
          (T, -1, 0),
          (B, 1, 0)]

LR = L | R
TB = T | B
TL = T | L
TR = T | R
BL = B | L
BR = B | R

VECTORS = [(L, 0, -1),
           (R, 0, 1),
           (T, -1, 0),
           (B, 1, 0)]

DIR_TYPES = [LR, TB, TL, TR, BL, BR]

'''Return all neighbors of a grid square at row i, column j.'''
def all_neighbors(i, j):
    return ((dir_bit, i+delta_i, j+delta_j)
            for (dir_bit, delta_i, delta_j) in VECTORS)

'''Return all actual on-grid neighbors of a grid square at row i, column j.'''
def valid_neighbors(size, i, j):
    return ((dir_bit, ni, nj) for (dir_bit, ni, nj)
            in all_neighbors(i, j)
            if helper.is_valid(size, ni, nj))

'''Creates the direction-type SAT variables for each cell.'''
def make_dir_vars(grid, start_var):
    size = len(grid)
    dir_vars = dict()
    num_dir_vars = 0

    for i, j, char in helper.flatten(grid):

        if char.isalnum(): # flow endpoint, no dir needed
            continue

        # collect bits for neighbors (T B L R)
        neighbor_bits = (dir_bit for (dir_bit, ni, nj)
                         in valid_neighbors(size, i, j))

        # OR them all together
        cell_flags = reduce(operator.or_, neighbor_bits, 0)

        # create a lookup for dir type vars in this cell
        dir_vars[i, j] = dict()

        for code in DIR_TYPES:
            # only add var if cell has correct flags (i.e. if cell has
            # T, B, R, don't add LR).
            if cell_flags & code == code:
                num_dir_vars += 1
                dir_vars[i, j][code] = start_var + num_dir_vars

    return dir_vars, num_dir_vars


    '''Generate CNF clauses entailing the N*M color SAT variables, where N
is the number of cells and M is the number of colors. Each cell
encodes a single color in a one-hot fashion.

    '''
def make_color_clauses(grid, colors, color_var):

    clauses = []
    num_colors = len(colors)
    size = len(grid)

    # for each cell
    for i, j, char in helper.flatten(grid):

        if char.isalnum(): # flow endpoint

            endpoint_color = colors[char]

            # color in this cell is this one
            clauses.append([color_var(i, j, endpoint_color)])

            # color in this cell is not the other ones
            for other_color in range(num_colors):
                if other_color != endpoint_color:
                    clauses.append([-color_var(i, j, other_color)])

            # gather neighbors' variables for this color
            neighbor_vars = [color_var(ni, nj, endpoint_color) for
                             _, ni, nj in valid_neighbors(size, i, j)]

            # one neighbor has this color
            clauses.append(neighbor_vars)

            # no two neighbors have this color
            clauses.extend(helper.no_two(neighbor_vars))

        else:

            # one of the colors in this cell is set
            clauses.append([color_var(i, j, color)
                            for color in range(num_colors)])

            # no two of the colors in this cell are set
            cell_color_vars = (color_var(i, j, color) for
                               color in range(num_colors))

            clauses.extend(helper.no_two(cell_color_vars))

    return clauses

######################################################################

'''Creates the direction-type SAT variables for each cell.'''
def make_dir_vars(grid, start_var):
    size = len(grid)
    dir_vars = dict()
    num_dir_vars = 0

    for i, j, char in helper.flatten(grid):

        if char.isalnum(): # flow endpoint, no dir needed
            continue

        # collect bits for neighbors (T B L R)
        neighbor_bits = (dir_bit for (dir_bit, ni, nj)
                         in valid_neighbors(size, i, j))

        # OR them all together
        cell_flags = reduce(operator.or_, neighbor_bits, 0)

        # create a lookup for dir type vars in this cell
        dir_vars[i, j] = dict()

        for code in DIR_TYPES:
            # only add var if cell has correct flags (i.e. if cell has
            # T, B, R, don't add LR).
            if cell_flags & code == code:
                num_dir_vars += 1
                dir_vars[i, j][code] = start_var + num_dir_vars

    return dir_vars, num_dir_vars

######################################################################

    '''Generate clauses involving the color and direction-type SAT
variables. Each free cell must be exactly one direction, and
directions imply color matching with neighbors.

    '''
def make_dir_clauses(grid, colors, color_var, dir_vars):

    dir_clauses = []
    num_colors = len(colors)
    size = len(grid)

    # for each cell
    for i, j, char in helper.flatten(grid):

        if char.isalnum(): # flow endpoint, no dir needed
            continue

        cell_dir_dict = dir_vars[(i, j)]
        cell_dir_vars = cell_dir_dict.values()

        # at least one direction is set in this cell
        dir_clauses.append(cell_dir_vars)

        # no two directions are set in this cell
        dir_clauses.extend(helper.no_two(cell_dir_vars))

        # for each color
        for color in range(num_colors):

            # get color var for this cell
            color_1 = color_var(i, j, color)

            # for each neighbor
            for dir_bit, n_i, n_j in all_neighbors(i, j):

                # get color var for other cell
                color_2 = color_var(n_i, n_j, color)

                # for each direction variable in this scell
                for dir_type, dir_var in cell_dir_dict.items():

                    # if neighbor is hit by this direction type
                    if dir_type & dir_bit:
                        # this direction type implies the colors are equal
                        dir_clauses.append([-dir_var, -color_1, color_2])
                        dir_clauses.append([-dir_var, color_1, -color_2])
                    elif helper.is_valid(size, n_i, n_j):
                        # neighbor is not along this direction type,
                        # so this direction type implies the colors are not equal
                        dir_clauses.append([-dir_var, -color_1, -color_2])

    return dir_clauses

    '''Reduces the given grid to a SAT problem specified in CNF. Returns
a list of clauses where each clause is a list of single SAT variables,
possibly negated.

    '''
def reduce_to_sat(grid, colors):

    size = len(grid)
    num_colors = len(colors)

    num_cells = size**2
    num_color_vars = num_colors * num_cells

    def color_var(i, j, color):
        '''Return the index of the SAT variable for the given color in row i,
 column j.

        '''
        return (i*size + j)*num_colors + color + 1

    start = datetime.now()

    color_clauses = make_color_clauses(grid,
                                       colors,
                                       color_var)

    dir_vars, num_dir_vars = make_dir_vars(grid, num_color_vars)

    dir_clauses = make_dir_clauses(grid, colors,
                                   color_var, dir_vars)

    num_vars = num_color_vars + num_dir_vars
    clauses = color_clauses + dir_clauses

    reduce_time = (datetime.now() - start).total_seconds()

    return color_var, dir_vars, num_vars, clauses, reduce_time
