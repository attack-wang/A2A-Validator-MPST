'''
renderer.py
Renderer: draws board, pieces, sidebar (score/level/lines/next piece) and
overlay messages (paused / game over).
'''
import pygame
from constants import (CELL_SIZE, COLS, ROWS, WINDOW_WIDTH, WINDOW_HEIGHT,
                       BLACK, WHITE, GRAY, GRID_COLOR, BORDER_COLOR,
                       GHOST_COLOR, OVERLAY_COLOR)
class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.board_left = 0
        self.board_top = 0
        self.sidebar_left = COLS * CELL_SIZE + 10
        self.font_large = pygame.font.SysFont('arial', 32, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 24, bold=True)
        self.font_small = pygame.font.SysFont('arial', 18)
    # -- main entry ---
    def draw(self, game):
        self.screen.fill(BLACK)
        self.draw_board_frame()
        self.draw_locked_cells(game)
        self.draw_ghost(game)
        self.draw_current_piece(game)
        self.draw_sidebar(game)
        if game.state == game.STATE_PAUSED:
            self.draw_overlay(['PAUSED', 'Press P to resume'])
        elif game.state == game.STATE_GAME_OVER:
            self.draw_overlay(['GAME OVER',
                               f'Final score: {game.score}',
                               'Press R to restart'])
        pygame.display.flip()
    # -- board ---
    def draw_board_frame(self):
        board_rect = pygame.Rect(self.board_left, self.board_top,
                                 COLS * CELL_SIZE, ROWS * CELL_SIZE)
        pygame.draw.rect(self.screen, GRID_COLOR, board_rect)
        for r in range(ROWS + 1):
            pygame.draw.line(self.screen, GRID_COLOR, ...)
        ...