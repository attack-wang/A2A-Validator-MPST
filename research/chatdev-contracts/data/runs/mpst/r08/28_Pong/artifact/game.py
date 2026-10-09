'''
game.py
Defines the Game class: pygame window setup, the main loop, input
handling, collision detection, scoring, win condition, and rendering.
Restored after a corrupted write left only an orphaned fragment of
Ball.bounce_off_wall in this file, which removed the Game class and
caused: ImportError: cannot import name 'Game' from 'game'.
'''
import random
import pygame
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE,
                       PADDLE_MARGIN, PADDLE_WIDTH, SERVE_DELAY_FRAMES,
                       BLACK, GRAY, ACCENT, ACCENT2)
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
class Game:
    """Two-player Pong: owns the window, entities, main loop, and game flow."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.scoreboard = Scoreboard()
        self.left_paddle = Paddle(PADDLE_MARGIN, pygame.K_w, pygame.K_s, ACCENT)
        self.right_paddle = Paddle(SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH,
                                   pygame.K_UP, pygame.K_DOWN, ACCENT2)
        self.ball = Ball()
        self.serve_timer = SERVE_DELAY_FRAMES
        self.next_serve_direction = random.choice((-1, 1))
        self.game_over = False
        self.running = True
    def reset_for_new_game(self):
        """Reset scores, paddles, and ball for a fresh match."""
        self.scoreboard.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.moving = False
        self.ball.reset_position()
        self.serve_timer = SERVE_DELAY_FRAMES
        self.next_serve_direction = random.choice((-1, 1))
        self.game_over = False
    def prepare_serve(self, serve_direction):
        """Stop the ball, center it, and schedule the next serve."""
        self.ball.moving = False
        self.ball.reset_position()
        self.serve_timer = SERVE_DELAY_FRAMES
        self.next_serve_direction = serve_direction
    def handle_events(self):
        """Process quit / restart events and per-player movement keys."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.game_over and event.key == pygame.K_SPACE:
                    self.reset_for_new_game()
        keys = pygame.key.get_pressed()
        self.left_paddle.move(keys)    # Player 1: W / S
        self.right_paddle.move(keys)   # Player 2: Up / Down arrows
    def update(self):
        """Advance one frame of game logic."""
        if self.game_over:
            return
        # Serve countdown before the match and after every point.
        if not self.ball.moving:
            self.serve_timer -= 1
            if self.serve_timer <= 0:
                self.ball.serve(self.next_serve_direction)
            return
        self.ball.update()
        # Top / bottom edge bounces.
        rect = self.ball.get_rect()
        if rect.top <= 0 or rect.bottom >= SCREEN_HEIGHT:
            self.ball.bounce_off_wall()
        # Paddle bounces (only against the paddle the ball travels toward).
        if self.ball.speed_x < 0 and \
                self.ball.get_rect().colliderect(self.left_paddle.get_rect()):
            self.ball.bounce_off_paddle(self.left_paddle)
        elif self.ball.speed_x > 0 and \
                self.ball.get_rect().colliderect(self.right_paddle.get_rect()):
            self.ball.bounce_off_paddle(self.right_paddle)
        # Scoring: the opponent of the side the ball exited on gets a point,
        # then the ball is reset and re-served toward the player who missed.
        side = self.ball.off_screen_side()
        if side == 'left':
            self.scoreboard.award_point(1)          # player 2 scores
            self.prepare_serve(serve_direction=-1)
        elif side == 'right':
            self.scoreboard.award_point(0)          # player 1 scores
            self.prepare_serve(serve_direction=1)
        # Winning score threshold (WINNING_SCORE from constants.py).
        if self.scoreboard.get_winner() is not None:
            self.game_over = True
    def draw(self):
        """Render court, entities, scores, and status messages."""
        self.screen.fill(BLACK)
        # Dashed center net.
        for y in range(0, SCREEN_HEIGHT, 30):
            pygame.draw.rect(self.screen, GRAY,
                             (SCREEN_WIDTH // 2 - 2, y, 4, 15))
        self.scoreboard.draw(self.screen)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        if not self.game_over and not self.ball.moving:
            self.scoreboard.draw_center_text(self.screen, "Get ready...",
                                             GRAY, y_offset=60, small=True)
        elif self.game_over:
            winner = self.scoreboard.get_winner()
            if winner is not None:
                color = ACCENT if winner == 0 else ACCENT2
                self.scoreboard.draw_center_text(
                    self.screen, f"Player {winner + 1} wins!", color)
                self.scoreboard.draw_center_text(
                    self.screen, "Press SPACE to play again  |  ESC to quit",
                    GRAY, y_offset=70, small=True)
        pygame.display.flip()
    def run(self):
        """Run the game until the window is closed or ESC is pressed."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()