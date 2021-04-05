import itertools
import math

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

'''Called in order to parse the grid based on file or code'''
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
        print(grid)

    if len(grid) < len(grid[0]):
        print ('Invalid format')
        return None, None, None

    grid = grid[:len(grid[0])]

    return grid, get_colors(grid, filename), grid_to_code(grid)

'''Returns a list of colors in the grid and finds errors in the colors'''
def get_colors(grid, filename):

    # count colors and build lookup
    colors = dict()
    color_count = []

    for i, row in enumerate(grid):
        if len(row) != len(grid[0]):
            print ('{}:{} row size mismatch'.format(filename, i+1))
            return None
        for j, char in enumerate(row):
            if char.isalnum(): # flow endpoint
                if char in colors:
                    color = colors[char]
                    if color_count[color]:
                        print ('{}:{}:{} too many {} already'.format(
                            filename, i+1, j, char))
                        return None
                    color_count[color] = 1
                else:
                    color = len(colors)
                    colors[char] = color
                    color_count.append(0)

    # check parity
    for char, color in colors.items():
        if not color_count[color]:
            print ('color {} has start but no end!'.format(char))
            return None

    return colors

'''Convert code to grid'''
def code_to_grid(code, size):
    print(code)
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

'''Convert grid to code'''
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