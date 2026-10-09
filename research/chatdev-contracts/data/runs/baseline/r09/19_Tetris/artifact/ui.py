'''
ui.py
Defines the UI class: all pygame rendering.
Draws the board grid, locked blocks, the falling piece, a ghost preview
of where the piece will land, the side panel (score, level, lines, next
piece) and overlay messages (paused / game over / controls).
'''
import pygame
from settings import (CELL_SIZE, COLS, ROWS, SIDEBAR_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT,
                      COLOR_BG, COLOR_GRID, COLOR_GRID_BORDER, COLOR_TEXT,
                      COLOR_PANEL, COLOR_PANEL_BORDER, COLOR_GAME_OVER, COLOR_PAUSED)
class UI:
    """Renders the game state to the screen."""
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("consolas", 30, bold=True)
        self.font_medium = pygame.font.SysFont("consolas", 22, bold=True)
        self.font_small = pygame.font.SysFont("consolas", 16)
    def draw(self):
        self.window.fill(COLOR_BG)
        self._draw_board()
        self._draw_ghost()
        self._draw_piece()
        self._draw_sidebar()
        if self.game.paused:
            self._draw_overlay("PAUSED", COLOR_PAUSED)
        if self.game.game_over:
            self._draw_overlay("GAME OVER", COLOR_GAME_OVER)
        pygame.display.flip()
    def _cell_rect(self, col, row):
        return pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    def _draw_block(self, col, row, color):
        rect = self._cell_rect(col, row)
        pygame.draw.rect(self.window, color, rect.inflate(-2, -2), border_radius=4)
    def _draw_board(self):
        board_rect = pygame.Rect(0, 0, COLS * CELL_SIZE, ROWS * CELL_SIZE)
        pygame.draw.rect(self.window, COLOR_PANEL, board_rect)
        # grid lines
        for c in range(COLS + 1):
            pygame.draw.line(self.window, COLOR_GRID,
                             (c * CELL_SIZE, 0), (c * CELL_SIZE, ROWS * CELL_SIZE))
        for r in range(ROWS + 1):
            pygame.draw.line(self.window, COLOR_GRID,
                             (0, r * CELL_SIZE), (COLS * CELL_SIZE, r * CELL_SIZE))
        pygame.draw.rect(self.window, COLOR_GRID_BORDER, board_rect, 2)
        # locked cells
        for r, row in enumerate(self.game.board.grid):
            for c, color in enumerate(row):
                if color:
                    self._draw_block(c, r, color)
    def _draw_ghost(self):
        """Outline showing where the current piece would land."""
        if self.game.game_over or self.game.paused:
            return
        piece = self.game.current_piece
        dy = 0
        while self.game.board.is_valid_position(piece, dy=dy + 1):
            dy += 1
        for col, row in piece.cells(dy=dy):
            rect = self._cell_rect(col, row).inflate(-6, -6)
            pygame.draw.rect(self.window, piece.color, rect, 2, border_radius=4)
    def _draw_piece(self):
        if self.game.game_over:
            return
        for col, row in self.game.current_piece.cells():
            if row >= 0:
                self._draw_block(col, row, self.game.current_piece.color)
    def _draw_sidebar(self):
        x = COLS * CELL_SIZE
        panel_rect = pygame.Rect(x, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.window, COLOR_PANEL, panel_rect)
        pygame.draw.line(self.window, COLOR_PANEL_BORDER, (x, 0), (x, WINDOW_HEIGHT), 2)
        # Score / level / lines
        self._text("SCORE", x + 20, 30, self.font_small, COLOR_TEXT)
        self._text(str(self.game.score), x + 20, 52, self.font_medium, COLOR_TEXT)
        self._text("LEVEL", x + 20, 110, self.font_small, COLOR_TEXT)
        self._text(str(self.game.level), x + 20, 132, self.font_medium, COLOR_TEXT)
        self._text("LINES", x + 20, 190, self.font_small, COLOR_TEXT)
        self._text(str(self.game.lines), x + 20, 212, self.font_medium, COLOR_TEXT)
        # Next piece preview
        self._text("NEXT", x + 20, 280, self.font_small, COLOR_TEXT)
        preview_box = pygame.Rect(x + 20, 305, 4 * CELL_SIZE, 3 * CELL_SIZE)
        pygame.draw.rect(self.window, COLOR_BG, preview_box)
        pygame.draw.rect(self.window, COLOR_PANEL_BORDER, preview_box, 1)
        piece = self.game.next_piece
        offset_x = x + 20 + (4 * CELL_SIZE - piece.width * CELL_SIZE) // 2
        offset_y = 305 + (3 * CELL_SIZE - piece.height * CELL_SIZE) // 2
        for r, row in enumerate(piece.matrix):
            for c, val in enumerate(row):
                if val:
                    rect = pygame.Rect(offset_x + c * CELL_SIZE,
                                       offset_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.window, piece.color,
                                     rect.inflate(-2, -2), border_radius=4)
        # Controls help
        controls = [
            "CONTROLS",
            "Left/Right : move",
            "Up         : rotate",
            "Down       : soft drop",
            "Space      : hard drop",
            "P          : pause",
            "R          : restart",
            "Esc        : quit",
        ]
        y = 405
        for i, line in enumerate(controls):
            color = COLOR_PANEL_BORDER if i == 0 else COLOR_TEXT
            self._text(line, x + 20, y + i * 24, self.font_small, color)
    def _text(self, string, x, y, font, color):
        surface = font.render(string, True, color)
        self.window.blit(surface, (x, y))
    def _draw_overlay(self, message, color):
        overlay = pygame.Surface((COLS * CELL_SIZE, ROWS * CELL_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.window.blit(overlay, (0, 0))
        text = self.font_large.render(message, True, color)
        rect = text.get_rect(center=(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2))
        self.window.blit(text, rect)