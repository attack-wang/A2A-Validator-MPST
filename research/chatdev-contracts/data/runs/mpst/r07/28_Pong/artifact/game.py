'''
game.py
Defines the Game class: owns the pygame window, the main loop, the game
states (playing / game over), event handling, collision detection and
scoring logic that ties Paddle, Ball and Scoreboard together.
'''
import random
import pygame
import settings
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
class Game:
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.WINDOW_CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = self.STATE_PLAYING
        self.scoreboard = Scoreboard()
        self.paddles = [
            Paddle(settings.PADDLE_MARGIN, settings.PLAYER1_UP_KEY, settings.PLAYER1_DOWN_KEY),
            Paddle(settings.SCREEN_WIDTH - settings.PADDLE_MARGIN - settings.PADDLE_WIDTH,
                   settings.PLAYER2_UP_KEY, settings.PLAYER2_DOWN_KEY),
        ]
        self.ball = Ball()
        self.serve_timer = settings.SERVE_DELAY_FRAMES
    # ------------------------------------------------------------------ loop
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(settings.FPS)
        pygame.quit()
    # --------------------------------------------------------------- events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.state == self.STATE_GAME_OVER and event.key == pygame.K_r:
                    self.restart()
    # -------------------------------------------------------------- updates
    def update(self):
        if self.state != self.STATE_PLAYING:
            return
        keys = pygame.key.get_pressed()
        for paddle in self.paddles:
            paddle.update(keys)
        if self.serve_timer > 0:
            self.serve_timer -= 1
            return
        self.ball.update()
        self.check_paddle_collisions()
        self.check_scoring()
    def check_paddle_collisions(self):
        left_paddle, right_paddle = self.paddles
        if self.ball.velocity_x < 0 and self.ball.rect.colliderect(left_paddle.rect):
            self.ball.bounce_off_paddle(left_paddle, direction=1)
        elif self.ball.velocity_x > 0 and self.ball.rect.colliderect(right_paddle.rect):
            self.ball.bounce_off_paddle(right_paddle, direction=-1)
    def check_scoring(self):
        if self.ball.rect.right < 0:
            # Ball left through the left edge -> right player scores.
            self.handle_point(scorer_index=1, serve_direction=-1)
        elif self.ball.rect.left > settings.SCREEN_WIDTH:
            # Ball left through the right edge -> left player scores.
            self.handle_point(scorer_index=0, serve_direction=1)
    def handle_point(self, scorer_index, serve_direction):
        self.scoreboard.score_point(scorer_index)
        if self.scoreboard.get_winner() is not None:
            self.state = self.STATE_GAME_OVER
        else:
            self.ball.reset(serve_direction)
            self.serve_timer = settings.SERVE_DELAY_FRAMES
    def restart(self):
        self.scoreboard.reset()
        self.ball.reset(random.choice((-1, 1)))
        self.serve_timer = settings.SERVE_DELAY_FRAMES
        self.state = self.STATE_PLAYING
    # -------------------------------------------------------------- drawing
    def render(self):
        self.screen.fill(settings.BACKGROUND_COLOR)
        self.draw_center_line()
        self.scoreboard.draw(self.screen)
        self.scoreboard.draw_centered_message(
            self.screen,
            f"First to {settings.WINNING_SCORE} points",
            10,
            settings.ACCENT_COLOR,
            self.scoreboard.small_font,
        )
        for paddle in self.paddles:
            paddle.draw(self.screen)
        self.ball.draw(self.screen)
        if self.serve_timer > 0 and self.state == self.STATE_PLAYING:
            self.scoreboard.draw_centered_message(
                self.screen, "Get ready...", settings.SCREEN_HEIGHT // 2 + 40
            )
        if self.state == self.STATE_GAME_OVER:
            self.draw_game_over_screen()
        pygame.display.flip()
    def draw_center_line(self):
        dash_height = 18
        gap = 12
        x = settings.SCREEN_WIDTH // 2 - 2
        y = 0
        while y < settings.SCREEN_HEIGHT:
            pygame.draw.rect(self.screen, settings.ACCENT_COLOR, (x, y, 4, dash_height))
            y += dash_height + gap
    def draw_game_over_screen(self):
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        winner = self.scoreboard.get_winner()
        winner_name = "Player 1 (left)" if winner == 0 else "Player 2 (right)"
        self.scoreboard.draw_centered_message(self.screen, f"{winner_name} wins!", settings.SCREEN_HEIGHT // 2 - 60)
        self.scoreboard.draw_centered_message(self.screen, "Press R to play again", settings.SCREEN_HEIGHT // 2 + 10)
        self.scoreboard.draw_centered_message(self.screen, "Press ESC to quit", settings.SCREEN_HEIGHT // 2 + 50)