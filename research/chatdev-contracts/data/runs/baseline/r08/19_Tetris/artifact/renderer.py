'''
renderer.py
Draws the Tetris playfield, falling piece, ghost piece, next-piece preview,
and HUD (score, level, lines) using pygame.
'''
import pygame
from constants import (CELL_SIZE, SIDEBAR_WIDTH, COLORS, COLOR_BACKGROUND,
                       COLOR_GRID, COLOR_BORDER, COLOR_TEXT, COLOR_TEXT_DIM,
                       COLOR_GHOST, COLOR_OVERLAY, BOARD_WIDTH, BOARD_HEIGHT)
class Renderer:
    '''Renders the full game frame each tick.'''
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont('consolas', 20)
        self.big_font = pygame.font.SysFont('consolas', 32, bold=True)
        self.small_font = pygame.font.SysFont('consolas', 14)
    # -- primitives -------------------------------------------------------
    def draw_cell(self, x, y, color):
        '''Draw one board cell at grid coordinates (x, y).'''
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
    def draw_ghost_cell(self, x, y):
        '''Draw a hollow outline cell for the ghost piece.'''
        rect = pygame.Rect(x * CELL_SIZE + 2, y * CELL_SIZE + 2,
                           CELL_SIZE - 4, CELL_SIZE - 4)
        pygame.draw.rect(self.screen, COLOR_GHOST, rect, 2)
    # -- sections ---------------------------------------------------------
    def draw_board(self):
        '''Draw the playfield background, grid lines, and locked cells.'''
        board_rect = pygame.Rect(0, 0, BOARD_WIDTH * CELL_SIZE,
                                 BOARD_HEIGHT * CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_BACKGROUND, board_rect)
        # grid lines
        for gx in range(BOARD_WIDTH + 1):
            pygame.draw.line(self.screen, COLOR_GRID,
                             (gx * CELL_SIZE, 0), (gx * CELL_SIZE, board_rect.height))
        for gy in range(BOARD_HEIGHT + 1):
            pygame.draw.line(self.screen, COLOR_GRID,
                             (0, gy * CELL_SIZE), (board_rect.width, gy * CELL_SIZE))
        # locked cells
        for y, row in enumerate(self.game.board.grid):
            for x, color in enumerate(row):
                if color is not None:
                    self.draw_cell(x, y, color)
    def draw_piece(self):
        '''Draw the currently falling piece.'''
        piece = self.game.current_piece
        if piece is None:
            return
        for x, y in piece.cells():
            if y >= 0:
                self.draw_cell(x, y, COLORS[piece.type])
    def draw_ghost(self):
        '''Draw the landing preview (ghost) of the current piece.'''
        piece = self.game.current_piece
        if piece is None or self.game.game_over:
            return
        distance = self.game.board.get_drop_distance(piece)
        if distance <= 0:
            return
        ghost = piece.moved(0, distance)
        for x, y in ghost.cells():
            if y >= 0:
                self.draw_ghost_cell(x, y)
    def draw_next_preview(self, top_x, top_y):
        '''Draw the next piece inside a small preview box.'''
        piece = self.game.next_piece
        if piece is None:
            return
        shape = piece.shape
        offset_x = top_x + (4 - piece.width) * CELL_SIZE // 2
        offset_y = top_y + (2 - piece.height) * CELL_SIZE // 2
        for row, line in enumerate(shape):
            for col, filled in enumerate(line):
                if filled:
                    rect = pygame.Rect(offset_x + col * CELL_SIZE,
                                       offset_y + row * CELL_SIZE,
                                       CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, COLORS[piece.type], rect)
                    pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
    def draw_sidebar(self):
        '''Draw the right-hand info panel: score, level, lines, next piece, controls.'''
        sidebar_rect = pygame.Rect(BOARD_WIDTH * CELL_SIZE, 0,
                                   SIDEBAR_WIDTH, BOARD_HEIGHT * CELL_SIZE)
        pygame.draw.rect(self.screen, (28, 28, 40), sidebar_rect)
        x = sidebar_rect.left + 15
        def label(text, y, font=None, color=COLOR_TEXT):
            surf = (font or self.font).render(text, True, color)
            self.screen.blit(surf, (x, y))
        label('SCORE', 20, self.small_font, COLOR_TEXT_DIM)
        label(str(self.game.score), 42)
        label('LEVEL', 90, self.small_font, COLOR_TEXT_DIM)
        label(str(self.game.level), 112)
        label('LINES', 160, self.small_font, COLOR_TEXT_DIM)
        label(str(self.game.lines), 182)
        label('NEXT', 240, self.small_font, COLOR_TEXT_DIM)
        box = pygame.Rect(x, 262, 4 * CELL_SIZE, 2 * CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_BACKGROUND, box)
        pygame.draw.rect(self.screen, COLOR_GRID, box, 1)
        self.draw_next_preview(x, 262)
        controls = [
            'CONTROLS',
            '<- ->  move',
            'DOWN   soft drop',
            'SPACE  hard drop',
            'UP / X rotate CW',
            'Z      rotate CCW',
            'P      pause',
            'R      restart',
        ]
        y = 360
        for i, line in enumerate(controls):
            label(line, y + i * 22, self.small_font,
                  COLOR_TEXT if i == 0 else COLOR_TEXT_DIM)
    def draw_overlay(self, text, subtext=''):
        '''Dim the board and show a centered message.'''
        board_rect = pygame.Rect(0, 0, BOARD_WIDTH * CELL_SIZE,
                                 BOARD_HEIGHT * CELL_SIZE)
        overlay = pygame.Surface(board_rect.size, pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        self.screen.blit(overlay, board_rect.topleft)
        surf = self.big_font.render(text, True, COLOR_TEXT)
        rect = surf.get_rect(center=(board_rect.centerx, board_rect.centery - 20))
        self.screen.blit(surf, rect)
        if subtext:
            sub = self.font.render(subtext, True, COLOR_TEXT_DIM)
            sub_rect = sub.get_rect(center=(board_rect.centerx, board_rect.centery + 24))
            self.screen.blit(sub, sub_rect)
    def draw(self):
        '''Render one complete frame.'''
        self.screen.fill(COLOR_BACKGROUND)
        self.draw_board()
        self.draw_ghost()
        self.draw_piece()
        self.draw_sidebar()
        if self.game.paused:
            self.draw_overlay('PAUSED', 'Press P to resume')
        elif self.game.game_over:
            self.draw_overlay('GAME OVER',
                              f'Score: {self.game.score}  -  Press R to restart')