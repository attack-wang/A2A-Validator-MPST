'''
renderer.py
This module handles all pygame-based drawing for the 2048 game: the
window, the score panel, the 4x4 grid, individual tiles with their
value-dependent colors, and the game-over overlay.
'''
import pygame
from constants import (
    GRID_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, CELL_GAP,
    GRID_TOP, GRID_LEFT, FPS,
    COLOR_BACKGROUND, COLOR_GRID_BACKGROUND, COLOR_EMPTY_CELL,
    COLOR_TEXT_DARK, COLOR_TEXT_LIGHT, COLOR_SCORE_BOX,
    TILE_COLORS, TILE_COLOR_SUPER,
    FONT_SIZE_TITLE, FONT_SIZE_SCORE, FONT_SIZE_TILE_LARGE,
    FONT_SIZE_TILE_MEDIUM, FONT_SIZE_TILE_SMALL, FONT_SIZE_MESSAGE,
)
class Renderer:
    '''Responsible for rendering the entire game window each frame.'''
    def __init__(self):
        '''Initialize pygame, the window, and all fonts.'''
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('2048')
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, FONT_SIZE_TITLE)
        self.font_score = pygame.font.Font(None, FONT_SIZE_SCORE)
        self.font_message = pygame.font.Font(None, FONT_SIZE_MESSAGE)
        self.font_tile_large = pygame.font.Font(None, FONT_SIZE_TILE_LARGE)
        self.font_tile_medium = pygame.font.Font(None, FONT_SIZE_TILE_MEDIUM)
        self.font_tile_small = pygame.font.Font(None, FONT_SIZE_TILE_SMALL)
    def draw(self, game):
        '''Render one full frame: background, score panel, grid, tiles, overlays.'''
        self.screen.fill(COLOR_BACKGROUND)
        self._draw_title()
        self._draw_score_panel(game.score, game.highest_tile)
        self._draw_grid_background()
        self._draw_tiles(game.grid)
        if game.is_game_over():
            self._draw_game_over_overlay(game.score, game.highest_tile)
        pygame.display.flip()
        self.clock.tick(FPS)
    def _draw_title(self):
        '''Draw the game title in the top-left corner.'''
        title_surface = self.font_title.render('2048', True, COLOR_TEXT_DARK)
        self.screen.blit(title_surface, (GRID_LEFT, 20))
    def _draw_score_panel(self, score, highest_tile):
        '''Draw the current score and the highest tile reached.'''
        grid_width = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_GAP
        box_width = (grid_width - 20) // 2
        # Current score box
        score_rect = pygame.Rect(GRID_LEFT, 80, box_width, 60)
        pygame.draw.rect(self.screen, COLOR_SCORE_BOX, score_rect, border_radius=6)
        label = self.font_score.render('SCORE', True, COLOR_TEXT_LIGHT)
        self.screen.blit(label, label.get_rect(centerx=score_rect.centerx, top=score_rect.top + 8))
        value = self.font_score.render(str(score), True, COLOR_TEXT_LIGHT)
        self.screen.blit(value, value.get_rect(centerx=score_rect.centerx, top=score_rect.top + 30))
        # Highest tile box
        highest_rect = pygame.Rect(GRID_LEFT + box_width + 20, 80, box_width, 60)
        pygame.draw.rect(self.screen, COLOR_SCORE_BOX, highest_rect, border_radius=6)
        label = self.font_score.render('BEST TILE', True, COLOR_TEXT_LIGHT)
        self.screen.blit(label, label.get_rect(centerx=highest_rect.centerx, top=highest_rect.top + 8))
        value = self.font_score.render(str(highest_tile), True, COLOR_TEXT_LIGHT)
        self.screen.blit(value, value.get_rect(centerx=highest_rect.centerx, top=highest_rect.top + 30))
    def _cell_rect(self, row, col):
        '''Return the pygame.Rect for the cell at (row, col).'''
        x = GRID_LEFT + CELL_GAP + col * (CELL_SIZE + CELL_GAP)
        y = GRID_TOP + CELL_GAP + row * (CELL_SIZE + CELL_GAP)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    def _draw_grid_background(self):
        '''Draw the rounded grid panel and the empty cell slots.'''
        grid_width = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_GAP
        grid_rect = pygame.Rect(GRID_LEFT, GRID_TOP, grid_width, grid_width)
        pygame.draw.rect(self.screen, COLOR_GRID_BACKGROUND, grid_rect, border_radius=8)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                pygame.draw.rect(self.screen, COLOR_EMPTY_CELL,
                                 self._cell_rect(row, col), border_radius=6)
    def _font_for_value(self, value):
        '''Choose a font size based on the number of digits in the tile value.'''
        if value < 100:
            return self.font_tile_large
        elif value < 1000:
            return self.font_tile_medium
        return self.font_tile_small
    def _draw_tiles(self, grid):
        '''Draw every non-empty tile with its value-dependent color and font.'''
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = grid[row][col]
                if value == 0:
                    continue
                background_color, text_color = TILE_COLORS.get(value, TILE_COLOR_SUPER)
                cell_rect = self._cell_rect(row, col)
                pygame.draw.rect(self.screen, background_color, cell_rect, border_radius=6)
                text = self._font_for_value(value).render(str(value), True, text_color)
                self.screen.blit(text, text.get_rect(center=cell_rect.center))
    def _draw_game_over_overlay(self, score, highest_tile):
        '''Dim the grid and show the game-over message with a restart hint.'''
        grid_width = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * CELL_GAP
        overlay_rect = pygame.Rect(GRID_LEFT, GRID_TOP, grid_width, grid_width)
        overlay = pygame.Surface((grid_width, grid_width), pygame.SRCALPHA)
        overlay.fill((250, 248, 239, 180))
        self.screen.blit(overlay, (GRID_LEFT, GRID_TOP))
        message = self.font_message.render('Game Over!', True, COLOR_TEXT_DARK)
        message_rect = message.get_rect(center=(overlay_rect.centerx, overlay_rect.centery - 30))
        self.screen.blit(message, message_rect)
        hint = self.font_score.render('Press R to restart', True, COLOR_TEXT_DARK)
        hint_rect = hint.get_rect(center=(overlay_rect.centerx, overlay_rect.centery + 20))
        self.screen.blit(hint, hint_rect)