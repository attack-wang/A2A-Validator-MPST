'''
renderer.py
Handles all pygame drawing: board, grid, locked cells, current piece, ghost
piece, next-piece preview, score/level/lines panel, controls help and the
game-over overlay.
'''
import pygame
from constants import (BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE, SIDEBAR_WIDTH,
                       WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, GRAY,
                       DARK_GRAY, GRID_COLOR, BORDER_COLOR, OVERLAY_COLOR,
                       SHAPE_COLORS, SHAPES)
class Renderer:
    """Draws the complete game state onto the pygame screen."""
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont('consolas', 40, bold=True)
        self.font_medium = pygame.font.SysFont('consolas', 24, bold=True)
        self.font = pygame.font.SysFont('consolas', 20)
        self.font_small = pygame.font.SysFont('consolas', 15)
    def draw(self, game):
        """Render one full frame for the given game state."""
        self.screen.fill(BLACK)
        self._draw_board_panel(game)
        self._draw_sidebar(game)
        if game.game_over:
            self._draw_game_over()
        if game.paused and not game.game_over:
            self._draw_paused()
        pygame.display.flip()
    # ------------------------------------------------------------------
    # Board area
    # ------------------------------------------------------------------
    def _draw_cell(self, px, py, col, row, color):
        """Draw one filled cell with a darker border for a block look."""
        rect = pygame.Rect(px + col * CELL_SIZE, py + row * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, DARK_GRAY, rect, 1)
        # small highlight for depth
        highlight = pygame.Rect(rect.x + 3, rect.y + 3,
                                CELL_SIZE - 6, 4)
        lighter = tuple(min(255, channel + 40) for channel in color)
        pygame.draw.rect(self.screen, lighter, highlight)
    def _draw_board_panel(self, game):
        """Draw the playfield: border, grid, locked cells, ghost and piece."""
        board_px, board_py = 0, 0
        board_rect = pygame.Rect(board_px, board_py,
                                 BOARD_WIDTH * CELL_SIZE,
                                 BOARD_HEIGHT * CELL_SIZE)
        pygame.draw.rect(self.screen, BLACK, board_rect)
        # grid lines
        for col in range(BOARD_WIDTH + 1):
            x = board_px + col * CELL_SIZE
            pygame.draw.line(self.screen, GRID_COLOR,
                             (x, board_py), (x, board_py + board_rect.height))
        for row in range(BOARD_HEIGHT + 1):
            y = board_py + row * CELL_SIZE
            pygame.draw.line(self.screen, GRID_COLOR,
                             (board_px, y), (board_px + board_rect.width, y))
        # locked cells
        for row_idx, row in enumerate(game.board.grid):
            for col_idx, color in enumerate(row):
                if color is not None:
                    self._draw_cell(board_px, board_py, col_idx, row_idx, color)
        # ghost piece + current piece
        if game.current_piece is not None:
            distance = game.board.ghost_drop_distance(game.current_piece)
            for x, y in game.current_piece.cells(dy=distance):
                if y >= 0:
                    rect = pygame.Rect(board_px + x * CELL_SIZE,
                                       board_py + y * CELL_SIZE,
                                       CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, DARK_GRAY, rect, 1)
            for x, y in game.current_piece.cells():
                if y >= 0:
                    self._draw_cell(board_px, board_py, x, y,
                                    game.current_piece.color)
        pygame.draw.rect(self.screen, BORDER_COLOR, board_rect, 2)
    # ------------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------------
    def _draw_sidebar(self, game):
        """Draw next-piece preview and the score/level/lines statistics."""
        px = BOARD_WIDTH * CELL_SIZE + 20
        py = 20
        title = self.font_medium.render("TETRIS", True, WHITE)
        self.screen.blit(title, (px, py))
        pygame.draw.line(self.screen, BORDER_COLOR,
                         (px, py + 34), (px + SIDEBAR_WIDTH - 40, py + 34), 2)
        # NEXT preview
        next_label = self.font.render("NEXT", True, GRAY)
        self.screen.blit(next_label, (px, py + 55))
        self._draw_preview(px + 10, py + 90, game.randomizer.next_type)
        # stats
        stats_y = py + 190
        stats = [
            ("SCORE", str(game.score)),
            ("LEVEL", str(game.level)),
            ("LINES", str(game.lines_cleared)),
        ]
        for i, (label, value) in enumerate(stats):
            y = stats_y + i * 62
            label_surf = self.font_small.render(label, True, GRAY)
            value_surf = self.font_medium.render(value, True, WHITE)
            self.screen.blit(label_surf, (px, y))
            self.screen.blit(value_surf, (px, y + 22))
        # controls help
        help_y = stats_y + 3 * 62 + 15
        controls = [
            "LEFT/RIGHT : move",
            "DOWN       : soft drop",
            "UP / Z     : rotate",
            "SPACE      : hard drop",
            "P          : pause",
            "R          : restart",
            "ESC        : quit",
        ]
        for i, line in enumerate(controls):
            surf = self.font_small.render(line, True, GRAY)
            self.screen.blit(surf, (px, help_y + i * 22))
    def _draw_preview(self, px, py, shape_type):
        """Draw the upcoming piece centered inside a small box."""
        box = pygame.Rect(px, py, 4 * CELL_SIZE, 3 * CELL_SIZE)
        pygame.draw.rect(self.screen, DARK_GRAY, box, 1)
        matrix = SHAPES[shape_type]
        filled = [(c, r) for r, row in enumerate(matrix)
                  for c, val in enumerate(row) if val]
        if not filled:
            return
        min_c = min(c for c, _ in filled)
        max_c = max(c for c, _ in filled)
        min_r = min(r for _, r in filled)
        max_r = max(r for _, r in filled)
        piece_w = (max_c - min_c + 1) * CELL_SIZE
        piece_h = (max_r - min_r + 1) * CELL_SIZE
        offset_x = px + (box.width - piece_w) // 2 - min_c * CELL_SIZE
        offset_y = py + (box.height - piece_h) // 2 - min_r * CELL_SIZE
        color = SHAPE_COLORS[shape_type]
        for c, r in filled:
            rect = pygame.Rect(offset_x + c * CELL_SIZE,
                               offset_y + r * CELL_SIZE,
                               CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, DARK_GRAY, rect, 1)
    # ------------------------------------------------------------------
    # Overlays
    # ------------------------------------------------------------------
    def _draw_overlay_base(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*OVERLAY_COLOR, 180))
        self.screen.blit(overlay, (0, 0))
    def _draw_game_over(self):
        self._draw_overlay_base()
        center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)
        title = self.font_large.render("GAME OVER", True, WHITE)
        rect = title.get_rect(center=center)
        self.screen.blit(title, rect)
        hint = self.font.render("Press R to restart", True, GRAY)
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2,
                                          WINDOW_HEIGHT // 2 + 30))
        self.screen.blit(hint, hint_rect)
    def _draw_paused(self):
        self._draw_overlay_base()
        title = self.font_large.render("PAUSED", True, WHITE)
        rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(title, rect)
        hint = self.font.render("Press P to resume", True, GRAY)
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2,
                                          WINDOW_HEIGHT // 2 + 30))
        self.screen.blit(hint, hint_rect)