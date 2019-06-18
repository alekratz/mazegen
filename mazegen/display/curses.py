import curses
from mazegen.grid import Grid
from mazegen.solver import Solver
from mazegen.display.base import Display
from mazegen.display.exception import DisplayCloseError

class CursesDisplay(Display):
    ##GUY = "\u001b[36m▪\u001b[0m"
    GUY = "▪"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.savetty()
        curses.noecho()
        curses.curs_set(0)
        self.last_pos = None

    def loop(self, solver: Solver):
        self.screen.clear()
        canvas = solver.grid.draw()
        for y, row in enumerate(canvas):
            self.screen.addstr(y, 0, "".join(row))
        super().loop(solver)

    def draw(self, solver: Solver):
        if self.last_pos:
            x, y = self.last_pos
            self.screen.addstr(y, x, " ")

        x, y = solver.pos
        tx = x * 4 + 2
        ty = y * 2 + 1
        self.screen.addstr(ty, tx, self.GUY, curses.color_pair(1))
        self.last_pos = (tx, ty)
        self.screen.refresh()

    def __del__(self):
        curses.resetty()
        curses.endwin()
