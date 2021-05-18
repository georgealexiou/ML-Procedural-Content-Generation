import solver
from argparse import ArgumentParser
import helper
import sat_gen
import sys

def get_data(code):
    size = helper.get_grid_size(code)

    grid, colors, code = helper.parse_grid(code, False, size)

    if(grid == None):
        print('Invalid Code')
    
    else:
        var_calc, pos_vars, num_vars, clauses, reduce_time = sat_gen.cnf(grid, colors)
        solution, parsed, cycles_fixed, solve_time = solver.solve_sat(grid, colors, var_calc, pos_vars, clauses)
        total_time = reduce_time + solve_time

        print('Variable Count: {}'.format(num_vars))
        print('Clause Count: {}'.format(len(clauses)))
        print('Reduce Time: {}'.format(reduce_time))
        print('Solve Time: {}'.format(solve_time))
        print('Total Time: {}'.format(total_time))
        solver.output(colors, parsed)

def pysat():

    parser = ArgumentParser(description='SAT Solver')
    parser.add_argument('code', metavar='grid', nargs='*', help='filename or code')

    parser.add_argument('-f', dest='file', default=False,
                        action='store_true',
                        help='read file')

    parser.add_argument('-i', dest='id', default=False,
                        action='store_true',
                        help='read id')

    arguments = parser.parse_args()

    if not arguments.file and not arguments.id and code == '':
        print ('-f -i: Error invalid selection')

    elif arguments.file and arguments.id:
        print ('-f -i: Error invalid selection')

    elif arguments.id:
        get_data(arguments.code[0])
    
    elif arguments.file:
        try:
            with open(arguments.code[0], 'r') as infile:
                grid, colors, code = helper.parse_grid(infile, True, 0)
        except IOError:
            print ('Could not open file')
            sys.exit()

        if not colors is None:
            var_calc, pos_vars, num_vars, clauses, reduce_time = sat_gen.cnf(grid, colors)
            _, parsed, _, solve_time = solver.solve_sat(grid, colors, var_calc, pos_vars, clauses)
            total_time = reduce_time + solve_time

            print('Variable Count: {}'.format(num_vars))
            print('Clause Count: {}'.format(len(clauses)))
            print('Reduce Time: {}'.format(reduce_time))
            print('Solve Time: {}'.format(solve_time))
            print('Total Time: {}'.format(total_time))
            
            if(parsed == None):
                print('Cannot be solved')
            else:
                solver.output(colors, parsed)


if __name__ == '__main__':
    pysat()
