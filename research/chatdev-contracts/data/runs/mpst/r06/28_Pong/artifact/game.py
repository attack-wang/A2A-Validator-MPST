'''
game.py
Core game orchestration: owns the pygame window, the main loop,
game states (serving / playing / game over), input handling,
collision detection, scoring and rendering.
'''
import random
import pygame
import settings
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
class Game:
    """Two-player Pong game: loop, states, collisions and rendering."""
    SERVING = "serving"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.CAPTION)
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont("consolas", 28)
        self.font_medium = pygame.font.SysFont("consolas", 32, bold=True)
        self.player1 = Paddle(settings.PADDLE_MARGIN,
                              settings.PLAYER1_KEYS["up"], settings.PLAYER1_KEYS["down"])
        self.player2 = Paddle(settings.WIDTH - settings.PADDLE_MARGIN - settings.PADDLE_WIDTH,
                              settings.PLAYER2_KEYS["up"], settings.PLAYER2_KEYS["down"])
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.state = self.SERVING
        self.serve_timer_ms = 0
        self.last_scorer = None
        self.running = True
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.state == self.GAME_OVER and event.key == pygame.K_r:
                    self.restart()
    def restart(self):
        self.scoreboard.reset()
        self.ball.reset()
        self.state = self.SERVING
        self.serve_timer_ms = 0
        self.last_scorer = None
    def update(self, dt_ms):
        keys = pygame.key.get_pressed()
        self.player1.update(keys)
        self.player2.update(keys)
        if self.state == self.SERVING:
            self.serve_timer_ms += dt_ms
            if self.serve_timer_ms >= settings.SERVE_DELAY_MS:
                # Serve toward the player who just conceded (or random at start)
                direction = -1 if self.last_scorer == 1 else 1 if self.last_scorer == 2 else random.choice([-1, 1])
                self.ball.reset(direction=direction)
                self.state = self.PLAYING
        elif self.state == self.PLAYING:
            self.ball.update()
            self.check_wall_collisions()
            self.check_paddle_collisions()
            self.check_scoring()
        # GAME_OVER: nothing to update
    def check_wall_collisions(self):
        # Top edge
        if self.ball.rect.top <= 0:
            self.ball.rect.top = 0
            self.ball.bounce_top_bottom()
        # Bottom edge
        if self.ball.rect.bottom >= settings.HEIGHT:
            self.ball.rect.bottom = settings.HEIGHT
            self.ball.bounce_top_bottom()
    def check_paddle_collisions(self):
        """Bounce the ball off a paddle only when moving toward it."""
        if self.ball.rect.colliderect(self.player1.rect) and self.ball.speed_x < 0:
            self.ball.bounce_paddle(self.player1)
        elif self.ball.rect.colliderect(self.player2.rect) and self.ball.speed_x > 0:
            self.ball.bounce_paddle(self.player2)
    def check_scoring(self):
        if self.ball.rect.right <= 0:
            # Player 2 missed -> Player 1 scores
            self.score_point(1)
        elif self.ball.rect.left >= settings.WIDTH:
            self.score_point(2)
    def score_point(self, player):
        self.scoreboard.score_point(player)
        self.last_scorer = player
        if self.scoreboard.has_winner():
            self.state = self.GAME_OVER
        else:
            self.ball.reset()          # reposition at center for the countdown
            self.state = self.SERVING
            self.serve_timer_ms = 0
    def render(self):
        self.screen.fill(settings.BLACK)
        self.draw_center_line()
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        if self.state != self.GAME_OVER:
            self.ball.draw(self.screen)
        self.scoreboard.draw(self.screen)
        self.draw_messages()
        pygame.display.flip()
    def draw_center_line(self):
        """Draw a dashed vertical line at mid-court."""
        dash_height, gap, y = 20, 14, 0
        x = settings.WIDTH // 2 - 2
        while y < settings.HEIGHT:
            pygame.draw.rect(self.screen, settings.GRAY, (x, y, 4, dash_height))
            y += dash_height + gap
    def draw_messages(self):
        """Render serve prompt, control hints and game-over banner."""
        if self.state == self.SERVING:
            surface = self.font_medium.render("Get ready...", True, settings.WHITE)
            self.screen.blit(surface, surface.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT - 60)))
            hint = self.font_small.render("Player 1: W/S    Player 2: UP/DOWN arrows", True, settings.GRAY)
            self.screen.blit(hint, hint.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT - 25)))
        elif self.state == self.GAME_OVER:
            winner = self.scoreboard.get_winner()
            surface = self.font_medium.render(f"Player {winner} wins!  Press R to restart", True, settings.WHITE)
            self.screen.blit(surface, surface.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 80)))
    def run(self):
        while self.running:
            dt_ms = self.clock.tick(settings.FPS)
            self.handle_events()
            self.update(dt_ms)
            self.render()
        pygame.quit()