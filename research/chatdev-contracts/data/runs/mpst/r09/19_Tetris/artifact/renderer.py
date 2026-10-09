'''Pygame rendering: board, pieces, sidebar with score/level/next piece.'''
import pygame
from constants import (CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT, SIDEBAR_WIDTH,
                       WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, GRID_COLOR,
                       BORDER_COLOR, WHITE, GRAY, COLORS)
from tetromino import BASE_SHAPES, shape_matrix
from game import Game
class Renderer:
    """Draws the entire game screen each frame."""
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont('arial', 32, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 24, bold=True)
        self.font_small = pygame.font.SysFont('arial', 18)
    def draw(self, game):
        """Render one full frame of the game."""
        self.screen.fill(BLACK)
        self.draw_board(game)
        self.draw_sidebar(game)
        if game.state == Game.STATE_PAUSED:
            self.draw_overlay('PAUSED', 'Press P to resume')
        elif game.state == Game.STATE_GAME_OVER:
            self.draw_overlay('GAME OVER', f'Score: {game.score}  -  Press R to restart')
    def draw_board(self, game):
        """Draw the playfield border, locked cells, ghost and current piece."""
        board_rect = pygame.Rect(0, 0, BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE)
        pygame.draw.rect(self.screen, BLACK, board_rect)
        # grid lines
        for x in range(BOARD_WIDTH + 1):
            pygame.draw.line(self.screen, GRID_COLOR,
                             (x * CELL_SIZE, 0), (x * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE))
        for y in range(BOARD_HEIGHT + 1):
            pygame.draw.line(self.screen, GRID_COLOR,
                             (0, y * CELL_SIZE), (BOARD_WIDTH * CELL_SIZE, y * CELL_SIZE))
        # locked cells
        for row_idx, row in enumerate(game.board.grid):
            for col_idx, color in enumerate(row):
                if color is not None:
                    self.draw_cell(col_idx, row_idx, color)
        # ghost piece
        ghost = game.ghost_piece()
        if ghost is not None and game.current_piece is not None:
            for cell_x, cell_y in ghost.cells():
                if cell_y >= 0:
                    self.draw_cell(cell_x, cell_y, ghost.color, dim=True)
        # current piece
        if game.current_piece is not None:
            for cell_x, cell_y in game.current_piece.cells():
                if cell_y >= 0:
                    self.draw_cell(cell_x, cell_y, game.current_piece.color)
        # border
        pygame.draw.rect(self.screen, BORDER_COLOR, board_rect, 2)
    def draw_cell(self, x, y, color, offset_x=0, offset_y=0, size=CELL_SIZE, dim=False):
        """Draw a single tetromino cell with a subtle 3D bevel effect."""
        rect = pygame.Rect(offset_x + x * size, offset_y + y * size, size, size)
        fill = tuple(c // 2 for c in color) if dim else color
        pygame.draw.rect(self.screen, fill, rect)
        if not dim:
            highlight = tuple(min(255, c + 60) for c in color)
            shadow = tuple(max(0, c - 60) for c in color)
            pygame.draw.line(self.screen, highlight, rect.topleft, rect.topright, 2)
            pygame.draw.line(self.screen, highlight, rect.topleft, rect.bottomleft, 2)
            pygame.draw.line(self.screen, shadow, rect.bottomright, rect.topright, 2)
            pygame.draw.line(self.screen, shadow, rect.bottomright, rect.bottomleft, 2)
        pygame.draw.rect(self.screen, BLACK, rect, 1)
    def draw_sidebar(self, game):
        """Draw score, level, lines and next-piece preview in the sidebar."""
        sidebar_x = BOARD_WIDTH * CELL_SIZE
        pygame.draw.line(self.screen, BORDER_COLOR,
                         (sidebar_x, 0), (sidebar_x, WINDOW_HEIGHT), 2)
        # Score
        score_title = self.font_medium.render('SCORE', True, GRAY)
        score_value = self.font_large.render(str(game.score), True, WHITE)
        self.screen.blit(score_title, (sidebar_x + 20, 30))
        self.screen.blit(score_value, (sidebar_x + 20, 60))
        # Level
        level_title = self.font_medium.render('LEVEL', True, GRAY)
        level_value = self.font_large.render(str(game.level), True, WHITE)
        self.screen.blit(level_title, (sidebar_x + 20, 130))
        self.screen.blit(level_value, (sidebar_x + 20, 160))
        # Lines
        lines_title = self.font_medium.render('LINES', True, GRAY)
        lines_value = self.font_large.render(str(game.lines), True, WHITE)
        self.screen.blit(lines_title, (sidebar_x + 20, 230))
        self.screen.blit(lines_value, (sidebar_x + 20, 260))
        # Next piece
        self.draw_next_piece(game, sidebar_x + 20, 330)
        # Controls
        controls = [
            'LEFT/RIGHT: move',
            'DOWN: soft drop',
            'SPACE: hard drop',
            'UP: rotate',
            'P: pause',
            'R: restart',
        ]
        y = WINDOW_HEIGHT - 20 - len(controls) * 22
        for line in controls:
            text = self.font_small.render(line, True, GRAY)
            self.screen.blit(text, (sidebar_x + 20, y))
            y += 22
    def draw_next_piece(self, game, origin_x, origin_y):
        """Draw the next-piece preview centered in a box."""
        box_size = 4 * 22 + 20
        box_rect = pygame.Rect(origin_x, origin_y, box_size, box_size)
        pygame.draw.rect(self.screen, BLACK, box_rect)
        pygame.draw.rect(self.screen, GRID_COLOR, box_rect, 2)
        title = self.font_medium.render('NEXT', True, GRAY)
        self.screen.blit(title, (origin_x, origin_y - 30))
        size = 22
        matrix = shape_matrix(game.next_type)
        color = COLORS[game.next_type]
        cells = [(c, r) for r, row in enumerate(matrix) for c, v in enumerate(row) if v]
        if not cells:
            return
        min_c = min(c for c, r in cells)
        max_c = max(c for c, r in cells)
        min_r = min(r for c, r in cells)
        max_r = max(r for c, r in cells)
        width = (max_c - min_c + 1) * size
        height = (max_r - min_r + 1) * size
        offset_x = origin_x + (box_size - width) // 2
        offset_y = origin_y + (box_size - height) // 2
        for c, r in cells:
            self.draw_cell(c - min_c, r - min_r, color,
                           offset_x=offset_x, offset_y=offset_y, size=size)
    def draw_overlay(self, title, subtitle):
        """Draw a translucent overlay with a title and subtitle centered."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))
        title_text = self.font_large.render(title, True, WHITE)
        sub_text = self.font_small.render(subtitle, True, GRAY)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        sub_rect = sub_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 25))
        self.screen.blit(title_text, title_rect)
        self.screen.blit(sub_text, sub_rect)