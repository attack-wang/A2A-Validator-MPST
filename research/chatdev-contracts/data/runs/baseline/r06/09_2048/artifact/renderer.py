'''
renderer.py
Pygame-based rendering layer for the 2048 game.
The Renderer class owns the pygame window and is responsible for drawing:
    * The window background, title and instruction hints.
    * The score panel (current score) and highest-tile panel.
    * The 4x4 board with colour-coded tiles.
    * The game-over overlay with restart instructions.
'''
import pygame
# ----------------------------------------------------------------------
# Layout constants (pixels)
# ----------------------------------------------------------------------
CELL_SIZE = 100          # Side length of one board cell.
CELL_GAP = 10            # Gap between cells / board padding.
GRID_PIXELS = 4 * CELL_SIZE + 5 * CELL_GAP   # 450 px board incl. padding.
MARGIN = 25              # Outer margin around the board.
HEADER_HEIGHT = 150      # Space for title + score panels above the board.
WINDOW_WIDTH = GRID_PIXELS + 2 * MARGIN      # 500 px
WINDOW_HEIGHT = HEADER_HEIGHT + GRID_PIXELS + MARGIN  # 625 px
# ----------------------------------------------------------------------
# Colour palette (classic 2048 look)
# ----------------------------------------------------------------------
COLOR_BACKGROUND = (250, 248, 239)
COLOR_BOARD = (187, 173, 160)
COLOR_EMPTY_CELL = (205, 192, 180)
COLOR_TEXT_DARK = (119, 110, 101)
COLOR_TEXT_LIGHT = (249, 246, 242)
COLOR_OVERLAY = (238, 228, 218, 150)  # RGBA for the game-over veil.
TILE_COLORS = {
    2:    ((238, 228, 218), COLOR_TEXT_DARK),
    4:    ((237, 224, 200), COLOR_TEXT_DARK),
    8:    ((242, 177, 121), COLOR_TEXT_LIGHT),
    16:   ((245, 149, 99),  COLOR_TEXT_LIGHT),
    32:   ((246, 124, 95),  COLOR_TEXT_LIGHT),
    64:   ((246, 94, 59),   COLOR_TEXT_LIGHT),
    128:  ((237, 207, 114), COLOR_TEXT_LIGHT),
    256:  ((237, 204, 97),  COLOR_TEXT_LIGHT),
    512:  ((237, 200, 80),  COLOR_TEXT_LIGHT),
    1024: ((237, 197, 63),  COLOR_TEXT_LIGHT),
    2048: ((237, 194, 46),  COLOR_TEXT_LIGHT),
}
COLOR_SUPER_TILE = (60, 58, 50)  # For values above 2048.
class Renderer:
    '''Draws the full 2048 game state into a pygame window.'''
    def __init__(self, caption='2048'):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont('arial', 48, bold=True)
        self.font_score_label = pygame.font.SysFont('arial', 16, bold=True)
        self.font_score_value = pygame.font.SysFont('arial', 26, bold=True)
        self.font_tile_small = pygame.font.SysFont('arial', 34, bold=True)
        self.font_tile_tiny = pygame.font.SysFont('arial', 26, bold=True)
        self.font_hint = pygame.font.SysFont('arial', 15)
        self.font_overlay = pygame.font.SysFont('arial', 34, bold=True)
    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def draw(self, game):
        '''Render one complete frame for the given Game2048 instance.'''
        self.window.fill(COLOR_BACKGROUND)
        self._draw_header(game)
        self._draw_board(game)
        if game.is_game_over():
            self._draw_game_over(game)
        pygame.display.flip()
    def tick(self, fps=60):
        '''Cap the frame rate and return milliseconds since last frame.'''
        return self.clock.tick(fps)
    def quit(self):
        '''Shut pygame down cleanly.'''
        pygame.quit()
    # ------------------------------------------------------------------
    # Private drawing helpers
    # ------------------------------------------------------------------
    def _draw_header(self, game):
        '''Draw the title, score panel and highest-tile panel.'''
        # Title
        title = self.font_title.render('2048', True, COLOR_TEXT_DARK)
        self.window.blit(title, (MARGIN, 30))
        hint = self.font_hint.render(
            'Arrow keys to move  |  R: new game', True, COLOR_TEXT_DARK)
        self.window.blit(hint, (MARGIN, 92))
        # Score panel and highest-tile panel on the right side.
        panel_width, panel_height = 110, 70
        panel_gap = 10
        right_edge = WINDOW_WIDTH - MARGIN
        highest_x = right_edge - panel_width
        score_x = highest_x - panel_gap - panel_width
        panel_y = 30
        self._draw_stat_panel(
            'SCORE', str(game.score), score_x, panel_y,
            panel_width, panel_height)
        self._draw_stat_panel(
            'HIGHEST', str(game.get_highest_tile()), highest_x, panel_y,
            panel_width, panel_height)
    def _draw_stat_panel(self, label, value, x, y, width, height):
        '''Draw one rounded stat box with a label and a numeric value.'''
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.window, COLOR_BOARD, rect, border_radius=6)
        pygame.draw.rect(self.window, COLOR_BOARD, rect, 1, border_radius=6)
        label_surf = self.font_score_label.render(label, True, COLOR_TEXT_LIGHT)
        value_surf = self.font_score_value.render(value, True, COLOR_TEXT_LIGHT)
        label_rect = label_surf.get_rect(center=(rect.centerx, y + 22))
        value_rect = value_surf.get_rect(center=(rect.centerx, y + 48))
        self.window.blit(label_surf, label_rect)
        self.window.blit(value_surf, value_rect)
    def _draw_board(self, game):
        '''Draw the board background, empty cells and all tiles.'''
        board_rect = pygame.Rect(
            MARGIN, HEADER_HEIGHT, GRID_PIXELS, GRID_PIXELS)
        pygame.draw.rect(self.window, COLOR_BOARD, board_rect, border_radius=8)
        for row in range(game.size):
            for col in range(game.size):
                x = MARGIN + CELL_GAP + col * (CELL_SIZE + CELL_GAP)
                y = HEADER_HEIGHT + CELL_GAP + row * (CELL_SIZE + CELL_GAP)
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                value = game.grid[row][col]
                if value == 0:
                    pygame.draw.rect(
                        self.window, COLOR_EMPTY_CELL, cell_rect,
                        border_radius=6)
                else:
                    self._draw_tile(cell_rect, value)
    def _draw_tile(self, rect, value):
        '''Draw a single numbered tile centred inside `rect`.'''
        fill, text_color = TILE_COLORS.get(value, (COLOR_SUPER_TILE, COLOR_TEXT_LIGHT))
        pygame.draw.rect(self.window, fill, rect, border_radius=6)
        text = str(value)
        if len(text) <= 2:
            font = self.font_tile_small
        else:
            font = self.font_tile_tiny
        surf = font.render(text, True, text_color)
        surf_rect = surf.get_rect(center=rect.center)
        self.window.blit(surf, surf_rect)
    def _draw_game_over(self, game):
        '''Draw a translucent veil with the final message and restart hint.'''
        board_rect = pygame.Rect(
            MARGIN, HEADER_HEIGHT, GRID_PIXELS, GRID_PIXELS)
        veil = pygame.Surface((GRID_PIXELS, GRID_PIXELS), pygame.SRCALPHA)
        veil.fill(COLOR_OVERLAY)
        self.window.blit(veil, board_rect.topleft)
        message = self.font_overlay.render('Game Over!', True, COLOR_TEXT_DARK)
        message_rect = message.get_rect(center=board_rect.center)
        self.window.blit(message, message_rect)
        hint_font = pygame.font.SysFont('arial', 20, bold=True)
        hint = hint_font.render(
            f'Final score: {game.score}  -  Press R for a new game',
            True, COLOR_TEXT_DARK)
        hint_rect = hint.get_rect(center=(board_rect.centerx, board_rect.centery + 45))
        self.window.blit(hint, hint_rect)