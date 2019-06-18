import abc
import time
from mazegen.grid import Grid
from mazegen.solver import Solver
from .base import *
from .exception import *

ALL = [
    'DISPLAYS_AVAILABLE',
    'StdoutDisplay',
    'Display',
    'DisplayCloseError',
]

DISPLAYS_AVAILABLE = ['stdout']
try:
    from .curses import *
    DISPLAYS_AVAILABLE += ['curses']
    ALL += ['CursesDisplay']
except ImportError:
    pass
try:
    from .bearlib import *
    DISPLAYS_AVAILABLE += ['blt']
    ALL += ['BearLibTermDisplay']
except ImportError:
    pass

__all__ = ALL


class StdoutDisplay(Display):
    def draw(self, solver: Solver):
        canvas = solver.grid.draw()
        x, y = solver.pos
        tx = x * 4 + 2
        ty = y * 2 + 1
        canvas[ty][tx] = "\u001b[36m" + self.guy + "\u001b[0m"
        # TODO more involved terminal commands that allow the maze to be drawn in the terminal
        # without newlines
        for row in canvas:
            print("".join(row))

