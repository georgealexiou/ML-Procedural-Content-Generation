import itertools
from datetime import datetime
import pycosat
import sys

import sat_gen
import helper

''' Generate output for terminal '''
def output(colors, parsed):
    color_chars = [None]*len(colors)
    for char, color in colors.items():
        color_chars[color] = char

    # assign the correct letter to each color for output
    for row in parsed:
        for (color, pos_count) in row:
            assert color >= 0 and color < len(colors)
            color_char = color_chars[color]

            if pos_count == -1:
                    display_char = color_char
            else:
                display_char = sat_gen.PATH[pos_count]

                #print row
                sys.stdout.write('\033[0m')
            sys.stdout.write(display_char)
        sys.stdout.write('\033[0m\n')

'''Take decoded sat solution and parse it into a grid'''
def parse_solution(grid, colors, get_colors, dir_vars, solution_sat):

    solution_sat = set(solution_sat)
    num_colors = len(colors)

    parsed = []

    for i, row in enumerate(grid):
        decoded_row = []
        for j, char in enumerate(row):

            cell_color = -1

            for color in range(num_colors):
                if get_colors(i, j, color) in solution_sat:
                    assert cell_color == -1
                    cell_color = color

            assert cell_color != -1

            cell_pos_count = -1

            if not char.isalnum():
                for pos_count, dir_var in dir_vars[i, j].items():
                    if dir_var in solution_sat:
                        assert cell_pos_count == -1
                        cell_pos_count = pos_count

                assert cell_pos_count != -1

            decoded_row.append((cell_color, cell_pos_count))

        parsed.append(decoded_row)

    return parsed

def draw_flow(parsed, visited_nodes, x, y):

    flow = []
    is_cycle = False
    last_n, last_e = -1, -1

    while True:
        advanced = False
        color, pos_count = parsed[x][y]
        visited_nodes[x][y] = 1
        flow.append((x, y))

        for pos, var_n, var_e in sat_gen.colorable_adjacent(len(parsed), x, y):

            if (var_n, var_e) == (last_n, last_e):
                continue

            n_color, n_pos_count = parsed[var_n][var_e]

            #There is a cycle if we determine a loop (larger path variable connects to smaller)
            if ((pos_count >= 0 and (pos_count & pos)) or (pos_count == -1 and n_pos_count >= 0 and n_pos_count & sat_gen.SWAP[pos])):
                assert color == n_color
                if visited_nodes[var_n][var_e]:
                    is_cycle = True
                else:
                    last_n, last_e = x, y
                    x, y = var_n, var_e
                    advanced = True

                break

        if not advanced:
            break

    return flow, is_cycle

''' In this stage we remove all the cycles from our grid '''
def post_process(parsed, pos_vars):

    visited_colors = set()
    parsed_size = range(len(parsed))
    visited_nodes = [[0]*len(parsed) for _ in parsed_size]
    restrictions = []

    # start from each endpoint and visit all nodes in the flows
    # determine which nodes form a cycle by finding which nodes have not been visited
    for i, j, (color, pos_count) in helper.flatten(parsed):

        if pos_count == -1 and color not in visited_colors:
            assert not visited_nodes[i][j]
            visited_colors.add(color)
            flow, is_cycle = draw_flow(parsed, visited_nodes, i, j)
            assert not is_cycle
    

    for i, j in itertools.product(parsed_size, parsed_size):

        if not visited_nodes[i][j]:
            flow, is_cycle = draw_flow(parsed, visited_nodes, i, j)
            assert is_cycle
            clause = []

            # create new restricted cnf where these clauses are not allowed to form a cycle
            for cycle_a, cycle_b in flow:
                _, pos_count = parsed[cycle_a][cycle_b]
                dir_var = pos_vars[cycle_a, cycle_b][pos_count]
                clause.append(-dir_var)

            restrictions.append(clause)

def solve_sat(grid, colors, get_colors, dir_vars, clauses):
    start = datetime.now()

    parsed = None
    all_decoded = []
    repairs = 0

    while True:
        solution_sat = pycosat.solve(clauses)

        if not isinstance(solution_sat, list):
            parsed = None
            all_decoded.append(parsed)
            break

        parsed = parse_solution(grid, colors, get_colors, dir_vars, solution_sat)
        all_decoded.append(parsed)

        restrictions = post_process(parsed, dir_vars)

        if not restrictions:
            break

        clauses += restrictions
        repairs += 1

    solve_time = (datetime.now() - start).total_seconds()
    return solution_sat, parsed, repairs, solve_time