'''
tictactoeui.py
Defines the Tkinter GUI for the two-player tic-tac-toe game:
renders the 3x3 board, handles cell clicks, highlights the winning
line, and displays status messages and running scores.
'''
import tkinter as tk
from game import Game
class TicTacToeUI:
    """Tkinter GUI for the two-player tic-tac-toe game."""
    MARK_COLORS = {"X": "#e74c3c", "O": "#3498db"}
    WIN_COLOR = "#f1c40f"
    EMPTY_COLOR = "#34495e"
    FILLED_COLOR = "#3b5368"
    BG_COLOR = "#2c3e50"
    TEXT_COLOR = "#ecf0f1"
    def __init__(self, root):
        self.game = Game()
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)
        self.cells = {}
        self._build_widgets()
        self._refresh_board()
        self._update_status()
    def _build_widgets(self):
        """Create and arrange all interface components."""
        title = tk.Label(
            self.root,
            text="Tic-Tac-Toe",
            font=("Helvetica", 22, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR,
        )
        title.grid(row=0, column=0, columnspan=3, pady=(12, 4))
        self.score_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 12),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR,
        )
        self.score_label.grid(row=1, column=0, columnspan=3, pady=(0, 6))
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 14, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR,
        )
        self.status_label.grid(row=2, column=0, columnspan=3, pady=(0, 8))
        board_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        board_frame.grid(row=3, column=0, columnspan=3, padx=12)
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    board_frame,
                    text=" ",
                    width=4,
                    height=2,
                    font=("Helvetica", 28, "bold"),
                    bg=self.EMPTY_COLOR,
                    fg=self.TEXT_COLOR,
                    disabledforeground=self.TEXT_COLOR,
                    activebackground="#46627f",
                    relief=tk.RAISED,
                    bd=3,
                    command=lambda r=row, c=col: self._on_cell_click(r, c),
                )
                button.grid(row=row, column=col, padx=3, pady=3)
                self.cells[(row, col)] = button
        controls = tk.Frame(self.root, bg=self.BG_COLOR)
        controls.grid(row=4, column=0, columnspan=3, pady=(10, 12))
        new_round_btn = tk.Button(
            controls,
            text="New Round",
            font=("Helvetica", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            command=self._on_new_round,
        )
        new_round_btn.pack(side=tk.LEFT, padx=6)
        reset_scores_btn = tk.Button(
            controls,
            text="Reset Scores",
            font=("Helvetica", 12, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#95a5a6",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            command=self._on_reset_scores,
        )
        reset_scores_btn.pack(side=tk.LEFT, padx=6)
    def _on_cell_click(self, row, col):
        """Handle a click on the board cell at (row, col)."""
        if not self.game.play_turn(row, col):
            return
        self._refresh_board()
        self._update_status()
    def _on_new_round(self):
        """Start a fresh round, keeping the running scores."""
        self.game.reset_game()
        self._refresh_board()
        self._update_status()
    def _on_reset_scores(self):
        """Reset the scoreboard and start a fresh round."""
        self.game.reset_scores()
        self.game.reset_game()
        self._refresh_board()
        self._update_status()
    def _refresh_board(self):
        """Sync every button's text and color with the board state."""
        winning_line = self.game.board.get_winning_line()
        for (row, col), button in self.cells.items():
            mark = self.game.board.grid[row][col]
            if mark == " ":
                button.config(
                    text=" ",
                    bg=self.EMPTY_COLOR,
                    fg=self.TEXT_COLOR,
                    disabledforeground=self.TEXT_COLOR,
                    state=tk.NORMAL,
                )
            else:
                fg_color = self.MARK_COLORS.get(mark, self.TEXT_COLOR)
                bg_color = (
                    self.WIN_COLOR
                    if winning_line and (row, col) in winning_line
                    else self.FILLED_COLOR
                )
                button.config(
                    text=mark,
                    bg=bg_color,
                    fg=fg_color,
                    disabledforeground=fg_color,
                    state=tk.NORMAL,
                )
        if self.game.state != Game.STATE_ONGOING:
            for button in self.cells.values():
                button.config(state=tk.DISABLED)
    def _update_status(self):
        """Update the status and score labels based on the game state."""
        scores = self.game.scores
        self.score_label.config(
            text=f"X wins: {scores['X']}    O wins: {scores['O']}    Draws: {scores['Draw']}"
        )
        if self.game.state == Game.STATE_WON:
            winner_name = self.game.get_winner_name()
            self.status_label.config(
                text=f"{winner_name} wins! 🎉",
                fg=self.MARK_COLORS.get(self.game.winner, self.TEXT_COLOR),
            )
        elif self.game.state == Game.STATE_DRAW:
            self.status_label.config(text="It's a draw!", fg=self.TEXT_COLOR)
        else:
            self.status_label.config(
                text=f"{self.game.get_current_player()}'s turn",
                fg=self.MARK_COLORS.get(self.game.current_mark, self.TEXT_COLOR),
            )