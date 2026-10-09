'''
Core Minesweeper game logic: cells, board generation, revealing, flagging, win/lose detection.
'''
import random
class Cell:
    '''Represents a single cell on the Minesweeper board.'''
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
    def can_reveal(self):
        return not self.is_revealed and not self.is_flagged
    def can_flag(self):
        return not self.is_revealed
class MinesweeperBoard:
    '''Holds the grid of cells and implements the game rules.'''
    def __init__(self, rows, cols, num_mines):
        if num_mines >= rows * cols:
            raise ValueError("Too many mines for board size")
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.mines_placed = False
        self.game_over = False
        self.won = False
        self.exploded_at = None  # (row, col) of the mine that lost the game
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
    def get_neighbors(self, row, col):
        '''Yield (row, col) of all 8 adjacent cells within bounds.'''
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.in_bounds(r, c):
                    yield r, c
    def place_mines(self, safe_row, safe_col):
        '''Randomly place mines, keeping the first-clicked cell and its neighbors mine-free.'''
        safe_cells = {(safe_row, safe_col)} | set(self.get_neighbors(safe_row, safe_col))
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        candidates = [pos for pos in all_positions if pos not in safe_cells]
        # If board is too small to fully avoid safe area, fall back to excluding only the clicked cell
        if len(candidates) < self.num_mines:
            candidates = [pos for pos in all_positions if pos != (safe_row, safe_col)]
        mines = random.sample(candidates, self.num_mines)
        for r, c in mines:
            self.grid[r][c].is_mine = True
        self._calculate_adjacent_counts()
        self.mines_placed = True
    def _calculate_adjacent_counts(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.grid[r][c].is_mine:
                    self.grid[r][c].adjacent_mines = sum(
                        1 for nr, nc in self.get_neighbors(r, c) if self.grid[nr][nc].is_mine
                    )
    def reveal(self, row, col):
        '''
        Reveal the cell at (row, col).
        Returns list of (row, col) revealed by this action.
        '''
        if self.game_over:
            return []
        cell = self.grid[row][col]
        if cell.is_revealed or cell.is_flagged:
            return []
        if not self.mines_placed:
            self.place_mines(row, col)
        if cell.is_mine:
            cell.is_revealed = True
            self.exploded_at = (row, col)
            self.game_over = True
            self.won = False
            return [(row, col)]
        revealed = self._flood_reveal(row, col)
        if self.check_win():
            self.game_over = True
            self.won = True
        return revealed
    def _flood_reveal(self, row, col):
        '''Iteratively reveal cells starting from (row, col), expanding through zero-count cells.'''
        revealed = []
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            cell = self.grid[r][c]
            if cell.is_revealed or cell.is_flagged or cell.is_mine:
                continue
            cell.is_revealed = True
            revealed.append((r, c))
            if cell.adjacent_mines == 0:
                for nr, nc in self.get_neighbors(r, c):
                    ncell = self.grid[nr][nc]
                    if not ncell.is_revealed and not ncell.is_flagged and not ncell.is_mine:
                        stack.append((nr, nc))
        return revealed
    def toggle_flag(self, row, col):
        '''Flag/unflag a covered cell. Returns True if the flag state changed.'''
        if self.game_over:
            return False
        cell = self.grid[row][col]
        if cell.is_revealed:
            return False
        cell.is_flagged = not cell.is_flagged
        return True
    def count_flags(self):
        return sum(1 for row in self.grid for cell in row if cell.is_flagged)
    def check_win(self):
        '''Win when every non-mine cell is revealed.'''
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
    def reveal_all_mines(self):
        '''Mark all mines as revealed (used when the game is lost).'''
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    cell.is_revealed = True
    def flag_all_mines(self):
        '''Flag every mine (used when the game is won so the board looks complete).'''
        for row in self.grid:
            for cell in row:
                if cell.is_mine and not cell.is_flagged:
                    cell.is_flagged = True