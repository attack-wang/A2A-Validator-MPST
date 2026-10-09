'''
game.py
Core game controller for Gomoku: main loop, event handling,
turn management and rendering orchestration.
'''
import pygame
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, FPS, PLAYER_BLACK,
                    PLAYER_WHITE, FONT_SIZE_BUTTON, STATUS_BAR_HEIGHT,
                    MSG_BLACK_TURN, MSG_WHITE_TURN, MSG_BLACK_WIN,
                    MSG_WHITE_WIN, MSG_DRAW)
from board import Board
from gui import (Button, pixel_to_grid, draw_board, draw_stones,
                 draw_winning_line, draw_last_move_marker, draw_status)
class Game:
    """Controls the Gomoku game flow and rendering."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Gomoku - Five in a Row")
        self.clock = pygame.time.Clock()
        self.button_font = pygame.font.SysFont("arial", FONT_SIZE_BUTTON, bold=True)
        self.board = Board()
        self.current_player = PLAYER_BLACK
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.status_message = MSG_BLACK_TURN
        self.restart_button = Button(
            (WINDOW_WIDTH - 150, WINDOW_HEIGHT - STATUS_BAR_HEIGHT + 15, 120, 40),
            "Restart", self.button_font, callback=self.restart)
        self.running = True
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()
    def handle_events(self):
        """Process quit, mouse clicks and keyboard shortcuts."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.restart_button.rect.collidepoint(event.pos):
                    self.restart()
                elif not self.game_over:
                    move = pixel_to_grid(event.pos)
                    if move:
                        self.try_place_stone(*move)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    def try_place_stone(self, row, col):
        """Attempt to place a stone for the current player and update state."""
        if self.board.place_stone(row, col, self.current_player):
            self.last_move = (row, col)
            if self.board.check_win(row, col, self.current_player):
                self.game_over = True
                self.winner = self.current_player
                self.status_message = (MSG_BLACK_WIN if self.winner == PLAYER_BLACK
                                       else MSG_WHITE_WIN)
            elif self.board.is_full():
                self.game_over = True
                self.status_message = MSG_DRAW
            else:
                self.switch_player()
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_player = (PLAYER_WHITE if self.current_player == PLAYER_BLACK
                               else PLAYER_BLACK)
        self.status_message = (MSG_BLACK_TURN if self.current_player == PLAYER_BLACK
                               else MSG_WHITE_TURN)
    def restart(self):
        """Reset the board and all game state for a new match."""
        self.board.reset()
        self.current_player = PLAYER_BLACK
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.status_message = MSG_BLACK_TURN
    def update(self):
        """Per-frame updates (button hover state)."""
        self.restart_button.update(pygame.mouse.get_pos())
    def render(self):
        """Draw the full scene: board, stones, markers, status and button."""
        draw_board(self.screen)
        draw_stones(self.screen, self.board)
        if self.board.winning_cells:
            draw_winning_line(self.screen, self.board.winning_cells)
        if self.last_move:
            draw_last_move_marker(self.screen, self.last_move)
        draw_status(self.screen, self.status_message,
                    self.current_player if not self.game_over else None)
        self.restart_button.draw(self.screen)
        pygame.display.flip()