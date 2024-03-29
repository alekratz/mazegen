import random
from argparse import ArgumentParser
from .grid import *
from .maze import DepthFirst
from .solver import Solver
from .display import *


DISPLAY_HELP = {
    "stdout": "will print each step to STDOUT with line breaks.",
    "curses": "will use the curses library to print directly to the terminal.",
    "blt": "will attempt to open a bearlibterminal session and use that.",
}


def main():
    parser = ArgumentParser(description="Generate a maze.")
    parser.add_argument("width", metavar="W", type=int, help="the width of the maze.")
    parser.add_argument("height", metavar="H", type=int, help="the height of the maze.")
    parser.add_argument(
        "--seed", metavar="SEED", type=int, help="the random seed to use."
    )
    parser.add_argument(
        "--step",
        metavar="STEP",
        type=float,
        default=0.1,
        help="the time step between each draw.",
    )
    display_help = (
        "the display strategy to use. "
        + " ".join(["`{}` {}".format(k, v) for k, v in DISPLAY_HELP.items()])
        + " (default: %(default)s)"
    )
    parser.add_argument(
        "--display",
        metavar="DISPLAY",
        type=str,
        choices=DISPLAYS_AVAILABLE,  # set in displays/__init__.py
        default=DISPLAYS_AVAILABLE[-1],  # this uses the most desirable display
        help=display_help,
    )

    parser.add_argument(
        "--cycles",
        metavar="CYCLES",
        type=int,
        default=-1,
        help="the number of mazes to solve. If less than 0, it will generate and solve infinite "
             "mazes. (default: %(default)s)"
    )

    if "blt" in DISPLAYS_AVAILABLE:
        # add BLT-specific settings, but only when it's enabled
        parser.add_argument(
            "--blt-setting",
            metavar="SETTING",
            type=str,
            nargs="*",
            default=[],
            help="a list of bearlibterminal settings."
        )

    args = parser.parse_args()
    if args.seed:
        random.seed(args.seed)

    if args.display == "stdout":
        display = StdoutDisplay(sleep=args.step)
    elif args.display == "blt":
        display = BearLibTermDisplay(settings=args.blt_setting, sleep=args.step)
    elif args.display == "curses":
        display = CursesDisplay(sleep=args.step)
    else:
        assert False, "No display"

    count = 0
    cycles = args.cycles
    while count != cycles:
        count += 1
        grid = Grid(args.width, args.height)
        DepthFirst(grid).generate()
        solver = Solver(grid)
        try:
            display.loop(solver)
        except DisplayCloseError:
            break


if __name__ == "__main__":
    main()
