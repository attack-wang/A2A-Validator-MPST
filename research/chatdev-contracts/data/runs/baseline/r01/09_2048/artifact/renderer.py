'''
Pygame rendering for the 2048 game: board, tiles, score header, banners,
and the game-over overlay.
'''
import pygame
from config import (
    COLOR_BACKGROUND, COLOR_CELL_EMPTY, COLOR_GRID_BG, COLOR_OVERLAY,
    COLOR_TEXT_DARK, COLOR_TEXT_LIGHT, CELL_GAP, CELL_SIZE, GRID_LEFT,
    GRID_PADDING, GRID_PIXELS, GRID_SIZE, GRID_TOP, TILE_COLORS,
    TILE_COLOR_DEFAULT, WINDOW_HEIGHT, WINDOW_WIDTH,
    FONT_SIZE_BANNER, FONT_SIZE_HINT, FONT_SIZE_MESSAGE,
    FONT_SIZE_SCORE_LABEL, FONT_SIZE_SCORE_VALUE, FONT_SIZE_TITLE,
)
def _font(size):
    '''Return a pygame Font of the given size using the built-in typeface.'''
    return pygame.font.Font(None, size)
class Renderer:
    '''Draws the complete 2048 window for a Game instance.'''
    def __init__(self, window):
        self.window = window
        self.font_title = _font(FONT_SIZE_TITLE)
        self.font_score_label = _font(FONT_SIZE_SCORE_LABEL)
        self.font_score_value = _font(FONT_SIZE_SCORE_VALUE)
        self.font_message = _font(FONT_SIZE_MESSAGE)
        self.font_banner = _font(FONT_SIZE_BANNER)
        self.font_hint = _font(FONT_SIZE_HINT)
        self._tile_fonts = {}
    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def draw(self, game):
        '''Render one full frame: background, header, grid, tiles, overlays.'''
        self.window.fill(COLOR_BACKGROUND)
        self._draw_header(game)
        self._draw_win_banner(game)
        self._draw_grid()
        self._draw_tiles(game)
        self._draw_hint()
        if game.game_over:
            self._draw_game_over()
    # ------------------------------------------------------------------
    # Header / score
    # ------------------------------------------------------------------
    def _draw_header(self, game):
        title = self.font_title.render('2048', True, COLOR_TEXT_DARK)
        self.window.blit(title, (GRID_LEFT, 18))
        box_w, box_h = 120, 64
        gap = 12
        right_edge = GRID_LEFT + GRID_PIXELS
        best_rect = pygame.Rect(right_edge - box_w, 18, box_w, box_h)
        score_rect = pygame.Rect(best_rect.left - gap - box_w, 18, box_w, box_h)
        self._draw_score_box(score_rect, 'SCORE', str(game.score))
        self._draw_score_box(best_rect, 'BEST TILE', str(game.highest_tile()))
    def _draw_score_box(self, rect, label, value):
        pygame.draw.rect(self.window, COLOR_GRID_BG, rect, border_radius=6)
        label_surf = self.font_score_label.render(label, True, COLOR_TEXT_LIGHT)
        value_surf = self.font_score_value.render(value, True, COLOR_TEXT_LIGHT)
        lx = rect.centerx - label_surf.get_width() // 2
        vx = rect.centerx - value_surf.get_width() // 2
        self.window.blit(label_surf, (lx, rect.top + 8))
        self.window.blit(value_surf, (vx, rect.top + 30))
    def _draw_win_banner(self, game):
        if not game.won or game.game_over:
            return
        banner_rect = pygame.Rect(GRID_LEFT, 118, GRID_PIXELS, 24)
        pygame.draw.rect(self.window, (237, 194, 46), banner_rect, border_radius=6)
        text = self.font_banner.render(
            'You reached 2048! Keep going!', True, COLOR_TEXT_LIGHT)
        self.window.blit(
            text,
            (banner_rect.centerx - text.get_width() // 2,
             banner_rect.centery - text.get_height() // 2))
    # ------------------------------------------------------------------
    # Grid and tiles
    # ------------------------------------------------------------------
    def _cell_rect(self, row, col):
        x = GRID_LEFT + GRID_PADDING + col * (CELL_SIZE + CELL_GAP)
        y = GRID_TOP + GRID_PADDING + row * (CELL_SIZE + CELL_GAP)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    def _draw_grid(self):
        grid_rect = pygame.Rect(GRID_LEFT, GRID_TOP, GRID_PIXELS, GRID_PIXELS)
        pygame.draw.rect(self.window, COLOR_GRID_BG, grid_rect, border_radius=8)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                pygame.draw.rect(
                    self.window, COLOR_CELL_EMPTY, self._cell_rect(row, col),
                    border_radius=6)
    def _draw_tiles(self, game):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = game.grid[row][col]
                if value == 0:
                    continue
                self._draw_tile(value, self._cell_rect(row, col))
    def _draw_tile(self, value, rect):
        color = TILE_COLORS.get(value, TILE_COLOR_DEFAULT)
        pygame.draw.rect(self.window, color, rect, border_radius=6)
        text_color = COLOR_TEXT_DARK if value <= 4 else COLOR_TEXT_LIGHT
        font = self._font_for(value)
        surf = font.render(str(value), True, text_color)
        self.window.blit(
            surf,
            (rect.centerx - surf.get_width() // 2,
             rect.centery - surf.get_height() // 2))
    def _font_for(self, value):
        '''Pick a font size that fits the number of digits in the tile.'''
        digits = len(str(value))
        size = {1: 52, 2: 48, 3: 38, 4: 30}.get(digits, 24)
        if size not in self._tile_fonts:
            self._tile_fonts[size] = _font(size)
        return self._tile_fonts[size]
    # ------------------------------------------------------------------
    # Footer and overlays
    # ------------------------------------------------------------------
    def _draw_hint(self):
        hint = ('Arrow keys / WASD: move   |   R: restart   |   Esc: quit')
        surf = self.font_hint.render(hint, True, COLOR_TEXT_DARK)
        self.window.blit(
            surf,
            (GRID_LEFT + GRID_PIXELS // 2 - surf.get_width() // 2,
             GRID_TOP + GRID_PIXELS + 12))
    def _draw_game_over(self):
        overlay = pygame.Surface((GRID_PIXELS, GRID_PIXELS), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        self.window.blit(overlay, (GRID_LEFT, GRID_TOP))
        line1 = self.font_message.render('Game Over!', True, COLOR_TEXT_DARK)
        line2 = self.font_hint.render(
            'No moves left - press R to restart', True, COLOR_TEXT_DARK)
        center_x = GRID_LEFT + GRID_PIXELS // 2
        center_y = GRID_TOP + GRID_PIXELS // 2
        self.window.blit(
            line1,
            (center_x - line1.get_width() // 2, center_y - line1.get_height() - 8))
        self.window.blit(
            line2,
            (center_x - line2.get_width() // 2, center_y + 8))