import itertools

'''Generates clause that no two vars can be the same out of a given list'''
def no_two(satvars):
    return ((-a, -b) for (a, b) in itertools.combinations(satvars, 2))

'''Flattens 2D Grid to a 1D list for iteration'''
def flatten(grid):
    for x, row in enumerate(grid):
        for y, item in enumerate(row):
            yield x, y, item

'''Returns true if the coordinates given are on the grid'''
def is_valid(size, x, y):
    if (x >= 0 and x < size and y >= 0 and y < size):
        return True
    else:
        return False

def print_seperator():
    print ('\n'+('#'*80)+'\n')

'''Flattens 2D Grid to a 1D list for iteration'''
def flatten(grid):
    for x, row in enumerate(grid):
        for y, item in enumerate(row):
            yield x, y, item