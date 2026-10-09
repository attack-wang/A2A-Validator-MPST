'''
game.py
Contains the Game class that wires everything together and runs the loop.
'''
import random
import pygame
import settings
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
class Game:
    STATE_SERVING = "serving"
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        """Initialise pygame, the window, fonts and all game entities."""
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.WINDOW_CAPTION)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("consolas", 72, bold=True)
        self.font_medium = pygame.font.SysFont("consolas", 32)
        self.font_small = pygame.font.SysFont("consolas", 22)
        self.left_paddle = Paddle("left")
        self.right_paddle = Paddle("right")
        self.paddles = [self.left_paddle, self.right_paddle]
        self.ball = Ball()
        self.scoreboard = Scoreboard(self.font_big)
        self.state = self.STATE_SERVING
        self.running = True
    def handle_events(self):
        """Process the event queue: quit, serve, restart and exit keys."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.state == self.STATE_SERVING and event.key == pygame.K_SPACE:
                    self.state = self.STATE_PLAYING
                elif self.state == self.STATE_GAME_OVER and event.key == pygame.K_r:
                    self._restart()
    def _restart(self):
        """Reset scores, paddles and ball for a brand-new match."""
        self.scoreboard.reset()
        self.left_paddle = Paddle("left")
        self.right_paddle = Paddle("right")
        self.paddles = [self.left_paddle, self.right_paddle]
        self.ball.reset(random.choice([-1, 1]))
        self.state = self.STATE_SERVING
    def update(self):
        """Advance one logic step: paddles always move; ball only while playing."""
        keys = pygame.key.get_pressed()
        self.left_paddle.handle_input(keys)
        self.right_paddle.handle_input(keys)
        if self.state == self.STATE_PLAYING:
            result = self.ball.update(self.paddles)
            if result is not None:
                # Ball exited on `result` side; the opposite player scores.
                scorer = "right" if result == "left" else "left"
                self.scoreboard.award_point(scorer)
                if self.scoreboard.has_winner():
                    self.state = self.STATE_GAME_OVER
                else:
                    # Reset the ball and wait for the next serve.
                    self.ball.reset(serve_direction=-1 if scorer == "left" else 1)
                    self.state = self.STATE_SERVING
    def _draw_center_line(self, surface):
        """Draw the dashed vertical line in the middle of the court."""
        line_width = 4
        segment_height = 24
        gap = 16
        x = settings.SCREEN_WIDTH // 2 - line_width // 2
        y = 0
        while y < settings.SCREEN_HEIGHT:
            pygame.draw.rect(surface, settings.COLOR_CENTER_LINE,
                             (x, y, line_width, segment_height))
            y += segment_height + gap
    def draw(self):
        """Render background, court, entities, scores and state messages."""
        self.screen.fill(settings.COLOR_BACKGROUND)
        self._draw_center_line(self.screen)
        self.scoreboard.draw(self.screen)
        for paddle in self.paddles:
            paddle.draw(self.screen)
        if self.state != self.STATE_GAME_OVER:
            self.ball.draw(self.screen)
        if self.state == self.STATE_SERVING:
            msg = self.font_medium.render("Press SPACE to serve", True,
                                          settings.COLOR_TEXT)
            self.screen.blit(msg, msg.get_rect(
                center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 80)))
        elif self.state == self.STATE_GAME_OVER:
            winner = self.scoreboard.winner_side()
            winner_text = "Player 1 (left)" if winner == "left" else "Player 2 (right)"
            color = (settings.COLOR_PADDLE_LEFT if winner == "left"
                     else settings.COLOR_PADDLE_RIGHT)
            title = self.font_big.render(f"{winner_text} wins!", True, color)
            self.screen.blit(title, title.get_rect(
                center=(settings.SCREEN_WIDTH // 2,
                        settings.SCREEN_HEIGHT // 2 - 40)))
            sub = self.font_medium.render("Press R to restart - ESC to quit",
                                          True, settings.COLOR_TEXT)
            self.screen.blit(sub, sub.get_rect(
                center=(settings.SCREEN_WIDTH // 2,
                        settings.SCREEN_HEIGHT // 2 + 40)))
        pygame.display.flip()
    def run(self):
        """Main loop: events -> update -> draw, capped at FPS."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)
        pygame.quit()