import itertools
from argparse import ArgumentParser
from datetime import datetime
import pycosat
import sys

import sat_gen
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

DIR_TYPES = [LR, TB, TL, TR, BL, BR]

DIR_FLIP = {
    L: R,
    R: L,
    T: B,
    B: T
    }

ANSI_LOOKUP = dict(R=101, B=104, Y=103, G=42,
                   O=43, C=106, M=105, m=41,
                   P=45, A=100, W=107, g=102,
                   T=47, b=44, c=46, p=35)

ANSI_RESET = '\033[0m'

ANSI_CELL_FORMAT = '\033[30;{}m'

PATH_REPRESENTATION = {
    LR: '─',
    TB: '│',
    TL: '┘',
    TR: '└',
    BL: '┐',
    BR: '┌'
    }

RESULT_STRINGS = dict(s='successful',
                      f='failed',
                      u='unsolvable')

def parse_grid(file, is_grid, filename = 'input'):
    grid = []
    code = ''
    
    if is_grid:
        if not isinstance(file, str):
            file = file.read()
        
        grid = file.splitlines()

    else:
        code = file
        grid = code_to_grid(code)

    if len(grid) < len(grid[0]):
        print ('Invalid format')
        return None, None, None

    grid = grid[:len(grid[0])]

    return grid, get_colors(grid, filename), grid_to_code(grid)

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


'''Convert grid to code'''
def code_to_grid(code):
    grid = []
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

    return code

######################################################################

'''Takes the solution set from SAT and decodes it by undoing the
one-hot encoding in each cell for color and direction-type. Returns a
2D array of (color, direction-type) pairs.'''
def decode_solution(grid, colors, color_var, dir_vars, sol):

    sol = set(sol)
    num_colors = len(colors)

    decoded = []

    for i, row in enumerate(grid):

        decoded_row = []

        for j, char in enumerate(row):

            # find which color variable for this cell is in the
            # solution set
            cell_color = -1

            for color in range(num_colors):
                if color_var(i, j, color) in sol:
                    assert cell_color == -1
                    cell_color = color

            assert cell_color != -1

            cell_dir_type = -1

            if not char.isalnum(): # not a flow endpoint

                # find which dir type variable for this cell is in the
                # solution set
                for dir_type, dir_var in dir_vars[i, j].items():
                    if dir_var in sol:
                        assert cell_dir_type == -1
                        cell_dir_type = dir_type

                assert cell_dir_type != -1

            decoded_row.append((cell_color, cell_dir_type))

        decoded.append(decoded_row)

    return decoded

######################################################################

    '''Follow a path starting from an arbitrary row, column location on
the grid until a non-path cell is detected, or a cycle is
found. Returns a list of (row, column) pairs on the path, as well as a
boolean flag indicating if a cycle was detected.

    '''
def make_path(decoded, visited, cur_i, cur_j):

    size = len(decoded)

    run = []
    is_cycle = False
    prev_i, prev_j = -1, -1

    while True:

        advanced = False

        # get current cell, set visited, add to path
        color, dir_type = decoded[cur_i][cur_j]
        visited[cur_i][cur_j] = 1
        run.append((cur_i, cur_j))

        # loop over valid neighbors
        for dir_bit, n_i, n_j in sat_gen.valid_neighbors(size, cur_i, cur_j):

            # do not consider prev pos
            if (n_i, n_j) == (prev_i, prev_j):
                continue

            # get neighbor color & dir type
            n_color, n_dir_type = decoded[n_i][n_j]

            # these are connected if one of the two dir type variables
            # includes the (possibly flipped) direction bit.
            if ((dir_type >= 0 and (dir_type & dir_bit)) or
                    (dir_type == -1 and n_dir_type >= 0 and
                     n_dir_type & DIR_FLIP[dir_bit])):

                # if connected, they better be the same color
                assert color == n_color

                # detect cycle
                if visited[n_i][n_j]:
                    is_cycle = True
                else:
                    prev_i, prev_j = cur_i, cur_j
                    cur_i, cur_j = n_i, n_j
                    advanced = True

                # either cycle detected or path advanced, so sT
                # looking at neighbors
                break

        # if path not advanced, quit
        if not advanced:
            break

    return run, is_cycle

######################################################################

'''Examine the decoded SAT solution to see if any cycles exist; if so,
return the CNF clauses that need to be added to the problem in order
to prevent them.'''
def detect_cycles(decoded, dir_vars):

    size = len(decoded)
    colors_seen = set()
    visited = [[0]*size for _ in range(size)]

    # for each cell
    for i, j, (color, dir_type) in helper.flatten(decoded):

        # if flow endpoint for color we haven't dealt with yet
        if dir_type == -1 and color not in colors_seen:

            # add it to set of colors dealt with
            assert not visited[i][j]
            colors_seen.add(color)

            # mark the path as visited
            run, is_cycle = make_path(decoded, visited, i, j)
            assert not is_cycle

    # see if there are any unvisited cells, if so they have cycles
    extra_clauses = []

    for i, j in itertools.product(range(size), range(size)):

        if not visited[i][j]:

            # get the path
            run, is_cycle = make_path(decoded, visited, i, j)
            assert is_cycle

            # generate a clause negating the conjunction of all
            # direction types along the cycle path.
            clause = []

            for r_i, r_j in run:
                _, dir_type = decoded[r_i][r_j]
                dir_var = dir_vars[r_i, r_j][dir_type]
                clause.append(-dir_var)

            extra_clauses.append(clause)

    # return whatever clauses we had to generate
    return extra_clauses

######################################################################

'''Print the grid solution to the terminal.'''
def show_solution(colors, decoded):

    # make an array to flip the key/value in the colors dict so we can
    # index characters numerically:

    color_chars = [None]*len(colors)

    do_color = True

    for char, color in colors.items():
        color_chars[color] = char
        do_color = do_color and char in ANSI_LOOKUP

    for decoded_row in decoded:
        for (color, dir_type) in decoded_row:

            assert color >= 0 and color < len(colors)

            color_char = color_chars[color]

            if dir_type == -1:
                if do_color:
                    display_char = color_char
                else:
                    display_char = color_char
            else:
                display_char = PATH_REPRESENTATION[dir_type]

            if do_color:

                if color_char in ANSI_LOOKUP:
                    ansi_code = ANSI_CELL_FORMAT.format(
                        ANSI_LOOKUP[color_char])
                else:
                    ansi_code = ANSI_RESET

                sys.stdout.write(ansi_code)

            sys.stdout.write(display_char)

        sys.stdout.write(ANSI_RESET)

        sys.stdout.write('\n')

######################################################################

'''Solve the SAT now that it has been reduced to a list of clauses in
CNF.  This is an iterative process: first we try to solve a SAT, then
we detect cycles. If cycles are found, they are prevented from
recurring, and the next iteration begins. Returns the SAT solution
set, the decoded grid solution, and the number of cycle repairs
needed.'''
def solve_sat(grid, colors, color_var, dir_vars, clauses):

    start = datetime.now()

    decoded = None
    all_decoded = []
    repairs = 0

    while True:

        sol = pycosat.solve(clauses) # pylint: disable=E1101

        if not isinstance(sol, list):
            decoded = None
            all_decoded.append(decoded)
            break

        decoded = decode_solution(grid, colors, color_var, dir_vars, sol)
        all_decoded.append(decoded)

        extra_clauses = detect_cycles(decoded, dir_vars)

        if not extra_clauses:
            break

        clauses += extra_clauses
        repairs += 1

    solve_time = (datetime.now() - start).total_seconds()

    if decoded is None:
        print ('solver returned {} after {:,} cycle '\
            'repairs and {:.3f} seconds'.format(
                str(sol), repairs, solve_time))
    else:
        show_solution(colors, decoded)

    return sol, decoded, repairs, solve_time

######################################################################

'''Main loop if module run as script.'''
def pyflow_solver_main(code):

    parser = ArgumentParser(
        description='Solve Flow Free grids via reduction to SAT')
    parser.add_argument('code', metavar='grid', nargs='*', help='.txt file containing grid')

    parser.add_argument('-f', dest='file', default=False,
                        action='store_true',
                        help='quiet mode (reduce output)')
    
    parser.add_argument('-i', dest='id', default=False,
                        action='store_true',
                        help='quiet mode (reduce output)')

    arguments = parser.parse_args()

    max_width = max(len(f) for f in arguments.code)

    grid_count = 0

    stats = dict()


    if not arguments.file and not arguments.id and code == '':
        print ('-f -i: Error invalid selection')

    elif arguments.file and arguments.id:
        print ('-f -i: Error invalid selection')
    
    elif arguments.file:
        # open file
        try:
            with open(arguments.code[0], 'r') as infile:
                grid, colors, code = parse_grid(infile, True)
                print (code)
        except IOError:
            print ('{}: error opening file'.format(arguments.code))
            sys.exit()

        if not colors is None:
            color_var, dir_vars, num_vars, clauses, reduce_time = sat_gen.reduce_to_sat(grid, colors)
            sol, _, repairs, solve_time = solve_sat(grid, colors, color_var, dir_vars, clauses)
            total_time = reduce_time + solve_time

            if isinstance(sol, list):
                result_char = 's'
            elif str(sol) == 'UNSAT':
                result_char = 'u'
            else:
                result_char = 'f'

            cur_stats = dict(repairs=repairs,
                                reduce_time=reduce_time,
                                solve_time=solve_time,
                                total_time=total_time,
                                num_vars=num_vars,
                                num_clauses=len(clauses),
                                count=1)

            if not result_char in stats:
                stats[result_char] = cur_stats
            else:
                for key in cur_stats.keys():
                    stats[result_char][key] += cur_stats[key]

                print ('{:>{}s} {} {:9,d} {:9,d} {:12,.3f} '\
                    '{:3d} {:12,.3f} {:12,.3f}'.format(
                        code, max_width, result_char,
                        num_vars, len(clauses), reduce_time,
                        repairs, solve_time, total_time))

    elif arguments.id:
        print('hello')

if __name__ == '__main__':
    pyflow_solver_main('')
