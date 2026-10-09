'''
renderer.py
All drawing routines for the Tetris application.
Renders the playfield panel, grid lines, locked cells, the ghost piece
(landing preview), the current falling piece, the sidebar (score, level,
lines, next-piece preview) and translucent overlays for pause / game over.
'''
import pygame
from settings import (CELL_SIZE, COLS, ROWS, PADDING, SIDEBAR_WIDTH,
                      WINDOW_WIDTH, WINDOW_HEIGHT, TETROMINO_COLORS,
                      BLACK, GRID_LINE, WHITE, GRAY, PANEL_BG,
                      OVERLAY_BG, GHOST_COLOR)
class Renderer:
    """Draws the whole game frame from the current Game state."""
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.SysFont('arial', 32, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 22, bold=True)
        self.font_small = pygame.font.SysFont('arial', 18)
    # ------------------------------------------------------------ top level
    def draw(self, game):
        """Render one complete frame."""
        self.screen.fill(BLACK)
        self.draw_board_panel()
        self.draw_grid_lines()
        self.draw_locked_cells(game.board)
        self.draw_ghost(game)
        self.draw_current_piece(game)
        self.draw_sidebar(game)
        if game.state == 'paused':
            self.draw_overlay('PAUSED', 'Press P to resume')
        elif game.state == 'game_over':
            self.draw_overlay('GAME OVER',
                              'Score: %d   Press R to restart' % game.score)
    # -------------------------------------------------------------- helpers
    def cell_rect(self, x, y):
        """Pixel rectangle of board cell (x, y)."""
        px = PADDING + x * CELL_SIZE
        py = PADDING + y * CELL_SIZE
        return pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)
    def draw_cell(self, x, y, color):
        """Draw one filled, outlined board cell."""
        rect = self.cell_rect(x, y)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 1)
    # ------------------------------------------------------------ playfield
    def draw_board_panel(self):
        """Background panel behind the playfield."""
        rect = pygame.Rect(PADDING, PADDING, COLS * CELL_SIZE,
                           ROWS * CELL_SIZE)
        pygame.draw.rect(self.screen, PANEL_BG, rect)
    def draw_grid_lines(self):
        """Subtle grid so empty cells are visible."""
        for c in range(COLS + 1):
            x = PADDING + c * CELL_SIZE
            pygame.draw.line(self.screen, GRID_LINE, (x, PADDING),
                             (x, PADDING + ROWS * CELL_SIZE))
        for r in range(ROWS + 1):
            y = PADDING + r * CELL_SIZE
            pygame.draw.line(self.screen, GRID_LINE, (PADDING, y),
                             (PADDING + COLS * CELL_SIZE, y))
    def draw_locked_cells(self, board):
        """Draw every locked cell of the stack."""
        for y in range(ROWS):
            for x in range(COLS):
                key = board.grid[y][x]
                if key is not None:
                    self.draw_cell(x, y, TETROMINO_COLORS[key])
    def draw_ghost(self, game):
        """Outline preview showing where the piece will land."""
        piece = game.current_piece
        dy = 0
        while game.board.is_valid_position(piece, 0, dy + 1):
            dy += 1
        if dy <= 0:
            return  # piece already at landing spot; skip ghost
        for x, y in piece.cells(0, dy):
            if y >= 0:
                rect = self.cell_rect(x, y).inflate(-2, -2)
                pygame.draw.rect(self.screen, GHOST_COLOR, rect, 1)
    def draw_current_piece(self, game):
        """Draw the falling piece (cells above the board are clipped)."""
        for x, y in game.current_piece.cells():
            if y >= 0:
                self.draw_cell(x, y, game.current_piece.color)
    # -------------------------------------------------------------- sidebar
    def draw_sidebar(self, game):
        """Score / level / lines panel plus next-piece preview."""
        panel_x = PADDING * 2 + COLS * CELL_SIZE
        panel_rect = pygame.Rect(panel_x, PADDING, SIDEBAR_WIDTH,
                                 ROWS * CELL_SIZE)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)
        title = self.font_big.render('TETRIS', True, WHITE)
        self.screen.blit(title, (panel_x + 20, PADDING + 15))
        labels = [('Score', str(game.score)),
                  ('Level', str(game.level)),
                  ('Lines', str(game.lines))]
        y = PADDING + 80
        for label, value in labels:
            name = self.font_small.render(label, True, GRAY)
            num = self.font_medium.render(value, True, WHITE)
            self.screen.blit(name, (panel_x + 20, y))
            self.screen.blit(num, (panel_x + 20, y + 20))
            y += 62
        # Next-piece preview
        y += 10
        nxt = self.font_small.render('NEXT', True, GRAY)
        self.screen.blit(nxt, (panel_x + 20, y))
        self.draw_preview(game.next_key, panel_x + 20, y + 30)
        controls = self.font_small.render(
            'Arrows: move/rotate', True, GRAY)
        self.screen.blit(controls, (panel_x + 20, PADDING + ROWS * CELL_SIZE - 90))
        ...