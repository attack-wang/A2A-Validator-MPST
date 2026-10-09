'''
gui.py
Tkinter-based graphical interface for the 2048 game. Renders the board
and tiles, displays the current score and highest tile, handles arrow
key input, and shows a game-over overlay with restart support.
'''
import tkinter as tk
from constants import (
    GRID_SIZE, CELL_SIZE, CELL_PADDING, BOARD_PADDING,
    BOARD_WIDTH, BOARD_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT,
    WINDOW_MARGIN, WINDOW_BG_COLOR, BOARD_COLOR, EMPTY_CELL_COLOR,
    TEXT_COLOR_DARK, TEXT_COLOR_LIGHT, SCORE_BOX_COLOR,
    SCORE_LABEL_COLOR, SCORE_VALUE_COLOR, BUTTON_BG_COLOR,
    BUTTON_FG_COLOR, NEW_TILE_BORDER_COLOR, GAME_OVER_OVERLAY_COLOR,
    TILE_COLORS, DEFAULT_TILE_COLOR,
    FONT_FAMILY, TITLE_FONT_SIZE, SCORE_LABEL_FONT_SIZE,
    SCORE_VALUE_FONT_SIZE, BUTTON_FONT_SIZE,
)
from game_logic import Game2048
class GameGUI:
    """Main application window: board canvas, score header, and input handling."""
    # Maps keyboard events to game directions (arrow keys + WASD).
    KEY_BINDINGS = {
        "Up": "up", "Down": "down", "Left": "left", "Right": "right",
        "w": "up", "a": "left", "s": "down", "d": "right",
        "W": "up", "A": "left", "S": "down", "D": "right",
    }
    def __init__(self, game):
        """Build the window, widgets, key bindings, and initial display."""
        self.game = game
        self.root = tk.Tk()
        self.root.title("2048")
        self.root.configure(bg=WINDOW_BG_COLOR)
        self.root.resizable(False, False)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self._build_header()
        self._build_board()
        self._bind_keys()
        self._update_display()
    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_header(self):
        """Create the title, score boxes, and new-game button."""
        header = tk.Frame(self.root, bg=WINDOW_BG_COLOR,
                          width=WINDOW_WIDTH, height=130)
        header.pack(fill="x")
        header.pack_propagate(False)
        # Title on the left
        title = tk.Label(header, text="2048", bg=WINDOW_BG_COLOR,
                         fg=TEXT_COLOR_DARK,
                         font=(FONT_FAMILY, TITLE_FONT_SIZE, "bold"))
        title.place(x=WINDOW_MARGIN, y=14)
        subtitle = tk.Label(header, text="Join the tiles, reach 2048!",
                            bg=WINDOW_BG_COLOR, fg=TEXT_COLOR_DARK,
                            font=(FONT_FAMILY, 11))
        subtitle.place(x=WINDOW_MARGIN, y=78)
        # Score boxes on the right
        box_w, box_h = 90, 60
        self.score_value_label = self._make_score_box(
            header, "SCORE", box_w, box_h,
            x=WINDOW_WIDTH - WINDOW_MARGIN - 2 * (box_w + 10), y=20)
        self.highest_value_label = self._make_score_box(
            header, "HIGHEST", box_w, box_h,
            x=WINDOW_WIDTH - WINDOW_MARGIN - box_w, y=20)
        # New game button under the score boxes
        new_game_btn = tk.Button(header, text="New Game", command=self._restart,
                                 bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR,
                                 activebackground=TEXT_COLOR_DARK,
                                 activeforeground=BUTTON_FG_COLOR,
                                 relief="flat", cursor="hand2",
                                 font=(FONT_FAMILY, BUTTON_FONT_SIZE, "bold"))
        new_game_btn.place(x=WINDOW_WIDTH - WINDOW_MARGIN - box_w, y=88,
                           width=box_w, height=26)
    def _make_score_box(self, parent, label, width, height, x, y):
        """Create one score box (label + value) and return its value label."""
        box = tk.Frame(parent, bg=SCORE_BOX_COLOR, width=width, height=height)
        box.place(x=x, y=y)
        box.pack_propagate(False)
        label_widget = tk.Label(box, text=label, bg=SCORE_BOX_COLOR,
                                fg=SCORE_LABEL_COLOR,
                                font=(FONT_FAMILY, SCORE_LABEL_FONT_SIZE, "bold"))
        label_widget.pack(pady=(8, 0))
        value_widget = tk.Label(box, text="0", bg=SCORE_BOX_COLOR,
                                fg=SCORE_VALUE_COLOR,
                                font=(FONT_FAMILY, SCORE_VALUE_FONT_SIZE, "bold"))
        value_widget.pack()
        return value_widget
    def _build_board(self):
        """Create the canvas on which the board and tiles are drawn."""
        self.canvas = tk.Canvas(self.root, width=BOARD_WIDTH, height=BOARD_HEIGHT,
                                bg=BOARD_COLOR, highlightthickness=0)
        self.canvas.pack(padx=WINDOW_MARGIN, pady=(0, WINDOW_MARGIN))
    def _bind_keys(self):
        """Bind keyboard events for movement and restart."""
        self.root.bind("<Key>", self._on_key)
    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def _on_key(self, event):
        """Respond to arrow keys (moves), R (restart); ignore the rest."""
        key = event.keysym
        if key in self.KEY_BINDINGS:
            self.game.move(self.KEY_BINDINGS[key])
            self._update_display()
        elif key in ("r", "R"):
            self._restart()
    def _restart(self):
        """Reset the game state and refresh the display."""
        self.game.reset()
        self._update_display()
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def _cell_origin(self, row, col):
        """Return the pixel (x, y) of a cell's top-left corner."""
        x = BOARD_PADDING + col * (CELL_SIZE + CELL_PADDING)
        y = BOARD_PADDING + row * (CELL_SIZE + CELL_PADDING)
        return x, y
    def _draw_background(self):
        """Draw the board background and empty cell slots."""
        self.canvas.delete("all")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x, y = self._cell_origin(row, col)
                self.canvas.create_rectangle(
                    x, y, x + CELL_SIZE, y + CELL_SIZE,
                    fill=EMPTY_CELL_COLOR, outline="")
    def _draw_tiles(self):
        """Draw every non-empty tile with value-appropriate color and font."""
        grid = self.game.get_grid()
        last_spawn = self.game.get_last_spawn()
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = grid[row][col]
                if value == 0:
                    continue
                x, y = self._cell_origin(row, col)
                fill = TILE_COLORS.get(value, DEFAULT_TILE_COLOR)
                outline = NEW_TILE_BORDER_COLOR if (row, col) == last_spawn else ""
                self.canvas.create_rectangle(
                    x, y, x + CELL_SIZE, y + CELL_SIZE,
                    fill=fill, outline=outline, width=3)
                self.canvas.create_text(
                    x + CELL_SIZE // 2, y + CELL_SIZE // 2,
                    text=str(value),
                    fill=TEXT_COLOR_LIGHT if value > 4 else TEXT_COLOR_DARK,
                    font=(FONT_FAMILY, self._font_size_for(value), "bold"))
    @staticmethod
    def _font_size_for(value):
        """Pick a font size so the tile number fits inside its cell."""
        digits = len(str(value))
        if digits <= 2:
            return 36
        if digits == 3:
            return 30
        if digits == 4:
            return 24
        return 18
    def _update_display(self):
        """Redraw the board and refresh score/highest-tile labels."""
        self._draw_background()
        self._draw_tiles()
        self.score_value_label.config(text=str(self.game.get_score()))
        self.highest_value_label.config(text=str(self.game.get_highest_tile()))
        if self.game.is_game_over():
            self._draw_game_over_overlay()
    def _draw_game_over_overlay(self):
        """Draw a translucent overlay announcing the game is over."""
        self.canvas.create_rectangle(
            0, 0, BOARD_WIDTH, BOARD_HEIGHT,
            fill=GAME_OVER_OVERLAY_COLOR, stipple="gray50", outline="")
        self.canvas.create_text(
            BOARD_WIDTH // 2, BOARD_HEIGHT // 2 - 40,
            text="Game Over!", fill=TEXT_COLOR_LIGHT,
            font=(FONT_FAMILY, 34, "bold"))
        self.canvas.create_text(
            BOARD_WIDTH // 2, BOARD_HEIGHT // 2 + 5,
            text=f"Final Score: {self.game.get_score()}",
            fill=TEXT_COLOR_LIGHT, font=(FONT_FAMILY, 18, "bold"))
        self.canvas.create_text(
            BOARD_WIDTH // 2, BOARD_HEIGHT // 2 + 45,
            text=f"Highest Tile: {self.game.get_highest_tile()}",
            fill=TEXT_COLOR_LIGHT, font=(FONT_FAMILY, 16))
        self.canvas.create_text(
            BOARD_WIDTH // 2, BOARD_HEIGHT // 2 + 85,
            text="Press R or click 'New Game' to restart",
            fill=TEXT_COLOR_LIGHT, font=(FONT_FAMILY, 13))
    def run(self):
        """Start the tkinter main event loop."""
        self.root.mainloop()