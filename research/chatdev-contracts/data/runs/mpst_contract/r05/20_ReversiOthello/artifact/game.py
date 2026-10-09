"""Game flow management for Reversi (Othello)."""

from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.current = Board.BLACK

    def switch_turn(self):
        self.current = 3 - self.current

    def over(self):
        """Game ends when the board is full or neither player has a valid move."""
        if self.board.is_full():
            return True
        return not (self.board.valid_moves(self.current)
                    or self.board.valid_moves(3 - self.current))

    def step(self, r, c):
        """Attempt a move for the current player; switch turns on success."""
        if self.board.apply_move(self.current, r, c):
            self.switch_turn()
            return True
        return False