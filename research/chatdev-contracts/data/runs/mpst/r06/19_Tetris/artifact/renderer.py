'''
Renderer module drawing the board, pieces, sidebar and overlays with pygame.
'''
import pygame
from config import (CELL_SIZE, MARGIN, WINDOW_WIDTH, WINDOW_HEIGHT,
                    BLACK, WHITE, GRID_COLOR, BORDER_COLOR, GHOST_COLOR)
class Renderer:
    '''Handles all pygame drawing for the Tetris game.'''
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont('consolas', 28, bold=True)
        self.font_medium = pygame.font.SysFont('consolas', 22)
        self.font_small = pygame.font.SysFont('consolas', 18)
    def draw(self, game):
        '''Render the complete game frame.'''
        self.screen.fill(BLACK)
        self._draw_board(game)
        self._draw_ghost(game)
        self._draw_piece(game)
        self._draw_sidebar(game)
        if game.paused:
            self._draw_overlay('PAUSED', 'Press P to resume')
        elif game.game_over:
            self._draw_overlay('GAME OVER', f'Score: {game.score} - Press R to restart')
        pygame.display.flip()
    def _cell_rect(self, x, y):
        '''Return the pygame Rect for a board cell.'''
        return pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    def _draw_cell(self, rect, color, border=True):
        '''Draw a single filled cell with an optional border.'''
        pygame.draw.rect(self.screen, color, rect)
        if border:
            pygame.draw.rect(self.screen, BORDER_COLOR, rect, 1)
    def _draw_board(self, game):
        '''Draw the playfield border and all locked cells.'''
        board_rect = pygame.Rect(MARGIN - 2, MARGIN - 2,
                                 game.board.width * CELL_SIZE + 4,
                                 game.board.height * CELL_SIZE + 4)
        pygame.draw.rect(self.screen, BORDER_COLOR, board_rect, 2)
        for y, row in enumerate(game.board.grid):
            for x, color in enumerate(row):
                if color:
                    self._draw_cell(self._cell_rect(x, y), color)
    def _draw_piece(self, game):
        '''Draw the current falling piece.'''
        if game.game_over or game.current_piece is None:
            return
        for x, y in game.current_piece.cells():
            if y >= 0:
                self._draw_cell(self._cell_rect(x, y), game.current_piece.color)
    def _draw_ghost(self, game):
        '''Draw the landing preview outline of the current piece.'''
        if game.game_over or game.paused or game.current_piece is None:
            return
        ghost_y = game.ghost_y()
        for row_idx, row in enumerate(game.current_piece.matrix):
            for col_idx, val in enumerate(row):
                if val:
                    x = game.current_piece.x + col_idx
                    y = ghost_y + row_idx
                    if y >= 0:
                        rect = self._cell_rect(x, y)
                        pygame.draw.rect(self.screen, GHOST_COLOR, rect, 1)
    def _draw_sidebar(self, game):
        '''Draw score, level, lines, next-piece preview and control help.'''
        sx = MARGIN * 2 + game.board.width * CELL_SIZE + 10
        # Score
        title = self.font_medium.render('SCORE', True, WHITE)
        value = self.font_large.render(str(game.score), True, WHITE)
        self.screen.blit(title, (sx, MARGIN))
        self.screen.blit(value, (sx, MARGIN + 30))
        # Level & lines
        level_t = self.font_medium.render(f'LEVEL {game.level}', True, WHITE)
        lines_t = self.font_medium.render(f'LINES {game.lines}', True, WHITE)
        self.screen.blit(level_t, (sx, MARGIN + 90))
        self.screen.blit(lines_t, (sx, MARGIN + 120))
        # Next piece
        next_t = self.font_medium.render('NEXT', True, WHITE)
        self.screen.blit(next_t, (sx, MARGIN + 170))
        box = pygame.Rect(sx, MARGIN + 200, 4 * CELL_SIZE, 4 * CELL_SIZE)
        pygame.draw.rect(self.screen, GRID_COLOR, box, 1)
        self._draw_next_piece(game, box)
        # Controls
        controls = ['LEFT/RIGHT: move', 'DOWN: soft drop', 'UP: rotate',
                    'SPACE: hard drop', 'P: pause', 'R: restart', 'ESC/Q: quit']
        cy = box.bottom + 20
        for i, line in enumerate(controls):
            self.screen.blit(self.font_small.render(line, True, WHITE),
                             (sx, cy + i * 22))
    def _draw_next_piece(self, game, box_rect):
        '''Draw the next piece centered inside the given preview box.'''
        piece = game.next_piece
        cells = [(c, r) for r, row in enumerate(piece.matrix) for c, v in enumerate(row) if v]
        if not cells:
            return
        min_c = min(c for c, r in cells)
        max_c = max(c for c, r in cells)
        min_r = min(r for c, r in cells)
        max_r = max(r for c, r in cells)
        w = (max_c - min_c + 1) * CELL_SIZE
        h = (max_r - min_r + 1) * CELL_SIZE
        ox = box_rect.x + (box_rect.width - w) // 2
        oy = box_rect.y + (box_rect.height - h) // 2
        for c, r in cells:
            rect = pygame.Rect(ox + (c - min_c) * CELL_SIZE,
                               oy + (r - min_r) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            self._draw_cell(rect, piece.color)
    def _draw_overlay(self, title, subtitle):
        '''Draw a translucent overlay with a title and subtitle centered on screen.'''
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        t = self.font_large.render(title, True, WHITE)
        s = self.font_small.render(subtitle, True, WHITE)
        self.screen.blit(t, t.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20)))
        self.screen.blit(s, s.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)))