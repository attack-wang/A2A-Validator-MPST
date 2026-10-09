'''
game_ui.py
Tkinter-based graphical front-end for the 2048 game.
Responsibilities:
- create the game window and render the 4x4 board,
- draw every tile with the classic 2048 colour palette,
- display the current score and the highest tile reached,
- capture arrow-key (and WASD) input and forward it to the game logic,
- show "You win" / "Game over" overlays,
- support restarting the game with the R key.
Uses only the Python standard library (tkinter) - no external packages needed.
'''
import tkinter as tk
from game_logic import Game2048
class GameUI:
    """Graphical 2048 client built on top of the Game2048 logic class."""
    # ------------------------- layout constants ------------------------ #
    GRID_SIZE = 4
    CELL_SIZE = 100
    GAP = 10
    PADDING = 15
    HEADER_HEIGHT = 130
    GRID_PIXELS = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * GAP  # 450 px
    WINDOW_WIDTH = GRID_PIXELS + 2 * PADDING                     # 480 px
    WINDOW_HEIGHT = HEADER_HEIGHT + GRID_PIXELS + 2 * PADDING    # 610 px
    # ----------------------------- colours ----------------------------- #
    COLOR_WINDOW = "#faf8ef"
    COLOR_BOARD = "#bbada0"
    COLOR_EMPTY = "#cdc1b4"
    COLOR_TEXT_DARK = "#776e65"
    COLOR_TEXT_LIGHT = "#f9f6f2"
    COLOR_SCORE_BOX = "#bbada0"
    COLOR_OVERLAY = "#eee4da"
    TILE_COLORS = {
        2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
        16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
        128: "#edcf72", 256: "#edcc61", 512: "#edc850",
        1024: "#edc53f", 2048: "#edc22e",
    }
    TILE_COLOR_SUPER = "#3c3a32"  # tiles above 2048
    TILE_FONT_SIZES = {1: 46, 2: 42, 3: 34, 4: 26, 5: 20}
    KEY_MAP = {
        "Left": "left", "Right": "right", "Up": "up", "Down": "down",
        "a": "left", "d": "right", "w": "up", "s": "down",
        "A": "left", "D": "right", "W": "up", "S": "down",
    }
    def __init__(self):
        self.game = Game2048(self.GRID_SIZE)
        self.win_dismissed = False
        self.root = tk.Tk()
        self.root.title("2048 - ChatDev Edition")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLOR_WINDOW)
        self.canvas = tk.Canvas(
            self.root,
            width=self.WINDOW_WIDTH,
            height=self.WINDOW_HEIGHT,
            bg=self.COLOR_WINDOW,
            highlightthickness=0,
        )
        self.canvas.pack()
        # keyboard bindings (arrow keys + WASD + R to restart)
        self.root.bind("<Key>", self._on_key)
        self._render()
        self.root.mainloop()
    # ----------------------------- helpers ----------------------------- #
    def _tile_color(self, value):
        if value == 0:
            return self.COLOR_EMPTY
        return self.TILE_COLORS.get(value, self.TILE_COLOR_SUPER)
    def _tile_text_color(self, value):
        return self.COLOR_TEXT_DARK if value in (2, 4) else self.COLOR_TEXT_LIGHT
    # ----------------------------- drawing ----------------------------- #
    def _draw_tile(self, value, x, y):
        color = self._tile_color(value)
        self.canvas.create_rectangle(
            x, y, x + self.CELL_SIZE, y + self.CELL_SIZE,
            fill=color, outline="", width=0,
        )
        if value == 0:
            return
        digits = len(str(value))
        font_size = self.TILE_FONT_SIZES.get(digits, self.TILE_FONT_SIZES[5])
        self.canvas.create_text(
            x + self.CELL_SIZE // 2, y + self.CELL_SIZE // 2,
            text=str(value),
            fill=self._tile_text_color(value),
            font=("Helvetica", font_size, "bold"),
        )
    def _draw_header(self):
        # title + subtitle
        self.canvas.create_text(
            self.PADDING + 2, 45, anchor="w",
            text="2048", fill=self.COLOR_TEXT_DARK,
            font=("Helvetica", 44, "bold"),
        )
        self.canvas.create_text(
            self.PADDING, 88, anchor="w",
            text="Join the tiles, reach 2048!",
            fill=self.COLOR_TEXT_DARK,
            font=("Helvetica", 13),
        )
        hint = "Arrows / WASD to move - R to restart"
        self.canvas.create_text(
            self.PADDING, self.HEADER_HEIGHT - 12, anchor="w",
            text=hint, fill=self.COLOR_TEXT_DARK,
            font=("Helvetica", 11),
        )
        # score boxes (right aligned): BEST TILE and SCORE
        box_w, box_h = 115, 62
        box_y = 18
        score_x = self.WINDOW_WIDTH - self.PADDING - box_w
        best_x = score_x - self.GAP - box_w
        for x, label, value in ((best_x, "BEST TILE", self.game.highest_tile),
                                (score_x, "SCORE", self.game.score)):
            self.canvas.create_rectangle(
                x, box_y, x + box_w, box_y + box_h,
                fill=self.COLOR_SCORE_BOX, outline="", width=0,
            )
            self.canvas.create_text(
                x + box_w // 2, box_y + 18,
                text=label, fill=self.COLOR_TEXT_LIGHT,
                font=("Helvetica", 11, "bold"),
            )
            self.canvas.create_text(
                x + box_w // 2, box_y + 42,
                text=str(value), fill=self.COLOR_TEXT_LIGHT,
                font=("Helvetica", 18, "bold"),
            )
    def _draw_grid(self):
        board_x = self.PADDING
        board_y = self.HEADER_HEIGHT
        self.canvas.create_rectangle(
            board_x, board_y,
            board_x + self.GRID_PIXELS, board_y + self.GRID_PIXELS,
            fill=self.COLOR_BOARD, outline="", width=0,
        )
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                x = board_x + self.GAP + c * (self.CELL_SIZE + self.GAP)
                y = board_y + self.GAP + r * (self.CELL_SIZE + self.GAP)
                self._draw_tile(self.game.grid[r][c], x, y)
    def _draw_overlays(self):
        """Draw the win / game-over translucent overlay when appropriate."""
        show_win = self.game.won and not self.win_dismissed
        show_over = self.game.is_game_over()
        if not (show_win or show_over):
            return
        board_x = self.PADDING
        board_y = self.HEADER_HEIGHT
        # tkinter has no alpha blending; use a solid overlay colour instead
        self.canvas.create_rectangle(
            board_x, board_y,
            board_x + self.GRID_PIXELS, board_y + self.GRID_PIXELS,
            fill=self.COLOR_OVERLAY, outline="", width=0,
        )
        if show_over:
            big, small = "Game over!", "Press R to restart"
        else:
            big, small = "You win!", "Press any arrow key to keep going"
        cx = board_x + self.GRID_PIXELS // 2
        cy = board_y + self.GRID_PIXELS // 2
        self.canvas.create_text(
            cx, cy - 20, text=big,
            fill=self.COLOR_TEXT_DARK,
            font=("Helvetica", 40, "bold"),
        )
        self.canvas.create_text(
            cx, cy + 30, text=small,
            fill=self.COLOR_TEXT_DARK,
            font=("Helvetica", 15),
        )
    def _render(self):
        self.canvas.delete("all")
        self._draw_header()
        self._draw_grid()
        self._draw_overlays()
    # ----------------------------- input ------------------------------- #
    def _on_key(self, event):
        key = event.keysym
        if key in ("r", "R"):
            self.game.reset()
            self.win_dismissed = False
            self._render()
            return
        direction = self.KEY_MAP.get(key)
        if direction is None:
            return
        if self.game.is_game_over():
            return  # no moves possible; wait for restart
        if self.game.won and not self.win_dismissed:
            self.win_dismissed = True  # dismiss win overlay, keep playing
        self.game.move(direction)
        self._render()