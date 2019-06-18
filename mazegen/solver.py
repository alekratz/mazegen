import random
from typing import Optional
from .grid import *


class Solver:
    def __init__(self, grid: Grid):
        self._grid = grid
        self._backtrack = []
        self._pos = (0, 0)
        self._dir = None
        self._backtracking = False

        self._branches = {
            self._pos: set(self.valid_cells().keys()),
        }

        # Add entrance and exit
        self.grid.cells[0][0].remove_wall(Wall.NORTH)
        self.grid.cells[self.grid.height - 1][self.grid.width - 1].remove_wall(
            Wall.EAST
        )

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

    def valid_cells(self):
        "Gets the cells that are available to move into."
        cell = self.cell
        return {w: n for w, n in self.cell.neighbors().items() if w not in cell.walls}

    def move(self, wall: Wall):
        assert wall in self.valid_cells()
        x, y = self.pos
        if wall == Wall.NORTH:
            y -= 1
        elif wall == Wall.SOUTH:
            y += 1
        elif wall == Wall.EAST:
            x += 1
        elif wall == Wall.WEST:
            x -= 1
        else:
            assert False
        # Add this motion to the backtrack list
        self._backtrack.append(self.pos)
        self._pos = (x, y)

    def step(self):
        if self.is_done:
            return

        valid_cells = self.valid_cells()
        # Register this branch if there are multiple targets to go to
        if len(valid_cells) > 1 and self.pos not in self._branches:
            self._branches[self.pos] = set(valid_cells.keys())
            # Also, if we have backtrack positions available, disable the cell that we just came
            # from.
            if self._backtrack:
                x1, y1 = self.pos
                x2, y2 = self._backtrack[-1]
                diff = (x2 - x1, y2 - y1)
                if diff == (-1, 0):
                    wall = Wall.WEST
                elif diff == (1, 0):
                    wall = Wall.EAST
                elif diff == (0, -1):
                    wall = Wall.NORTH
                elif diff == (0, 1):
                    wall = Wall.SOUTH
                else:
                    assert False
                self._branches[self.pos].remove(wall)

        if self.pos in self._branches and self._branches[self.pos]:
            # Choose a direction to move if we're at a branch
            self._backtracking = False
            self._dir = random.choice(list(self._branches[self.pos]))
            self._branches[self.pos].remove(self._dir)

        if self.backtracking:
            # Set up for backtracking, but there's no backtrack left.
            if not self._backtrack:
                self._backtracking = False
                self.step()
            else:
                self._pos = self._backtrack.pop()
        else:
            if self._dir not in valid_cells:
                # Can't move this direction, try these options in this order:
                # * Choose a random direction on this branch if we are on a branch,
                # * Start backtracking
                if self.pos in self._branches and self._branches[self.pos]:
                    self._dir = random.choice(list(self._branches[self.pos]))
                    self._branches[self.pos].remove(self._dir)
                else:
                    self._backtracking = True
                    # TODO : prevent stack overflow where we have no backtrack available
                    assert self._backtrack
                    self.step()
                    return
            self.move(self._dir)
