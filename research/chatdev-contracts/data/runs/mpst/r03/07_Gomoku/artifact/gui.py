'''
gui.py
Tkinter-based graphical interface for the Gomoku game. Renders the
board and stones, converts mouse clicks into board coordinates, and
displays turn/win/draw status messages.
'''
import tkinter as tk
from constants import (
    BOARD_SIZE, EMPTY, BLACK, WHITE,
    CELL_SIZE, MARGIN, STONE_RADIUS, CANVAS_SIZE,
    COLOR_BACKGROUND, COLOR_GRID_LINE, COLOR_STAR_POINT,
    COLOR_BLACK_STONE, COLOR_WHITE_STONE, COLOR_STONE_OUTLINE,
    COLOR_LAST_MOVE, COLOR_WIN_LINE, COLOR_STATUS_BG,
    STAR_POINTS, BLACK_NAME, WHITE_NAME,
)
from game import Game
class GomokuGUI:
    """Main application window: board canvas, status bar, and controls."""
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title("Gomoku - Five in a Row")
        self.root.resizable(False, False)
        self._setup_widgets()
        self.redraw()
    def _setup_widgets(self):
        """Build the canvas, status label, and control buttons."""
        self.canvas = tk.Canvas(
            self.root, width=CANVAS_SIZE, height=CANVAS_SIZE,
            bg=COLOR_BACKGROUND, highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=(10, 5))
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.status_label = tk.Label(
            self.root, text="", font=("Helvetica", 14, "bold"),
            bg=COLOR_STATUS_BG, fg="#333333", pady=8,
        )
        self.status_label.pack(fill=tk.X, padx=10)
        button_frame = tk.Frame(self.root, bg=COLOR_STATUS_BG)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.reset_button = tk.Button(
            button_frame, text="New Game", font=("Helvetica", 12),
            command=self.reset_game,
        )
        self.reset_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.quit_button = tk.Button(
            button_frame, text="Quit", font=("Helvetica", 12),
            command=self.root.destroy,
        )
        self.quit_button.pack(side=tk.RIGHT, padx=5, pady=5)
    # --- Coordinate conversion -------------------------------------------
    def pixel_to_board(self, x, y):
        """
        Convert canvas pixel coordinates to the nearest board intersection.
        Returns (row, col) or None if the click is off-board or too far away.
        """
        col = round((x - MARGIN) / CELL_SIZE)
        row = round((y - MARGIN) / CELL_SIZE)
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return None
        px = MARGIN + col * CELL_SIZE
        py = MARGIN + row * CELL_SIZE
        if abs(x - px) > CELL_SIZE / 2 or abs(y - py) > CELL_SIZE / 2:
            return None
        return row, col
    def board_to_pixel(self, row, col):
        """Return the canvas center point of the intersection (row, col)."""
        return MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE
    # --- Drawing ----------------------------------------------------------
    def draw_grid(self):
        """Draw the 15x15 grid lines and star point markers."""
        last = MARGIN + (BOARD_SIZE - 1) * CELL_SIZE
        for i in range(BOARD_SIZE):
            pos = MARGIN + i * CELL_SIZE
            width = 2 if i in (0, BOARD_SIZE - 1) else 1
            self.canvas.create_line(MARGIN, pos, last, pos,
                                    fill=COLOR_GRID_LINE, width=width)
            self.canvas.create_line(pos, MARGIN, pos, last,
                                    fill=COLOR_GRID_LINE, width=width)
        for row, col in STAR_POINTS:
            x, y = self.board_to_pixel(row, col)
            r = 4
            self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                    fill=COLOR_STAR_POINT, outline="")
    def draw_stone(self, row, col, stone):
        """Draw a single black or white stone at (row, col)."""
        x, y = self.board_to_pixel(row, col)
        fill = COLOR_BLACK_STONE if stone == BLACK else COLOR_WHITE_STONE
        self.canvas.create_oval(
            x - STONE_RADIUS, y - STONE_RADIUS,
            x + STONE_RADIUS, y + STONE_RADIUS,
            fill=fill, outline=COLOR_STONE_OUTLINE, width=1,
        )
    def draw_last_move_marker(self):
        """Put a small red dot on the most recently placed stone."""
        if self.game.last_move is None:
            return
        row, col = self.game.last_move
        x, y = self.board_to_pixel(row, col)
        r = 4
        self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                fill=COLOR_LAST_MOVE, outline="")
    def draw_winning_line(self):
        """Draw a highlight line through the five winning stones."""
        if not self.game.winning_line:
            return
        points = []
        for row, col in self.game.winning_line:
            x, y = self.board_to_pixel(row, col)
            points.extend([x, y])
        self.canvas.create_line(*points, fill=COLOR_WIN_LINE, width=3)
    def redraw(self):
        """Repaint the entire board, stones, markers, and status text."""
        self.canvas.delete("all")
        self.draw_grid()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                stone = self.game.board.get_stone(row, col)
                if stone != EMPTY:
                    self.draw_stone(row, col, stone)
        self.draw_last_move_marker()
        self.draw_winning_line()
        self.update_status()
    # --- Event handling ----------------------------------------------------
    def on_canvas_click(self, event):
        """Handle a left click: place a stone if the move is legal."""
        move = self.pixel_to_board(event.x, event.y)
        if move is None:
            return
        row, col = move
        if self.game.make_move(row, col):
            self.redraw()
    def update_status(self):
        """Refresh the status bar text according to the game state."""
        if self.game.game_over:
            if self.game.winner is None:
                text = "It's a draw! Board is full."
            else:
                name = BLACK_NAME if self.game.winner == BLACK else WHITE_NAME
                text = f"{name} wins with five in a row! Click 'New Game' to play again."
        else:
            name = self.game.current_player_name
            text = f"{name}'s turn - click an intersection to place a stone."
        self.status_label.config(text=text)
    def reset_game(self):
        """Start a fresh game and repaint the board."""
        self.game.reset()
        self.redraw()