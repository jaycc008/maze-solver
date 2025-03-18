import time
from cell import Cell


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        self._break_entrance_and_exit()
    
    def _create_cells(self):
        self._cells = []
        for i in range(self._num_cols):
            col = []
            self._cells.append(col)
            for j in range(self._num_rows):
                cell = Cell(self._win)
                col.append(cell)
                self._draw_cell(i, j)


    def _draw_cell(self, i, j):
        x1 = self._x1 + i * self._cell_size_x
        x2 = self._x1 + (i + 1) * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        y2 = self._y1 + (j + 1) * self._cell_size_y
        self._cells[i][j].draw(x1, x2, y1, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.001)

    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        exit = self._cells[self._num_cols - 1][self._num_rows - 1]
        
        entrance.has_top_wall = False
        entrance.draw(
            entrance._x1,
            entrance._x2,
            entrance._y1,
            entrance._y2
        )

        exit.has_bottom_wall = False
        exit.draw(
            exit._x1,
            exit._x2,
            exit._y1,
            exit._y2
        )
