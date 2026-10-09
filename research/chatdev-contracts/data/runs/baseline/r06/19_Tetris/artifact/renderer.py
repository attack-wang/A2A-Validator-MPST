'''
renderer.py
Draws the board, pieces, sidebar and overlays to the screen.
'''
import pygame
from constants import (CELL_SIZE, BOARD_PIXEL_WIDTH, BOARD_PIXEL_HEIGHT,
                       SIDEBAR_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT,
                       COLOR_BG, COLOR_BOARD, COLOR_GRID, COLOR_BORDER,
                       COLOR_TEXT, COLOR_GHOST, COLOR_GAME_OVER,
                       PREVIEW_SIZE)
from tetromino import Tetromino
class Renderer:
    """Responsible for all drawing of the game."""
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont('arial', 32, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 22, bold=True)
        self.font_small = pygame.font.SysFont('arial', 18)
    def draw(self, game):
        """Render the whole game frame."""
        self.screen.fill(COLOR_BG)
        self._draw_board_frame()
        self._draw_locked_cells(game.board)
        self._draw_ghost(game)
        self._draw_current_piece(game)
        self._draw_sidebar(game)
        if game.paused and not game.game_over:
            self._draw_center_text('PAUSED', COLOR_TEXT)
        if game.game_over:
            self._draw_center_text('GAME OVER', COLOR_GAME_OVER)
        pygame.display.flip()
    def _draw_board_frame(self):
        pygame.draw.rect(self.screen, COLOR_BOARD,
                         (0, 0, BOARD_PIXEL_WIDTH, BOARD_PIXEL_HEIGHT))
        for x in range(0, BOARD_PIXEL_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, BOARD_PIXEL_HEIGHT))
        for y in range(0, BOARD_PIXEL_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (BOARD_PIXEL_WIDTH, y))
        pygame.draw.rect(self.screen, COLOR_BORDER,
                         (0, 0, BOARD_PIXEL_WIDTH, BOARD_PIXEL_HEIGHT), 2)
    def _draw_cell(self, x, y, color):
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
    def _draw_locked_cells(self, board):
        for y, row in enumerate(board.grid):
            for x, color in enumerate(row):
                if color is not None:
                    self._draw_cell(x, y, color)
    def _draw_current_piece(self, game):
        if game.current_piece is None:
            return
        for x, y in game.current_piece.get_cells():
            if y >= 0:
                self._draw_cell(x, y, game.current_piece.color)
    def _draw_ghost(self, game):
        if game.current_piece is None or game.game_over:
            return
        ghost = game.get_ghost_position()
        for x, y in ghost.get_cells():
            if y >= 0:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, COLOR_GHOST, rect, 1)
    def _draw_sidebar(self, game):
        panel_x = BOARD_PIXEL_WIDTH + 10
        # Score
        self._draw_label('SCORE', panel_x, 20, self.font_medium)
        self._draw_value(str(game.score), panel_x, 50, self.font_large)
        # Level
        self._draw_label('LEVEL', panel_x, 110, self.font_medium)
        self._draw_value(str(game.level), panel_x, 140, self.font_large)
        # Lines
        self._draw_label('LINES', panel_x, 200, self.font_medium)
        self._draw_value(str(game.lines), panel_x, 230, self.font_large)
        # Next piece
        self._draw_label('NEXT', panel_x, 300, self.font_medium)
        self._draw_next_piece(game.next_piece, panel_x, 330)
        # Controls
        controls = [
            'LEFT/RIGHT: Move',
            'DOWN: Soft drop',
            'UP: Rotate',
            'SPACE: Hard drop',
            'P: Pause',
            'R: Restart',
            'ESC: Quit',
        ]
        y = 470
        for line in controls:
            text = self.font_small.render(line, True, COLOR_TEXT)
            self.screen.blit(text, (panel_x, y))
            y += 24
    def _draw_next_piece(self, piece, panel_x, panel_y):
        if piece is None:
            return
        box = pygame.Rect(panel_x, panel_y, PREVIEW_SIZE, PREVIEW_SIZE)
        pygame.draw.rect(self.screen, COLOR_BOARD, box)
        pygame.draw.rect(self.screen, COLOR_BORDER, box, 1)
        matrix = piece.matrix
        offset_x = (PREVIEW_SIZE - len(matrix[0]) * CELL_SIZE) // 2
        offset_y = (PREVIEW_SIZE - len(matrix) * CELL_SIZE) // 2
        for row_idx, row in enumerate(matrix):
            for col_idx, val in enumerate(row):
                if val:
                    rect = pygame.Rect(panel_x + offset_x + col_idx * CELL_SIZE,
                                       panel_y + offset_y + row_idx * CELL_SIZE,
                                       CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, piece.color, rect)
                    pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
    def _draw_label(self, text, x, y, font):
        label = font.render(text, True, COLOR_TEXT)
        self.screen.blit(label, (x, y))
    def _draw_value(self, text, x, y, font):
        value = font.render(text, True, COLOR_TEXT)
        self.screen.blit(value, (x, y))
    def _draw_center_text(self, text, color):
        overlay = pygame.Surface((BOARD_PIXEL_WIDTH, BOARD_PIXEL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        rendered = self.font_large.render(text, True, color)
        rect = rendered.get_rect(center=(BOARD_PIXEL_WIDTH // 2, BOARD_PIXEL_HEIGHT // 2))
        self.screen.blit(rendered, rect)