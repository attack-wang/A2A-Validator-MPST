'''
Rendering module for the 2048 game.
Draws the complete game window each frame: the title header with score
and highest-tile boxes, the 4x4 board grid, every tile with its
color-coded background and value, and the translucent game-over overlay.
'''
import pygame
from config import (WINDOW_WIDTH, GRID_SIZE, CELL_SIZE, CELL_PADDING,
                    GRID_WIDTH, GRID_TOP, GRID_LEFT,
                    COLOR_BACKGROUND, COLOR_EMPTY_CELL, COLOR_TEXT_DARK,
                    COLOR_TEXT_LIGHT, COLOR_OVERLAY, COLOR_BOX,
                    TILE_COLORS, TILE_COLOR_SUPER)
def _cell_rect(row, col):
    '''Return the pygame.Rect of board cell (row, col).'''
    x = GRID_LEFT + CELL_PADDING + col * (CELL_SIZE + CELL_PADDING)
    y = GRID_TOP + CELL_PADDING + row * (CELL_SIZE + CELL_PADDING)
    return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
class Renderer:
    '''Draws the complete 2048 game window each frame.'''
    def __init__(self, window):
        '''Pre-render fonts and store the target surface.'''
        self.window = window
        self.font_title = pygame.font.SysFont('arial', 52, bold=True)
        self.font_label = pygame.font.SysFont('arial', 14, bold=True)
        self.font_value = pygame.font.SysFont('arial', 22, bold=True)
        self.font_hint = pygame.font.SysFont('arial', 14)
        self.font_tile_large = pygame.font.SysFont('arial', 48, bold=True)
        self.font_tile_medium = pygame.font.SysFont('arial', 36, bold=True)
        self.font_tile_small = pygame.font.SysFont('arial', 28, bold=True)
        self.font_overlay_big = pygame.font.SysFont('arial', 40, bold=True)
        self.font_overlay_small = pygame.font.SysFont('arial', 18)
    def draw(self, game):
        '''Render one full frame for the given game state.'''
        self.window.fill(COLOR_BACKGROUND)
        self._draw_header(game)
        self._draw_grid()
        self._draw_tiles(game)
        if game.game_over:
            self._draw_game_over(game)
    def _draw_header(self, game):
        '''Draw the "2048" title plus the score and highest-tile boxes.'''
        title = self.font_title.render('2048', True, COLOR_TEXT_DARK)
        self.window.blit(title, (GRID_LEFT, 20))
        # Score box
        self._draw_score_box('SCORE', str(game.score),
                             WINDOW_WIDTH - GRID_LEFT - 110, 25)
        # Highest tile box
        self._draw_score_box('HIGHEST TILE', str(game.highest_tile),
                             WINDOW_WIDTH - GRID_LEFT - 230, 25)
        hint = self.font_hint.render(
            'Arrow keys / WASD: move   R: restart', True, COLOR_TEXT_DARK)
        self.window.blit(hint, (GRID_LEFT, GRID_TOP - 30))
    def _draw_score_box(self, label, value, x, y):
        '''Draw one rounded box showing a label and its current value.'''
        box = pygame.Rect(x, y, 110, 60)
        pygame.draw.rect(self.window, COLOR_BOX, box, border_radius=6)
        label_surf = self.font_label.render(label, True, COLOR_TEXT_LIGHT)
        value_surf = self.font_value.render(value, True, COLOR_TEXT_LIGHT)
        self.window.blit(label_surf,
                         label_surf.get_rect(center=(box.centerx, box.y + 20)))
        self.window.blit(value_surf,
                         value_surf.get_rect(center=(box.centerx, box.y + 42)))
    def _draw_grid(self):
        '''Draw the board background and the empty cell placeholders.'''
        board_rect = pygame.Rect(GRID_LEFT, GRID_TOP, GRID_WIDTH, GRID_WIDTH)
        pygame.draw.rect(self.window, COLOR_EMPTY_CELL, board_rect,
                         border_radius=6)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                pygame.draw.rect(self.window, COLOR_EMPTY_CELL,
                                 _cell_rect(row, col), border_radius=6)
    def _draw_tiles(self, game):
        '''Draw every non-zero tile with its color and appropriately sized font.'''
        for row in range(game.grid_size):
            for col in range(game.grid_size):
                value = game.board[row][col]
                if value == 0:
                    continue
                rect = _cell_rect(row, col)
                color = TILE_COLORS.get(value, TILE_COLOR_SUPER)
                pygame.draw.rect(self.window, color, rect, border_radius=6)
                text_color = COLOR_TEXT_DARK if value <= 4 else COLOR_TEXT_LIGHT
                font = self._font_for(value)
                text = font.render(str(value), True, text_color)
                self.window.blit(text, text.get_rect(center=rect.center))
    def _font_for(self, value):
        '''Choose a font size that lets long numbers fit inside a cell.'''
        text = str(value)
        if len(text) <= 2:
            return self.font_tile_large
        if len(text) == 3:
            return self.font_tile_medium
        return self.font_tile_small
    def _draw_game_over(self, game):
        '''Draw a translucent overlay announcing the end of the game.'''
        overlay = pygame.Surface((GRID_WIDTH, GRID_WIDTH), pygame.SRCALPHA)
        overlay.fill((*COLOR_OVERLAY, 180))
        self.window.blit(overlay, (GRID_LEFT, GRID_TOP))
        big = self.font_overlay_big.render('Game Over!', True, COLOR_TEXT_DARK)
        small = self.font_overlay_small.render(
            f'Final score: {game.score}   Highest tile: {game.highest_tile}',
            True, COLOR_TEXT_DARK)
        restart = self.font_overlay_small.render(
            'Press R to play again', True, COLOR_TEXT_DARK)
        center_x = GRID_LEFT + GRID_WIDTH // 2
        center_y = GRID_TOP + GRID_WIDTH // 2
        self.window.blit(big, big.get_rect(center=(center_x, center_y - 40)))
        self.window.blit(small,
                         small.get_rect(center=(center_x, center_y + 10)))
        self.window.blit(restart,
                         restart.get_rect(center=(center_x, center_y + 45)))