# board.py
'''Board module for the Reversi (Othello) game...'''
EMPTY = 0
BLACK = 1
WHITE = 2
BOARD_SIZE = 8
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]
class Board:
    def __init__(self):
        self.size = BOARD_SIZE
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        mid = self.size // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
        self.grid[mid][mid] = WHITE
    def in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size
    def get_cell(self, row, col):
        if not self.in_bounds(row, col):
            raise IndexError(...)
        return self.grid[row][col]
    def get_flippable_discs(self, player, row, col):
        if not self.in_bounds(row, col) or self.grid[row][col] != EMPTY:
            return []
        opponent = 3 - player  # works since BLACK=1, WHITE=2
        flippable = []
        for dr, dc in DIRECTIONS:
            line = []
            r, c = row + dr, col + dc
            while self.in_bounds(r, c) and self.grid[r][c] == opponent:
                line.append((r, c))
                r += dr
                c += dc
            if line and self.in_bounds(r, c) and self.grid[r][c] == player:
                flippable.extend(line)
        return flippable
    def is_valid_move(self, player, row, col):
        return bool(self.get_flippable_discs(player, row, col))
    def get_valid_moves(self, player):
        return [(r, c) for r in range(self.size) for c in range(self.size)
                if self.is_valid_move(player, r, c)]
    def place_disc(self, player, row, col):
        flippable = self.get_flippable_discs(player, row, col)
        if not flippable:
            raise ValueError("Invalid move")
        self.grid[row][col] = player
        for r, c in flippable:
            self.grid[r][c] = player
        return 1 + len(flippable)  # number of discs gained
    def get_score(self):
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return {BLACK: black, WHITE: white}
    def is_full(self):
        return all(cell != EMPTY for row in self.grid for cell in row)
    def has_valid_move(self, player):
        return bool(self.get_valid_moves(player))
    def is_game_over(self):
        if self.is_full():
            return True
        return not (self.has_valid_move(BLACK) or self.has_valid_move(WHITE))
    def copy(self):
        new_board = Board.__new__(Board)
        new_board.size = self.size
        new_board.grid = [row[:] for row in self.grid]
        return new_board
    def __str__(self):
        # text rendering
        ...