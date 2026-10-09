'''
gui.py
This module implements a tkinter-based graphical user interface for the
Gomoku game, including board rendering, click handling, status display,
winning-line highlighting, and game restart functionality.
'''
import tkinter as tk
from tkinter import messagebox
from board import Board
from game import GomokuGame
class GomokuGUI:
    """Tkinter GUI for the Gomoku game."""
    CELL_SIZE = 40
    MARGIN = 30
    STONE_RADIUS = 16
    BOARD_BG = "#DCB35C"  # wooden board color
    LINE_COLOR = "#5A3A1A"
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku - Five in a Row")
        self.root.resizable(False, False)
        self.game = GomokuGame()
        self.board_size = self.game.board.size
        self.canvas_size = self.MARGIN * 2 + self.CELL_SIZE * (self.board_size - 1)
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Black player's turn - click an intersection to place a stone")
        status_label = tk.Label(root, textvariable=self.status_var,
                                font=("Helvetica", 13, "bold"))
        status_label.pack(pady=(8, 4))
        # Canvas
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size,
                                bg=self.BOARD_BG, highlightthickness=1,
                                highlightbackground="black")
        self.canvas.pack(padx=12, pady=6)
        self.canvas.bind("<Button-1>", self.on_click)
        # Buttons frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=(2, 10))
        restart_btn = tk.Button(button_frame, text="New Game", font=("Helvetica", 12),
                                width=12, command=self.restart)
        restart_btn.pack()
        self.draw_board()
        self.update_status()
    def draw_board(self):
        """Draw the grid lines, star points, and coordinate labels."""
        pad = self.MARGIN
        step = self.CELL_SIZE
        end = pad + (self.board_size - 1) * step
        for i in range(self.board_size):
            # horizontal line
            self.canvas.create_line(pad, pad + i * step, end, pad + i * step,
                                    fill=self.LINE_COLOR, width=1)
            # vertical line
            self.canvas.create_line(pad + i * step, pad, pad + i * step, end,
                                    fill=self.LINE_COLOR, width=1)
        # border slightly thicker
        self.canvas.create_rectangle(pad, pad, end, end,
                                     outline=self.LINE_COLOR, width=2)
        # star points
        stars = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
        for r, c in stars:
            cx = pad + c * step
            cy = pad + r * step
            self.canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3,
                                    fill=self.LINE_COLOR, outline=self.LINE_COLOR)
        # coordinate labels
        for i in range(self.board_size):
            self.canvas.create_text(pad + i * step, pad - 14, text=str(i),
                                    font=("Helvetica", 9), fill="#333333")
            self.canvas.create_text(pad - 16, pad + i * step, text=str(i),
                                    font=("Helvetica", 9), fill="#333333")
    def draw_stone(self, row, col, stone):
        """Draw a black or white stone at (row, col)."""
        cx = self.MARGIN + col * self.CELL_SIZE
        cy = self.MARGIN + row * self.CELL_SIZE
        r = self.STONE_RADIUS
        fill = "black" if stone == Board.BLACK else "white"
        outline = "black"
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                fill=fill, outline=outline, width=1)
    def draw_last_move_marker(self):
        """Draw a small marker on the most recent move, based on the
        true last move tracked by the Board (not the last stone drawn)."""
        self.canvas.delete("lastmove")
        if not self.game.board.last_move:
            return
        lr, lc = self.game.board.last_move
        stone = self.game.board.get_stone(lr, lc)
        cx = self.MARGIN + lc * self.CELL_SIZE
        cy = self.MARGIN + lr * self.CELL_SIZE
        marker_r = 4
        marker_color = "white" if stone == Board.BLACK else "black"
        self.canvas.create_oval(cx - marker_r, cy - marker_r,
                                cx + marker_r, cy + marker_r,
                                fill=marker_color, outline=marker_color,
                                tags="lastmove")
    def redraw_all_stones(self):
        """Clear stones and redraw every stone currently on the board."""
        self.canvas.delete("all")
        self.draw_board()
        for r in range(self.board_size):
            for c in range(self.board_size):
                stone = self.game.board.get_stone(r, c)
                if stone != Board.EMPTY:
                    self.draw_stone(r, c, stone)
        self.draw_last_move_marker()
        self.highlight_winning_line()
    def highlight_winning_line(self):
        """Draw a highlight around the five winning stones, if any."""
        if not self.game.winning_line:
            return
        pad = self.MARGIN
        step = self.CELL_SIZE
        for (r, c) in self.game.winning_line:
            cx = pad + c * step
            cy = pad + r * step
            self.canvas.create_oval(cx - self.STONE_RADIUS - 3, cy - self.STONE_RADIUS - 3,
                                    cx + self.STONE_RADIUS + 3, cy + self.STONE_RADIUS + 3,
                                    outline="red", width=2)
    def on_click(self, event):
        """Handle a left-click on the canvas: place a stone if valid."""
        if self.game.state != GomokuGame.STATE_ONGOING:
            return
        col = round((event.x - self.MARGIN) / self.CELL_SIZE)
        row = round((event.y - self.MARGIN) / self.CELL_SIZE)
        if not self.game.board.is_in_bounds(row, col):
            return
        if not self.game.make_move(row, col):
            return
        self.draw_stone(row, col, self.game.board.get_stone(row, col))
        self.draw_last_move_marker()
        self.highlight_winning_line()
        self.update_status()
        if self.game.state == GomokuGame.STATE_WON:
            winner = self.game.winner
            messagebox.showinfo("Game Over",
                                f"{winner.name} ({winner.stone_name}) wins with five in a row!")
        elif self.game.state == GomokuGame.STATE_DRAW:
            messagebox.showinfo("Game Over", "The board is full. It's a draw!")
    def update_status(self):
        """Update the status bar text according to the game state."""
        if self.game.state == GomokuGame.STATE_WON:
            winner = self.game.winner
            self.status_var.set(f"{winner.name} ({winner.stone_name}) wins! "
                                "Click 'New Game' to play again.")
        elif self.game.state == GomokuGame.STATE_DRAW:
            self.status_var.set("It's a draw! Click 'New Game' to play again.")
        else:
            player = self.game.get_current_player()
            self.status_var.set(f"{player.name} ({player.stone_name})'s turn - "
                                "click an intersection to place a stone")
    def restart(self):
        """Reset the game and redraw the empty board."""
        self.game.reset()
        self.redraw_all_stones()
        self.update_status()