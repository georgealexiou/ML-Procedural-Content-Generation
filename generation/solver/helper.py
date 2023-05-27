import itertools
import math

def flatten(grid):
    generated = []
    for row in grid:
        for item in row:
            generated.append(item)
    
    for x, row in enumerate(grid):
        for y, item in enumerate(row):
            yield x, y, item

def is_valid(size, x, y):
    if (x >= 0 and x < size and y >= 0 and y < size):
        return True
    else:
        return False

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

    