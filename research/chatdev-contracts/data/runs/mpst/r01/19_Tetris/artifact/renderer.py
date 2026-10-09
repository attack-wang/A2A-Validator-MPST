'''
Handles all pygame rendering: board, pieces, sidebar, and overlays.
'''
import pygame
from constants import (
    BOARD_COLS, BOARD_ROWS, CELL_SIZE, SIDEBAR_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT,
    COLOR_BG, COLOR_BOARD, COLOR_GRID, COLOR_BORDER,
    COLOR_TEXT, COLOR_ACCENT, COLOR_GHOST, COLOR_OVERLAY,
)
class Renderer:
    """Draws every visual element of the Tetris game onto the pygame screen."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.font_big = pygame.font.SysFont("arial", 32, bold=True)
        self.font = pygame.font.SysFont("arial", 20)
        self.font_small = pygame.font.SysFont("arial", 16)
    def _draw_cell(self, x, y, color):
        """Draw one board cell at grid coordinate (x, y) with a top highlight."""
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
        highlight = tuple(min(255, c + 40) for c in color)
        pygame.draw.rect(self.screen, highlight, (rect.x + 2, rect.y + 2, rect.w - 4, 4))
    def draw_board_frame(self):
        """Draw the playfield background, grid lines and border."""
        board_rect = pygame.Rect(0, 0, BOARD_COLS * CELL_SIZE, BOARD_ROWS * CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_BOARD, board_rect)
        for col in range(BOARD_COLS + 1):
            pygame.draw.line(self.screen, COLOR_GRID,
                             (col * CELL_SIZE, 0), (col * CELL_SIZE, BOARD_ROWS * CELL_SIZE))
        for row in range(BOARD_ROWS + 1):
            pygame.draw.line(self.screen, COLOR_GRID,
                             (0, row * CELL_SIZE), (BOARD_COLS * CELL_SIZE, row * CELL_SIZE))
        pygame.draw.rect(self.screen, COLOR_BORDER, board_rect, 2)
    def draw_locked_cells(self, game):
        """Draw every locked block stored on the board grid."""
        for y, row in enumerate(game.board.grid):
            for x, color in enumerate(row):
                if color is not None:
                    self._draw_cell(x, y, color)
    def draw_ghost_piece(self, game):
        """Draw the landing preview outline of the current piece."""
        if game.game_over or game.current_piece is None:
            return
        dy = game.ghost_drop_distance()
        for x, y in game.current_piece.get_cells(dx=0, dy=dy):
            if y >= 0:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, COLOR_GHOST, rect, 1)
    def draw_current_piece(self, game):
        """Draw the currently falling tetromino."""
        if game.game_over or game.current_piece is None:
            return
        for x, y in game.current_piece.get_cells():
            if y >= 0:
                self._draw_cell(x, y, game.current_piece.color)
    def draw_sidebar(self, game):
        """Draw score / level / lines / next-piece preview and controls help."""
        px = BOARD_COLS * CELL_SIZE
        pygame.draw.rect(self.screen, COLOR_BOARD,
                         pygame.Rect(px, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(self.font_big.render("TETRIS", True, COLOR_ACCENT), (px + 20, 20))
        for i, (label, value) in enumerate(
                [("Score", game.score), ("Level", game.level), ("Lines", game.lines)]):
            self.screen.blit(self.font.render(label, True, COLOR_TEXT), (px + 20, 90 + i * 70))
            self.screen.blit(self.font.render(str(value), True, COLOR_ACCENT), (px + 20, 115 + i * 70))
        self.screen.blit(self.font.render("Next", True, COLOR_TEXT), (px + 20, 310))
        if game.next_piece is not None:
            for r, row in enumerate(game.next_piece.matrix):
                for c, val in enumerate(row):
                    if val:
                        rect = pygame.Rect(px + 20 + c * CELL_SIZE, 340 + r * CELL_SIZE,
                                           CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, game.next_piece.color, rect)
                        pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
        for i, line in enumerate(["Left/Right: move", "Up: rotate", "Down: soft drop",
                                  "Space: hard drop", "P: pause", "R: restart"]):
            self.screen.blit(self.font_small.render(line, True, COLOR_TEXT), (px + 20, 460 + i * 22))
    def _overlay(self, alpha, text):
        """Blit a dark overlay with a centered message."""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        surface.fill((*COLOR_OVERLAY, alpha))
        self.screen.blit(surface, (0, 0))
        label = self.font_big.render(text, True, COLOR_ACCENT)
        self.screen.blit(label, label.get_rect(
            center=(BOARD_COLS * CELL_SIZE // 2, SCREEN_HEIGHT // 2)))
    def draw_game_over(self):
        """Game-over overlay with restart hint."""
        self._overlay(200, "GAME OVER")
        sub = self.font.render("Press R to restart", True, COLOR_TEXT)
        self.screen.blit(sub, sub.get_rect(
            center=(BOARD_COLS * CELL_SIZE // 2, SCREEN_HEIGHT // 2 + 30)))
    def draw(self, game, paused=False):
        """Render one full frame."""
        self.screen.fill(COLOR_BG)
        self.draw_board_frame()
        self.draw_locked_cells(game)
        self.draw_ghost_piece(game)
        self.draw_current_piece(game)
        self.draw_sidebar(game)
        if paused:
            self._overlay(160, "PAUSED")
        if game.game_over:
            self.draw_game_over()
        pygame.display.flip()