'''
gui.py
This module implements the Tkinter-based graphical interface for the
Gomoku game. It renders the 15x15 board, draws stones, handles mouse
clicks for stone placement, displays the current turn, marks the last
move, and announces the winner with a highlighted winning line.
'''
import tkinter as tk
from tkinter import messagebox
from constants import (
    BOARD_SIZE, CELL_SIZE, MARGIN, STONE_RADIUS, STAR_RADIUS, LINE_WIDTH,
    LAST_MOVE_MARKER_RADIUS, CANVAS_SIZE, BLACK, WHITE, EMPTY,
    STATE_BLACK_WINS, STATE_WHITE_WINS, STATE_DRAW,
    COLOR_BOARD, COLOR_GRID, COLOR_STAR,
    COLOR_BLACK_STONE, COLOR_WHITE_STONE, COLOR_HIGHLIGHT,
    COLOR_BG, COLOR_TEXT, WINDOW_TITLE, STATUS_FONT, BUTTON_FONT,
)
from game import Game
class GomokuGUI:
    """Tkinter interface that visualizes the board and handles user input."""
    def __init__(self, root, game):
        """Construct the window, canvas, status bar, and control buttons."""
        self.root = root
        self.game = game
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)
        # Status label showing whose turn it is or the result
        self.status_label = tk.Label(
            root, text="", font=STATUS_FONT, bg=COLOR_BG, fg=COLOR_TEXT
        )
        self.status_label.pack(pady=(10, 5))
        # Canvas for the board
        self.canvas = tk.Canvas(
            root, width=CANVAS_SIZE, height=CANVAS_SIZE,
            bg=COLOR_BOARD, highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=5)
        self.canvas.bind("<Button-1>", self.on_click)
        # Control buttons
        button_frame = tk.Frame(root, bg=COLOR_BG)
        button_frame.pack(pady=(5, 10))
        self.reset_button = tk.Button(
            button_frame, text="New Game", font=BUTTON_FONT,
            command=self.reset_game
        )
        self.reset_button.pack()
        self.stone_ids = {}  # (row, col) -> canvas item id
        self.last_move_marker_id = None  # Canvas id of the last-move marker
        self.draw_board()
        self.update_status()
    def draw_board(self):
        """Draw the grid lines and star point markers on the canvas."""
        # Grid lines
        for i in range(BOARD_SIZE):
            x = MARGIN + i * CELL_SIZE
            self.canvas.create_line(
                x, MARGIN, x, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE,
                width=LINE_WIDTH, fill=COLOR_GRID
            )
            y = MARGIN + i * CELL_SIZE
            self.canvas.create_line(
                MARGIN, y, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, y,
                width=LINE_WIDTH, fill=COLOR_GRID
            )
        # Star points (hoshi) at traditional positions for a 15x15 board
        star_indices = [3, 7, 11]
        for r in star_indices:
            for c in star_indices:
                cx = MARGIN + c * CELL_SIZE
                cy = MARGIN + r * CELL_SIZE
                self.canvas.create_oval(
                    cx - STAR_RADIUS, cy - STAR_RADIUS,
                    cx + STAR_RADIUS, cy + STAR_RADIUS,
                    fill=COLOR_STAR, outline=COLOR_STAR
                )
    def draw_stone(self, row, col, player):
        """Draw a black or white stone at the given intersection."""
        cx = MARGIN + col * CELL_SIZE
        cy = MARGIN + row * CELL_SIZE
        if player == BLACK:
            fill = COLOR_BLACK_STONE
            outline = COLOR_BLACK_STONE
        else:
            fill = COLOR_WHITE_STONE
            outline = COLOR_GRID
        stone_id = self.canvas.create_oval(
            cx - STONE_RADIUS, cy - STONE_RADIUS,
            cx + STONE_RADIUS, cy + STONE_RADIUS,
            fill=fill, outline=outline, width=1
        )
        self.stone_ids[(row, col)] = stone_id
    def draw_last_move_marker(self, row, col):
        """Draw a small contrast dot on the most recently placed stone."""
        if self.last_move_marker_id is not None:
            self.canvas.delete(self.last_move_marker_id)
        cx = MARGIN + col * CELL_SIZE
        cy = MARGIN + row * CELL_SIZE
        player = self.game.board.get_stone(row, col)
        marker_color = COLOR_WHITE_STONE if player == BLACK else COLOR_BLACK_STONE
        self.last_move_marker_id = self.canvas.create_oval(
            cx - LAST_MOVE_MARKER_RADIUS, cy - LAST_MOVE_MARKER_RADIUS,
            cx + LAST_MOVE_MARKER_RADIUS, cy + LAST_MOVE_MARKER_RADIUS,
            fill=marker_color, outline=marker_color
        )
    def on_click(self, event):
        """Translate a canvas click into board coordinates and play a move."""
        if self.game.is_over:
            return
        col = round((event.x - MARGIN) / CELL_SIZE)
        row = round((event.y - MARGIN) / CELL_SIZE)
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return
        if not self.game.board.is_empty(row, col):
            return
        player = self.game.current_player
        if self.game.make_move(row, col):
            self.draw_stone(row, col, player)
            self.draw_last_move_marker(row, col)
            self.handle_state_change()
    def handle_state_change(self):
        """React to the game state after a move: win, draw, or next turn."""
        state = self.game.state
        if state == STATE_BLACK_WINS or state == STATE_WHITE_WINS:
            self.highlight_win(self.game.winning_cells)
            self.update_status()
            winner = "Black" if state == STATE_BLACK_WINS else "White"
            messagebox.showinfo("Game Over", f"{winner} wins!")
        elif state == STATE_DRAW:
            self.update_status()
            messagebox.showinfo("Game Over", "It's a draw!")
        else:
            self.update_status()
    def highlight_win(self, cells):
        """Highlight the five (or more) winning stones."""
        for (row, col) in cells:
            stone_id = self.stone_ids.get((row, col))
            if stone_id is not None:
                self.canvas.itemconfig(stone_id, outline=COLOR_HIGHLIGHT, width=3)
    def update_status(self):
        """Refresh the status label with the current turn or result."""
        if self.game.state == STATE_BLACK_WINS:
            text = "Black wins! Click 'New Game' to play again."
        elif self.game.state == STATE_WHITE_WINS:
            text = "White wins! Click 'New Game' to play again."
        elif self.game.state == STATE_DRAW:
            text = "Draw! Click 'New Game' to play again."
        elif self.game.current_player == BLACK:
            text = "Black's turn"
        else:
            text = "White's turn"
        self.status_label.config(text=text)
    def reset_game(self):
        """Start a fresh game: clear the board and reset state."""
        self.game.reset()
        self.canvas.delete("all")
        self.stone_ids = {}
        self.last_move_marker_id = None  # Marker was deleted with canvas clear
        self.draw_board()
        self.update_status()