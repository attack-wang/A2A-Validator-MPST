'''
game.py
Core orchestration for the two-player Pong game.
Owns the pygame window and main loop, routes keyboard input to both
paddles, runs the SERVING -> PLAYING -> GAME_OVER state machine,
detects paddle collisions and missed balls, awards points, resets the
ball after each point, and handles the restart flow after a player wins.
'''
import random
import sys
import pygame
from settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_CAPTION,
    FPS,
    COLOR_BACKGROUND,
    COLOR_SERVE_TEXT,
    COLOR_PADDLE_LEFT,
    COLOR_PADDLE_RIGHT,
    PADDLE_MARGIN,
    SERVE_DELAY_FRAMES,
    KEY_LEFT_UP,
    KEY_LEFT_DOWN,
    KEY_RIGHT_UP,
    KEY_RIGHT_DOWN,
    KEY_RESTART,
    KEY_QUIT,
)
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
STATE_SERVING = "SERVING"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"
class Game:
    """Runs the full Pong match: loop, input, physics, scoring and UI."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_CAPTION)
        self.clock = pygame.time.Clock()
        self.font_serve = pygame.font.SysFont("consolas", 30, bold=True)
        self.left_paddle = Paddle(PADDLE_MARGIN, COLOR_PADDLE_LEFT,
                                  KEY_LEFT_UP, KEY_LEFT_DOWN)
        self.right_paddle = Paddle(WINDOW_WIDTH - PADDLE_MARGIN - self.left_paddle.rect.width,
                                   COLOR_PADDLE_RIGHT, KEY_RIGHT_UP, KEY_RIGHT_DOWN)
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.state = STATE_SERVING
        self.serve_timer = 0
        self._start_serve(random.choice((-1, 1)))
    # ------------------------------------------------------------------
    # State transitions
    # ------------------------------------------------------------------
    def _start_serve(self, serve_direction):
        """Reset the ball and arm the countdown that precedes the next serve."""
        self.ball.reset(serve_direction)
        self.state = STATE_SERVING
        self.serve_timer = SERVE_DELAY_FRAMES
    def _after_point(self, serve_direction):
        """After a miss: declare a winner if the threshold is reached, else re-serve."""
        if self.scoreboard.has_winner():
            self.state = STATE_GAME_OVER
        else:
            self._start_serve(serve_direction)
    # ------------------------------------------------------------------
    # Per-frame updates
    # ------------------------------------------------------------------
    def _handle_events(self):
        """Process window close, quit key, and the restart key after a win."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == KEY_QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.key == KEY_RESTART and self.state == STATE_GAME_OVER:
                    self.scoreboard.reset()
                    self._start_serve(random.choice((-1, 1)))
    def _update_serving(self):
        """Count down the serve delay, then launch the ball."""
        self.serve_timer -= 1
        if self.serve_timer <= 0:
            self.ball.launch()
            self.state = STATE_PLAYING
    def _update_playing(self):
        """Move the ball, resolve paddle hits and detect missed balls."""
        self.ball.update()
        # Bounce only when the ball travels toward the paddle, so a single
        # hit cannot register twice on consecutive frames.
        if self.ball.vx < 0 and self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.bounce_off_paddle(self.left_paddle)
        elif self.ball.vx > 0 and self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.bounce_off_paddle(self.right_paddle)
        # A ball fully past an edge means the opponent of that side scores.
        if self.ball.is_out_left():
            self.scoreboard.award_right()
            # Serve again toward the player who just missed.
            self._after_point(serve_direction=-1)
        elif self.ball.is_out_right():
            self.scoreboard.award_left()
            self._after_point(serve_direction=1)
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def _draw(self):
        """Render the field, entities and any state-specific overlay."""
        self.screen.fill(COLOR_BACKGROUND)
        self.scoreboard.draw(self.screen)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        if self.state == STATE_SERVING:
            text = self.font_serve.render("Get ready...", True, COLOR_SERVE_TEXT)
            self.screen.blit(text, text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90)))
        elif self.state == STATE_GAME_OVER:
            self.scoreboard.draw_winner_overlay(self.screen)
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        """Run the game loop until the player quits the window."""
        while True:
            self._handle_events()
            keys = pygame.key.get_pressed()
            self.left_paddle.handle_input(keys)
            self.right_paddle.handle_input(keys)
            if self.state == STATE_SERVING:
                self._update_serving()
            elif self.state == STATE_PLAYING:
                self._update_playing()
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)