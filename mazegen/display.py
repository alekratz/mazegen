import abc
import time
from bearlibterminal import terminal as blt
from .grid import Grid
from .solver import Solver


class DisplayCloseError(Exception):
    "An exception that is raised when the display is closed and should stop looping."


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
        time.sleep(duration)

    def update(self, solver: Solver):
        solver.step()

    @abc.abstractmethod
    def draw(self, solver: Solver):
        "Draws the given grid to this display"


class StdoutDisplay(Display):
    GUY = "\u001b[36m▪\u001b[0m"

    def draw(self, solver: Solver):
        canvas = solver.grid.draw()
        x, y = solver.pos
        tx = x * 4 + 2
        ty = y * 2 + 1
        canvas[ty][tx] = self.GUY
        # TODO more involved terminal commands that allow the maze to be drawn in the terminal
        # without newlines
        for row in canvas:
            print("".join(row))


class BearLibTermDisplay(Display):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert blt.open() != 0

    def loop(self, solver: Solver):
        w = solver.grid.canvas_width
        h = solver.grid.canvas_height
        settings = "window.size={}x{}".format(w, h)
        blt.set(settings)
        blt.clear()
        blt.refresh()
        super().loop(solver)

    def update(self, solver: Solver):
        while blt.has_input():
            key = blt.read()
            if key == blt.TK_ESCAPE:
                raise DisplayCloseError()

        super().update(solver)

    def delay(self, duration=None):
        duration = int((duration or self.sleep) * 1000)
        blt.delay(duration)

    def draw(self, solver: Solver):
        canvas = solver.grid.draw()
        x, y = solver.pos
        tx = x * 4 + 2
        ty = y * 2 + 1
        canvas[ty][tx] = "▪"

        for y, row in enumerate(canvas):
            for x, c in enumerate(row):
                if (x, y) == (tx, ty):
                    blt.color("cyan")
                blt.put(x, y, ord(c))
                if (x, y) == (tx, ty):
                    blt.color("white")
        blt.refresh()

    def __del__(self):
        blt.close()
