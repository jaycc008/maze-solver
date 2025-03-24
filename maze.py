import random
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
        seed = None
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
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        if seed is not None:
            random.seed(seed)
    
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
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            possible_directions = []
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                possible_directions.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                possible_directions.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                possible_directions.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                possible_directions.append((i, j + 1))

            if len(possible_directions) == 0:
                self._draw_cell(i, j)
                return
            
            dir_index = random.randrange(len(possible_directions))
            direction = possible_directions[dir_index]
            
            # left
            if direction[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
            # right
            if direction[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False
            # up
            if direction[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False
            # down
            if direction[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False
            
            self._break_walls_r(direction[0], direction[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            print("Maze solved!")
            return True
        
        # left
        if (
            i > 0 and
            not self._cells[i][j].has_left_wall and
            not self._cells[i - 1][j].has_right_wall and
            not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i - 1][j], True)

       # right
        if (
            i < self._num_cols - 1 and
            not self._cells[i][j].has_right_wall and
            not self._cells[i + 1][j].has_left_wall and
            not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # up
        if (
            j > 0 and
            not self._cells[i][j].has_top_wall and
            not self._cells[i][j - 1].has_bottom_wall and
            not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        # down
        if (
            j < self._num_rows - 1 and
            not self._cells[i][j].has_bottom_wall and
            not self._cells[i][j + 1].has_top_wall and
            not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], True)
        
        return False
        