'''
gui.py
Tkinter-based graphical interface for the Gomoku game.
Renders the 15x15 board on a canvas, handles mouse clicks as moves,
highlights the most recent stone, shows the current turn in a status
bar, announces the result with a pop-up, and supports restarting.
'''
import tkinter as tk
from tkinter import messagebox
from board import EMPTY, BLACK, WHITE
from game import STATE_DRAW  # Regulation 1: import every referenced symbol
CELL_SIZE = 40
MARGIN = 30
STONE_RADIUS = 16
class GomokuGUI:
    """Graphical Gomoku interface built with tkinter."""
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Gomoku - Five in a Row")
        self.root.resizable(False, False)
        board_px = MARGIN * 2 + (game.board.size - 1) * CELL_SIZE
        # Status bar
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self.root, textvariable=self.status_var,
                                     font=("Helvetica", 14))
        self.status_label.pack(pady=5)
        # Canvas
        self.canvas = tk.Canvas(self.root, width=board_px, height=board_px,
                                bg="#DCB35C")  # wooden board color
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        # New game button
        self.reset_button = tk.Button(self.root, text="New Game",
                                      font=("Helvetica", 12),
                                      command=self.reset_game)
        self.reset_button.pack(pady=5)
        self.draw_board()
        self.update_status()
    def run(self):
        """Start the tkinter event loop (called by main.py)."""
        self.root.mainloop()
    def to_pixel(self, index):
        """Convert a board index (0-based) to a pixel coordinate."""
        return MARGIN + index * CELL_SIZE
    def to_index(self, pixel):
        """Convert a pixel coordinate to the nearest board index."""
        return round((pixel - MARGIN) / CELL_SIZE)
    def draw_board(self):
        """Draw grid lines and star points."""
        size = self.game.board.size
        for i in range(size):
            self.canvas.create_line(self.to_pixel(0), self.to_pixel(i),
                                    self.to_pixel(size - 1), self.to_pixel(i))
            self.canvas.create_line(self.to_pixel(i), self.to_pixel(0),
                                    self.to_pixel(i), self.to_pixel(size - 1))
        # Star points
        stars = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
        for r, c in stars:
            if r < size and c < size:
                x, y = self.to_pixel(c), self.to_pixel(r)
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
    def draw_stones(self):
        """Draw all stones currently on the board, plus last-move marker."""
        board = self.game.board
        for r in range(board.size):
            for c in range(board.size):
                stone = board.get_stone(r, c)
                if stone != EMPTY:
                    self.draw_stone(r, c, stone)
        # Highlight the most recent move with a small red dot
        if self.game.last_move:
            r, c = self.game.last_move
            x, y = self.to_pixel(c), self.to_pixel(r)
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                                    fill="red", outline="red")
    def draw_stone(self, row, col, stone):
        """Draw a single stone centred on the intersection (row, col)."""
        x, y = self.to_pixel(col), self.to_pixel(row)
        fill = "black" if stone == BLACK else "white"
        self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                x + STONE_RADIUS, y + STONE_RADIUS,
                                fill=fill, outline="black", width=1)
    def redraw(self):
        """Clear the canvas and redraw board + stones."""
        self.canvas.delete("all")
        self.draw_board()
        self.draw_stones()
    def on_click(self, event):
        """Translate a left-click into a board move and refresh the view."""
        if self.game.is_over():
            return
        row = self.to_index(event.y)
        col = self.to_index(event.x)
        if not (0 <= row < self.game.board.size and 0 <= col < self.game.board.size):
            return
        accepted = self.game.make_move(row, col)
        if not accepted:
            return
        self.redraw()
        self.update_status()
        if self.game.is_over():
            self.announce_result()
    def update_status(self):
        """Refresh the status bar text."""
        if self.game.is_over():
            if self.game.state == STATE_DRAW:
                self.status_var.set("Game over: it's a draw!")
            else:
                self.status_var.set(f"Game over: {self.game.winner} wins!")
        else:
            self.status_var.set(f"{self.game.current_player}'s turn")
    def announce_result(self):
        """Show a pop-up announcing the final result."""
        if self.game.state == STATE_DRAW:
            messagebox.showinfo("Gomoku", "The game is a draw!")
        else:
            messagebox.showinfo("Gomoku", f"{self.game.winner} wins with five in a row!")
    def reset_game(self):
        """Restart the match and refresh the view."""
        self.game.reset()
        self.redraw()
        self.update_status()