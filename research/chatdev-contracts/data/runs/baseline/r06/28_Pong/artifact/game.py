'''
game.py
Main game orchestration: game states, event handling, per-frame updates
and rendering for the two-player Pong game.
'''
import random
import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE,
    BLACK, WHITE, GRAY, P1_COLOR, P2_COLOR,
    PADDLE_WIDTH, PADDLE_MARGIN,
    P1_UP_KEY, P1_DOWN_KEY, P2_UP_KEY, P2_DOWN_KEY,
    WINNING_SCORE, SERVE_DELAY_FRAMES,
    MESSAGE_FONT_SIZE, SMALL_FONT_SIZE,
)
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
# Game state identifiers
STATE_MENU = "menu"
STATE_SERVING = "serving"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
class Game:
    """Owns the window, entities, state machine and the main loop."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_big = pygame.font.Font(None, MESSAGE_FONT_SIZE)
        self.font_small = pygame.font.Font(None, SMALL_FONT_SIZE)
        self.paddles = [
            Paddle(PADDLE_MARGIN, P1_UP_KEY, P1_DOWN_KEY, P1_COLOR),
            Paddle(SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH,
                   P2_UP_KEY, P2_DOWN_KEY, P2_COLOR),
        ]
        self.ball = Ball()
        self.scoreboard = Scoreboard(WINNING_SCORE)
        self.state = STATE_MENU
        self.serve_timer = 0
        self.message = ""
    # ---------------- Main loop ----------------
    def run(self):
        """Run the game loop until the window is closed."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
    # ---------------- Event handling ----------------
    def handle_events(self):
        """Process quit, start/restart (SPACE) and pause (P) events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    if self.state in (STATE_MENU, STATE_GAME_OVER):
                        self.start_game()
                elif event.key == pygame.K_p:
                    if self.state == STATE_PLAYING:
                        self.state = STATE_PAUSED
                    elif self.state == STATE_PAUSED:
                        self.state = STATE_PLAYING
    # ---------------- State transitions ----------------
    def start_game(self):
        """(Re)start a match: reset scores, paddles and serve the ball."""
        self.scoreboard.reset()
        self.ball.reset(direction=random.choice([-1, 1]))
        for paddle in self.paddles:
            paddle.reset()
        self.state = STATE_SERVING
        self.serve_timer = SERVE_DELAY_FRAMES
        self.message = f"First to {WINNING_SCORE} points wins!"
    def _handle_point(self, scorer_index):
        """Award a point, then either end the game or serve the next ball."""
        self.scoreboard.score_point(scorer_index)
        if self.scoreboard.get_winner() is not None:
            self.state = STATE_GAME_OVER
            self.message = f"Player {scorer_index + 1} wins!"
        else:
            serve_direction = 1 if scorer_index == 0 else -1
            self.ball.reset(direction=serve_direction)
            self.state = STATE_SERVING
            self.serve_timer = SERVE_DELAY_FRAMES
            self.message = f"Player {scorer_index + 1} scores!"
    # ---------------- Per-frame update ----------------
    def update(self):
        """Advance paddles/ball and the serve countdown according to state."""
        keys = pygame.key.get_pressed()
        if self.state in (STATE_PLAYING, STATE_SERVING):
            for paddle in self.paddles:
                paddle.update(keys)
        if self.state == STATE_PLAYING:
            result = self.ball.update(self.paddles)
            if result is not None:
                self._handle_point(result)
        elif self.state == STATE_SERVING:
            self.serve_timer -= 1
            if self.serve_timer <= 0:
                self.state = STATE_PLAYING
    # ---------------- Rendering helpers ----------------
    def _draw_center_line(self):
        """Draw the center divider line."""
        pygame.draw.line(self.screen, GRAY,
                         (SCREEN_WIDTH // 2, 0),
                         (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)
    def _draw_message(self, text, y_offset=0, font=None, color=WHITE):
        """Blit a centered text message, optionally offset vertically."""
        font = font if font is not None else self.font_big
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
        self.screen.blit(rendered, rect)
    # ---------------- Rendering ----------------
    def draw(self):
        """Render everything for the current state, then flip the display."""
        self.screen.fill(BLACK)
        self._draw_center_line()
        self.scoreboard.draw(self.screen)
        for paddle in self.paddles:
            paddle.draw(self.screen)
        if self.state in (STATE_PLAYING, STATE_SERVING, STATE_PAUSED):
            self.ball.draw(self.screen)
        if self.state == STATE_MENU:
            self._draw_message("TWO - PLAYER PONG", -120)
            self._draw_message("Player 1 (left):  W / S", -40, self.font_small, P1_COLOR)
            self._draw_message("Player 2 (right): UP / DOWN arrows", 0, self.font_small, P2_COLOR)
            self._draw_message(f"First to {WINNING_SCORE} points wins", 40, self.font_small, GRAY)
            self._draw_message("Press SPACE to start", 120)
        elif self.state == STATE_SERVING:
            self._draw_message(self.message, -60)
            self._draw_message("Get ready...", 0, self.font_small, GRAY)
        elif self.state == STATE_PAUSED:
            self._draw_message("PAUSED", -40)
            self._draw_message("Press P to resume", 20, self.font_small, GRAY)
        elif self.state == STATE_GAME_OVER:
            self._draw_message(self.message, -60)
            self._draw_message("Press SPACE for a rematch - ESC to quit", 20, self.font_small, GRAY)
        pygame.display.flip()