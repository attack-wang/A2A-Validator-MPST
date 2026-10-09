'''
Graphical interface module for the Gomoku game.
Defines the GUI class which renders the board, stones, status bar and
restart button with pygame, and converts mouse coordinates into board
intersections.
'''
import pygame
from board import Board
class GUI:
    """Handles all rendering and coordinate conversion for the game."""
    # Layout constants (pixels).
    MARGIN = 40          # Space around the playing grid.
    CELL = 40            # Distance between two adjacent intersections.
    STATUS_HEIGHT = 90   # Extra space below the board for status/button.
    # Colors.
    COLOR_BACKGROUND = (222, 184, 135)   # Wood-like board color.
    COLOR_LINE = (60, 40, 20)
    COLOR_TEXT = (30, 30, 30)
    COLOR_BUTTON = (70, 130, 180)
    COLOR_BUTTON_TEXT = (255, 255, 255)
    COLOR_HIGHLIGHT = (200, 60, 60)
    COLOR_LAST_MOVE = (220, 40, 40)
    def __init__(self, game):
        self.game = game
        self.board_size = game.board.size
        self.grid_pixels = (self.board_size - 1) * self.CELL
        self.width = self.grid_pixels + 2 * self.MARGIN
        self.height = self.grid_pixels + 2 * self.MARGIN + self.STATUS_HEIGHT
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Gomoku - Five in a Row")
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.button_font = pygame.font.SysFont("arial", 20, bold=True)
        # Restart button rectangle (centered under the board).
        button_width, button_height = 160, 40
        self.button_rect = pygame.Rect(
            (self.width - button_width) // 2,
            self.grid_pixels + 2 * self.MARGIN + (self.STATUS_HEIGHT - button_height) // 2,
            button_width,
            button_height,
        )
        self.hover_pos = None  # Board coordinates currently hovered.
    # ------------------------------------------------------------------
    # Coordinate conversion
    # ------------------------------------------------------------------
    def get_board_position(self, mouse_pos):
        """Convert pixel coordinates to the nearest board intersection.
        Returns (row, col) if the click is close enough to an
        intersection, otherwise None.
        """
        x, y = mouse_pos
        col = round((x - self.MARGIN) / self.CELL)
        row = round((y - self.MARGIN) / self.CELL)
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            px = self.MARGIN + col * self.CELL
            py = self.MARGIN + row * self.CELL
            # Only accept clicks reasonably close to the intersection.
            if abs(x - px) <= self.CELL // 2 and abs(y - py) <= self.CELL // 2:
                return row, col
        return None
    def point_to_pixel(self, row, col):
        """Convert board coordinates to pixel coordinates of center."""
        return (self.MARGIN + col * self.CELL, self.MARGIN + row * self.CELL)
    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------
    def draw_board(self):
        """Draw the wooden background, grid lines and star points."""
        self.screen.fill(self.COLOR_BACKGROUND)
        for i in range(self.board_size):
            start = self.point_to_pixel(i, 0)
            end = self.point_to_pixel(i, self.board_size - 1)
            pygame.draw.line(self.screen, self.COLOR_LINE, start, end, 2)
            start = self.point_to_pixel(0, i)
            end = self.point_to_pixel(self.board_size - 1, i)
            pygame.draw.line(self.screen, self.COLOR_LINE, start, end, 2)
        # Star points (hoshi) as on a standard Go/Gomoku board.
        stars = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
        for row, col in stars:
            px, py = self.point_to_pixel(row, col)
            pygame.draw.circle(self.screen, self.COLOR_LINE, (px, py), 5)
    def draw_stones(self):
        """Draw all placed stones, the last-move marker and hover ghost."""
        radius = self.CELL // 2 - 3
        for row in range(self.board_size):
            for col in range(self.board_size):
                stone = self.game.board.get_stone(row, col)
                if stone == Board.EMPTY:
                    continue
                px, py = self.point_to_pixel(row, col)
                if stone == Board.BLACK:
                    pygame.draw.circle(self.screen, (20, 20, 20), (px, py), radius)
                    pygame.draw.circle(self.screen, (80, 80, 80),
                                       (px - radius // 3, py - radius // 3), radius // 3)
                else:
                    pygame.draw.circle(self.screen, (245, 245, 245), (px, py), radius)
                    pygame.draw.circle(self.screen, (120, 120, 120), (px, py), radius, 2)
                    pygame.draw.circle(self.screen, (200, 200, 200),
                                       (px - radius // 3, py - radius // 3), radius // 3)
        # Highlight the most recent move.
        if self.game.board.last_move is not None:
            row, col = self.game.board.last_move
            px, py = self.point_to_pixel(row, col)
            pygame.draw.circle(self.screen, self.COLOR_LAST_MOVE, (px, py), 4)
        # Ghost stone under the cursor while the game is running.
        if self.hover_pos is not None and not self.game.is_over:
            row, col = self.hover_pos
            if self.game.board.is_valid_move(row, col):
                px, py = self.point_to_pixel(row, col)
                color = (40, 40, 40) if self.game.current_player == Board.BLACK else (230, 230, 230)
                ghost = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(ghost, (*color, 120), (radius, radius), radius)
                self.screen.blit(ghost, (px - radius, py - radius))
    def draw_winning_line(self):
        """Draw a highlight over the five winning stones."""
        if self.game.winning_line:
            for row, col in self.game.winning_line:
                px, py = self.point_to_pixel(row, col)
                pygame.draw.circle(self.screen, self.COLOR_HIGHLIGHT,
                                   (px, py), self.CELL // 2 - 3, 3)
    def draw_status(self):
        """Draw the status text and the restart button."""
        message = self.game.status_message()
        text = self.font.render(message, True, self.COLOR_TEXT)
        text_rect = text.get_rect(midbottom=(self.width // 2, self.button_rect.top - 8))
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, self.COLOR_BUTTON, self.button_rect, border_radius=8)
        label = self.button_font.render("Restart", True, self.COLOR_BUTTON_TEXT)
        label_rect = label.get_rect(center=self.button_rect.center)
        self.screen.blit(label, label_rect)
    def render(self):
        """Render one complete frame."""
        self.draw_board()
        self.draw_stones()
        self.draw_winning_line()
        self.draw_status()
        pygame.display.flip()
    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------
    def handle_event(self, event):
        """Process a single pygame event; returns True if a move was made."""
        if event.type == pygame.MOUSEMOTION:
            self.hover_pos = self.get_board_position(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.game.reset()
                return False
            pos = self.get_board_position(event.pos)
            if pos is not None:
                row, col = pos
                if self.game.try_move(row, col):
                    return True
        return False
    def quit(self):
        """Clean up pygame resources."""
        pygame.quit()