from satispy import Variable, Cnf 
from satispy.solver import Minisat
import numpy as np

variables = empty_array = np. empty((5, 5), Variable)

for x in range(0,9):
    for y in range(0,9):
        variables[x][y] = Variable('V{}{}cd'.format(x,y))

#every cell is one color
color_rule = 

# Returns all combinations of pairs
def all_pairs(collection):
    return itertools.combinations(collection, 2)

# Given sat variables it generates an expretion that specifies that no two can be the same
def no_two(satvars):
    return ((-a, -b) for (a, b) in all_pairs(satvars))

#iterator for 2d arrays
def explode(puzzle):
    for i, row in enumerate(puzzle):
        for j, char in enumerate(row):
            yield i, j, char

# Checks validity of position in a block
def valid_pos(size, i, j):
    return i >= 0 and i < size and j >= 0 and j < size

# Returns all neighbours of the block
def all_neighbors(i, j):
    '''Return all neighbors of a grid square at row i, column j.'''
    return ((dir_bit, i+delta_i, j+delta_j)
            for (dir_bit, delta_i, delta_j) in DELTAS)

# Returns on grid neighnours
def valid_neighbors(size, i, j):
    '''Return all actual on-grid neighbors of a grid square at row i,
column j.'''

    return ((dir_bit, ni, nj) for (dir_bit, ni, nj)
            in all_neighbors(i, j)
            if valid_pos(size, ni, nj))



# exp = v1 & v2 | v3
# solver = Minisat()
# solution = solver.solve(exp)
# if solution.success:
#     print ('Found a solution:') 
#     print (v1, solution[v1]) 
#     print (v2, solution[v2]) 
#     print (v3, solution[v3])
# else:
#     print ('The expression cannot be satisfied')