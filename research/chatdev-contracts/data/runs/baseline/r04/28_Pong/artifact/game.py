'''
game.py
Main game orchestration: state machine, event handling, update loop,
collision/scoring logic, and rendering.
'''
import random
import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_CAPTION, FPS, MAX_DT,
    COLOR_BACKGROUND, COLOR_CENTER_LINE, COLOR_MESSAGE,
    COLOR_PADDLE_LEFT, COLOR_PADDLE_RIGHT,
    FONT_NAME, FONT_SIZE_MESSAGE, CONTROLS,
)
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
class Game:
    """Two-player Pong: owns entities, state machine, main loop, rendering."""
    STATE_SERVING = "serving"
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        """Initialize pygame, window, entities, fonts, and initial state."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_CAPTION)
        self.clock = pygame.time.Clock()
        self.font_message = pygame.font.SysFont(FONT_NAME, FONT_SIZE_MESSAGE, bold=True)
        self.paddles = [
            Paddle("left", CONTROLS["left"]["up"], CONTROLS["left"]["down"], COLOR_PADDLE_LEFT),
            Paddle("right", CONTROLS["right"]["up"], CONTROLS["right"]["down"], COLOR_PADDLE_RIGHT),
        ]
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.rally_hits = 0
        self.winner = None
        self.state = self.STATE_SERVING
        self.running = True
    def run(self):
        """Main loop: process events, update simulation, render at FPS."""
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, MAX_DT)  # clamp frame hitches
            self._handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
    def _handle_events(self):
        """Quit on window close; SPACE serves the ball or restarts the match."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.state == self.STATE_SERVING:
                    self.ball.serve()
                    self.state = self.STATE_PLAYING
                elif self.state == self.STATE_GAME_OVER:
                    self._restart()
    def _restart(self):
        """Reset scores, entities, and state for a fresh match."""
        self.scoreboard.reset()
        self.ball.reset(serve_direction=random.choice((-1, 1)))
        for paddle in self.paddles:
            paddle.reset_position()
        self.rally_hits = 0
        self.winner = None
        self.state = self.STATE_SERVING
    # ---------------------------------------------------------------- update
    def update(self, dt):
        """Move paddles always; simulate ball (sub-stepped) only while playing."""
        keys = pygame.key.get_pressed()
        for paddle in self.paddles:
            paddle.update(dt, keys)
        if self.state != self.STATE_PLAYING:
            return
        # Sub-step the ball so fast movement cannot tunnel through paddles.
        distance = self.ball.speed * dt
        steps = max(1, int(distance // 6) + 1)
        step_dt = dt / steps
        for _ in range(steps):
            self.ball.update(step_dt)
            self._handle_paddle_collisions()
            if self._handle_scoring():
                break
    def _handle_paddle_collisions(self):
        """Bounce the ball off the front face of a paddle it overlaps."""
        ball_rect = self.ball.rect
        for paddle in self.paddles:
            if not ball_rect.colliderect(paddle.rect):
                continue
            moving_right = self.ball.vx > 0
            if paddle.side == "left" and not moving_right:
                self.ball.x = paddle.rect.right + self.ball.radius
                self.ball.bounce_off_paddle(paddle, +1)
                self.rally_hits += 1
            elif paddle.side == "right" and moving_right:
                self.ball.x = paddle.rect.left - self.ball.radius
                self.ball.bounce_off_paddle(paddle, -1)
                self.rally_hits += 1
    def _handle_scoring(self):
        """Award a point when the ball exits left/right; returns True on point."""
        if self.ball.right < 0.0:
            scorer = 1  # right player scores; serve toward right (conceder)
        elif self.ball.left > WINDOW_WIDTH:
            scorer = 0
        else:
            return False
        self.scoreboard.score_point(scorer)
        self.winner = self.scoreboard.get_winner()
        if self.winner is not None:
            self.state = self.STATE_GAME_OVER
            self.ball.reset(serve_direction=1)  # re-center ball for display
        else:
            # Serve toward the player who just conceded (loser receives).
            serve_direction = 1 if scorer == 0 else -1
            self.ball.reset(serve_direction)
            self.rally_hits = 0
            self.state = self.STATE_SERVING
        return True
    # ---------------------------------------------------------------- render
    def draw(self):
        """Render background, center line, entities, scores, and messages."""
        self.screen.fill(COLOR_BACKGROUND)
        y = 0  # dashed center line
        while y < WINDOW_HEIGHT:
            pygame.draw.rect(self.screen, COLOR_CENTER_LINE,
                             (WINDOW_WIDTH // 2 - 2, y, 4, 18))
            y += 30
        for paddle in self.paddles:
            paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.scoreboard.draw(self.screen)
        if self.state == self.STATE_SERVING:
            self._draw_message("Press SPACE to serve", WINDOW_HEIGHT * 0.75)
        elif self.state == self.STATE_GAME_OVER:
            name = "Left" if self.winner == 0 else "Right"
            self._draw_message(f"{name} player wins!", WINDOW_HEIGHT * 0.45)
            self._draw_message("Press SPACE for a new match", WINDOW_HEIGHT * 0.55)
        pygame.display.flip()
    def _draw_message(self, text, y):
        """Blit a centered message at the given vertical position."""
        surf = self.font_message.render(text, True, COLOR_MESSAGE)
        rect = surf.get_rect(center=(WINDOW_WIDTH // 2, int(y)))
        self.screen.blit(surf, rect)