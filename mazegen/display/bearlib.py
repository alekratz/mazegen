from bearlibterminal import terminal as blt
from mazegen.grid import Grid
from mazegen.solver import Solver
from mazegen.display.base import Display
from mazegen.display.exception import DisplayCloseError


__all__ = ('BearLibTermDisplay',)


class BearLibTermDisplay(Display):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert blt.open() != 0
        self.last_pos = None

    def loop(self, solver: Solver):
        w = solver.grid.canvas_width
        h = solver.grid.canvas_height
        settings = "window.size={}x{}".format(w, h)
        blt.set(settings)
        blt.clear()
        blt.refresh()

        canvas = solver.grid.draw()
        for y, row in enumerate(canvas):
            for x, c in enumerate(row):
                blt.put(x, y, ord(c))
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
        if self.last_pos:
            x, y = self.last_pos
            blt.put(x, y, " ")

        x, y = solver.pos
        tx = x * 4 + 2
        ty = y * 2 + 1
        blt.color("cyan")
        blt.put(tx, ty, "▪")
        blt.color("white")
        self.last_pos = (tx, ty)
        blt.refresh()

    def __del__(self):
        blt.close()
