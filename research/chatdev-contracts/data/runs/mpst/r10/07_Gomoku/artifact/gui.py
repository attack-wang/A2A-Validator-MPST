'''
gui.py
Tkinter based graphical interface for the Gomoku game.
Draws the board, handles mouse clicks, renders stones and shows
the game status plus a result dialog when the match ends.
'''
import tkinter as tk
from tkinter import messagebox
from board import Board
from game import Game
class GomokuGUI:
    """Main application window for the Gomoku game."""
    MARGIN = 30        # pixels between canvas edge and outer grid lines
    CELL_SIZE = 38     # pixels between adjacent intersections
    STONE_RADIUS = 16  # radius of drawn stones
    def __init__(self, game):
        """Build the window, canvas and widgets for the given Game."""
        self.game = game
        self.root = tk.Tk()
        self.root.title("Gomoku - Five in a Row")
        self.root.resizable(False, False)
        board_px = self.MARGIN * 2 + self.CELL_SIZE * (game.board.size - 1)
        # Status bar
        self.status_var = tk.StringVar(value=self.game.get_status_text())
        tk.Label(self.root, textvariable=self.status_var,
                 font=("Helvetica", 14, "bold")).pack(pady=(10, 4))
        # Board canvas
        self.canvas = tk.Canvas(self.root, width=board_px, height=board_px,
                                bg="#DCB35C", highlightthickness=0)
        self.canvas.pack(padx=10, pady=4)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_hover)
        # New game button
        tk.Button(self.root, text="New Game", font=("Helvetica", 12),
                  command=self.reset_game).pack(pady=(4, 10))
        self.draw_board()
    def run(self):
        """Start the tkinter event loop."""
        self.root.mainloop()
    # ------------------------------------------------------------------ #
    # Drawing helpers
    # ------------------------------------------------------------------ #
    def _to_px(self, index):
        """Convert a board index (0..size-1) to a canvas pixel coordinate."""
        return self.MARGIN + index * self.CELL_SIZE
    def draw_board(self):
        """Draw grid lines, star points, stones and game-over highlights."""
        self.canvas.delete("all")
        size = self.game.board.size
        # Grid lines
        for i in range(size):
            p = self._to_px(i)
            self.canvas.create_line(self._to_px(0), p,
                                    self._to_px(size - 1), p,
                                    fill="#5A3A1A", width=1)
            self.canvas.create_line(p, self._to_px(0),
                                    p, self._to_px(size - 1),
                                    fill="#5A3A1A", width=1)
        # Traditional star point markers
        for r, c in [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]:
            if r < size and c < size:
                x, y = self._to_px(c), self._to_px(r)
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                                        fill="#5A3A1A", outline="")
        # Stones
        for r in range(size):
            for c in range(size):
                cell = self.game.board.get_cell(r, c)
                if cell == Board.BLACK:
                    self._draw_stone(r, c, "#000000")
                elif cell == Board.WHITE:
                    self._draw_stone(r, c, "#FFFFFF")
        # Highlight the winning line
        for r, c in self.game.winning_line:
            x, y = self._to_px(c), self._to_px(r)
            self.canvas.create_oval(x - self.STONE_RADIUS - 4,
                                    y - self.STONE_RADIUS - 4,
                                    x + self.STONE_RADIUS + 4,
                                    y + self.STONE_RADIUS + 4,
                                    outline="#FF2222", width=2)
        # Small marker on the last move (hidden when the win line is shown)
        if self.game.last_move and not self.game.winning_line:
            r, c = self.game.last_move
            x, y = self._to_px(c), self._to_px(r)
            marker = "#FFFFFF" if self.game.board.get_cell(r, c) == Board.BLACK else "#FF2222"
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                                    fill=marker, outline="", tags="preview")
    def _draw_stone(self, row, col, color):
        """Draw a single stone centred on intersection (row, col)."""
        x, y = self._to_px(col), self._to_px(row)
        self.canvas.create_oval(x - self.STONE_RADIUS, y - self.STONE_RADIUS,
                                x + self.STONE_RADIUS, y + self.STONE_RADIUS,
                                fill=color, outline="#333333", width=1)
    # ------------------------------------------------------------------ #
    # Event handling
    # ------------------------------------------------------------------ #
    def _event_to_cell(self, event):
        """Convert a mouse event to the nearest board intersection, or None."""
        col = round((event.x - self.MARGIN) / self.CELL_SIZE)
        row = round((event.y - self.MARGIN) / self.CELL_SIZE)
        if self.game.board.in_bounds(row, col):
            return row, col
        return None
    def on_click(self, event):
        """Translate a left mouse click into a board move."""
        cell = self._event_to_cell(event)
        if cell is None or self.game.is_over:
            return
        row, col = cell
        if self.game.handle_move(row, col):
            self.draw_board()
            self.status_var.set(self.game.get_status_text())
            if self.game.is_over:
                self.show_result()
    def on_hover(self, event):
        """Show a ghost stone preview at the nearest empty intersection."""
        self.canvas.delete("preview")
        if self.game.is_over:
            return
        cell = self._event_to_cell(event)
        if cell is None:
            return
        row, col = cell
        if self.game.board.get_cell(row, col) != Board.EMPTY:
            return
        x, y = self._to_px(col), self._to_px(row)
        color = "#000000" if self.game.current_player == Board.BLACK else "#FFFFFF"
        self.canvas.create_oval(x - self.STONE_RADIUS, y - self.STONE_RADIUS,
                                x + self.STONE_RADIUS, y + self.STONE_RADIUS,
                                outline=color, width=1, tags="preview")
    def show_result(self):
        """Display a dialog announcing the result and offer a rematch."""
        if self.game.state == Game.STATE_WON:
            message = (f"{self.game.PLAYER_NAMES[self.game.winner]} wins with "
                       f"five in a row!\n\nPlay again?")
        else:
            message = "The board is full - it's a draw!\n\nPlay again?"
        if messagebox.askyesno("Game Over", message):
            self.reset_game()
    def reset_game(self):
        """Start a new game and refresh the display."""
        self.game.reset()
        self.status_var.set(self.game.get_status_text())
        self.draw_board()