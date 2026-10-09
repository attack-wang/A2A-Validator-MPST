'''
gui.py
This module builds the graphical user interface for the Tic-Tac-Toe game
using tkinter. It renders a 3x3 clickable grid, displays whose turn it is,
announces the winner or a draw, highlights the winning line, and provides
a "New Game" button to restart.
'''
import tkinter as tk
from tkinter import messagebox
from game_logic import TicTacToeGame
class TicTacToeGUI:
    """
    Tkinter-based front end for TicTacToeGame.
    Attributes:
        root (tk.Tk): The main application window.
        game (TicTacToeGame): The underlying game-logic instance.
        cells (list[list[tk.Button]]): 3x3 grid of clickable board buttons.
    """
    def __init__(self, root):
        """
        Initialize the GUI: build widgets, bind the game logic, and show
        the initial state.
        Args:
            root (tk.Tk): The root Tk window.
        """
        self.root = root
        self.game = TicTacToeGame()
        self.cells = [[None for _ in range(3)] for _ in range(3)]
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        self._setup_ui()
        self._update_board_display()
        self._update_status(f"Player {self.game.get_current_player()}'s turn")
    def _setup_ui(self):
        """Create and lay out all widgets: title, status bar, grid, reset button."""
        # Title banner
        title_label = tk.Label(
            self.root,
            text="Tic-Tac-Toe",
            font=("Helvetica", 26, "bold"),
            fg="#ecf0f1",
            bg="#2c3e50",
        )
        title_label.pack(pady=(15, 5))
        # Status label showing turn / result information
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 14),
            fg="#f1c40f",
            bg="#2c3e50",
        )
        self.status_label.pack(pady=(0, 10))
        # 3x3 grid of buttons
        board_frame = tk.Frame(self.root, bg="#2c3e50")
        board_frame.pack(padx=15, pady=5)
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    board_frame,
                    text=" ",
                    width=6,
                    height=3,
                    font=("Helvetica", 22, "bold"),
                    bg="#34495e",
                    fg="#ecf0f1",
                    activebackground="#46637f",
                    relief=tk.RAISED,
                    bd=2,
                    command=lambda r=row, c=col: self._on_cell_click(r, c),
                )
                button.grid(row=row, column=col, padx=4, pady=4)
                self.cells[row][col] = button
        # New Game button
        reset_button = tk.Button(
            self.root,
            text="New Game",
            font=("Helvetica", 13, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            relief=tk.RAISED,
            bd=2,
            padx=12,
            pady=6,
            command=self._reset_game,
        )
        reset_button.pack(pady=(10, 18))
    def _on_cell_click(self, row, col):
        """
        Handle a click on board cell (row, col): apply the move, refresh the
        display, and react to a win, draw, or turn change.
        Args:
            row (int): Row index of the clicked cell.
            col (int): Column index of the clicked cell.
        """
        if self.game.game_over:
            return  # Ignore clicks after the game has ended
        if not self.game.make_move(row, col):
            return  # Illegal move (occupied cell) — do nothing
        self._update_board_display()
        if self.game.winner is not None:
            self._handle_game_end(f"Player {self.game.winner} wins!")
        elif self.game.is_draw():
            self._handle_game_end("It's a draw!")
        else:
            self._update_status(
                f"Player {self.game.get_current_player()}'s turn"
            )
    def _update_board_display(self):
        """Refresh every button's text and color to mirror the game board."""
        board = self.game.get_board()
        for row in range(3):
            for col in range(3):
                mark = board[row][col]
                button = self.cells[row][col]
                button.config(text=mark)
                if mark == 'X':
                    button.config(fg="#e74c3c")   # Red for X
                elif mark == 'O':
                    button.config(fg="#3498db")   # Blue for O
                else:
                    button.config(fg="#ecf0f1")   # Default for empty
    def _update_status(self, message):
        """
        Write a message to the status label.
        Args:
            message (str): Text to display above the board.
        """
        self.status_label.config(text=message)
    def _handle_game_end(self, message):
        """
        Finalize the game: announce the result, highlight the winning line
        (when a player has won), lock the board, and show a pop-up dialog.
        Args:
            message (str): The result message (win or draw).
        """
        self._update_status(message)
        if self.game.winner is not None:
            self._highlight_winning_line()
        self._disable_board()
        messagebox.showinfo("Game Over", message)
    def _highlight_winning_line(self):
        """
        Visually emphasize the three cells that form the winning line by
        giving them a bright background, so the winning row, column, or
        diagonal is immediately obvious to both players.
        """
        if self.game.winning_line is None:
            return
        for row, col in self.game.winning_line:
            self.cells[row][col].config(bg="#f1c40f")
    def _disable_board(self):
        """Set every board button to a disabled state so no more moves can be made."""
        for row in range(3):
            for col in range(3):
                self.cells[row][col].config(state=tk.DISABLED)
    def _enable_board(self):
        """Re-enable every board button and restore its default appearance."""
        for row in range(3):
            for col in range(3):
                self.cells[row][col].config(
                    state=tk.NORMAL,
                    text=" ",
                    bg="#34495e",
                    fg="#ecf0f1",
                )
    def _reset_game(self):
        """Reset both the game logic and the GUI to the starting state."""
        self.game.reset()
        self._enable_board()
        self._update_board_display()
        self._update_status(f"Player {self.game.get_current_player()}'s turn")