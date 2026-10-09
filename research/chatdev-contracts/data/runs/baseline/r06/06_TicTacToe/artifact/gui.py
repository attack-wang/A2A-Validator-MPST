'''
gui.py
Implements the TicTacToeGUI class for the tic-tac-toe game using tkinter.
Renders a 3x3 clickable grid, alternates turns between X and O,
detects wins/draws, highlights the winning line, and supports restart.
'''
import tkinter as tk
from tkinter import messagebox
class TicTacToeGUI:
    """Tic-tac-toe game controller and view built with tkinter."""
    def __init__(self, root):
        """Initialize game state, build all widgets, and start with player X."""
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        # --- Game state ---
        self.current_player = "X"      # X always moves first
        self.board = [""] * 9          # Flattened 3x3 board; "" = empty cell
        self.game_over = False         # True once a win or draw occurs
        # All 8 winning line index combinations (rows, columns, diagonals)
        self.winning_combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
            (0, 4, 8), (2, 4, 6),              # diagonals
        ]
        self._build_ui()
    def _build_ui(self):
        """Create the status label, the 3x3 grid of cell buttons, and restart button."""
        # Status bar: shows current turn or final result
        self.status_label = tk.Label(
            self.root, text="Player X's turn", font=("Helvetica", 16, "bold")
        )
        self.status_label.grid(row=0, column=0, columnspan=3, pady=(10, 5))
        # 3x3 grid of clickable buttons
        self.buttons = []
        for index in range(9):
            button = tk.Button(
                self.root, text="", width=6, height=3,
                font=("Helvetica", 24, "bold"),
                command=lambda idx=index: self.on_cell_click(idx),
            )
            button.grid(row=1 + index // 3, column=index % 3, padx=5, pady=5)
            self.buttons.append(button)
        # Remember platform-default colors so reset can restore them safely
        self.default_bg = self.buttons[0].cget("bg")
        self.default_fg = self.buttons[0].cget("fg")
        # Restart button: starts a fresh game at any time
        restart_button = tk.Button(
            self.root, text="Restart", font=("Helvetica", 12),
            command=self.reset_game,
        )
        restart_button.grid(row=4, column=0, columnspan=3, pady=(5, 10))
    def on_cell_click(self, index):
        """Handle a cell click: place the mark, evaluate the result, switch turns."""
        # Ignore clicks on occupied cells or after the game has ended
        if self.game_over or self.board[index] != "":
            return
        # Place the current player's mark on the board and the button
        self.board[index] = self.current_player
        self.buttons[index]["text"] = self.current_player
        self.buttons[index]["fg"] = "blue" if self.current_player == "X" else "red"
        # Evaluate the move: win, draw, or continue
        winning_combo = self.check_winner()
        if winning_combo:
            self.game_over = True
            self.highlight_winner(winning_combo)
            self.status_label["text"] = f"Player {self.current_player} wins!"
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
        elif "" not in self.board:
            # Board full with no winner: it's a draw
            self.game_over = True
            self.status_label["text"] = "It's a draw!"
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            # Switch turns and update the status label
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label["text"] = f"Player {self.current_player}'s turn"
    def check_winner(self):
        """Return the winning (a, b, c) index combo for the current player, else None."""
        for a, b, c in self.winning_combos:
            if self.board[a] != "" and self.board[a] == self.board[b] == self.board[c]:
                return (a, b, c)
        return None
    def highlight_winner(self, combo):
        """Highlight the three winning cells with a green background."""
        for index in combo:
            self.buttons[index]["bg"] = "lightgreen"
    def reset_game(self):
        """Reset the board, turn order, and all widgets for a new game."""
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.status_label["text"] = "Player X's turn"
        for button in self.buttons:
            button["text"] = ""
            button["bg"] = self.default_bg
            button["fg"] = self.default_fg