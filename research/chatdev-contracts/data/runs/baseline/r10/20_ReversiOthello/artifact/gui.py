'''
gui.py
Renders the Reversi board with pygame, handles mouse input, and displays
scores, turn info, valid-move hints, and game-over results.
'''
import pygame
from board import EMPTY, BLACK, WHITE, BOARD_SIZE
CELL_SIZE = 64
MARGIN_TOP = 70
MARGIN_BOTTOM = 40
BOARD_PIXELS = CELL_SIZE * BOARD_SIZE
WINDOW_WIDTH = BOARD_PIXELS
WINDOW_HEIGHT = BOARD_PIXELS + MARGIN_TOP + MARGIN_BOTTOM
GREEN = (0, 128, 0)
LINE_COLOR = (0, 0, 0)
HINT_COLOR = (255, 255, 0)
TEXT_COLOR = (255, 255, 255)
class GUI:
    """Graphical interface: draws board/discs/hints and processes clicks."""
    def __init__(self, game):
        """Initialize pygame, the window, fonts, and the game reference."""
        self.game = game
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Reversi (Othello)")
        self.font = pygame.font.SysFont(None, 28)
        self.clock = pygame.time.Clock()
        self.running = True
    def _cell_center(self, row, col):
        """Return the pixel center of board cell (row, col)."""
        return col * CELL_SIZE + CELL_SIZE // 2, \
               MARGIN_TOP + row * CELL_SIZE + CELL_SIZE // 2
    def _pixel_to_cell(self, x, y):
        """Convert a mouse position to a board (row, col), or None if outside."""
        col, row = x // CELL_SIZE, (y - MARGIN_TOP) // CELL_SIZE
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return int(row), int(col)
        return None
    def _draw_board_and_discs(self):
        """Draw the grid lines and every disc currently on the board."""
        self.screen.fill(GREEN)
        for i in range(BOARD_SIZE + 1):
            pygame.draw.line(self.screen, LINE_COLOR,
                             (i * CELL_SIZE, MARGIN_TOP),
                             (i * CELL_SIZE, MARGIN_TOP + BOARD_PIXELS), 2)
            pygame.draw.line(self.screen, LINE_COLOR,
                             (0, MARGIN_TOP + i * CELL_SIZE),
                             (BOARD_PIXELS, MARGIN_TOP + i * CELL_SIZE), 2)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell = self.game.board.grid[row][col]
                if cell in (BLACK, WHITE):
                    color = (0, 0, 0) if cell == BLACK else (255, 255, 255)
                    pygame.draw.circle(self.screen, color,
                                       self._cell_center(row, col),
                                       CELL_SIZE // 2 - 6)
    def _draw_hints(self):
        """Mark all valid moves for the current player with small dots."""
        for row, col in self.game.board.get_valid_moves(self.game.current_player):
            pygame.draw.circle(self.screen, HINT_COLOR,
                               self._cell_center(row, col), 6)
    def _draw_status(self):
        """Display the live score, current turn or result, and messages."""
        black, white = self.game.board.count_discs()
        self.screen.blit(self.font.render(
            f"Black: {black}   White: {white}", True, TEXT_COLOR), (10, 20))
        if self.game.game_over:
            status = "Game over - Draw!" if self.game.winner is None else \
                f"Game over - {'Black' if self.game.winner == BLACK else 'White'} wins!"
        else:
            status = f"{'Black' if self.game.current_player == BLACK else 'White'}'s turn"
        if self.game.message:
            status += f"  |  {self.game.message}"
        self.screen.blit(self.font.render(status, True, TEXT_COLOR),
                         (10, WINDOW_HEIGHT - MARGIN_BOTTOM + 10))
    def _handle_events(self):
        """Process quit and left-click (place disc) events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                    and not self.game.game_over:
                cell = self._pixel_to_cell(*event.pos)
                if cell:
                    self.game.handle_click(*cell)
    def run(self):
        """Main loop: handle input, redraw everything, ~30 FPS."""
        while self.running:
            self._handle_events()
            self._draw_board_and_discs()
            if not self.game.game_over:
                self._draw_hints()
            self._draw_status()
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()