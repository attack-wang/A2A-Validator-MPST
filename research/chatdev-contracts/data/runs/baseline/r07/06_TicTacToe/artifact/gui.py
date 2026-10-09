'''
gui.py
Tkinter-based graphical user interface for the Tic-Tac-Toe game.
This module contains the TicTacToeGUI class, which renders the 3x3 board
as clickable buttons, displays turn/win/draw status messages, highlights
the winning line, maintains a cross-game scoreboard, and provides a
restart control.
'''
import tkinter as tk
from tkinter import font as tkfont
from game_logic import TicTacToeGame
class TicTacToeGUI:
    """
    Interactive Tkinter front-end for TicTacToeGame.
    Attributes:
        root (tk.Tk): The main application window.
        game (TicTacToeGame): The underlying game-logic instance.
        scores (dict[str, int]): Cross-game scoreboard counting wins for
            'X' and 'O' plus the number of drawn games.
    """
    # Visual configuration
    BOARD_SIZE = 3
    CELL_SIZE = 6  # width/height of each cell button in text units
    BG_COLOR = "#1e1e2e"
    BOARD_COLOR = "#2b2b3d"
    STATUS_COLOR = "#f5f5f5"
    X_COLOR = "#ff6b6b"
    O_COLOR = "#4ecdc4"
    WIN_COLOR = "#ffd93d"
    DISABLED_COLOR = "#3a3a4d"
    def __init__(self, root):
        """
        Build the GUI and bind it to a fresh game instance.
        Args:
            root (tk.Tk): The main application window.
        """
        self.root = root
        self.game = TicTacToeGame()
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self.cell_buttons = [[None] * self.BOARD_SIZE
                             for _ in range(self.BOARD_SIZE)]
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)
        self._create_widgets()
        self._update_board()
        self._update_status()
        self._update_scoreboard()
    def _create_widgets(self):
        """Create the scoreboard, status label, 3x3 button grid, and restart button."""
        # Scoreboard bar
        self.score_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 12),
            bg=self.BG_COLOR,
            fg=self.STATUS_COLOR,
            pady=6,
        )
        self.score_label.pack(fill=tk.X)
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 16, "bold"),
            bg=self.BG_COLOR,
            fg=self.STATUS_COLOR,
            pady=10,
        )
        self.status_label.pack(fill=tk.X)
        # Board frame
        board_frame = tk.Frame(self.root, bg=self.BOARD_COLOR, padx=10, pady=10)
        board_frame.pack(padx=15, pady=5)
        cell_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                button = tk.Button(
                    board_frame,
                    text=" ",
                    font=cell_font,
                    width=self.CELL_SIZE,
                    height=1,
                    bg=self.BOARD_COLOR,
                    fg=self.STATUS_COLOR,
                    activebackground=self.DISABLED_COLOR,
                    relief=tk.RAISED,
                    bd=2,
                    command=lambda r=row, c=col: self._on_cell_click(r, c),
                )
                button.grid(row=row, column=col, padx=4, pady=4,
                            sticky="nsew")
                self.cell_buttons[row][col] = button
        # Make cells expand uniformly
        for i in range(self.BOARD_SIZE):
            board_frame.grid_rowconfigure(i, weight=1)
            board_frame.grid_columnconfigure(i, weight=1)
        # Restart button
        self.restart_button = tk.Button(
            self.root,
            text="Restart Game",
            font=("Helvetica", 12, "bold"),
            bg=self.X_COLOR,
            fg="#ffffff",
            activebackground=self.O_COLOR,
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self._restart,
        )
        self.restart_button.pack(pady=12)
    def _on_cell_click(self, row, col):
        """
        Handle a click on the cell at (row, col).
        Applies the move through the game logic, then refreshes the
        board, status message, and (if applicable) the winning-line
        highlight and the cross-game scoreboard.
        Args:
            row (int): Row index of the clicked cell (0-2).
            col (int): Column index of the clicked cell (0-2).
        """
        if self.game.game_over:
            return
        if not self.game.make_move(row, col):
            return  # Invalid move (occupied cell) — ignore silently
        self._update_board()
        if self.game.game_over:
            if self.game.winning_line:
                self._highlight_winner(self.game.winning_line)
            self._disable_board()
            self._record_result()
        self._update_status()
    def _record_result(self):
        """Update the cross-game scoreboard once a game has finished."""
        if self.game.winner:
            self.scores[self.game.winner] += 1
        else:
            self.scores["Draws"] += 1
        self._update_scoreboard()
    def _update_scoreboard(self):
        """Refresh the scoreboard label with the current tally."""
        self.score_label.config(
            text=(f"X wins: {self.scores['X']}    |    "
                  f"O wins: {self.scores['O']}    |    "
                  f"Draws: {self.scores['Draws']}")
        )
    def _update_board(self):
        """Refresh every cell button to reflect the current board state."""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                mark = self.game.board[row][col]
                button = self.cell_buttons[row][col]
                button.config(text=mark)
                if mark == "X":
                    button.config(fg=self.X_COLOR)
                elif mark == "O":
                    button.config(fg=self.O_COLOR)
    def _highlight_winner(self, winning_line):
        """
        Visually emphasize the three cells that form the winning line.
        Args:
            winning_line (list[tuple[int, int]]): Coordinates of the
                winning cells.
        """
        for row, col in winning_line:
            button = self.cell_buttons[row][col]
            button.config(bg=self.WIN_COLOR,
                          activebackground=self.WIN_COLOR)
    def _disable_board(self):
        """Disable all cell buttons so no further moves can be made."""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                button = self.cell_buttons[row][col]
                button.config(
                    state=tk.DISABLED,
                    disabledforeground=button.cget("fg"),
                )
    def _update_status(self):
        """Refresh the status label with the current game-state message."""
        self.status_label.config(text=self.game.get_status_message())
    def _restart(self):
        """Reset the game logic and restore the board UI for a new game."""
        self.game.reset()
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                button = self.cell_buttons[row][col]
                button.config(
                    text=" ",
                    state=tk.NORMAL,
                    bg=self.BOARD_COLOR,
                    fg=self.STATUS_COLOR,
                    activebackground=self.DISABLED_COLOR,
                )
        self._update_status()