'''
board.py
Game-logic layer for the Minesweeper game.
Defines the cell-state constants (HIDDEN, REVEALED, FLAGGED) imported by
the GUI, the Cell class representing one grid square, and the Board class
implementing mine placement, reveal / flag / chord moves, flood-fill
opening of empty areas and win/loss detection.
'''
import random
# Cell states (imported by gui.py)
HIDDEN = "hidden"
REVEALED = "revealed"
FLAGGED = "flagged"
class Cell:
    '''One square of the Minesweeper grid.'''
    __slots__ = ("row", "col", "is_mine", "adjacent_mines", "state")
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.adjacent_mines = 0
        self.state = HIDDEN
class Board:
    '''Rows x cols grid of Cells; owns all game rules.'''
    def __init__(self, rows, cols, mines):
        if not 0 < mines < rows * cols:
            raise ValueError("invalid mine count for the board size")
        self.rows = rows
        self.cols = cols
        self.total_mines = mines
        self.cells = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.game_over = False
        self.won = False
        self.exploded_cell = None
        self._mines_placed = False
    # ------------------------------------------------------------ helpers
    def get_cell(self, row, col):
        '''Return the Cell at (row, col).'''
        return self.cells[row][col]
    def _neighbors(self, row, col):
        '''Yield the (up to 8) orthogonal/diagonal neighbours of a cell.'''
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    yield self.cells[r][c]
    def flags_placed(self):
        '''Number of cells currently flagged.'''
        return sum(1 for row in self.cells for cell in row
                   if cell.state == FLAGGED)
    # ------------------------------------------------------- mine set-up
    def _place_mines(self, safe_row, safe_col):
        '''Randomly place the mines on the first reveal, keeping the clicked
        cell (and, if possible, its whole neighbourhood) mine-free so the
        first click always opens an area.'''
        safe = {(safe_row, safe_col)}
        safe.update((n.row, n.col) for n in self._neighbors(safe_row, safe_col))
        candidates = [(r, c) for r in range(self.rows)
                      for c in range(self.cols) if (r, c) not in safe]
        if len(candidates) < self.total_mines:      # tiny-board fallback
            candidates = [(r, c) for r in range(self.rows)
                          for c in range(self.cols)
                          if (r, c) != (safe_row, safe_col)]
        random.shuffle(candidates)
        for r, c in candidates[:self.total_mines]:
            self.cells[r][c].is_mine = True
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.cells[r][c]
                cell.adjacent_mines = sum(n.is_mine
                                          for n in self._neighbors(r, c))
        self._mines_placed = True
    # -------------------------------------------------------------- moves
    def reveal(self, row, col):
        '''Reveal the cell at (row, col). Returns True if the board changed.
        Revealing a mine ends the game (lost); revealing a zero cell opens
        its neighbourhood by flood fill.'''
        if self.game_over:
            return False
        cell = self.get_cell(row, col)
        if cell.state != HIDDEN:
            return False
        if not self._mines_placed:
            self._place_mines(row, col)
        cell.state = REVEALED
        if cell.is_mine:
            self.game_over = True
            self.won = False
            self.exploded_cell = cell
            self._reveal_all_mines()
            return True
        if cell.adjacent_mines == 0:
            self._flood_reveal(cell)
        self._check_win()
        return True
    def _flood_reveal(self, start):
        '''Iteratively reveal the connected region of empty cells around
        `start` (including its numbered border cells).'''
        stack = [start]
        while stack:
            cell = stack.pop()
            for n in self._neighbors(cell.row, cell.col):
                if n.state == HIDDEN and not n.is_mine:
                    n.state = REVEALED
                    if n.adjacent_mines == 0:
                        stack.append(n)
    def _reveal_all_mines(self):
        '''On loss, uncover every still-hidden mine (correct flags stay).'''
        for row in self.cells:
            for cell in row:
                if cell.is_mine and cell.state == HIDDEN:
                    cell.state = REVEALED
    def toggle_flag(self, row, col):
        '''Flag / unflag a hidden cell. Returns True if the board changed.
        Flagging is refused on revealed cells.'''
        if self.game_over:
            return False
        cell = self.get_cell(row, col)
        if cell.state == REVEALED:
            return False
        cell.state = FLAGGED if cell.state == HIDDEN else HIDDEN
        return True
    def chord(self, row, col):
        '''"Chord" move on a revealed numbered cell: if the number of flags
        around it equals its mine count, reveal every other hidden
        neighbour. Returns True if the board changed.'''
        if self.game_over:
            return False
        cell = self.get_cell(row, col)
        if cell.state != REVEALED or cell.adjacent_mines == 0:
            return False
        neighbors = list(self._neighbors(row, col))
        flags = sum(1 for n in neighbors if n.state == FLAGGED)
        if flags != cell.adjacent_mines:
            return False
        changed = False
        for n in neighbors:
            if n.state == HIDDEN:
                if self.reveal(n.row, n.col):
                    changed = True
                if self.game_over:
                    break
        return changed
    # ---------------------------------------------------------- win check
    def _check_win(self):
        '''The game is won when the only unrevealed cells are the mines.'''
        unrevealed = sum(1 for row in self.cells for cell in row
                         if cell.state != REVEALED)
        if unrevealed == self.total_mines:
            self.game_over = True
            self.won = True
            for row in self.cells:          # tidy final board: flag mines
                for cell in row:
                    if cell.is_mine and cell.state != FLAGGED:
                        cell.state = FLAGGED