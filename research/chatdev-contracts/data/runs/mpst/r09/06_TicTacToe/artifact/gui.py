'''
gui.py
Builds the tkinter graphical interface for the tic-tac-toe game:
  * a 3x3 grid of buttons the players click to place their marks,
  * a status bar announcing whose turn it is and the result,
  * a running scoreboard with "New Round" and "Reset Scores" controls.
This is the single, authoritative GUI module for the project.
'''
import tkinter as tk
from tkinter import messagebox
from game import Game
class TicTacToeGUI:
    """Tkinter front-end that renders the board and handles player clicks."""
    def __init__(self, root, game=None):
        """
        Construct every widget and put the first round on screen.
        Args:
            root (tk.Tk): the application's main window.
            game (Game, optional): an already-configured Game instance;
                a default one is created when omitted.
        """
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.game = game if game is not None else Game()
        self.score = {"X": 0, "O": 0, "Draw": 0}
        self.buttons = []
        self.default_bg = None
        self.default_fg = None
        self._build_status_bar()
        self._build_grid()
        self._build_control_bar()
        self._refresh()
    # ------------------------------------------------------------------ #
    # Widget construction                                                #
    # ------------------------------------------------------------------ #
    def _build_status_bar(self):
        """Create the label that shows turn information and results."""
        self.status_label = tk.Label(
            self.root, text="", font=("Helvetica", 14, "bold"), pady=10
        )
        self.status_label.pack()
    def _build_grid(self):
        """Create the 3x3 grid of clickable cell buttons."""
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=5)
        for index in range(9):
            button = tk.Button(
                frame,
                text=" ",
                width=6,
                height=3,
                font=("Helvetica", 24, "bold"),
                command=lambda i=index: self._on_cell_click(i),
            )
            # Capture the platform's real default colors once, so that
            # resetting never depends on hard-coded, platform-specific names.
            if self.default_bg is None:
                self.default_bg = button.cget("bg")
                self.default_fg = button.cget("fg")
            row, col = divmod(index, 3)
            button.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(button)
    def _build_control_bar(self):
        """Create the scoreboard label and the control buttons."""
        self.score_label = tk.Label(self.root, text="", font=("Helvetica", 11))
        self.score_label.pack(pady=(5, 0))
        controls = tk.Frame(self.root)
        controls.pack(pady=10)
        tk.Button(
            controls, text="New Round", width=12, command=self._new_round
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            controls, text="Reset Scores", width=12, command=self._reset_scores
        ).pack(side=tk.LEFT, padx=5)
    # ------------------------------------------------------------------ #
    # Event handling                                                     #
    # ------------------------------------------------------------------ #
    def _on_cell_click(self, index):
        """Apply the current player's move when cell `index` is clicked."""
        if self.game.is_over():
            return
        if not self.game.play_move(index):
            return  # cell already occupied -> ignore the click
        symbol = self.game.board.cells[index]
        self.buttons[index]["text"] = symbol
        self.buttons[index]["fg"] = "red" if symbol == "X" else "blue"
        if self.game.status == "win":
            self._highlight_winning_line()
            self.score[self.game.winner.symbol] += 1
            self._refresh()
            messagebox.showinfo(
                "Game Over",
                f"{self.game.winner.name} ({self.game.winner.symbol}) wins!",
            )
        elif self.game.status == "draw":
            self.score["Draw"] += 1
            self._refresh()
            messagebox.showinfo("Game Over", "It's a draw! Board is full.")
        else:
            self._refresh()
    def _new_round(self):
        """Clear the board so the next round can begin."""
        self.game.reset()
        for button in self.buttons:
            button["text"] = " "
            button["fg"] = self.default_fg
            button["bg"] = self.default_bg
        self._refresh()
    def _reset_scores(self):
        """Zero the scoreboard and start a fresh round."""
        self.score = {"X": 0, "O": 0, "Draw": 0}
        self._new_round()
    # ------------------------------------------------------------------ #
    # Display helpers                                                    #
    # ------------------------------------------------------------------ #
    def _highlight_winning_line(self):
        """Paint the three winning cells green so the win is obvious."""
        for index in self.game.winning_line:
            self.buttons[index]["bg"] = "light green"
    def _refresh(self):
        """Update the status bar and the scoreboard text."""
        if self.game.status == "win":
            text = (
                f"{self.game.winner.name} ({self.game.winner.symbol}) wins!  "
                "Click 'New Round' to play again."
            )
        elif self.game.status == "draw":
            text = "It's a draw!  Click 'New Round' to play again."
        else:
            player = self.game.current_player
            text = f"{player.name}'s turn - place {player.symbol}"
        self.status_label["text"] = text
        player_x, player_o = self.game.players
        self.score_label["text"] = (
            f"Score  |  {player_x.name} (X): {self.score['X']}    "
            f"{player_o.name} (O): {self.score['O']}    "
            f"Draws: {self.score['Draw']}"
        )