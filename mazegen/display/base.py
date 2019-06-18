import abc
import time
from mazegen.grid import Grid
from mazegen.solver import Solver


class Display(metaclass=abc.ABCMeta):
    def __init__(self, sleep=None):
        self.sleep = sleep or 0.1

    def loop(self, solver):
        "A basic blocking update loop"
        grid = solver.grid
        while not solver.is_done:
            self.draw(solver)
            self.update(solver)
            self.delay()
        self.draw(solver)

    def delay(self, duration=None):
        duration = duration or self.sleep
        try:
            time.sleep(duration)
        except KeyboardInterrupt:
            raise DisplayCloseError()

    def update(self, solver: Solver):
        solver.step()

    @abc.abstractmethod
    def draw(self, solver: Solver):
        "Draws the given grid to this display"
