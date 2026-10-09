'''
Graphical user interface module for the Tic-Tac-Toe game.
This module implements the user-friendly interface using tkinter.
It renders the 3x3 grid as clickable buttons, displays whose turn
it is, tracks and shows each player's move history, keeps a running
scoreboard, highlights the winning line, and offers a "Play Again"
button so a new round can start instantly.
'''
import tkinter as tk
from tkinter import messagebox
from game_logic import Board, Game
class TicTacToeGUI:
    """Main application window for the Tic-Tac-Toe game."""
    # --- Appearance constants -------------------------------------------------
    CELL_FONT = ("Helvetica", 42, "bold")
    TITLE_FONT = ("Helvetica", 22, "bold")
    STATUS_FONT = ("Helvetica", 14, "bold")
    INFO_FONT = ("Helvetica", 11)
    BUTTON_FONT = ("Helvetica", 12, "bold")
    BG_COLOR = "#1e1e2e"
    BOARD_COLOR = "#313244"
    CELL_COLOR = "#45475a"
    CELL_HOVER = "#585b70"
    X_COLOR = "#f38ba8"
    O_COLOR = "#89b4fa"
    WIN_COLOR = "#a6e3a1"
    TEXT_COLOR = "#cdd6f4"
    def __init__(self):
        """Set up the main window, the game instance, and all UI widgets."""
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_COLOR)
        self.game = Game()
        self.cells = {}
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self._create_widgets()
        self._refresh_ui()
    def run(self):
        """Start the tkinter main event loop."""
        self.root.mainloop()
    # --- Widget construction ----------------------------------------------------
    def _create_widgets(self):
        """Build the title, 3x3 button grid, status bar, history, scoreboard and reset button."""
        title = tk.Label(
            self.root, text="Tic-Tac-Toe",
            font=self.TITLE_FONT, bg=self.BG_COLOR, fg=self.TEXT_COLOR,
        )
        title.grid(row=0, column=0, columnspan=3, pady=(15, 5))
        board_frame = tk.Frame(self.root, bg=self.BOARD_COLOR, padx=6, pady=6)
        board_frame.grid(row=1, column=0, columnspan=3, padx=15, pady=10)
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    board_frame, text=" ", width=4, height=2,
                    font=self.CELL_FONT,
                    bg=self.CELL_COLOR, fg=self.TEXT_COLOR,
                    disabledforeground=self.TEXT_COLOR,
                    activebackground=self.CELL_HOVER,
                    activeforeground=self.TEXT_COLOR,
                    relief=tk.FLAT, bd=0, highlightthickness=0,
                    command=lambda r=row, c=col: self._on_cell_click(r, c),
                )
                button.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
                self.cells[(row, col)] = button
        for i in range(3):
            board_frame.grid_rowconfigure(i, weight=1)
            board_frame.grid_columnconfigure(i, weight=1)
        self.status_label = tk.Label(
            self.root, text="", font=self.STATUS_FONT,
            bg=self.BG_COLOR, fg=self.TEXT_COLOR,
        )
        self.status_label.grid(row=2, column=0, columnspan=3, pady=(5, 2))
        self.history_label = tk.Label(
            self.root, text="", font=self.INFO_FONT,
            bg=self.BG_COLOR, fg=self.TEXT_COLOR,
            wraplength=340, justify=tk.CENTER,
        )
        self.history_label.grid(row=3, column=0, columnspan=3, pady=(2, 2))
        self.score_label = tk.Label(
            self.root, text="", font=self.INFO_FONT,
            bg=self.BG_COLOR, fg=self.TEXT_COLOR,
        )
        self.score_label.grid(row=4, column=0, columnspan=3, pady=(2, 5))
        reset_button = tk.Button(
            self.root, text="Play Again", font=self.BUTTON_FONT,
            bg=self.CELL_COLOR, fg=self.TEXT_COLOR,
            activebackground=self.CELL_HOVER, activeforeground=self.TEXT_COLOR,
            relief=tk.FLAT, padx=20, pady=5, cursor="hand2",
            command=self._reset_game,
        )
        reset_button.grid(row=5, column=0, columnspan=3, pady=(5, 15))
    # --- Event handlers -----------------------------------------------------------
    def _on_cell_click(self, row, col):
        """Handle a click on a grid cell: attempt the move and refresh the UI."""
        if self.game.get_game_state() != Game.STATE_PLAYING:
            return
        if not self.game.handle_move(row, col):
            return  # Invalid move (cell already occupied) - ignore the click.
        state = self.game.get_game_state()
        if state in (Game.STATE_WON, Game.STATE_DRAW):
            self._record_score(state)
        self._refresh_ui()
        if state == Game.STATE_WON:
            self._highlight_winner(self.game.winning_line)
            self.root.after(700, self._show_game_over)
        elif state == Game.STATE_DRAW:
            self.root.after(700, self._show_game_over)
    def _reset_game(self):
        """Reset the game state and restore the UI to its initial appearance."""
        self.game.reset()
        self._refresh_ui()
    # --- UI refresh helpers ---------------------------------------------------------
    def _refresh_ui(self):
        """Refresh the board, status bar, move history and scoreboard."""
        self._update_board_display()
        self._update_status()
        self._update_move_history()
        self._update_scoreboard()
    def _update_board_display(self):
        """Refresh all cell buttons to reflect the current board state."""
        for row in range(3):
            for col in range(3):
                symbol = self.game.board.grid[row][col]
                button = self.cells[(row, col)]
                if symbol == Board.EMPTY:
                    button.config(
                        text=" ",
                        bg=self.CELL_COLOR,
                        fg=self.TEXT_COLOR,
                        disabledforeground=self.TEXT_COLOR,
                        state=tk.NORMAL,
                    )
                else:
                    color = self.X_COLOR if symbol == "X" else self.O_COLOR
                    button.config(
                        text=symbol,
                        fg=color,
                        disabledforeground=color,
                        bg=self.CELL_COLOR,
                        state=tk.DISABLED,
                    )
    def _update_status(self):
        """Update the status bar text and colour based on the current game state."""
        state = self.game.get_game_state()
        if state == Game.STATE_PLAYING:
            player = self.game.current_player
            color = self.X_COLOR if player == "X" else self.O_COLOR
            self.status_label.config(text=f"Player {player}'s turn", fg=color)
        elif state == Game.STATE_WON:
            self.status_label.config(
                text=f"Player {self.game.winner} wins!", fg=self.WIN_COLOR
            )
        else:  # Draw
            self.status_label.config(text="It's a draw!", fg=self.TEXT_COLOR)
    def _update_move_history(self):
        """Show a compact, human-readable log of every move made this round."""
        if not self.game.move_history:
            self.history_label.config(text="No moves yet - Player X starts.")
            return
        moves_text = "   ".join(
            f"{player}: ({row + 1},{col + 1})"
            for player, row, col in self.game.move_history
        )
        self.history_label.config(text=f"Moves:  {moves_text}")
    def _update_scoreboard(self):
        """Show the running win/draw tally across rounds."""
        self.score_label.config(
            text=(
                f"Score   X: {self.scores['X']}   |   "
                f"O: {self.scores['O']}   |   Draws: {self.scores['Draws']}"
            )
        )
    def _record_score(self, state):
        """Increment the scoreboard entry matching the finished round."""
        if state == Game.STATE_WON:
            self.scores[self.game.winner] += 1
        else:
            self.scores["Draws"] += 1
    def _highlight_winner(self, winning_line):
        """Highlight the three cells that form the winning line."""
        for row, col in winning_line:
            self.cells[(row, col)].config(
                bg=self.WIN_COLOR,
                fg=self.BG_COLOR,
                disabledforeground=self.BG_COLOR,
            )
    def _show_game_over(self):
        """Display a game-over dialog announcing the result of the round."""
        state = self.game.get_game_state()
        if state == Game.STATE_WON:
            message = f"Player {self.game.winner} wins the game!"
        elif state == Game.STATE_DRAW:
            message = "The game ended in a draw!"
        else:
            return  # Game was reset before the dialog could appear.
        messagebox.showinfo("Game Over", message)