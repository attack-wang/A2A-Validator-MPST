'''
Graphical user interface for the Reversi game using pygame.
Renders the board, discs, valid moves, score, and pass notifications;
handles player input and game-over / restart flow.
'''
import pygame
from game_logic import ReversiGame
# Constants
CELL_SIZE = 70
MARGIN = 60  # Space for score panel at top
BOARD_PIXELS = ReversiGame.BOARD_SIZE * CELL_SIZE
WINDOW_WIDTH = BOARD_PIXELS
WINDOW_HEIGHT = BOARD_PIXELS + MARGIN
# Colors
COLOR_BACKGROUND = (30, 100, 30)      # Dark green felt
COLOR_GRID_LINE = (15, 60, 15)
COLOR_BLACK_DISC = (20, 20, 20)
COLOR_WHITE_DISC = (245, 245, 245)
COLOR_VALID_MOVE = (100, 200, 100)
COLOR_TEXT = (255, 255, 200)
COLOR_PANEL = (20, 70, 20)
COLOR_HIGHLIGHT = (255, 215, 0)
class GameGUI:
    '''Pygame-based interface for playing Reversi.'''
    def __init__(self):
        pygame.init()
        self.game = ReversiGame()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Reversi (Othello)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.big_font = pygame.font.SysFont("arial", 40, bold=True)
        self.running = True
        self.game_over = False
    def cell_to_pixel(self, row, col):
        '''Convert board coordinates to top-left pixel of the cell.'''
        x = col * CELL_SIZE
        y = MARGIN + row * CELL_SIZE
        return x, y
    def pixel_to_cell(self, px, py):
        '''Convert pixel coordinates to board coordinates, or None if outside.'''
        col = px // CELL_SIZE
        row = (py - MARGIN) // CELL_SIZE
        if 0 <= row < ReversiGame.BOARD_SIZE and 0 <= col < ReversiGame.BOARD_SIZE:
            return row, col
        return None
    def handle_events(self):
        '''Process pygame events: quitting and mouse clicks.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_over:
                    # Restart on click after game over
                    self.game = ReversiGame()
                    self.game_over = False
                else:
                    cell = self.pixel_to_cell(*event.pos)
                    if cell:
                        row, col = cell
                        if self.game.is_valid_move(row, col, self.game.current_player):
                            self.game.make_move(row, col, self.game.current_player)
                            if self.game.is_game_over():
                                self.game_over = True
    def draw_board(self):
        '''Draw the grid lines and cell backgrounds.'''
        self.screen.fill(COLOR_BACKGROUND)
        for row in range(ReversiGame.BOARD_SIZE):
            for col in range(ReversiGame.BOARD_SIZE):
                x, y = self.cell_to_pixel(row, col)
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, COLOR_BACKGROUND, rect)
                pygame.draw.rect(self.screen, COLOR_GRID_LINE, rect, 2)
    def draw_discs(self):
        '''Draw all discs currently on the board.'''
        radius = CELL_SIZE // 2 - 6
        for row in range(ReversiGame.BOARD_SIZE):
            for col in range(ReversiGame.BOARD_SIZE):
                cell = self.game.board[row][col]
                if cell != ReversiGame.EMPTY:
                    x, y = self.cell_to_pixel(row, col)
                    center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                    color = COLOR_BLACK_DISC if cell == ReversiGame.BLACK else COLOR_WHITE_DISC
                    pygame.draw.circle(self.screen, color, center, radius)
                    # Outline for white discs visibility
                    pygame.draw.circle(self.screen, COLOR_GRID_LINE, center, radius, 1)
    def draw_valid_moves(self):
        '''Highlight valid moves for the current player with small markers.'''
        for row, col in self.game.get_valid_moves(self.game.current_player):
            x, y = self.cell_to_pixel(row, col)
            center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, COLOR_VALID_MOVE, center, 8)
    def get_pass_notice(self):
        '''Return a message if the opponent must pass (has no valid moves).'''
        if self.game_over:
            return ""
        opponent = self.game.get_opponent(self.game.current_player)
        if not self.game.get_valid_moves(opponent):
            name = "White" if opponent == ReversiGame.WHITE else "Black"
            return f"{name} must pass"
        return ""
    def draw_pass_banner(self):
        '''Draw a translucent banner announcing that a player must pass.'''
        notice = self.get_pass_notice()
        if notice:
            banner = pygame.Surface((WINDOW_WIDTH, 36), pygame.SRCALPHA)
            banner.fill((255, 215, 0, 180))
            self.screen.blit(banner, (0, MARGIN + 10))
            text = self.font.render(notice, True, (40, 40, 40))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, MARGIN + 28))
            self.screen.blit(text, text_rect)
    def draw_score(self):
        '''Draw the score panel and current player's turn at the top.'''
        pygame.draw.rect(self.screen, COLOR_PANEL, (0, 0, WINDOW_WIDTH, MARGIN))
        score = self.game.get_score()
        black_text = self.font.render(f"Black: {score[ReversiGame.BLACK]}", True, COLOR_TEXT)
        white_text = self.font.render(f"White: {score[ReversiGame.WHITE]}", True, COLOR_TEXT)
        turn_names = {ReversiGame.BLACK: "Black", ReversiGame.WHITE: "White"}
        turn_text = self.font.render(
            f"Turn: {turn_names[self.game.current_player]}", True, COLOR_HIGHLIGHT)
        self.screen.blit(black_text, (20, 15))
        self.screen.blit(white_text, (200, 15))
        self.screen.blit(turn_text, (WINDOW_WIDTH - 220, 15))
    def draw_game_over(self):
        '''Overlay the final result when the game has ended.'''
        score = self.game.get_score()
        winner = self.game.get_winner()
        if winner is None:
            message = "It's a tie!"
        else:
            name = "Black" if winner == ReversiGame.BLACK else "White"
            message = f"{name} wins!"
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        # Headline kept short so it fits within the window width
        text = self.big_font.render(message, True, COLOR_HIGHLIGHT)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        self.screen.blit(text, text_rect)
        # Final score rendered on its own line in the smaller font
        score_text = self.font.render(
            f"Black {score[ReversiGame.BLACK]} - White {score[ReversiGame.WHITE]}",
            True, COLOR_TEXT)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)
        hint = self.font.render("Click anywhere to play again", True, COLOR_TEXT)
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(hint, hint_rect)
    def run(self):
        '''Main game loop.'''
        while self.running:
            self.handle_events()
            self.draw_board()
            self.draw_discs()
            if not self.game_over:
                self.draw_valid_moves()
                self.draw_pass_banner()
            self.draw_score()
            if self.game_over:
                self.draw_game_over()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()