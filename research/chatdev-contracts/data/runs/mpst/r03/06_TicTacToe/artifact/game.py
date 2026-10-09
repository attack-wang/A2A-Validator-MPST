'''
game.py
Contains the TicTacToeGame class: a tkinter-based graphical application
that wires the Board and Player components together into a complete,
user-friendly, two-player tic-tac-toe game.
UI features:
    * 3x3 grid of large clickable buttons.
    * Status line that always shows whose turn it is (or the result).
    * Automatic win detection with the winning line highlighted in gold.
    * Draw detection when the board fills up with no winner.
    * Running scoreboard (X wins / O wins / draws).
    * "New Round" button (keeps scores) and "Reset Scores" button.
'''
import tkinter as tk
from tkinter import messagebox, simpledialog
from board import Board
from player import Player
class TicTacToeGame:
    """Main application class: builds the GUI and drives the game flow."""
    # ---- visual style constants -------------------------------------
    BG_COLOR = "#2c3e50"        # window background (dark blue)
    FG_COLOR = "#ecf0f1"        # default light text
    BOARD_BG = "#34495e"        # frame behind the grid
    X_COLOR = "#e74c3c"         # color of the X marks (red)
    O_COLOR = "#3498db"         # color of the O marks (blue)
    WIN_COLOR = "#f1c40f"       # highlight color for the winning line
    CELL_BG = "#ecf0f1"         # empty cell background
    def __init__(self, root):
        """Initialize state, build the UI, and prepare the first round."""
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)
        # Core game state
        self.board = Board()
        self.player_x = Player("Player 1", "X")
        self.player_o = Player("Player 2", "O")
        self.current_player = self.player_x
        self.round_over = False
        self.draws = 0
        self._build_ui()
        self._ask_player_names()
        self._update_scoreboard()
        self._update_status()
    def _build_ui(self):
        """Create all widgets: scoreboard, status line, 3x3 grid, controls."""
        # Scoreboard label
        self.score_label = tk.Label(
            self.root, text="", font=("Helvetica", 14, "bold"),
            bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.score_label.pack(pady=(10, 5))
        # Status line
        self.status_label = tk.Label(
            self.root, text="", font=("Helvetica", 14),
            bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.status_label.pack(pady=5)
        # 3x3 grid of clickable cells
        board_frame = tk.Frame(self.root, bg=self.BOARD_BG, padx=10, pady=10)
        board_frame.pack(padx=10, pady=10)
        self.cell_buttons = []
        for r in range(Board.SIZE):
            row_buttons = []
            for c in range(Board.SIZE):
                # Default args freeze r/c at definition time (avoids late-binding bug)
                btn = tk.Button(
                    board_frame, text=" ", width=6, height=3,
                    font=("Helvetica", 24, "bold"),
                    bg=self.CELL_BG, fg=self.FG_COLOR,
                    command=lambda r=r, c=c: self._handle_cell_click(r, c))
                btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
                row_buttons.append(btn)
            self.cell_buttons.append(row_buttons)
        # Control buttons
        controls = tk.Frame(self.root, bg=self.BG_COLOR)
        controls.pack(pady=(0, 10))
        tk.Button(controls, text="New Round", font=("Helvetica", 12),
                  bg=self.BOARD_BG, fg=self.FG_COLOR,
                  command=self._new_round).pack(side="left", padx=5)
        tk.Button(controls, text="Reset Scores", font=("Helvetica", 12),
                  bg=self.BOARD_BG, fg=self.FG_COLOR,
                  command=self._reset_scores).pack(side="left", padx=5)
    def _ask_player_names(self):
        """Prompt both players for names; fall back to defaults on cancel/blank."""
        name_x = simpledialog.askstring(
            "Player 1", "Name of Player 1 (X):",
            initialvalue="Player 1", parent=self.root)
        name_o = simpledialog.askstring(
            "Player 2", "Name of Player 2 (O):",
            initialvalue="Player 2", parent=self.root)
        if name_x and name_x.strip():
            self.player_x.name = name_x.strip()
        if name_o and name_o.strip():
            self.player_o.name = name_o.strip()
    def _handle_cell_click(self, row, col):
        """Apply the current player's move, then evaluate win/draw/turn switch."""
        if self.round_over:
            return  # ignore clicks after the round has ended
        if not self.board.make_move(row, col, self.current_player.symbol):
            return  # illegal move (occupied cell) — ignore
        self._render_cell(row, col)
        winner = self.board.check_winner()
        if winner is not None:
            self._end_round(winner)
        elif self.board.is_full():
            self._end_round(None)
        else:
            # Alternate turns between the two players
            self.current_player = (self.player_o
                                   if self.current_player is self.player_x
                                   else self.player_x)
            self._update_status()
    def _render_cell(self, row, col):
        """Draw the current player's symbol in the cell and lock the button."""
        symbol = self.current_player.symbol
        color = self.X_COLOR if symbol == "X" else self.O_COLOR
        self.cell_buttons[row][col].config(
            text=symbol, state="disabled",
            disabledforeground=color)  # keep symbol colored when disabled
    def _end_round(self, winner):
        """Finish the round: update scores, highlight the win, announce result."""
        self.round_over = True
        if winner is not None:
            winning_player = self.player_x if winner == "X" else self.player_o
            winning_player.record_win()
            line = self.board.get_winning_line()
            if line:
                for (r, c) in line:  # highlight winning line in gold
                    self.cell_buttons[r][c].config(bg=self.WIN_COLOR)
            self._update_scoreboard()
            self.status_label.config(
                text=f"{winning_player.name} ({winner}) wins!")
            messagebox.showinfo(
                "Round Over", f"{winning_player.name} ({winner}) wins!")
        else:
            self.draws += 1
            self._update_scoreboard()
            self.status_label.config(text="It's a draw!")
            messagebox.showinfo("Round Over", "It's a draw!")
    def _new_round(self):
        """Start a fresh round: clear board and UI; X always opens."""
        self.board.reset()
        self.round_over = False
        self.current_player = self.player_x
        for r in range(Board.SIZE):
            for c in range(Board.SIZE):
                self.cell_buttons[r][c].config(
                    text=" ", bg=self.CELL_BG, fg=self.FG_COLOR, state="normal")
        self._update_status()
    def _reset_scores(self):
        """Zero out wins and draws, then start a fresh round."""
        self.player_x.reset_score()
        self.player_o.reset_score()
        self.draws = 0
        self._update_scoreboard()
        self._new_round()
    def _update_scoreboard(self):
        """Refresh the scoreboard label with current win/draw counts."""
        self.score_label.config(
            text=f"{self.player_x.name}: {self.player_x.wins}   |   "
                 f"Draws: {self.draws}   |   "
                 f"{self.player_o.name}: {self.player_o.wins}")
    def _update_status(self):
        """Refresh the status line to show whose turn it is."""
        self.status_label.config(
            text=f"{self.current_player.name}'s turn "
                 f"({self.current_player.symbol})")