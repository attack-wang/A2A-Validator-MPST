'''
gui.py
Rendering module for the Gomoku game. Provides the GUI class, which draws
the wooden board, grid lines, star points, stones, last-move and winning
highlights, a hover preview of the pending move, and the status bar, using
pygame. It also converts mouse pixel positions into board intersections.
'''
import pygame
from constants import (
    BOARD_SIZE, CELL_SIZE, MARGIN, STONE_RADIUS,
    BOARD_PIXEL_SIZE, STATUS_BAR_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT,
    COLOR_BACKGROUND, COLOR_LINE, COLOR_STATUS_BG, COLOR_TEXT,
    COLOR_BLACK, COLOR_WHITE, COLOR_WHITE_OUTLINE,
    COLOR_LAST_MOVE, COLOR_WIN,
    EMPTY, BLACK,
)
class GUI:
    '''Handles all pygame drawing and mouse-to-board coordinate mapping.'''
    def __init__(self, screen):
        '''
        Store the target surface and prepare fonts used by the status bar.
        '''
        self.screen = screen
        try:
            self.font = pygame.font.SysFont("arial", 22, bold=True)
        except Exception:
            self.font = pygame.font.Font(None, 28)
    # ------------------------------------------------------------------
    # Coordinate conversion
    # ------------------------------------------------------------------
    def board_to_pixel(self, row, col):
        '''Convert board intersection (row, col) to pixel (x, y) center.'''
        x = MARGIN + col * CELL_SIZE
        y = MARGIN + row * CELL_SIZE
        return x, y
    def pixel_to_board(self, px, py):
        '''
        Convert a pixel position to the nearest board intersection.
        Returns (row, col) if the position maps onto the board area,
        otherwise None.
        '''
        col = round((px - MARGIN) / CELL_SIZE)
        row = round((py - MARGIN) / CELL_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            x, y = self.board_to_pixel(row, col)
            if abs(px - x) <= CELL_SIZE / 2 and abs(py - y) <= CELL_SIZE / 2:
                return row, col
        return None
    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def draw(self, board, status_text, win_cells=None, hover_cell=None,
             hover_player=BLACK):
        '''Render the complete game scene and flip the display.'''
        self.screen.fill(COLOR_BACKGROUND)
        self.draw_grid()
        self.draw_stones(board, win_cells)
        # Suppress the hover preview once a winning line is highlighted.
        if hover_cell and not win_cells:
            self.draw_hover(board, hover_cell, hover_player)
        self.draw_status(status_text)
        pygame.display.flip()
    def draw_grid(self):
        '''Draw the 15x15 grid lines and the five traditional star points.'''
        for i in range(BOARD_SIZE):
            thick = 2 if i in (0, BOARD_SIZE - 1) else 1
            # Horizontal line across row i.
            start = self.board_to_pixel(i, 0)
            end = self.board_to_pixel(i, BOARD_SIZE - 1)
            pygame.draw.line(self.screen, COLOR_LINE, start, end, thick)
            # Vertical line down column i.
            start = self.board_to_pixel(0, i)
            end = self.board_to_pixel(BOARD_SIZE - 1, i)
            pygame.draw.line(self.screen, COLOR_LINE, start, end, thick)
        # Star points (hoshi) used on a standard 15x15 board.
        star_points = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
        for row, col in star_points:
            x, y = self.board_to_pixel(row, col)
            pygame.draw.circle(self.screen, COLOR_LINE, (x, y), 4)
    def draw_stones(self, board, win_cells=None):
        '''
        Draw every placed stone. The last move gets a red ring and the
        cells of the winning line get an orange ring.
        '''
        win_set = set(win_cells) if win_cells else set()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                player = board.grid[row][col]
                if player == EMPTY:
                    continue
                x, y = self.board_to_pixel(row, col)
                if player == BLACK:
                    pygame.draw.circle(self.screen, COLOR_BLACK, (x, y), STONE_RADIUS)
                else:
                    pygame.draw.circle(self.screen, COLOR_WHITE, (x, y), STONE_RADIUS)
                    pygame.draw.circle(self.screen, COLOR_WHITE_OUTLINE, (x, y), STONE_RADIUS, 1)
                if (row, col) in win_set:
                    pygame.draw.circle(self.screen, COLOR_WIN, (x, y), STONE_RADIUS + 3, 2)
                elif (row, col) == board.last_move:
                    pygame.draw.circle(self.screen, COLOR_LAST_MOVE, (x, y), STONE_RADIUS + 3, 2)
    def draw_hover(self, board, cell, player):
        '''
        Draw a translucent preview stone at `cell` so the player can see
        where the stone will land before clicking.
        '''
        row, col = cell
        if not board.is_valid_move(row, col):
            return
        x, y = self.board_to_pixel(row, col)
        rgba = (0, 0, 0, 90) if player == BLACK else (255, 255, 255, 130)
        surface = pygame.Surface((STONE_RADIUS * 2 + 2, STONE_RADIUS * 2 + 2), pygame.SRCALPHA)
        center = (STONE_RADIUS + 1, STONE_RADIUS + 1)
        pygame.draw.circle(surface, rgba, center, STONE_RADIUS)
        self.screen.blit(surface, (x - STONE_RADIUS - 1, y - STONE_RADIUS - 1))
    def draw_status(self, status_text):
        '''Render the status bar and centered message at the window bottom.'''
        bar_rect = pygame.Rect(0, BOARD_PIXEL_SIZE, WINDOW_WIDTH, STATUS_BAR_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_STATUS_BG, bar_rect)
        pygame.draw.line(self.screen, COLOR_LINE, (0, BOARD_PIXEL_SIZE),
                         (WINDOW_WIDTH, BOARD_PIXEL_SIZE), 2)
        text = self.font.render(status_text, True, COLOR_TEXT)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, BOARD_PIXEL_SIZE + STATUS_BAR_HEIGHT // 2))
        self.screen.blit(text, text_rect)