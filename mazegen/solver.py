from typing import Optional
from .grid import *


class Solver:
    def __init__(self, grid: Grid):
        self._grid = grid
        self._backtrack = []
        self._branches = {}
        self._pos = (0, 0)
        self._dir = None
        self._backtracking = False

        # Add entrance and exit
        self.grid.cells[0][0].remove_wall(Wall.NORTH)
        self.grid.cells[self.grid.height - 1][self.grid.width - 1].remove_wall(Wall.EAST)

    @property
    def is_done(self) -> bool:
        return self.goal == self.pos

    @property
    def goal(self):
        return (self.grid.width - 1, self.grid.height - 1)

    @property
    def grid(self):
        return self._grid

    @property
    def pos(self):
        return self._pos

    @property
    def cell(self):
        x, y = self.pos
        return self.grid.cells[y][x]

    @property
    def backtracking(self) -> bool:
        return self._backtracking

    def draw(self):
        canvas = self.grid.draw()

        # draw our lil guy here
        guy = '\u001b[36m■\u001b[0m'
        x, y = self.pos
        tx = x * 4 + 2
        ty = y * 2 + 1
        canvas[ty][tx] = guy

        return canvas

    def valid_cells(self):
        "Gets the cells that are available to move into."
        return {
            w: n for w, n in self.cell.neighbors().items()
            if w not in n.walls
        }

    def step(self):
        if self.is_done:
            return

        if self.backtracking:
            if not self._backtrack:
                self._backtracking = False
                
        else:
            valid_cells = self.valid_cells()
            if self._dir is None:
                self._dir = random.choice(valid_cells.keys())

            if self._dir not in valid_cells:
                # choose a random cell that's not already visited, or start backtracking
                pass
