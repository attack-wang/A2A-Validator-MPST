'''
ui.py
This module implements the GameUI class, a pygame-based graphical interface
for the Reversi game. It renders the board, discs, valid-move hints, score
panel, and game-over overlay, and translates mouse clicks into board moves.
'''
import sys
import pygame
from constants import (
    BOARD_SIZE, CELL_SIZE, BOARD_PIXEL_SIZE, PANEL_HEIGHT,
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WINDOW_CAPTION,
    EMPTY, BLACK, WHITE, PLAYER_NAMES,
    COLOR_BACKGROUND, COLOR_BOARD, COLOR_GRID_LINE,
    COLOR_BLACK_DISC, COLOR_WHITE_DISC, COLOR_VALID_MOVE,
    COLOR_TEXT, COLOR_PANEL, COLOR_HIGHLIGHT,
)
class GameUI:
    """Pygame-based graphical interface for the Reversi game."""
    def __init__(self, game):
        """Initialize pygame, the game window, and fonts."""
        self.game = game
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_CAPTION)
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("arial", 36, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.running = True
    def run(self):
        """Run the main game loop until the user quits."""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.render()
        pygame.quit()
    def handle_events(self):
        """Process pygame events: quitting, restarting, and mouse clicks."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.reset()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell = self.get_cell_from_mouse(event.pos)
                if cell is not None:
                    row, col = cell
                    self.game.try_move(row, col)
    def get_cell_from_mouse(self, pos):
        """
        Convert a mouse position to a (row, col) board cell.
        Return None if the click is outside the board area.
        """
        x, y = pos
        if 0 <= x < BOARD_PIXEL_SIZE and 0 <= y < BOARD_PIXEL_SIZE:
            return (y // CELL_SIZE, x // CELL_SIZE)
        return None
    def render(self):
        """Draw the complete game frame."""
        self.screen.fill(COLOR_BACKGROUND)
        self.draw_board()
        self.draw_score_panel()
        if self.game.is_game_over():
            self.draw_game_over_overlay()
        pygame.display.flip()
    def draw_board(self):
        """Draw the grid, discs, valid-move hints, and last-move highlight."""
        board_rect = pygame.Rect(0, 0, BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE)
        pygame.draw.rect(self.screen, COLOR_BOARD, board_rect)
        # Grid lines
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(
                self.screen, COLOR_GRID_LINE,
                (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_PIXEL_SIZE), 2,
            )
            pygame.draw.line(
                self.screen, COLOR_GRID_LINE,
                (0, i * CELL_SIZE), (BOARD_PIXEL_SIZE, i * CELL_SIZE), 2,
            )
        grid = self.game.board.get_grid_copy()
        valid_moves = set(self.game.get_valid_moves())
        radius = CELL_SIZE // 2 - 6
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell_center = (
                    col * CELL_SIZE + CELL_SIZE // 2,
                    row * CELL_SIZE + CELL_SIZE // 2,
                )
                disc = grid[row][col]
                if disc == BLACK:
                    pygame.draw.circle(self.screen, COLOR_BLACK_DISC, cell_center, radius)
                    pygame.draw.circle(self.screen, COLOR_WHITE_DISC, cell_center, radius, 1)
                elif disc == WHITE:
                    pygame.draw.circle(self.screen, COLOR_WHITE_DISC, cell_center, radius)
                    pygame.draw.circle(self.screen, COLOR_BLACK_DISC, cell_center, radius, 1)
                elif (row, col) in valid_moves:
                    # Small hint marker for valid moves
                    pygame.draw.circle(self.screen, COLOR_VALID_MOVE, cell_center, 8)
        # Highlight the last placed disc
        if self.game.last_move is not None:
            row, col = self.game.last_move
            center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, COLOR_HIGHLIGHT, center, radius + 3, 3)
    def draw_score_panel(self):
        """Draw the score panel showing both players' disc counts and turn."""
        panel_rect = pygame.Rect(0, BOARD_PIXEL_SIZE, WINDOW_WIDTH, PANEL_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect)
        score = self.game.get_score()
        current = self.game.get_current_player()
        # Black player's score
        black_center = (WINDOW_WIDTH // 4, BOARD_PIXEL_SIZE + PANEL_HEIGHT // 2)
        pygame.draw.circle(self.screen, COLOR_BLACK_DISC, (black_center[0] - 40, black_center[1]), 16)
        pygame.draw.circle(self.screen, COLOR_WHITE_DISC, (black_center[0] - 40, black_center[1]), 16, 1)
        black_text = self.font_medium.render(
            f"{PLAYER_NAMES[BLACK]}: {score[BLACK]}", True, COLOR_TEXT
        )
        black_rect = black_text.get_rect(midleft=(black_center[0] - 15, black_center[1]))
        self.screen.blit(black_text, black_rect)
        # White player's score
        white_center = (3 * WINDOW_WIDTH // 4, BOARD_PIXEL_SIZE + PANEL_HEIGHT // 2)
        pygame.draw.circle(self.screen, COLOR_WHITE_DISC, (white_center[0] - 40, white_center[1]), 16)
        pygame.draw.circle(self.screen, COLOR_BLACK_DISC, (white_center[0] - 40, white_center[1]), 16, 1)
        white_text = self.font_medium.render(
            f"{PLAYER_NAMES[WHITE]}: {score[WHITE]}", True, COLOR_TEXT
        )
        white_rect = white_text.get_rect(midleft=(white_center[0] - 15, white_center[1]))
        self.screen.blit(white_text, white_rect)
        # Turn indicator or game-over message
        if self.game.is_game_over():
            status_text = "Game Over - Press R to restart"
        else:
            status_text = f"Turn: {PLAYER_NAMES[current]}"
        status = self.font_small.render(status_text, True, COLOR_TEXT)
        status_rect = status.get_rect(center=(WINDOW_WIDTH // 2, BOARD_PIXEL_SIZE + PANEL_HEIGHT - 14))
        self.screen.blit(status, status_rect)
    def draw_game_over_overlay(self):
        """Draw a semi-transparent overlay announcing the final result."""
        overlay = pygame.Surface((BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))
        winner = self.game.get_winner()
        score = self.game.get_score()
        if winner is None:
            result_text = "It's a Draw!"
        else:
            result_text = f"{PLAYER_NAMES[winner]} Wins! ({score[winner]} - {score[WHITE if winner == BLACK else BLACK]})"
        title = self.font_large.render(result_text, True, COLOR_TEXT)
        title_rect = title.get_rect(center=(BOARD_PIXEL_SIZE // 2, BOARD_PIXEL_SIZE // 2 - 20))
        self.screen.blit(title, title_rect)
        hint = self.font_medium.render("Press R to Play Again", True, COLOR_HIGHLIGHT)
        hint_rect = hint.get_rect(center=(BOARD_PIXEL_SIZE // 2, BOARD_PIXEL_SIZE // 2 + 30))
        self.screen.blit(hint, hint_rect)