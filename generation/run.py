import os
from argparse import ArgumentParser
import timeit
import subprocess
import time
from generator import grid

print('Welcome to Numberlink')


def pyflow_main():

    parser = ArgumentParser(
        description='Solve Flow Free grids via reduction to SAT')
    parser.add_argument('size', metavar='N', type = int, nargs='*')

    parser.add_argument('-f', dest='file', default=False,
                        action='store_true',
                        help='quiet mode (reduce output)')
    
    parser.add_argument('-d', dest='display', default=False,
                        action='store_true',
                        help='quiet mode (reduce output)')
                            
    parser.add_argument('-s', dest='solve', default=False,
                        action='store_true',
                        help='quiet mode (reduce output)')

    arguments = parser.parse_args()

    if not len(arguments.size) > 0:
        print("Incorrect size")

    if arguments.display:
        start = timeit.timeit()
        print("Generated {}x{}".format(arguments.size[0], arguments.size[0]))
        
        # try:
        #     os.system("python3.8 gen.py {} {} 1".format(arguments.size[0], arguments.size[0]))
        # except:
        os.system("python3.8 generator/grid.py 6".format(arguments.size[0]))
            
        end = timeit.timeit()
        print("Generation Time: {}".format(abs(end - start)))

    if arguments.solve:
        print('What is the filename that ur puzzle is stored in?')
        name = str(input())
        os.system("python3.8 solver/run_solver.py -f {}".format(name))


if __name__ == '__main__':
    pyflow_main()
