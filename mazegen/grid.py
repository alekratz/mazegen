from enum import Enum, auto

__all__ = ("Grid", "Wall")


HORZ = "─"
VERT = "│"
SPLIT_RIGHT = "├"
SPLIT_LEFT = "┤"
SPLIT = "┼"
SPLIT_UP = "┴"
SPLIT_DOWN = "┬"
UP_LEFT = "┌"
UP_RIGHT = "┐"
DOWN_LEFT = "└"
DOWN_RIGHT = "┘"
CAP_NORTH = "╵"
CAP_EAST = "╶"
CAP_WEST = "╴"
CAP_SOUTH = "╷"

WALL_CHARS = {
    # No walls
    (False, False, False, False): " ",
    # Vertical end cap, north
    (True, False, False, False): "╵",
    # Horizontal end cap, east
    (False, True, False, False): "╶",
    # Bottom-left corner
    (True, True, False, False): "└",
    # Horizontal end cap, west
    (False, False, True, False): "╴",
    # Bottom-right corner
    (True, False, True, False): "┘",
    # Horizontal line
    (False, True, True, False): "─",
    # Upwards 'T' junction
    (True, True, True, False): "┴",
    # Vertical end cap, south
    (False, False, False, True): "╷",
    # Vertical line
    (True, False, False, True): "│",
    # Upper-left corner
    (False, True, False, True): "┌",
    # Right-facing 'T' junction
    (True, True, False, True): "├",
    # Upper-right corner
    (False, False, True, True): "┐",
    # Left-facing 'T' junction
    (True, False, True, True): "┤",
    # Downwards 'T' junction
    (False, True, True, True): "┬",
    # Full intersection
    (True, True, True, True): "┼",
}

NW_CORNER = {
    (False, False): " ",
    (True, False): CAP_EAST,
    (False, True): CAP_SOUTH,
    (True, True): UP_LEFT,
}


NE_CORNER = {
    (False, False): " ",
    (True, False): CAP_WEST,
    (False, True): CAP_SOUTH,
    (True, True): UP_RIGHT,
}

SW_CORNER = {
    (False, False): " ",
    (True, False): CAP_EAST,
    (False, True): CAP_NORTH,
    (True, True): DOWN_LEFT,
}

SE_CORNER = {
    (False, False): " ",
    (True, False): CAP_WEST,
    (False, True): CAP_NORTH,
    (True, True): DOWN_RIGHT,
}


class Wall(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()

    def opposite(self):
        if self is Wall.NORTH:
            return Wall.SOUTH
        elif self is Wall.EAST:
            return Wall.WEST
        elif self is Wall.SOUTH:
            return Wall.NORTH
        elif self is Wall.WEST:
            return Wall.EAST
        assert False


class Cell:
    def __init__(self, x: int, y: int, grid, walls=None):
        self._x = x
        self._y = y
        self._grid = grid
        self._walls = walls or set()

    @property
    def grid(self):
        return self._grid

    @property
    def cells(self):
        return self.grid.cells

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def pos(self):
        "Position of this cell as an (X, Y) tuple"
        return (self.x, self.y)

    @property
    def walls(self):
        return self._walls

    def neighbor(self, wall: Wall):
        if wall == Wall.NORTH and self.y > 0:
            return self.cells[self.y - 1][self.x]
        elif wall == Wall.EAST and self.x < self.grid.width - 1:
            return self.cells[self.y][self.x + 1]
        elif wall == Wall.SOUTH and self.y < self.grid.height - 1:
            return self.cells[self.y + 1][self.x]
        elif wall == Wall.WEST and self.x > 0:
            return self.cells[self.y][self.x - 1]
        else:
            return None

    def neighbors(self):
        return dict(
            list(
                filter(lambda t: bool(t[1]), map(lambda w: (w, self.neighbor(w)), Wall))
            )
        )

    def add_wall(self, wall: Wall):
        self.walls.add(wall)
        if wall == Wall.NORTH and self.y > 0:
            self.cells[self.y - 1][self.x].walls.add(wall.SOUTH)
        elif wall == Wall.SOUTH and self.y < len(self.cells) - 1:
            self.cells[self.y + 1][self.x].walls.add(wall.NORTH)
        elif wall == Wall.EAST and self.x < len(self.cells[0]) - 1:
            self.cells[self.y][self.x + 1].walls.add(wall.WEST)
        elif wall == Wall.WEST and self.x > 0:
            self.cells[self.y][self.x - 1].walls.add(wall.EAST)
        assert False

    def remove_wall(self, wall: Wall):
        self.walls.remove(wall)
        if wall == Wall.NORTH and self.y > 0:
            self.cells[self.y - 1][self.x].walls.remove(wall.SOUTH)
        elif wall == Wall.SOUTH and self.y < len(self.cells) - 1:
            self.cells[self.y + 1][self.x].walls.remove(wall.NORTH)
        elif wall == Wall.EAST and self.x < len(self.cells[0]) - 1:
            self.cells[self.y][self.x + 1].walls.remove(wall.WEST)
        elif wall == Wall.WEST and self.x > 0:
            self.cells[self.y][self.x - 1].walls.remove(wall.EAST)


class Grid:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        cells = [
            [Cell(x, y, self, set(Wall)) for x in range(width)] for y in range(height)
        ]
        self._cells = cells

    @property
    def cells(self):
        return self._cells

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def canvas_width(self) -> int:
        return self.width * 4 + 1

    @property
    def canvas_height(self) -> int:
        return self.height * 2 + 1

    def draw(self):
        global WALL_CHARS
        cwidth = self.canvas_width
        cheight = self.canvas_height
        canvas = [[" " for _ in range(cwidth)] for _ in range(cheight)]

        # Upper-left framing
        for y in range(self.height):
            ty = y * 2 + 1
            cell = self.cells[y][0]
            if Wall.WEST in cell.walls:
                canvas[ty][0] = VERT
        for x in range(self.width):
            tx = x * 4 + 2
            cell = self.cells[0][x]
            if Wall.NORTH in cell.walls:
                canvas[0][tx - 1] = HORZ
                canvas[0][tx] = HORZ
                canvas[0][tx + 1] = HORZ

        # This gives us something that looks like this (sans the numbers):
        #  ─── ───
        # │ 1 │ 2 │
        #  ─── ───
        # │ 3 │ 4 │
        #  ─── ───
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                tx = x * 4 + 2
                ty = y * 2 + 1
                if Wall.EAST in cell.walls:
                    canvas[ty][tx + 2] = VERT
                if Wall.SOUTH in cell.walls:
                    canvas[ty + 1][tx - 1] = HORZ
                    canvas[ty + 1][tx] = HORZ
                    canvas[ty + 1][tx + 1] = HORZ

        # This part fills in the cracks of the above, except at the corners and sides.
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                tx = x * 4 + 2
                ty = y * 2 + 1
                # Cells 1, 2, 3, and 4 are the same as their labels above.
                cell1, cell2, cell3, cell4 = (
                    self.cells[y][x],
                    self.cells[y][x + 1],
                    self.cells[y + 1][x],
                    self.cells[y + 1][x + 1],
                )
                walls = (
                    Wall.EAST in cell1.walls,
                    Wall.SOUTH in cell2.walls,
                    Wall.NORTH in cell3.walls,
                    Wall.WEST in cell4.walls,
                )
                char = WALL_CHARS[walls]
                canvas[ty + 1][tx + 2] = char

        # Fill in the sides
        for y in range(self.height - 1):
            ty = y * 2 + 1
            cell1, cell2, cell3, cell4 = (
                self.cells[y][self.width - 1],
                self.cells[y][0],
                self.cells[y + 1][self.width - 1],
                self.cells[y + 1][0],
            )
            walls = (True, Wall.SOUTH in cell2.walls, False, Wall.WEST in cell4.walls)
            char = WALL_CHARS[walls]
            canvas[ty + 1][0] = char

            walls = (Wall.EAST in cell1.walls, False, Wall.NORTH in cell3.walls, True)
            char = WALL_CHARS[walls]
            canvas[ty + 1][cwidth - 1] = char

        for x in range(self.width - 1):
            tx = x * 4 + 2
            cell1, cell2, cell3, cell4 = (
                self.cells[self.height - 1][x],
                self.cells[self.height - 1][x + 1],
                self.cells[0][x],
                self.cells[0][x + 1],
            )
            walls = (Wall.EAST in cell1.walls, Wall.SOUTH in cell2.walls, True, False)
            char = WALL_CHARS[walls]
            canvas[cheight - 1][tx + 2] = char

            walls = (False, True, Wall.NORTH in cell3.walls, Wall.WEST in cell4.walls)
            char = WALL_CHARS[walls]
            canvas[0][tx + 2] = char

        # Corners
        nw, ne, sw, se = (
            self.cells[0][0],
            self.cells[0][self.width - 1],
            self.cells[self.height - 1][0],
            self.cells[self.height - 1][self.width - 1],
        )
        nw_walls = (Wall.NORTH in nw.walls, Wall.WEST in nw.walls)
        ne_walls = (Wall.NORTH in ne.walls, Wall.EAST in ne.walls)
        sw_walls = (Wall.SOUTH in sw.walls, Wall.WEST in sw.walls)
        se_walls = (Wall.SOUTH in se.walls, Wall.EAST in se.walls)

        canvas[0][0] = NW_CORNER[nw_walls]
        canvas[0][cwidth - 1] = NE_CORNER[ne_walls]
        canvas[cheight - 1][0] = SW_CORNER[sw_walls]
        canvas[cheight - 1][cwidth - 1] = SE_CORNER[se_walls]

        return canvas
