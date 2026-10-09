'''
renderer.py
Defines the Renderer class that draws the entire game with tkinter's
Canvas widget: the playfield grid, locked cells, the falling piece, its
ghost landing preview, the next-piece preview and the score/level/lines
panel, plus the pause and game-over overlays. Only the Python standard
library is used, so the game no longer depends on pygame.
'''
import tkinter as tk
from constants import (CELL_SIZE, COLS, ROWS, BOARD_WIDTH, BOARD_HEIGHT,
                       BOARD_OFFSET_X, BOARD_OFFSET_Y, PANEL_WIDTH,
                       SCREEN_WIDTH, SCREEN_HEIGHT,
                       BLACK, WHITE, GRAY, GRID_COLOR, BORDER_COLOR,
                       TETROMINO_COLORS)
def _hex(color):
    """Convert an (R, G, B) tuple into a '#rrggbb' tkinter color string."""
    return '#%02x%02x%02x' % tuple(color)
class Renderer:
    """Draws the Tetris game state onto a tkinter Canvas."""
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
                                bg=_hex(BLACK), highlightthickness=0)
        self.canvas.pack()
        self.font_large = ('Arial', 24, 'bold')
        self.font_medium = ('Arial', 16, 'bold')
        self.font_small = ('Arial', 11)
    # ------------------------------------------------------------------ #
    # Top-level draw                                                      #
    # ------------------------------------------------------------------ #
    def draw(self, game, paused=False):
        """Redraw the complete scene for the current game state."""
        self.canvas.delete('all')
        self.draw_board_panel()
        self.draw_locked_cells(game)
        self.draw_ghost_piece(game)
        self.draw_current_piece(game)
        self.draw_grid_lines()
        self.draw_panel(game)
        if game.game_over:
            self.draw_game_over()
        elif paused:
            self.draw_paused()
    # ------------------------------------------------------------------ #
    # Board area                                                          #
    # ------------------------------------------------------------------ #
    def draw_cell(self, col, row, color, px=0, py=0):
        """Draw one filled cell; (px, py) is the pixel origin offset."""
        x0 = px + col * CELL_SIZE + 1
        y0 = py + row * CELL_SIZE + 1
        x1 = x0 + CELL_SIZE - 2
        y1 = y0 + CELL_SIZE - 2
        self.canvas.create_rectangle(x0, y0, x1, y1,
                                     fill=_hex(color), outline='', width=0)
    def draw_board_panel(self):
        """Frame around the playfield."""
        self.canvas.create_rectangle(
            BOARD_OFFSET_X - 2, BOARD_OFFSET_Y - 2,
            BOARD_OFFSET_X + BOARD_WIDTH + 1, BOARD_OFFSET_Y + BOARD_HEIGHT + 1,
            outline=_hex(BORDER_COLOR), width=2)
    def draw_grid_lines(self):
        """Subtle grid lines inside the playfield."""
        for c in range(1, COLS):
            x = BOARD_OFFSET_X + c * CELL_SIZE
            self.canvas.create_line(x, BOARD_OFFSET_Y,
                                    x, BOARD_OFFSET_Y + BOARD_HEIGHT,
                                    fill=_hex(GRID_COLOR))
        for r in range(1, ROWS):
            y = BOARD_OFFSET_Y + r * CELL_SIZE
            self.canvas.create_line(BOARD_OFFSET_X, y,
                                    BOARD_OFFSET_X + BOARD_WIDTH, y,
                                    fill=_hex(GRID_COLOR))
    def draw_locked_cells(self, game):
        """Draw every locked cell stored in the board grid."""
        for y in range(game.board.rows):
            for x in range(game.board.cols):
                cell = game.board.grid[y][x]
                if cell is not None:
                    self.draw_cell(x, y, TETROMINO_COLORS[cell],
                                   px=BOARD_OFFSET_X, py=BOARD_OFFSET_Y)
    def draw_current_piece(self, game):
        """Draw the falling piece."""
        if game.game_over or game.current_piece is None:
            return
        for (x, y) in game.current_piece.get_cells():
            if y >= 0:
                self.draw_cell(x, y, game.current_piece.color,
                               px=BOARD_OFFSET_X, py=BOARD_OFFSET_Y)
    def draw_ghost_piece(self, game):
        """Outline preview showing where the piece will land."""
        if game.game_over or game.current_piece is None:
            return
        piece = game.current_piece
        distance = 0
        while game.board.is_valid_position(piece, 0, distance + 1):
            distance += 1
        if distance <= 0:
            return
        for (x, y) in piece.get_cells():
            gy = y + distance
            if gy >= 0:
                x0 = BOARD_OFFSET_X + x * CELL_SIZE + 3
                y0 = BOARD_OFFSET_Y + gy * CELL_SIZE + 3
                x1 = x0 + CELL_SIZE - 6
                y1 = y0 + CELL_SIZE - 6
                self.canvas.create_rectangle(x0, y0, x1, y1,
                                             outline=_hex(piece.color), width=1)
    # ------------------------------------------------------------------ #
    # Side panel                                                          #
    # ------------------------------------------------------------------ #
    def draw_panel(self, game):
        """Score / level / lines readouts and next-piece preview."""
        px = BOARD_WIDTH + 20
        self._text(px, 30, 'TETRIS', WHITE, self.font_large)
        self._text(px, 95, 'SCORE', GRAY, self.font_small)
        self._text(px, 117, str(game.score), WHITE, self.font_medium)
        self._text(px, 165, 'LEVEL', GRAY, self.font_small)
        self._text(px, 187, str(game.level), WHITE, self.font_medium)
        self._text(px, 235, 'LINES', GRAY, self.font_small)
        self._text(px, 257, str(game.lines), WHITE, self.font_medium)
        self._text(px, 315, 'NEXT', GRAY, self.font_small)
        self.draw_next_piece(game, px, 345)
        controls = [
            'LEFT/RIGHT : move',
            'UP         : rotate',
            'DOWN       : soft drop',
            'SPACE      : hard drop',
            'P          : pause',
            'R          : restart (after game over)',
            'ESC        : quit',
        ]
        for i, line in enumerate(controls):
            self._text(px, 480 + i * 22, line, GRAY, self.font_small)
    def _text(self, x, y, text, color, font):
        """Left-aligned text helper."""
        self.canvas.create_text(x, y, text=text, fill=_hex(color),
                                font=font, anchor='w')
    def draw_next_piece(self, game, px, py):
        """Preview of the upcoming piece inside the side panel."""
        piece = game.next_piece
        cells = [(c, r) for r, row in enumerate(piece.shape)
                 for c, v in enumerate(row) if v]
        if not cells:
            return
        min_c = min(c for c, _ in cells)
        max_c = max(c for c, _ in cells)
        min_r = min(r for _, r in cells)
        max_r = max(r for _, r in cells)
        w = (max_c - min_c + 1) * CELL_SIZE
        h = (max_r - min_r + 1) * CELL_SIZE
        ox = px + (PANEL_WIDTH - 40 - w) // 2
        oy = py + (4 * CELL_SIZE - h) // 2
        for (c, r) in cells:
            self.draw_cell(c - min_c, r - min_r, piece.color, px=ox, py=oy)
    # ------------------------------------------------------------------ #
    # Overlays                                                            #
    # ------------------------------------------------------------------ #
    def _overlay(self):
        """Semi-transparent dark cover over the playfield."""
        self.canvas.create_rectangle(
            BOARD_OFFSET_X, BOARD_OFFSET_Y,
            BOARD_OFFSET_X + BOARD_WIDTH, BOARD_OFFSET_Y + BOARD_HEIGHT,
            fill='#000000', stipple='gray50', outline='')
    def draw_game_over(self):
        self._overlay()
        cx = BOARD_OFFSET_X + BOARD_WIDTH // 2
        cy = BOARD_OFFSET_Y + BOARD_HEIGHT // 2
        self.canvas.create_text(cx, cy - 20, text='GAME OVER',
                                fill='#e63c3c', font=self.font_large)
        self.canvas.create_text(cx, cy + 25, text='Press R to restart',
                                fill=_hex(WHITE), font=self.font_medium)
    def draw_paused(self):
        self._overlay()
        cx = BOARD_OFFSET_X + BOARD_WIDTH // 2
        cy = BOARD_OFFSET_Y + BOARD_HEIGHT // 2
        self.canvas.create_text(cx, cy - 20, text='PAUSED',
                                fill=_hex(WHITE), font=self.font_large)
        self.canvas.create_text(cx, cy + 25, text='Press P to resume',
                                fill=_hex(GRAY), font=self.font_medium)