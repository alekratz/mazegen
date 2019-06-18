import abc
import random
from .grid import *


class MazeGenerator(metaclass=abc.ABCMeta):
    """
    An abstract maze generator.
    """

    def __init__(self, grid: Grid):
        self._grid = grid

    @property
    def grid(self) -> Grid:
        return self._grid

    @abc.abstractmethod
    def generate(self):
        """
        Generates the maze.
        """


class DepthFirst(MazeGenerator):
    """
    A non-recursive depth-first maze generator.
    """

    def generate(self):
        visited = set()
        stack = [(0, 0)]

        while stack:
            x, y = pos = stack.pop()
            visited.add(pos)
            cell = self.grid.cells[y][x]
            neighbors = [(w, n) for w, n in cell.neighbors().items() if n.pos not in visited]
            if not neighbors:
                continue
            # choose a neighbor
            direction, chosen = random.choice(neighbors)
            cell.remove_wall(direction)
            stack.append(cell.pos)
            stack.append(chosen.pos)
