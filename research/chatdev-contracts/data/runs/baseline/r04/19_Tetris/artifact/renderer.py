'''
renderer.py
Renderer class responsible for drawing the board, falling piece, ghost
piece, next-piece preview, HUD (score/level/lines), and overlays.
'''
import pygame
from constants import (
    CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT, MARGIN, PANEL_WIDTH,
    COLOR_BACKGROUND, COLOR_BOARD, COLOR_GRID, COLOR_BORDER,
    COLOR_TEXT, COLOR_GHOST,
)
class Renderer:
    """Draws the entire game frame from the current Game state."""
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont('arial', 32, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 24, bold=True)
        self.font_small = pygame.font.SysFont('arial', 18)
    def _board_origin(self):
        return MARGIN, MARGIN
    def _draw_cell(self, x, y, color, ox, oy, border=True):
        rect = pygame.Rect(ox + x * CELL_SIZE, oy + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        if border:
            pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
    def _draw_tetromino_cells(self, tetromino, ox, oy, dy=0, ghost=False):
        """Draw all occupied cells of a tetromino, optionally offset vertically."""
        for x, y in tetromino.get_cells(dy=dy):
            if y >= 0:  # skip cells still above the visible board
                color = COLOR_GHOST if ghost else tetromino.color
                self._draw_cell(x, y, color, ox, oy, border=not ghost)
    def draw_board(self, board):
        """Draw board background, grid lines, locked cells, and border."""
        ox, oy = self._board_origin()
        board_rect = pygame.Rect(ox, oy, BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_BOARD, board_rect)
        for x in range(BOARD_WIDTH + 1):
            pygame.draw.line(self.screen, COLOR_GRID,
                             (ox + x * CELL_SIZE, oy),
                             (ox + x * CELL_SIZE, oy + BOARD_HEIGHT * CELL_SIZE))
        for y in range(BOARD_HEIGHT + 1):
            pygame.draw.line(self.screen, COLOR_GRID,
                             (ox, oy + y * CELL_SIZE),
                             (ox + BOARD_WIDTH * CELL_SIZE, oy + y * CELL_SIZE))
        for y, row in enumerate(board.grid):
            for x, color in enumerate(row):
                if color:
                    self._draw_cell(x, y, color, ox, oy)
        pygame.draw.rect(self.screen, COLOR_BORDER, board_rect, 2)
    def draw_tetromino(self, tetromino, ox, oy, ghost_y=None):
        """Draw ghost (landing preview) then the actual falling piece."""
        if tetromino is None:
            return
        if ghost_y is not None and ghost_y != tetromino.y:
            self._draw_tetromino_cells(tetromino, ox, oy, dy=ghost_y - tetromino.y, ghost=True)
        self._draw_tetromino_cells(tetromino, ox, oy)
    def draw_next(self, tetromino):
        """Draw the next-piece preview centered in the side panel."""
        ox, oy = self._board_origin()
        panel_x = ox + BOARD_WIDTH * CELL_SIZE + MARGIN
        self.screen.blit(self.font_medium.render('NEXT', True, COLOR_TEXT), (panel_x, oy))
        pw = len(tetromino.matrix[0]) * CELL_SIZE
        px = panel_x + (PANEL_WIDTH - pw) // 2
        py = oy + 60
        for cy, row in enumerate(tetromino.matrix):
            for cx, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(px + cx * CELL_SIZE, py + cy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, tetromino.color, rect)
                    pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
    def draw_hud(self, game):
        """Draw score / level / lines in the side panel."""
        ox, oy = self._board_origin()
        panel_x = ox + BOARD_WIDTH * CELL_SIZE + MARGIN
        y = oy + 180
        for label, value in (('SCORE', game.score), ('LEVEL', game.level), ('LINES', game.lines)):
            self.screen.blit(self.font_small.render(label, True, COLOR_TEXT), (panel_x, y))
            self.screen.blit(self.font_medium.render(str(value), True, COLOR_TEXT), (panel_x, y + 26))
            y += 80
    def _draw_overlay(self, text_lines):
        """Draw a translucent overlay with centered text over the board."""
        ox, oy = self._board_origin()
        w, h = BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (ox, oy))
        for i, line in enumerate(text_lines):
            surf = self.font_large.render(line, True, COLOR_TEXT)
            rect = surf.get_rect(center=(ox + w // 2, oy + h // 2 - 40 + i * 50))
            self.screen.blit(surf, rect)
    def draw_overlays(self, game):
        """Show PAUSED / GAME OVER overlays depending on state."""
        if game.paused:
            self._draw_overlay(['PAUSED', 'Press P to resume'])
        elif game.game_over:
            self._draw_overlay(['GAME OVER', f'Score: {game.score}', 'Press R to restart'])
    def render(self, game):
        """Render one complete frame: board, pieces, panel, overlays."""
        self.screen.fill(COLOR_BACKGROUND)
        ox, oy = self._board_origin()
        self.draw_board(game.board)
        if game.current_tetromino and not game.game_over:
            self.draw_tetromino(game.current_tetromino, ox, oy, ghost_y=game.get_ghost_y())
        self.draw_next(game.next_tetromino)
        self.draw_hud(game)
        self.draw_overlays(game)