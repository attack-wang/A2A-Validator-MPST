import tkinter as tk
from tkinter import messagebox
from game import Game
class TicTacToeGUI:
    """Tkinter front-end that renders the board and handles clicks."""
    CELL_SIZE = 6  # font size multiplier
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.game = Game()
        self.score = {"X": 0, "O": 0, "Draw": 0}
        self.buttons = []
        self._build_status_bar()
        self._build_grid()
        self._build_control_bar()
        self._refresh()
    def _build_status_bar(self):
        """Create the label that shows turn info and results."""
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 14, "bold"),
            pady=10,
        )
        self.status_label.pack()
    def _build_grid(self):
        """Create the 3x3 grid of clickable buttons."""
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
            row, col = divmod(index, 3)
            button.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(button)
    def _build_control_bar(self):
        """Create the score label and the New Game / Reset buttons."""
        self.score_label = tk.Label(self.root, text="", font=("Helvetica", 11))
        self.score_label.pack(pady=(5, 0))
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        new_round_btn = tk.Button(
            control_frame, text="New Round", width=12, command=self._new_round
        )
        new_round_btn.pack(side=tk.LEFT, padx=5)
        reset_btn = tk.Button(
            control_frame, text="Reset Scores", width=12, command=self._reset_scores
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
    def _on_cell_click(self, index):
        """Handle a click on board cell `index`."""
        if self.game.is_over():
            return
        if not self.game.play_move(index):
            return  # invalid move (cell occupied) — ignore
        symbol = self.game.board.cells[index]
        self.buttons[index]["text"] = symbol
        self.buttons[index]["fg"] = "red" if symbol == "X" else "blue"
        if self.game.status == "win":
            self._highlight_winning_line()
            self.score[self.game.winner.symbol] += 1
            self._refresh()
            messagebox.showinfo(
                "Game Over", f"{self.game.winner.name} ({self.game.winner.symbol}) wins!"
            )
        elif self.game.status == "draw":
            self.score["Draw"] += 1
            self._refresh()
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            self._refresh()
    def _highlight_winning_line(self):
        """Color the three winning cells so the win is easy to see."""
        for index in self.game.winning_line:
            self.buttons[index]["bg"] = "light green"
    def _refresh(self):
        """Update the status bar and score display."""
        if self.game.status == "win":
            text = f"{self.game.winner.name} ({self.game.winner.symbol}) wins!"
        elif self.game.status == "draw":
            text = "It's a draw!"
        else:
            text = f"{self.game.current_player.name}'s turn ({self.game.current_player.symbol})"
        self.status_label["text"] = text
        x_name, o_name = (p.name for p in self.game.players)
        self.score_label["text"] = (
            f"Score — {x_name} (X): {self.score['X']}   |   "
            f"{o_name} (O): {self.score['O']}   |   Draws: {self.score['Draw']}"
        )
    def _new_round(self):
        """Clear the board and start a new round."""
        self.game.reset()
        for button in self.buttons:
            button["text"] = " "
            button["bg"] = "SystemButtonFace"
        self._refresh()
    def _reset_scores(self):
        """Zero the scoreboard and start a fresh round."""
        self.score = {"X": 0, "O": 0, "Draw": 0}
        self._new_round()