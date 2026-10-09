'''
game.py
This module defines the GomokuGame class, which manages the overall game
flow: turn alternation, move processing, win/draw detection, and restarts.
'''
from board import Board
from player import Player
class GomokuGame:
    """Manages the state and flow of a Gomoku game between two players."""
    STATE_ONGOING = "ongoing"
    STATE_WON = "won"
    STATE_DRAW = "draw"
    def __init__(self, player1=None, player2=None, board_size=15):
        self.board = Board(board_size)
        self.player1 = player1 if player1 else Player("Player 1", Board.BLACK)
        self.player2 = player2 if player2 else Player("Player 2", Board.WHITE)
        self.current_player = self.player1  # Black always moves first
        self.state = self.STATE_ONGOING
        self.winner = None
        self.winning_line = None
    def reset(self):
        """Reset the game to its initial state."""
        self.board.reset()
        self.current_player = self.player1
        self.state = self.STATE_ONGOING
        self.winner = None
        self.winning_line = None
    def get_current_player(self):
        return self.current_player
    def switch_turn(self):
        """Switch the turn to the other player."""
        self.current_player = (self.player2 if self.current_player is self.player1
                               else self.player1)
    def make_move(self, row, col):
        """Attempt to place the current player's stone at (row, col).
        Returns True if the move was valid and processed."""
        if self.state != self.STATE_ONGOING:
            return False
        if not self.board.place_stone(row, col, self.current_player.stone):
            return False
        if self.board.check_win(row, col):
            self.state = self.STATE_WON
            self.winner = self.current_player
            self.winning_line = self._find_winning_line(row, col)
            return True
        if self.board.is_full():
            self.state = self.STATE_DRAW
            return True
        self.switch_turn()
        return True
    def _find_winning_line(self, row, col):
        """Return the list of (row, col) tuples forming the winning five
        in a row through (row, col), or None if not found."""
        stone = self.board.grid[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            cells = [(row, col)]
            r, c = row + dr, col + dc
            while self.board.is_in_bounds(r, c) and self.board.grid[r][c] == stone:
                cells.append((r, c))
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while self.board.is_in_bounds(r, c) and self.board.grid[r][c] == stone:
                cells.append((r, c))
                r -= dr
                c -= dc
            if len(cells) >= 5:
                # Return exactly five consecutive cells containing the last move
                cells.sort(key=lambda cell: (cell[0] - row) * dr + (cell[1] - col) * dc)
                idx = cells.index((row, col))
                start = max(0, min(idx, len(cells) - 5))
                return cells[start:start + 5]
        return None