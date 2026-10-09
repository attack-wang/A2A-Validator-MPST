'''
renderer.py
Handles all pygame drawing: the board grid, locked and falling pieces,
the next-piece preview, score/level/lines panel, and the game-over overlay.
'''
import pygame
from constants import (CELL_SIZE, COLS, ROWS, SIDEBAR_WIDTH, WINDOW_WIDTH,
                       WINDOW_HEIGHT, BLACK, WHITE, GRAY, DARK_GRAY, GRID_LINE)
class Renderer:
    """Draws the entire game window each frame."""
    def __init__(self, window):
        """Store the window surface and prepare fonts for HUD text."""
        self.window = window
        self.font_large = pygame.font.SysFont('arial', 28, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 22)
        self.font_small = pygame.font.SysFont('arial', 18)
    def draw_cell(self, x, y, color, offset_x=0, offset_y=0):
        """Draw one filled cell with a border at board coordinates (x, y)."""
        rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.window, color, rect)
        pygame.draw.rect(self.window, DARK_GRAY, rect, 1)  # border
    def draw_board(self, game):
        """Draw the playfield background, grid lines, and locked cells."""
        board_area = pygame.Rect(0, 0, COLS * CELL_SIZE, ROWS * CELL_SIZE)
        pygame.draw.rect(self.window, DARK_GRAY, board_area)
        # Locked cells
        for y in range(ROWS):
            for x in range(COLS):
                color = game.board.grid[y][x]
                if color is not None:
                    self.draw_cell(x, y, color)
        # Grid lines
        for x in range(COLS + 1):
            pygame.draw.line(self.window, GRID_LINE,
                             (x * CELL_SIZE, 0),
                             (x * CELL_SIZE, ROWS * CELL_SIZE))
        for y in range(ROWS + 1):
            pygame.draw.line(self.window, GRID_LINE,
                             (0, y * CELL_SIZE),
                             (COLS * CELL_SIZE, y * CELL_SIZE))
    def draw_current_piece(self, game):
        """Draw the falling piece (if any), skipping cells above the board."""
        if game.current_piece is None:
            return
        for (x, y) in game.current_piece.get_cells():
            if y >= 0:
                self.draw_cell(x, y, game.current_piece.color)
    def draw_sidebar(self, game):
        """Draw score/level/lines stats and the next-piece preview."""
        sidebar_x = COLS * CELL_SIZE
        pygame.draw.rect(self.window, DARK_GRAY,
                         (sidebar_x, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))
        # Stats
        score_text = self.font_medium.render(f"Score: {game.score}", True, WHITE)
        level_text = self.font_medium.render(f"Level: {game.level}", True, WHITE)
        lines_text = self.font_medium.render(f"Lines: {game.lines_cleared}", True, WHITE)
        self.window.blit(score_text, (sidebar_x + 20, 40))
        self.window.blit(level_text, (sidebar_x + 20, 80))
        self.window.blit(lines_text, (sidebar_x + 20, 120))
        # Next-piece preview
        next_title = self.font_medium.render("Next:", True, WHITE)
        self.window.blit(next_title, (sidebar_x + 20, 180))
        if game.next_piece is not None:
            matrix = game.next_piece.matrix
            color = game.next_piece.color
            for r, row in enumerate(matrix):
                for c, val in enumerate(row):
                    if val:
                        self.draw_cell(c + 1, r + 8, color, offset_x=sidebar_x)
    def draw_game_over(self):
        """Draw a translucent game-over overlay with a restart hint."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.window.blit(overlay, (0, 0))
        over_text = self.font_large.render("GAME OVER", True, WHITE)
        restart_text = self.font_small.render("Press R to restart", True, GRAY)
        over_rect = over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.window.blit(over_text, over_rect)
        self.window.blit(restart_text, restart_rect)
    def draw(self, game):
        """Render one full frame: board, falling piece, sidebar, overlay."""
        self.window.fill(BLACK)
        self.draw_board(game)
        self.draw_current_piece(game)
        self.draw_sidebar(game)
        if game.game_over:
            self.draw_game_over()
        pygame.display.flip()