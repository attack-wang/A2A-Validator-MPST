'''
gui.py
Graphical user interface for the Tic-Tac-Toe game, built with tkinter.
This module renders a 3x3 clickable grid, displays turn/game status,
highlights the winning line, and provides a reset button for new rounds.
It delegates all game rules to the TicTacToe engine in game_logic.py.
'''
import tkinter as tk
from tkinter import font as tkfont
from game_logic import TicTacToe
class TicTacToeGUI:
    """
    Tkinter-based user interface for the Tic-Tac-Toe game.
    Attributes:
        root (tk.Tk): The main application window.
        game (TicTacToe): The underlying game engine instance.
        cells (dict): Maps (row, col) tuples to their tk.Button widgets.
        status_label (tk.Label): Label showing turn / result information.
    """
    # Visual configuration
    BOARD_SIZE = 3
    CELL_SIZE = 6  # internal padding units for buttons
    BG_COLOR = "#1e1e2e"
    BOARD_COLOR = "#2b2b40"
    CELL_COLOR = "#3b3b55"
    CELL_HOVER = "#4a4a6a"
    TEXT_COLOR = "#f5f5f5"
    X_COLOR = "#ff6b6b"
    O_COLOR = "#4ecdc4"
    STATUS_WIN_BG = "#2e7d32"
    STATUS_DRAW_BG = "#f9a825"
    HIGHLIGHT_COLOR = "#ffd54f"
    def __init__(self, root):
        """
        Initialize the GUI: build widgets, bind events, and show the board.
        Args:
            root (tk.Tk): The main Tkinter window.
        """
        self.root = root
        self.game = TicTacToe()
        self.cells = {}
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)
        self._create_widgets()
        self._update_board()
        self._update_status()
    def _create_widgets(self):
        """Build the header, 3x3 button grid, status bar, and reset button."""
        # ---- Header ----
        header = tk.Label(
            self.root,
            text="TIC-TAC-TOE",
            font=("Helvetica", 22, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR,
            pady=10,
        )
        header.pack()
        # ---- Board frame ----
        board_frame = tk.Frame(self.root, bg=self.BOARD_COLOR, padx=10, pady=10)
        board_frame.pack(padx=15, pady=5)
        cell_font = tkfont.Font(family="Helvetica", size=28, weight="bold")
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                btn = tk.Button(
                    board_frame,
                    text=" ",
                    width=4,
                    height=2,
                    font=cell_font,
                    bg=self.CELL_COLOR,
                    fg=self.TEXT_COLOR,
                    activebackground=self.CELL_HOVER,
                    relief=tk.RAISED,
                    bd=2,
                    command=lambda r=r, c=c: self._on_cell_click(r, c),
                )
                btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                self.cells[(r, c)] = btn
        # Make grid cells expand uniformly
        for i in range(self.BOARD_SIZE):
            board_frame.grid_rowconfigure(i, weight=1)
            board_frame.grid_columnconfigure(i, weight=1)
        # ---- Status label ----
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 14),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR,
            pady=10,
        )
        self.status_label.pack(fill=tk.X)
        # ---- Reset button ----
        reset_btn = tk.Button(
            self.root,
            text="New Game",
            font=("Helvetica", 12, "bold"),
            bg="#5c6bc0",
            fg=self.TEXT_COLOR,
            activebackground="#7986cb",
            relief=tk.FLAT,
            padx=20,
            pady=6,
            cursor="hand2",
            command=self._reset_game,
        )
        reset_btn.pack(pady=(0, 15))
    def _on_cell_click(self, row, col):
        """
        Handle a click on cell (row, col).
        Applies the move through the game engine; if the move is accepted,
        refreshes the board and status. Illegal clicks (occupied cells or
        clicks after game over) are silently ignored.
        Args:
            row (int): Row index of the clicked cell.
            col (int): Column index of the clicked cell.
        """
        if self.game.game_over:
            return
        if not self.game.make_move(row, col):
            return  # Invalid move; ignore the click.
        self._update_board()
        self._update_status()
        if self.game.game_over and self.game.winning_line:
            self._highlight_winning_cells()
    def _update_board(self):
        """Refresh every cell button to mirror the engine's board state."""
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                value = self.game.get_cell(r, c)
                btn = self.cells[(r, c)]
                btn.config(text=value)
                if value == "X":
                    btn.config(fg=self.X_COLOR, state=tk.DISABLED)
                elif value == "O":
                    btn.config(fg=self.O_COLOR, state=tk.DISABLED)
                else:
                    btn.config(
                        text=" ",
                        fg=self.TEXT_COLOR,
                        state=tk.NORMAL if not self.game.game_over else tk.DISABLED,
                    )
    def _update_status(self):
        """Update the status label to reflect turn, win, or draw state."""
        if self.game.game_over:
            if self.game.is_draw():
                self.status_label.config(
                    text="It's a draw! 🤝",
                    bg=self.STATUS_DRAW_BG,
                    fg="#212121",
                )
            else:
                winner = self.game.winner
                color = self.X_COLOR if winner == "X" else self.O_COLOR
                self.status_label.config(
                    text=f"Player {winner} wins! 🎉",
                    bg=self.STATUS_WIN_BG,
                    fg=self.TEXT_COLOR,
                )
        else:
            player = self.game.current_player
            color = self.X_COLOR if player == "X" else self.O_COLOR
            self.status_label.config(
                text=f"Player {player}'s turn",
                bg=self.BG_COLOR,
                fg=color,
            )
    def _highlight_winning_cells(self):
        """Visually emphasize the three cells that formed the winning line."""
        for (r, c) in self.game.winning_line:
            self.cells[(r, c)].config(
                bg=self.HIGHLIGHT_COLOR,
                fg="#212121",
            )
    def _reset_game(self):
        """Reset the engine and rebuild the UI for a fresh round."""
        self.game.reset()
        for btn in self.cells.values():
            btn.config(
                text=" ",
                bg=self.CELL_COLOR,
                fg=self.TEXT_COLOR,
                state=tk.NORMAL,
            )
        self._update_status()