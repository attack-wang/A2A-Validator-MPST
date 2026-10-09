'''
Game logic module for the Tic-Tac-Toe game.
Implements the core rules independent of any GUI: a 3x3 board that
tracks X/O placements, turn alternation, move history, win detection
(rows, columns, diagonals), draw detection, and the game state machine.
'''
class Board:
    """Represents the 3x3 tic-tac-toe grid and the marks placed on it."""
    EMPTY = " "
    SIZE = 3
    def __init__(self):
        """Create an empty 3x3 grid."""
        self.grid = [[self.EMPTY for _ in range(self.SIZE)]
                     for _ in range(self.SIZE)]
    def reset(self):
        """Clear every cell so a fresh round can start."""
        self.grid = [[self.EMPTY for _ in range(self.SIZE)]
                     for _ in range(self.SIZE)]
    def is_valid_move(self, row, col):
        """Return True if (row, col) is inside the grid and still empty."""
        return (0 <= row < self.SIZE and 0 <= col < self.SIZE
                and self.grid[row][col] == self.EMPTY)
    def place_mark(self, row, col, player):
        """Place the player's mark on the board. Returns True on success."""
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = player
        return True
    def is_full(self):
        """Return True when no empty cell remains (draw condition)."""
        return all(self.grid[r][c] != self.EMPTY
                   for r in range(self.SIZE) for c in range(self.SIZE))
    def check_winner(self):
        """
        Detect three identical marks in a row, column or diagonal.
        Returns (winner_symbol, winning_line) if a player has won,
        otherwise (None, None). winning_line is a list of (row, col)
        coordinates used by the GUI for highlighting.
        """
        lines = []
        lines += [[(r, c) for c in range(self.SIZE)] for r in range(self.SIZE)]
        lines += [[(r, c) for r in range(self.SIZE)] for c in range(self.SIZE)]
        lines.append([(i, i) for i in range(self.SIZE)])
        lines.append([(i, self.SIZE - 1 - i) for i in range(self.SIZE)])
        for line in lines:
            symbols = [self.grid[r][c] for r, c in line]
            if symbols[0] != self.EMPTY and symbols[0] == symbols[1] == symbols[2]:
                return symbols[0], line
        return None, None
class Game:
    """Manages game flow: turns, moves, state machine and move history."""
    STATE_PLAYING = "playing"
    STATE_WON = "won"
    STATE_DRAW = "draw"
    def __init__(self):
        """Initialise the board, starting player (X) and move history."""
        self.board = Board()
        self.current_player = "X"
        self.move_history = []      # list of (player, row, col) tuples
        self.winner = None          # winning symbol, set when a round ends
        self.winning_line = None    # coordinates of the winning line
        self.state = self.STATE_PLAYING
    def get_game_state(self):
        """Return the current state: STATE_PLAYING, STATE_WON or STATE_DRAW."""
        return self.state
    def handle_move(self, row, col):
        """
        Attempt the current player's move at (row, col).
        Returns True if the move was valid and applied. Updates the
        state (won/draw) and switches turns only while the game continues.
        """
        if self.state != self.STATE_PLAYING:
            return False
        if not self.board.place_mark(row, col, self.current_player):
            return False
        self.move_history.append((self.current_player, row, col))
        winner, line = self.board.check_winner()
        if winner is not None:
            self.winner, self.winning_line = winner, line
            self.state = self.STATE_WON
        elif self.board.is_full():
            self.state = self.STATE_DRAW
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
        return True
    def reset(self):
        """Start a new round: clear board, history and state; X moves first."""
        self.board.reset()
        self.current_player = "X"
        self.move_history = []
        self.winner = None
        self.winning_line = None
        self.state = self.STATE_PLAYING