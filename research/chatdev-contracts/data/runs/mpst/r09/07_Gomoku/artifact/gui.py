'''
gui.py
Reusable GUI widgets and drawing helpers for the Gomoku game:
clickable button, coordinate conversion and all board rendering routines.
'''
import pygame
from config import (MARGIN, CELL_SIZE, BOARD_SIZE, BOARD_PIXEL_SIZE, EMPTY,
                    PLAYER_BLACK, PLAYER_WHITE, STONE_RADIUS,
                    LAST_MOVE_MARKER_COLOR, COLOR_BACKGROUND, COLOR_LINE,
                    COLOR_STAR, COLOR_BLACK_STONE, COLOR_WHITE_STONE,
                    COLOR_TEXT, COLOR_WIN_HIGHLIGHT, COLOR_PANEL,
                    COLOR_BUTTON, COLOR_BUTTON_HOVER, STATUS_BAR_HEIGHT,
                    WINDOW_WIDTH, WINDOW_HEIGHT, FONT_SIZE_STATUS)
class Button:
    """A simple clickable button with a hover highlight."""
    def __init__(self, rect, text, font, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.hovered = False
    def update(self, mouse_pos):
        """Refresh the hover state; call once per frame."""
        self.hovered = self.rect.collidepoint(mouse_pos)
    def handle_event(self, event):
        """Return True if the button was clicked inside this event."""
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.rect.collidepoint(event.pos)):
            if self.callback:
                self.callback()
            return True
        return False
    def draw(self, surface):
        """Render the button onto the given surface."""
        color = COLOR_BUTTON_HOVER if self.hovered else COLOR_BUTTON
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        label = self.font.render(self.text, True, (255, 255, 255))
        surface.blit(label, label.get_rect(center=self.rect.center))
def grid_to_pixel(row, col):
    """Convert grid coordinates to the pixel centre of an intersection."""
    return MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE
def pixel_to_grid(pos):
    """
    Convert a mouse position to (row, col) grid coordinates.
    Returns (row, col) when the click lands close enough to a valid
    intersection, otherwise None.
    """
    x, y = pos
    col = round((x - MARGIN) / CELL_SIZE)
    row = round((y - MARGIN) / CELL_SIZE)
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        cx, cy = grid_to_pixel(row, col)
        tolerance = CELL_SIZE * 0.75
        if (x - cx) ** 2 + (y - cy) ** 2 <= tolerance ** 2:
            return row, col
    return None
def draw_board(surface):
    """Draw the wooden background, the 15x15 grid and the star points."""
    surface.fill(COLOR_BACKGROUND)
    for i in range(BOARD_SIZE):
        # Horizontal grid line
        pygame.draw.line(surface, COLOR_LINE,
                         (MARGIN, MARGIN + i * CELL_SIZE),
                         (MARGIN + BOARD_PIXEL_SIZE, MARGIN + i * CELL_SIZE), 2)
        # Vertical grid line
        pygame.draw.line(surface, COLOR_LINE,
                         (MARGIN + i * CELL_SIZE, MARGIN),
                         (MARGIN + i * CELL_SIZE, MARGIN + BOARD_PIXEL_SIZE), 2)
    # Star points (hoshi) used as visual reference marks
    for row, col in ((3, 3), (3, 11), (7, 7), (11, 3), (11, 11)):
        pygame.draw.circle(surface, COLOR_STAR, grid_to_pixel(row, col), 5)
def draw_stones(surface, board):
    """Draw every stone currently placed on the board."""
    for row in range(board.size):
        for col in range(board.size):
            stone = board.grid[row][col]
            if stone == EMPTY:
                continue
            center = grid_to_pixel(row, col)
            color = (COLOR_BLACK_STONE if stone == PLAYER_BLACK
                     else COLOR_WHITE_STONE)
            pygame.draw.circle(surface, color, center, STONE_RADIUS)
            # Thin outline keeps white stones visible on the light board
            pygame.draw.circle(surface, COLOR_LINE, center, STONE_RADIUS, 1)
def draw_winning_line(surface, cells):
    """Highlight every stone belonging to the winning five-in-a-row."""
    for row, col in cells:
        pygame.draw.circle(surface, COLOR_WIN_HIGHLIGHT,
                           grid_to_pixel(row, col), STONE_RADIUS + 3, 3)
def draw_last_move_marker(surface, last_move):
    """Draw a small red dot marking the most recent move."""
    pygame.draw.circle(surface, LAST_MOVE_MARKER_COLOR,
                       grid_to_pixel(*last_move), 5)
def draw_status(surface, message, current_player=None):
    """
    Draw the status bar: an optional stone icon showing whose turn it is
    plus the current message (auto-shrunk so it always fits the bar).
    """
    bar_rect = pygame.Rect(0, WINDOW_HEIGHT - STATUS_BAR_HEIGHT,
                           WINDOW_WIDTH, STATUS_BAR_HEIGHT)
    pygame.draw.rect(surface, COLOR_PANEL, bar_rect)
    text_left = bar_rect.x + 15
    if current_player is not None:
        stone_color = (COLOR_BLACK_STONE if current_player == PLAYER_BLACK
                       else COLOR_WHITE_STONE)
        icon_center = (bar_rect.x + 30, bar_rect.centery)
        pygame.draw.circle(surface, stone_color, icon_center, 12)
        pygame.draw.circle(surface, COLOR_LINE, icon_center, 12, 1)
        text_left = bar_rect.x + 52
    max_width = bar_rect.right - text_left - 15
    size = FONT_SIZE_STATUS
    font = pygame.font.SysFont("arial", size, bold=True)
    text_img = font.render(message, True, COLOR_TEXT)
    while text_img.get_width() > max_width and size > 12:
        size -= 2
        font = pygame.font.SysFont("arial", size, bold=True)
        text_img = font.render(message, True, COLOR_TEXT)
    surface.blit(text_img, text_img.get_rect(midleft=(text_left, bar_rect.centery)))