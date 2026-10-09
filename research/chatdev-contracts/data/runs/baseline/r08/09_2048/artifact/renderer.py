'''
renderer.py
Rendering module for the 2048 game using pygame: draws the window,
grid, tiles, score header, and game-over overlay.
'''
import pygame
from constants import (GRID_SIZE, CELL_SIZE, CELL_GAP, GRID_PIXEL_SIZE,
                       GRID_X, GRID_Y, WINDOW_WIDTH, WINDOW_HEIGHT,
                       COLOR_BACKGROUND, COLOR_EMPTY_CELL, COLOR_TEXT_DARK,
                       COLOR_TEXT_LIGHT, COLOR_SCORE_BOX, COLOR_OVERLAY,
                       TILE_COLORS, COLOR_TILE_SUPER_BG, COLOR_TILE_SUPER_FG,
                       FONT_SIZE_TITLE, FONT_SIZE_TILE, FONT_SIZE_TILE_SMALL,
                       FONT_SIZE_SCORE_LABEL, FONT_SIZE_SCORE, FONT_SIZE_MESSAGE,
                       FONT_SIZE_HINT)
class Renderer:
    '''Handles all drawing of the game window, grid, tiles, and score.'''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('2048')
        self.font_tile = pygame.font.Font(None, FONT_SIZE_TILE)
        self.font_tile_small = pygame.font.Font(None, FONT_SIZE_TILE_SMALL)
        self.font_score = pygame.font.Font(None, FONT_SIZE_SCORE)
        self.font_score_label = pygame.font.Font(None, FONT_SIZE_SCORE_LABEL)
        self.font_title = pygame.font.Font(None, FONT_SIZE_TITLE)
        self.font_message = pygame.font.Font(None, FONT_SIZE_MESSAGE)
        self.font_hint = pygame.font.Font(None, FONT_SIZE_HINT)
    def draw(self, game):
        '''Draw the full game frame: background, score, grid, tiles, and overlays.'''
        self.screen.fill(COLOR_BACKGROUND)
        self._draw_header(game)
        self._draw_grid()
        self._draw_tiles(game)
        if game.game_over:
            self._draw_game_over()
        pygame.display.flip()
    def _draw_header(self, game):
        '''Draw the title, current score, and highest tile.'''
        # Title on the left.
        title = self.font_title.render('2048', True, COLOR_TEXT_DARK)
        self.screen.blit(title, (GRID_X, 20))
        # Score box (current score).
        score_label = self.font_score_label.render('SCORE', True, COLOR_TEXT_LIGHT)
        score_value = self.font_score.render(str(game.score), True, COLOR_TEXT_LIGHT)
        self._draw_info_box(WINDOW_WIDTH - 220, 20, 100, 80, score_label, score_value)
        # Highest tile box.
        highest_label = self.font_score_label.render('HIGHEST', True, COLOR_TEXT_LIGHT)
        highest_value = self.font_score.render(str(game.get_highest_tile()), True, COLOR_TEXT_LIGHT)
        self._draw_info_box(WINDOW_WIDTH - 110, 20, 100, 80, highest_label, highest_value)
    def _draw_info_box(self, x, y, width, height, label, value):
        '''Draw a rounded info box with a label on top and a value below.'''
        box = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, COLOR_SCORE_BOX, box, border_radius=6)
        label_rect = label.get_rect(center=(box.centerx, box.y + 22))
        value_rect = value.get_rect(center=(box.centerx, box.y + 55))
        self.screen.blit(label, label_rect)
        self.screen.blit(value, value_rect)
    def _draw_grid(self):
        '''Draw the empty grid background cells.'''
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = GRID_X + CELL_GAP + c * (CELL_SIZE + CELL_GAP)
                y = GRID_Y + CELL_GAP + r * (CELL_SIZE + CELL_GAP)
                cell = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, COLOR_EMPTY_CELL, cell, border_radius=6)
    def _draw_tiles(self, game):
        '''Draw each non-empty tile with its value and color scheme.'''
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = game.grid[r][c]
                if value == 0:
                    continue
                x = GRID_X + CELL_GAP + c * (CELL_SIZE + CELL_GAP)
                y = GRID_Y + CELL_GAP + r * (CELL_SIZE + CELL_GAP)
                cell = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                bg, fg = TILE_COLORS.get(value, (COLOR_TILE_SUPER_BG, COLOR_TILE_SUPER_FG))
                pygame.draw.rect(self.screen, bg, cell, border_radius=6)
                # Use the smaller font for 4+ digit values so text fits the cell.
                font = self.font_tile_small if value >= 1024 else self.font_tile
                text = font.render(str(value), True, fg)
                text_rect = text.get_rect(center=cell.center)
                self.screen.blit(text, text_rect)
    def _draw_game_over(self):
        '''Draw the game-over overlay with restart instructions.'''
        overlay = pygame.Surface((GRID_PIXEL_SIZE, GRID_PIXEL_SIZE), pygame.SRCALPHA)
        overlay.fill((*COLOR_OVERLAY, 180))
        self.screen.blit(overlay, (GRID_X, GRID_Y))
        message = self.font_message.render('Game Over!', True, COLOR_TEXT_DARK)
        message_rect = message.get_rect(center=(GRID_X + GRID_PIXEL_SIZE // 2,
                                                GRID_Y + GRID_PIXEL_SIZE // 2 - 20))
        self.screen.blit(message, message_rect)
        hint = self.font_hint.render('Press R to restart', True, COLOR_TEXT_DARK)
        hint_rect = hint.get_rect(center=(GRID_X + GRID_PIXEL_SIZE // 2,
                                          GRID_Y + GRID_PIXEL_SIZE // 2 + 30))
        self.screen.blit(hint, hint_rect)