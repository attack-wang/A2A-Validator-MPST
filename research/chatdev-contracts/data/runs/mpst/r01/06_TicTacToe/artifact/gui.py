'''
gui.py
Graphical user interface for the Tic-Tac-Toe game, built with tkinter.
The TicTacToeGUI class renders the 3x3 grid as clickable buttons, shows
whose turn it is and how many moves have been played, keeps a running
scoreboard across rounds, highlights the winning line, announces the
result (win or draw) and offers a "New Game" button to start over.
'''
import tkinter as tk
from tkinter import font as tkfont
from game_logic import GameLogic
class TicTacToeGUI:
    """Tkinter front-end that drives a GameLogic instance."""
    # Appearance settings
    WINDOW_BG = "#1e272e"
    CELL_BG = "#485460"
    CELL_HOVER_BG = "#57606f"
    WIN_BG = "#00b894"
    PLAYER_COLORS = {"X": "#ff6b6b", "O": "#48dbfb"}
    STATUS_FG = "#ffffff"
    def __init__(self, root):
        """Build the window layout and prepare a fresh game."""
        self.logic = GameLogic()
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg=self.WINDOW_BG)
        self.root.resizable(False, False)
        self.cell_buttons = [[None] * 3 for _ in range(3)]
        self._build_header()
        self._build_board()
        self._build_status_bar()
        self._build_scoreboard()
        self._build_controls()
        self._update_status("Player X's turn")
        self._update_scoreboard()
    # ------------------------------------------------------------------
    # Widget construction
    # ------------------------------------------------------------------
    def _build_header(self):
        """Create the game title displayed at the top of the window."""
        title_font = tkfont.Font(family="Helvetica", size=22, weight="bold")
        title = tk.Label(
            self.root,
            text="Tic-Tac-Toe",
            font=title_font,
            fg=self.STATUS_FG,
            bg=self.WINDOW_BG,
            pady=8,
        )
        title.pack()
    def _build_board(self):
        """Create the 3x3 grid of clickable cell buttons."""
        board_frame = tk.Frame(self.root, bg=self.WINDOW_BG)
        board_frame.pack(padx=12, pady=6)
        cell_font = tkfont.Font(family="Helvetica", size=34, weight="bold")
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    board_frame,
                    text=" ",
                    width=6,
                    height=2,
                    font=cell_font,
                    bg=self.CELL_BG,
                    fg=self.STATUS_FG,
                    disabledforeground=self.STATUS_FG,
                    activebackground=self.CELL_HOVER_BG,
                    relief="ridge",
                    bd=2,
                    cursor="hand2",
                    command=lambda r=row, c=col: self.on_cell_click(r, c),
                )
                button.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
                self.cell_buttons[row][col] = button
    def _build_status_bar(self):
        """Create the label that reports turns and results."""
        status_font = tkfont.Font(family="Helvetica", size=13)
        self.status_label = tk.Label(
            self.root,
            text="",
            font=status_font,
            fg=self.STATUS_FG,
            bg=self.WINDOW_BG,
            pady=6,
        )
        self.status_label.pack()
    def _build_scoreboard(self):
        """Create the label that tracks wins for X, O and draws."""
        score_font = tkfont.Font(family="Helvetica", size=11)
        self.score_label = tk.Label(
            self.root,
            text="",
            font=score_font,
            fg="#d2dae2",
            bg=self.WINDOW_BG,
        )
        self.score_label.pack()
    def _build_controls(self):
        """Create the 'New Game' button used to start a fresh round."""
        self.new_game_button = tk.Button(
            self.root,
            text="New Game",
            font=tkfont.Font(family="Helvetica", size=12, weight="bold"),
            bg="#00a8ff",
            fg=self.STATUS_FG,
            activebackground="#0097e6",
            activeforeground=self.STATUS_FG,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=22,
            pady=6,
            command=self.reset_game,
        )
        self.new_game_button.pack(pady=(4, 14))
    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def on_cell_click(self, row, col):
        """
        React to a click on cell (row, col).
        Places the current player's mark when the move is legal, refreshes
        the board, then checks for a win or a draw; otherwise the turn is
        handed to the other player.
        """
        if self.logic.game_over:
            return
        if not self.logic.make_move(row, col):
            return  # Cell already occupied — ignore the click.
        player = self.logic.get_current_player()
        color = self.PLAYER_COLORS[player]
        self.cell_buttons[row][col].config(
            text=player,
            fg=color,
            disabledforeground=color,
            state="disabled",
        )
        winning_combination = self.logic.check_winner()
        if winning_combination:
            self._handle_win(winning_combination)
        elif self.logic.check_draw():
            self._handle_draw()
        else:
            self.logic.switch_player()
            self._update_status(
                f"Move {self.logic.get_move_count() + 1} · "
                f"Player {self.logic.get_current_player()}'s turn"
            )
    def _handle_win(self, winning_combination):
        """Highlight the winning line, update the score and announce it."""
        self.scores[self.logic.winner] += 1
        for r, c in winning_combination:
            self.cell_buttons[r][c].config(
                bg=self.WIN_BG,
                fg="#ffffff",
                disabledforeground="#ffffff",
            )
        self._disable_all_cells()
        self._update_status(f"Player {self.logic.winner} wins! 🎉")
        self._update_scoreboard()
    def _handle_draw(self):
        """Record the draw and announce it."""
        self.scores["Draws"] += 1
        self._disable_all_cells()
        self._update_status("It's a draw! 🤝")
        self._update_scoreboard()
    def reset_game(self):
        """Start a new round: clear the board and re-enable every cell."""
        self.logic.reset()
        for row in range(3):
            for col in range(3):
                self.cell_buttons[row][col].config(
                    text=" ",
                    bg=self.CELL_BG,
                    fg=self.STATUS_FG,
                    disabledforeground=self.STATUS_FG,
                    state="normal",
                )
        self._update_status("Player X's turn")
    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------
    def _update_status(self, message):
        """Replace the text shown in the status bar."""
        self.status_label.config(text=message)
    def _update_scoreboard(self):
        """Refresh the running score line."""
        self.score_label.config(
            text=(
                f"Score — X: {self.scores['X']}   "
                f"O: {self.scores['O']}   Draws: {self.scores['Draws']}"
            )
        )
    def _disable_all_cells(self):
        """Disable every cell so the finished board cannot be changed."""
        for row in range(3):
            for col in range(3):
                self.cell_buttons[row][col].config(state="disabled")