'''
renderer.py
All drawing routines for the Tetris window, implemented with a tkinter
Canvas so the game runs on the Python standard library alone (no external
dependencies such as pygame are required).
Renders the board frame and grid, locked cells, the active piece with a
ghost landing preview, the next-piece preview, the score/level/lines
panel, and the game-over / pause overlays.
'''
import tkinter as tk
from constants import (
    BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE, SIDEBAR_WIDTH,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_BACKGROUND, COLOR_GRID, COLOR_BORDER,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_OVERLAY,
    lighten,
)
BOARD_PIXEL_WIDTH = BOARD_WIDTH * CELL_SIZE
class Renderer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.font_large = ("Consolas", 22, "bold")
        self.font_medium = ("Consolas", 16, "bold")
        self.font_small = ("Consolas", 12)
    def draw(self, game, paused):
        self.canvas.delete("all")
        self._draw_background()
        self._draw_board_grid()
        self._draw_locked_cells(game)
        if not game.game_over and game.current_piece:
            self._draw_ghost(game)
            self._draw_active_piece(game)
        self._draw_sidebar(game)
        if game.game_over:
            self._draw_overlay("GAME OVER", "Press R to restart")
        elif paused:
            self._draw_overlay("PAUSED", "Press P to resume")
    def _draw_background(self):
        self.canvas.create_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                                     fill=COLOR_BACKGROUND, outline="")
    def _draw_board_grid(self):
        # grid lines
        for col in range(BOARD_WIDTH + 1):
            x = col * CELL_SIZE
            self.canvas.create_line(x, 0, x, BOARD_HEIGHT * CELL_SIZE, fill=COLOR_GRID)
        for row in range(BOARD_HEIGHT + 1):
            y = row * CELL_SIZE
            self.canvas.create_line(0, y, BOARD_WIDTH * CELL_SIZE, y, fill=COLOR_GRID)
        # border
        self.canvas.create_rectangle(0, 0, BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE,
                                     outline=COLOR_BORDER, width=2)
    def _draw_cell(self, x, y, color):
        px = x * CELL_SIZE
        py = y * CELL_SIZE
        self.canvas.create_rectangle(px, py, px + CELL_SIZE, py + CELL_SIZE,
                                     fill=color, outline="")
        inner = 4
        self.canvas.create_rectangle(px + inner, py + inner,
                                     px + CELL_SIZE - inner, py + CELL_SIZE - inner,
                                     outline=lighten(color), width=2)
    def _draw_locked_cells(self, game):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                color = game.board.grid[row][col]
                if color is not None:
                    self._draw_cell(col, row, color)
    def _draw_ghost(self, game):
        drop_y = game.board.get_drop_y(game.current_piece)
        if drop_y == game.current_piece.y:
            return
        for cx, cy in game.current_piece.cells(game.current_piece.x, drop_y):
            if cy >= 0:
                px = cx * CELL_SIZE
                py = cy * CELL_SIZE
                self.canvas.create_rectangle(px + 2, py + 2, px + CELL_SIZE - 2, py + CELL_SIZE - 2,
                                             outline=game.current_piece.color)
    def _draw_active_piece(self, game):
        for cx, cy in game.current_piece.cells():
            if cy >= 0:
                self._draw_cell(cx, cy, game.current_piece.color)
    def _draw_sidebar(self, game):
        x0 = BOARD_WIDTH * CELL_SIZE
        self.canvas.create_line(x0, 0, x0, SCREEN_HEIGHT, fill=COLOR_BORDER, width=2)
        labels = [
            ("SCORE", str(game.score)),
            ("LEVEL", str(game.level)),
            ("LINES", str(game.lines)),
        ]
        y = 30
        for title, value in labels:
            self.canvas.create_text(x0 + SIDEBAR_WIDTH // 2, y, text=title,
                                    fill=COLOR_TEXT_DIM, font=self.font_small)
            self.canvas.create_text(x0 + SIDEBAR_WIDTH // 2, y + 24, text=value,
                                    fill=COLOR_TEXT, font=self.font_medium)
            y += 80
        # next piece preview
        self.canvas.create_text(x0 + SIDEBAR_WIDTH // 2, y, text="NEXT",
                                fill=COLOR_TEXT_DIM, font=self.font_small)
        self._draw_next_piece(game.next_piece, x0 + SIDEBAR_WIDTH // 2, y + 40)
        # controls help
        help_lines = [
            "LEFT/RIGHT  move",
            "UP          rotate",
            "DOWN        soft drop",
            "SPACE       hard drop",
            "P           pause",
            "R           restart",
        ]
        hy = SCREEN_HEIGHT - 30 - len(help_lines) * 20
        for line in help_lines:
            self.canvas.create_text(x0 + SIDEBAR_WIDTH // 2, hy, text=line,
                                    fill=COLOR_TEXT_DIM, font=self.font_small)
            hy += 20
    def _draw_next_piece(self, piece, center_x, top_y):
        matrix = piece.matrix
        size = CELL_SIZE // 2
        rows = len(matrix)
        cols = len(matrix[0])
        occupied = [(r, c) for r in range(rows) for c in range(cols) if matrix[r][c]]
        if not occupied:
            return
        min_r = min(r for r, _ in occupied)
        max_r = max(r for r, _ in occupied)
        min_c = min(c for _, c in occupied)
        max_c = max(c for _, c in occupied)
        w = (max_c - min_c + 1) * size
        h = (max_r - min_r + 1) * size
        start_x = center_x - w // 2
        start_y = top_y
        for r, c in occupied:
            px = start_x + (c - min_c) * size
            py = start_y + (r - min_r) * size
            self.canvas.create_rectangle(px, py, px + size, py + size,
                                         fill=piece.color, outline="")
            self.canvas.create_rectangle(px + 2, py + 2, px + size - 2, py + size - 2,
                                         outline=lighten(piece.color), width=1)
    def _draw_overlay(self, title, subtitle):
        self.canvas.create_rectangle(0, 0, BOARD_WIDTH * CELL_SIZE, SCREEN_HEIGHT,
                                     fill=COLOR_OVERLAY, stipple="gray50", outline="")
        cx = BOARD_WIDTH * CELL_SIZE // 2
        cy = SCREEN_HEIGHT // 2
        self.canvas.create_text(cx, cy - 20, text=title, fill=COLOR_TEXT, font=self.font_large)
        self.canvas.create_text(cx, cy + 20, text=subtitle, fill=COLOR_TEXT_DIM, font=self.font_small)