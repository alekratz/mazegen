from argparse import ArgumentParser
from .grid import *
from .maze import DepthFirst
from .solver import Solver


def main():
    parser = ArgumentParser(description='Generate a maze.')
    parser.add_argument('width', metavar='W', type=int, help='the width of the maze')
    parser.add_argument('height', metavar='H', type=int, help='the height of the maze')
    args = parser.parse_args()

    grid = Grid(args.width, args.height)
    DepthFirst(grid).generate()
    solver = Solver(grid)
    canvas = solver.draw()
    for row in canvas:
        print(''.join(row))


if __name__ == '__main__':
    main()
