'''Game orchestration: loop, states, collisions, scoring, rendering.'''
import pygame
import settings
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
class Game:
    '''Runs the two-player pong match: input, physics, scoring, rendering.'''
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.WINDOW_CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True
        self.left_paddle = Paddle("left", pygame.K_w, pygame.K_s)
        self.right_paddle = Paddle("right", pygame.K_UP, pygame.K_DOWN)
        self.paddles = [self.left_paddle, self.right_paddle]
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.state = self.STATE_PLAYING
        self.serve_timer = 0.0
        self.winner_index = None
    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.state == self.STATE_GAME_OVER and event.key == pygame.K_r:
                    self.restart_match()
    def restart_match(self):
        self.scoreboard.reset()
        self.ball.reset(direction=-1, immediate=False)  # loser of last point? just default
        self.state = self.STATE_PLAYING
        self.serve_timer = settings.SERVE_DELAY
        self.winner_index = None
    def update(self, dt):
        keys = pygame.key.get_pressed()
        for paddle in self.paddles:
            paddle.update(dt, keys)
        if self.state == self.STATE_PLAYING:
            if self.ball.is_serving():
                self.serve_timer -= dt
                if self.serve_timer <= 0:
                    self.ball.launch()
            else:
                self.ball.update(dt)
                self.handle_paddle_collisions()
                self.handle_scoring()
        # In game over state, freeze the ball.
    def handle_paddle_collisions(self):
        for paddle in self.paddles:
            if self.ball.rect.colliderect(paddle.rect):
                # Only bounce if the ball is moving toward the paddle (prevents double hits)
                moving_right = self.ball.velocity[0] > 0
                if paddle is self.left_paddle and not moving_right:
                    self.ball.bounce_off_paddle(paddle)
                elif paddle is self.right_paddle and moving_right:
                    self.ball.bounce_off_paddle(paddle)
    def handle_scoring(self):
        if self.ball.rect.right < 0:
            # Left player missed; player 2 (index 1) scores
            self.award_point(1)
        elif self.ball.rect.left > settings.SCREEN_WIDTH:
            self.award_point(0)
    def award_point(self, player_index):
        self.scoreboard.score_point(player_index)
        winner = self.scoreboard.get_winner()
        if winner is not None:
            self.winner_index = winner
            self.state = self.STATE_GAME_OVER
        else:
            # Serve toward the player who just lost the point
            serve_direction = -1 if player_index == 0 else 1
            # Wait: if player 1 (left, index 0) scored, the ball should go toward player 2 (right) => direction +1.
            ...