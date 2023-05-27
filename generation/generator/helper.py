import itertools
import math
import random
import model


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

def parse_grid(file, is_grid, size, filename = 'input'):
    grid = []
    code = ''
    
    if is_grid:
        if not isinstance(file, str):
            file = file.read()
        
        grid = file.splitlines()

    else:
        code = file
        grid = code_to_grid(code, size)

    if len(grid) < len(grid[0]):
        # print ('Invalid format')
        return None, None, None

    grid = grid[:len(grid[0])]

    return grid, get_colors(grid, filename), grid_to_code(grid)

def get_colors(grid, filename):
    colors = dict()
    pair_found = []
    wrong = False

    for i, row in enumerate(grid):
        #check if grid is square
        if len(row) != len(grid[0]):
            print ('grid not square')
            return None
        
        #fills color dictionary with colors and checks if a pair is found
        for j, char in enumerate(row):

            if char.isalnum():
                if char not in colors:
                    colors[char] = len(colors)
                    pair_found.append(False)
                else:
                    color = colors[char]
                    pair_found[color] = 1

    if wrong:
        print ('too many endpoints of a specific color')
        return None

    for char, color in colors.items():
        if not pair_found[color]:
            print ('no enough endpoints of a specific color')
            return None

    return colors

def init(size):
    try:
        return make_grid(size)
    except:
        return('')

def code_to_grid(code, size):
    grid = []
    split = [char for char in code]
    row = []

    save = 'n'
    for i in range(0,len(split)):
        dots = 0

        if split[i].isdigit():
            char = split[i]

            if not (i == len(split) - 1):
                if split[i+1].isdigit():
                    save = split[i]
                    continue
                if save != 'n':
                    char = '{}{}'.format(save, split[i])
                    save = 'n'

            dots = int(char)
            for i in range(0, dots):
                if len(row) == size:
                    grid.append(row)
                    row = []
                    row.append('.')
                
                else:
                    row.append('.')

        else:
            if len(row) < size:
                row.append(split[i])
                
            elif len(row) == size:
                grid.append(row)
                row = []
                row.append(split[i])
        
        
    
    grid.append(row)

    return grid

def make_grid(size):
    file = open("experiments/{}x{}.txt".format(size,size), "r")
    file = file.read()
    texts = file.split('\n\n')
    return(texts[random.randint(0,19)])

def grid_to_code(grid):
    code = ''
    counter = 0

    for row in grid:

        for char in row:
            if char.isalnum(): #endpoint
                if counter > 0:
                    code = code + '{}'.format(counter)
                    code = code + char
                    counter = 0
                elif counter == 0:
                    code = code + char
            else:
                counter += 1

    if counter > 0:
        code = code + '{}'.format(counter)

    return code

'''Returns size of the grid based on code'''
def get_grid_size(code):
    size = 0
    split = [char for char in code]

    save = 'n'
    for i in range(0,len(split)):

        if split[i].isdigit():
            num = split[i]

            if not (i == len(split) - 1):
                if split[i+1].isdigit():
                    save = split[i]
                    continue

                if save != 'n':
                    num = '{}{}'.format(save, split[i])
                    save = 'n'

            size += int(num)

        else:
            size += 1

    return math.sqrt(size)

def to_string(grid, size):
    string = ''
    for row in grid:

        if(len(row) < size):
            while (len(row) < size):
                row.append('.')

        for item in row:
            string = string + '{}'.format(item)
        string = string + '\n'
    
    return string