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

PATH_REPRESENTATION = {
    LR: '─',
    TB: '│',
    TL: '┘',
    TR: '└',
    BL: '┐',
    BR: '┌'
    }

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

    do_color = False

    for char, color in colors.items():
        color_chars[color] = char

    for decoded_row in decoded:
        for (color, dir_type) in decoded_row:

            assert color >= 0 and color < len(colors)

            color_char = color_chars[color]

            if dir_type == -1:
                    display_char = color_char
            else:
                display_char = PATH_REPRESENTATION[dir_type]

                sys.stdout.write('\033[0m')

            sys.stdout.write(display_char)

        sys.stdout.write('\033[0m')

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

    return sol, decoded, repairs, solve_time

######################################################################

def get_data(code):
    size = helper.get_grid_size(code)
    print (size)

    grid, colors, code = helper.parse_grid(code, False, size)

    if(grid == None):
        print('Invalid Code')
    
    else:
        color_var, dir_vars, num_vars, clauses, reduce_time = sat_gen.reduce_to_sat(grid, colors)
        sol, decoded, repairs, solve_time = solve_sat(grid, colors, color_var, dir_vars, clauses)
        total_time = reduce_time + solve_time

        print ('{}     {}     {}     {}     {}     {}     {}     {}'.format(code, size, num_vars, len(clauses), reduce_time, repairs, solve_time, total_time))
        show_solution(colors, decoded)
        #eturn code, size, num_vars, len(clauses), repairs, solve_time, total_time, sol, decoded

'''Main loop if module run as script.'''
def pyflow_solver_main():

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

    stats = dict()

    if not arguments.file and not arguments.id and code == '':
        print ('-f -i: Error invalid selection')

    elif arguments.file and arguments.id:
        print ('-f -i: Error invalid selection')
    
    elif arguments.file:
        # open file
        try:
            with open(arguments.code[0], 'r') as infile:
                grid, colors, code = helper.parse_grid(infile, True, 0)
        except IOError:
            print ('{}: error opening file'.format(arguments.code))
            sys.exit()

        if not colors is None:
            color_var, dir_vars, num_vars, clauses, reduce_time = sat_gen.reduce_to_sat(grid, colors)
            sol, decoded, repairs, solve_time = solve_sat(grid, colors, color_var, dir_vars, clauses)
            total_time = reduce_time + solve_time

            print ('{}     {}     {}     {}     {}     {}     {}'.format(code, num_vars, len(clauses), reduce_time, repairs, solve_time, total_time))
            show_solution(colors, decoded)


if __name__ == '__main__':
    get_data('4o1i9l6a11eb5g5e20j2g26n9f1f9l7h1o7n10j7c6pd3mc4h5p6im3kad23b2k1')
