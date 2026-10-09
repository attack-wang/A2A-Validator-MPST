"""Renderer module: draws the game using pygame."""
import pygame
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE,
                       BOARD_OFFSET_X, BOARD_OFFSET_Y,
                       BOARD_WIDTH, BOARD_HEIGHT,
                       COLOR_BACKGROUND, COLOR_BOARD, COLOR_GRID,
                       COLOR_BORDER, COLOR_TEXT, COLOR_TEXT_DIM,
                       SHAPE_COLORS, SHAPES)
class Renderer:
    """Handles all pygame drawing for the game."""
    def __init__(self, game):
        """Create the window, caption, and fonts used for drawing."""
        self.game = game
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.font = pygame.font.SysFont('arial', 24, bold=True)
        self.big_font = pygame.font.SysFont('arial', 48, bold=True)
        self.small_font = pygame.font.SysFont('arial', 18)
    def draw(self):
        """Render one full frame: board, pieces, sidebar, and overlays."""
        self.screen.fill(COLOR_BACKGROUND)
        self.draw_board()
        self.draw_ghost_piece()
        self.draw_current_piece()
        self.draw_sidebar()
        if self.game.game_over:
            self.draw_game_over()
        pygame.display.flip()
    def _draw_cell(self, x, y, color):
        """Draw one filled cell at board coordinates (x, y) with a border."""
        rect = pygame.Rect(BOARD_OFFSET_X + x * CELL_SIZE,
                           BOARD_OFFSET_Y + y * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
    def draw_board(self):
        """Draw the board background, grid lines, and locked cells."""
        board_rect = pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y,
                                 BOARD_WIDTH * CELL_SIZE,
                                 BOARD_HEIGHT * CELL_SIZE)
        pygame.draw.rect(self.screen, COLOR_BOARD, board_rect)
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                color = self.game.board.grid[y][x]
                if color is not None:
                    self._draw_cell(x, y, color)
        for x in range(BOARD_WIDTH + 1):
            start = (BOARD_OFFSET_X + x * CELL_SIZE, BOARD_OFFSET_Y)
            end = (BOARD_OFFSET_X + x * CELL_SIZE,
                   BOARD_OFFSET_Y + BOARD_HEIGHT * CELL_SIZE)
            pygame.draw.line(self.screen, COLOR_GRID, start, end)
        for y in range(BOARD_HEIGHT + 1):
            start = (BOARD_OFFSET_X, BOARD_OFFSET_Y + y * CELL_SIZE)
            end = (BOARD_OFFSET_X + BOARD_WIDTH * CELL_SIZE,
                   BOARD_OFFSET_Y + y * CELL_SIZE)
            pygame.draw.line(self.screen, COLOR_GRID, start, end)
        pygame.draw.rect(self.screen, COLOR_BORDER, board_rect, 2)
    def _ghost_drop_distance(self):
        """Return how many cells the current piece would fall before landing."""
        piece = self.game.current_piece
        distance = 0
        while self.game.board.is_valid_position(piece, dy=distance + 1):
            distance += 1
        return distance
    def draw_ghost_piece(self):
        """Draw a translucent preview of where the current piece will land."""
        piece = self.game.current_piece
        if piece is None:
            return
        ghost = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        ghost.fill((piece.color[0], piece.color[1], piece.color[2], 70))
        dy = self._ghost_drop_distance()
        for x, y in piece.get_cells(dy=dy):
            if y >= 0:
                self.screen.blit(ghost, (BOARD_OFFSET_X + x * CELL_SIZE,
                                         BOARD_OFFSET_Y + y * CELL_SIZE))
    def draw_current_piece(self):
        """Draw the currently falling tetromino."""
        piece = self.game.current_piece
        if piece is None:
            return
        for x, y in piece.get_cells():
            if y >= 0:
                self._draw_cell(x, y, piece.color)
    def draw_sidebar(self):
        """Draw score, level, lines, and the next-piece preview."""
        base_x = BOARD_OFFSET_X + BOARD_WIDTH * CELL_SIZE + 20
        y = BOARD_OFFSET_Y
        for title, value in (("Score", self.game.score),
                             ("Level", self.game.level),
                             ("Lines", self.game.lines)):
            title_surf = self.font.render(title, True, COLOR_TEXT_DIM)
            value_surf = self.font.render(str(value), True, COLOR_TEXT)
            self.screen.blit(title_surf, (base_x, y))
            self.screen.blit(value_surf, (base_x, y + 28))
            y += 70
        # Next piece preview
        next_surf = self.font.render("Next", True, COLOR_TEXT_DIM)
        self.screen.blit(next_surf, (base_x, y))
        shape = SHAPES[self.game.next_type]
        color = SHAPE_COLORS[self.game.next_type]
        preview_y = y + 36
        for row_index, row in enumerate(shape):
            for col_index, filled in enumerate(row):
                if filled:
                    rect = pygame.Rect(base_x + col_index * CELL_SIZE,
                                       preview_y + row_index * CELL_SIZE,
                                       CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
        # Controls hint
        hints = ["Left/Right: move", "Down: soft drop",
                 "Up: rotate", "Space: hard drop",
                 "R: restart", "Q: quit"]
        hint_y = preview_y + 4 * CELL_SIZE + 20
        for hint in hints:
            hint_surf = self.small_font.render(hint, True, COLOR_TEXT_DIM)
            self.screen.blit(hint_surf, (base_x, hint_y))
            hint_y += 22
    def draw_game_over(self):
        """Draw a translucent overlay with the GAME OVER message."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        text = self.big_font.render("GAME OVER", True, COLOR_TEXT)
        hint = self.small_font.render("Press R to restart, Q to quit",
                                      True, COLOR_TEXT_DIM)
        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2,
                                WINDOW_HEIGHT // 2 - 60))
        self.screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2,
                                WINDOW_HEIGHT // 2 + 10))