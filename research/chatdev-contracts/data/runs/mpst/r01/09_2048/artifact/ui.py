'''
ui.py
Pygame-based presentation layer for the 2048 game: window setup,
keyboard input mapping and all drawing routines (board, tiles, score
header, win banner and game-over overlay).
'''
import pygame
from constants import (
    BORDER_MARGIN,
    CELL_MARGIN,
    CELL_SIZE,
    COLOR_BACKGROUND,
    COLOR_EMPTY_CELL,
    COLOR_OVERLAY,
    COLOR_OVERLAY_ALPHA,
    COLOR_SCORE_BOX,
    COLOR_TEXT_DARK,
    COLOR_TEXT_LIGHT,
    FONT_NAME,
    FONT_SIZE_MESSAGE,
    FONT_SIZE_SCORE_LABEL,
    FONT_SIZE_SCORE_VALUE,
    FONT_SIZE_TILE_LARGE,
    FONT_SIZE_TILE_MEDIUM,
    FONT_SIZE_TILE_SMALL,
    FONT_SIZE_TITLE,
    GRID_SIZE,
    HEADER_HEIGHT,
    TILE_COLOR_SUPER,
    TILE_COLORS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
class GameUI:
    '''Handles the pygame window, input events and rendering.'''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('2048')
        self.clock = pygame.time.Clock()
        self._load_fonts()
    def _load_fonts(self):
        '''Create the font objects used across the different draw calls.'''
        self.font_title = pygame.font.Font(FONT_NAME, FONT_SIZE_TITLE)
        self.font_tile_large = pygame.font.Font(FONT_NAME, FONT_SIZE_TILE_LARGE)
        self.font_tile_medium = pygame.font.Font(FONT_NAME, FONT_SIZE_TILE_MEDIUM)
        self.font_tile_small = pygame.font.Font(FONT_NAME, FONT_SIZE_TILE_SMALL)
        self.font_score_label = pygame.font.Font(FONT_NAME, FONT_SIZE_SCORE_LABEL)
        self.font_score_value = pygame.font.Font(FONT_NAME, FONT_SIZE_SCORE_VALUE)
        self.font_message = pygame.font.Font(FONT_NAME, FONT_SIZE_MESSAGE)
    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def handle_events(self):
        '''
        Pump the pygame event queue.
        Returns a tuple (direction, restart, quit_game) where:
            direction -> 'up'/'down'/'left'/'right' or None
            restart   -> True when the player asked for a new game (R)
            quit_game -> True when the window was closed / ESC pressed
        '''
        direction = None
        restart = False
        quit_game = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    direction = 'left'
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    direction = 'right'
                elif event.key in (pygame.K_UP, pygame.K_w):
                    direction = 'up'
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    direction = 'down'
                elif event.key == pygame.K_r:
                    restart = True
                elif event.key == pygame.K_ESCAPE:
                    quit_game = True
        return direction, restart, quit_game
    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def draw(self, game):
        '''Render one full frame of the game state.'''
        self.screen.fill(COLOR_BACKGROUND)
        self._draw_header(game)
        self._draw_board(game)
        if game.won and not game.game_over:
            self._draw_win_banner()
        if game.game_over:
            self._draw_game_over(game)
        pygame.display.flip()
    def _cell_rect(self, row, col):
        '''Return the pygame.Rect of the cell at (row, col).'''
        x = BORDER_MARGIN + CELL_MARGIN + col * (CELL_SIZE + CELL_MARGIN)
        y = HEADER_HEIGHT + BORDER_MARGIN + CELL_MARGIN + row * (CELL_SIZE + CELL_MARGIN)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    def _draw_header(self, game):
        '''Draw the title and the score / best-tile boxes.'''
        # Title
        title = self.font_title.render('2048', True, COLOR_TEXT_DARK)
        self.screen.blit(title, (BORDER_MARGIN, 20))
        # Score box
        self._draw_score_box(
            'SCORE', str(game.score),
            WINDOW_WIDTH - 2 * (110 + BORDER_MARGIN), 20
        )
        # Highest tile box
        self._draw_score_box(
            'BEST TILE', str(game.get_highest_tile()),
            WINDOW_WIDTH - (110 + BORDER_MARGIN), 20
        )
    def _draw_score_box(self, label, value, x, y):
        '''Draw a small rounded box with a label and a value.'''
        box = pygame.Rect(x, y, 110, 70)
        pygame.draw.rect(self.screen, COLOR_SCORE_BOX, box, border_radius=6)
        label_surf = self.font_score_label.render(label, True, COLOR_TEXT_LIGHT)
        value_surf = self.font_score_value.render(value, True, COLOR_TEXT_LIGHT)
        label_rect = label_surf.get_rect(center=(box.centerx, box.y + 20))
        value_rect = value_surf.get_rect(center=(box.centerx, box.y + 48))
        self.screen.blit(label_surf, label_rect)
        self.screen.blit(value_surf, value_rect)
    def _draw_board(self, game):
        '''Draw the empty grid and every tile on it.'''
        # Board background (the gaps between cells show through)
        board_rect = pygame.Rect(
            BORDER_MARGIN + CELL_MARGIN,
            HEADER_HEIGHT + BORDER_MARGIN + CELL_MARGIN,
            GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * CELL_MARGIN,
            GRID_SIZE * CELL_SIZE + (GRID_SIZE - 1) * CELL_MARGIN,
        )
        pygame.draw.rect(self.screen, COLOR_EMPTY_CELL, board_rect, border_radius=6)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = self._cell_rect(row, col)
                value = game.grid[row][col]
                if value == 0:
                    pygame.draw.rect(self.screen, COLOR_EMPTY_CELL, rect, border_radius=6)
                else:
                    self._draw_tile(rect, value)
    def _draw_tile(self, rect, value):
        '''Draw a single numbered tile centered inside its cell.'''
        background, text_color = TILE_COLORS.get(value, TILE_COLOR_SUPER)
        pygame.draw.rect(self.screen, background, rect, border_radius=6)
        text = str(value)
        if len(text) <= 2:
            font = self.font_tile_large
        elif len(text) == 3:
            font = self.font_tile_medium
        else:
            font = self.font_tile_small
        surface = font.render(text, True, text_color)
        self.screen.blit(surface, surface.get_rect(center=rect.center))
    def _draw_win_banner(self):
        '''Show a small banner once the player has built a 2048 tile.'''
        text = self.font_message.render('You made 2048! Keep going!', True, COLOR_TEXT_DARK)
        rect = text.get_rect(midbottom=(WINDOW_WIDTH // 2, HEADER_HEIGHT - 5))
        self.screen.blit(text, rect)
    def _draw_game_over(self, game):
        '''Dim the board and show the game-over message and stats.'''
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(COLOR_OVERLAY_ALPHA)
        overlay.fill(COLOR_OVERLAY)
        self.screen.blit(overlay, (0, 0))
        lines = [
            ('Game Over!', self.font_message),
            (f'Final score: {game.score}', self.font_score_value),
            (f'Highest tile: {game.get_highest_tile()}', self.font_score_value),
            ('Press R to play again', self.font_score_label),
        ]
        y = WINDOW_HEIGHT // 2 - 80
        for text, font in lines:
            surface = font.render(text, True, COLOR_TEXT_DARK)
            rect = surface.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(surface, rect)
            y += 50