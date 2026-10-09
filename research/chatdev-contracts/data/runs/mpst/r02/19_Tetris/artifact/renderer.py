'''
renderer.py
Defines the Renderer class responsible for all drawing.
It renders the playfield with its locked cells and grid lines, the
currently falling tetromino, a ghost preview of where the piece will
land, the next-piece preview, and the score/level/lines panel, plus
pause and game-over overlays.
'''
import pygame
from settings import (CELL_SIZE, COLS, ROWS, PADDING, SIDEBAR_WIDTH,
                      WINDOW_WIDTH, WINDOW_HEIGHT,
                      COLOR_BG, COLOR_BOARD, COLOR_GRID, COLOR_BORDER,
                      COLOR_TEXT, COLOR_TEXT_DIM, COLOR_OVERLAY)
class Renderer:
    """Draws the entire game window each frame."""
    PREVIEW_BOX_HEIGHT = 110   # Height of the next-piece preview box
    def __init__(self):
        """Create the pygame window, fonts and cached geometry."""
        pygame.display.set_caption('Tetris')
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font_large = pygame.font.SysFont('arial', 40, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 26, bold=True)
        self.font_small = pygame.font.SysFont('arial', 20)
        self.board_rect = pygame.Rect(PADDING, PADDING,
                                      COLS * CELL_SIZE, ROWS * CELL_SIZE)
    # ------------------------------------------------------------------
    # Frame composition
    # ------------------------------------------------------------------
    def draw(self, game):
        """Render one full frame for the given Game instance."""
        self.screen.fill(COLOR_BG)
        self.draw_board(game)
        self.draw_ghost(game)
        self.draw_current_piece(game)
        self.draw_sidebar(game)
        if game.paused:
            self.draw_overlay('PAUSED', 'Press P to resume')
        elif game.game_over:
            self.draw_overlay('GAME OVER',
                              f'Score: {game.score}  -  Press R to restart')
        pygame.display.flip()
    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------
    def draw_cell(self, x, y, color):
        """Draw one board cell at grid coordinates (x, y)."""
        rect = pygame.Rect(self.board_rect.x + x * CELL_SIZE,
                           self.board_rect.y + y * CELL_SIZE,
                           CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
    def draw_board(self, game):
        """Draw the playfield background, grid lines and locked cells."""
        pygame.draw.rect(self.screen, COLOR_BOARD, self.board_rect)
        for x in range(COLS + 1):
            start = (self.board_rect.x + x * CELL_SIZE, self.board_rect.y)
            end = (self.board_rect.x + x * CELL_SIZE, self.board_rect.bottom)
            pygame.draw.line(self.screen, COLOR_GRID, start, end)
        for y in range(ROWS + 1):
            start = (self.board_rect.x, self.board_rect.y + y * CELL_SIZE)
            end = (self.board_rect.right, self.board_rect.y + y * CELL_SIZE)
            pygame.draw.line(self.screen, COLOR_GRID, start, end)
        for row in range(ROWS):
            for col in range(COLS):
                color = game.board.grid[row][col]
                if color is not None:
                    self.draw_cell(col, row, color)
        pygame.draw.rect(self.screen, COLOR_BORDER, self.board_rect, 2)
    def draw_ghost(self, game):
        """Draw a dimmed preview of where the current piece will land."""
        piece = game.current_tetromino
        if piece is None or game.game_over:
            return
        distance = 0
        while game.board.is_valid_position(piece, offset_y=distance + 1):
            distance += 1
        if distance <= 0:
            return
        ghost_color = tuple(max(0, channel // 3) for channel in piece.color)
        for cell_x, cell_y in piece.get_cells(offset_y=distance):
            if cell_y >= 0:
                rect = pygame.Rect(self.board_rect.x + cell_x * CELL_SIZE,
                                   self.board_rect.y + cell_y * CELL_SIZE,
                                   CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, ghost_color, rect)
                pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
    def draw_current_piece(self, game):
        """Draw the currently falling tetromino."""
        piece = game.current_tetromino
        if piece is None:
            return
        for cell_x, cell_y in piece.get_cells():
            if cell_y >= 0:
                self.draw_cell(cell_x, cell_y, piece.color)
    def draw_sidebar(self, game):
        """Draw the score/level/lines panel, next-piece preview and help."""
        panel_x = self.board_rect.right + PADDING
        panel_width = SIDEBAR_WIDTH
        # Statistics
        stats = [('SCORE', str(game.score)),
                 ('LEVEL', str(game.level)),
                 ('LINES', str(game.lines))]
        y = PADDING
        for label, value in stats:
            label_surf = self.font_small.render(label, True, COLOR_TEXT_DIM)
            value_surf = self.font_medium.render(value, True, COLOR_TEXT)
            self.screen.blit(label_surf, (panel_x, y))
            self.screen.blit(value_surf, (panel_x, y + 26))
            y += 74
        # Next-piece preview
        next_surf = self.font_small.render('NEXT', True, COLOR_TEXT_DIM)
        self.screen.blit(next_surf, (panel_x, y))
        box_y = y + 28
        box_rect = pygame.Rect(panel_x, box_y, panel_width, self.PREVIEW_BOX_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_BOARD, box_rect, 2)
        self.draw_preview(game.next_tetromino, box_rect)
        # Controls help
        help_lines = ['LEFT/RIGHT  move', 'UP/Z        rotate',
                      'DOWN        soft drop', 'SPACE       hard drop',
                      'P           pause', 'R           restart',
                      'ESC         quit']
        y = box_rect.bottom + PADDING
        for line in help_lines:
            surf = self.font_small.render(line, True, COLOR_TEXT_DIM)
            self.screen.blit(surf, (panel_x, y))
            y += 24
    def draw_preview(self, tetromino, box_rect):
        """Draw a tetromino centred inside the given preview box."""
        matrix = tetromino.matrix
        size = len(matrix)
        cells = [(col, row) for row in range(size)
                 for col in range(size) if matrix[row][col]]
        if not cells:
            return
        min_col = min(col for col, _ in cells)
        max_col = max(col for col, _ in cells)
        min_row = min(row for _, row in cells)
        max_row = max(row for _, row in cells)
        width = (max_col - min_col + 1) * CELL_SIZE
        height = (max_row - min_row + 1) * CELL_SIZE
        origin_x = box_rect.x + (box_rect.width - width) // 2
        origin_y = box_rect.y + (box_rect.height - height) // 2
        for col, row in cells:
            rect = pygame.Rect(origin_x + (col - min_col) * CELL_SIZE,
                               origin_y + (row - min_row) * CELL_SIZE,
                               CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, tetromino.color, rect)
            pygame.draw.rect(self.screen, COLOR_BORDER, rect, 1)
    # ------------------------------------------------------------------
    # Overlays
    # ------------------------------------------------------------------
    def draw_overlay(self, title, subtitle):
        """Dim the board and show a centred title/subtitle message."""
        overlay = pygame.Surface(self.board_rect.size, pygame.SRCALPHA)
        overlay.fill((*COLOR_OVERLAY, 180))
        self.screen.blit(overlay, self.board_rect.topleft)
        title_surf = self.font_large.render(title, True, COLOR_TEXT)
        sub_surf = self.font_small.render(subtitle, True, COLOR_TEXT_DIM)
        cx = self.board_rect.centerx
        cy = self.board_rect.centery
        self.screen.blit(title_surf, (cx - title_surf.get_width() // 2,
                                      cy - title_surf.get_height() // 2 - 20))
        self.screen.blit(sub_surf, (cx - sub_surf.get_width() // 2,
                                    cy + 10))