'''
GUI module: renders the Reversi board with pygame, handles mouse clicks,
highlights valid moves and the last move, and shows scores/messages.
'''
import sys
try:
    import pygame
except ImportError:
    pygame = None
from constants import (BOARD_SIZE, CELL_SIZE, INFO_HEIGHT, WINDOW_WIDTH,
                       WINDOW_HEIGHT, BLACK, WHITE, PLAYER_NAMES,
                       COLOR_BACKGROUND, COLOR_BOARD_GREEN, COLOR_GRID_LINE,
                       COLOR_BLACK_DISC, COLOR_WHITE_DISC, COLOR_VALID_MOVE,
                       COLOR_TEXT, COLOR_INFO_PANEL, COLOR_LAST_MOVE,
                       GAME_TITLE)
from game import Game
class ReversiGUI:
    '''Pygame-based graphical interface for the Reversi game.'''
    def __init__(self, game):
        '''Initialize pygame, create the window/fonts, store the game state.'''
        if pygame is None:
            print("Pygame is required to run this game. "
                  "Install it with: pip install pygame")
            sys.exit(1)
        pygame.init()
        self.game = game
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.font_medium = pygame.font.SysFont(None, 34)
        self.font_small = pygame.font.SysFont(None, 26)
        self.clock = pygame.time.Clock()
    def run(self):
        '''Main loop: handle events, redraw each frame, quit cleanly.'''
        running = True
        while running:
            running = self._handle_events()
            self._draw()
            self.clock.tick(60)
        pygame.quit()
    def _handle_events(self):
        '''Process quit / restart (R) / mouse-click events; False stops the loop.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.game = Game()  # restart with a fresh game state
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                  and not self.game.game_over):
                row, col = self._cell_from_mouse(pygame.mouse.get_pos())
                if row is not None:
                    self.game.make_move(row, col)
        return True
    def _cell_from_mouse(self, pos):
        '''Convert mouse position to (row, col); (None, None) if outside board.'''
        x, y = pos
        if 0 <= x < WINDOW_WIDTH and INFO_HEIGHT <= y < WINDOW_HEIGHT:
            return (y - INFO_HEIGHT) // CELL_SIZE, x // CELL_SIZE
        return None, None
    def _draw(self):
        '''Render one full frame: board area plus the score panel.'''
        self.screen.fill(COLOR_BACKGROUND)
        self._draw_board()
        self.draw_score()
        pygame.display.flip()
    def _draw_board(self):
        '''Draw grid, discs, valid-move hints, and last-move highlight.'''
        pygame.draw.rect(self.screen, COLOR_BOARD_GREEN,
                         (0, INFO_HEIGHT, BOARD_SIZE * CELL_SIZE,
                          BOARD_SIZE * CELL_SIZE))
        valid_moves = set(self.game.get_valid_moves())
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                center = (col * CELL_SIZE + CELL_SIZE // 2,
                          INFO_HEIGHT + row * CELL_SIZE + CELL_SIZE // 2)
                disc = self.game.board.get_disc(row, col)
                if disc in (BLACK, WHITE):
                    color = COLOR_BLACK_DISC if disc == BLACK else COLOR_WHITE_DISC
                    pygame.draw.circle(self.screen, color,
                                       center, CELL_SIZE // 2 - 6)
                elif (row, col) in valid_moves and not self.game.game_over:
                    pygame.draw.circle(self.screen, COLOR_VALID_MOVE, center, 8)
                if self.game.last_move == (row, col):
                    pygame.draw.circle(self.screen, COLOR_LAST_MOVE, center,
                                       CELL_SIZE // 2 - 6, 3)
        for i in range(BOARD_SIZE + 1):  # grid lines
            pygame.draw.line(self.screen, COLOR_GRID_LINE,
                             (i * CELL_SIZE, INFO_HEIGHT),
                             (i * CELL_SIZE, INFO_HEIGHT + BOARD_SIZE * CELL_SIZE), 2)
            pygame.draw.line(self.screen, COLOR_GRID_LINE,
                             (0, INFO_HEIGHT + i * CELL_SIZE),
                             (BOARD_SIZE * CELL_SIZE, INFO_HEIGHT + i * CELL_SIZE), 2)
    def draw_score(self):
        '''Draw the info panel: scores, turn indicator, messages, game result.'''
        pygame.draw.rect(self.screen, COLOR_INFO_PANEL,
                         (0, 0, WINDOW_WIDTH, INFO_HEIGHT))
        black_score, white_score = self.game.get_score()
        pygame.draw.circle(self.screen, COLOR_BLACK_DISC, (35, 30), 14)
        text_black = self.font_medium.render(f"Black: {black_score}", True, COLOR_TEXT)
        self.screen.blit(text_black, (60, 30 - text_black.get_height() // 2))
        pygame.draw.circle(self.screen, COLOR_WHITE_DISC, (280, 30), 14)
        text_white = self.font_medium.render(f"White: {white_score}", True, COLOR_TEXT)
        self.screen.blit(text_white, (305, 30 - text_white.get_height() // 2))
        if self.game.game_over:
            if self.game.winner is None:
                status_text = f"Draw! Final score {black_score}-{white_score}. Press R to restart."
            else:
                status_text = (f"{PLAYER_NAMES[self.game.winner]} wins "
                               f"{black_score}-{white_score}! Press R to restart.")
        elif self.game.message:
            status_text = self.game.message
        else:
            status_text = f"{self.game.get_current_player_name()}'s turn"
        text_status = self.font_small.render(status_text, True, COLOR_TEXT)
        self.screen.blit(text_status, (20, 75 - text_status.get_height() // 2))