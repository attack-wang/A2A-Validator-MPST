'''
Game class: main game logic, loop, collisions, and rendering.
Manages the Pong game state, the update/draw cycle, paddle-ball
collisions, scoring, win detection, pause and restart handling.
'''
import random
import pygame
import settings
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
class Game:
    '''Manages the Pong game state, loop, and rendering.'''
    def __init__(self):
        '''Initialize pygame, the window, and all game objects.'''
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.CAPTION)
        self.clock = pygame.time.Clock()
        self.message_font = pygame.font.Font(
            settings.FONT_NAME, settings.MESSAGE_FONT_SIZE)
        paddle_y = (settings.SCREEN_HEIGHT - settings.PADDLE_HEIGHT) // 2
        self.paddle_left = Paddle(settings.PADDLE_MARGIN, paddle_y, settings.GREEN)
        self.paddle_right = Paddle(
            settings.SCREEN_WIDTH - settings.PADDLE_MARGIN - settings.PADDLE_WIDTH,
            paddle_y, settings.BLUE)
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.paused = False
        self.game_over = False
        self.running = True
    def handle_events(self):
        '''Process pygame events (quit, pause, restart).'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_r and self.game_over:
                    self._restart()
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    def update(self):
        '''Update all game objects and handle collisions/scoring.'''
        if self.paused or self.game_over:
            return
        keys = pygame.key.get_pressed()
        # Player 1: W/S, Player 2: Up/Down arrows
        self.paddle_left.update(keys, pygame.K_w, pygame.K_s)
        self.paddle_right.update(keys, pygame.K_UP, pygame.K_DOWN)
        self.ball.update()
        self._check_paddle_collisions()
        self._check_scoring()
    def _check_paddle_collisions(self):
        '''Bounce the ball off paddles, adjusting angle by hit position.'''
        if self.ball.speed_x < 0 and self.ball.rect.colliderect(self.paddle_left.rect):
            offset = self._hit_offset(self.paddle_left)
            # FIXED: call the existing Ball.deflect(offset) method
            # (previously called a nonexistent deflect_from_paddle).
            self.ball.deflect(offset)
            # Push ball out of paddle to avoid repeated collisions
            self.ball.x = self.paddle_left.rect.right + 1
        elif self.ball.speed_x > 0 and self.ball.rect.colliderect(self.paddle_right.rect):
            offset = self._hit_offset(self.paddle_right)
            self.ball.deflect(offset)
            self.ball.x = self.paddle_right.rect.left - self.ball.size - 1
        self.ball.rect.topleft = (int(self.ball.x), int(self.ball.y))
    def _hit_offset(self, paddle):
        '''Return where the ball hit the paddle as a value in [-1, 1].'''
        ball_center = self.ball.y + self.ball.size / 2
        paddle_center = paddle.y + paddle.height / 2
        relative = (ball_center - paddle_center) / (paddle.height / 2)
        return max(-1.0, min(1.0, relative))
    def _check_scoring(self):
        '''Award a point when the ball exits left or right, then reset the ball.'''
        if self.ball.x + self.ball.size < 0:
            # Ball passed the left edge: Player 2 scores
            self.scoreboard.score_point(2)
            self._after_point()
        elif self.ball.x > settings.SCREEN_WIDTH:
            # Ball passed the right edge: Player 1 scores
            self.scoreboard.score_point(1)
            self._after_point()
    def _after_point(self):
        '''Reset the ball and check for a winner after a point.'''
        if self.scoreboard.has_winner():
            self.game_over = True
        else:
            loser = 1 if self.ball.x + self.ball.size < 0 else 2
            # Serve toward the player who just lost the point
            self.ball.reset(direction=-1 if loser == 1 else 1)
    def _restart(self):
        '''Reset the game for a new match.'''
        self.scoreboard.reset()
        paddle_y = (settings.SCREEN_HEIGHT - settings.PADDLE_HEIGHT) // 2
        self.paddle_left.y = paddle_y
        self.paddle_right.y = paddle_y
        self.paddle_left.rect.topleft = (int(self.paddle_left.x), int(paddle_y))
        self.paddle_right.rect.topleft = (int(self.paddle_right.x), int(paddle_y))
        self.ball.reset(random.choice([-1, 1]))
        self.game_over = False
        self.paused = False
    def draw(self):
        '''Render the court, objects, scores, and overlay messages.'''
        self.screen.fill(settings.BLACK)
        self._draw_center_line()
        self.paddle_left.draw(self.screen)
        self.paddle_right.draw(self.screen)
        if not self.game_over:
            self.ball.draw(self.screen)
        self.scoreboard.draw(self.screen)
        if self.paused and not self.game_over:
            self._draw_message("PAUSED - Press P to resume")
        if self.game_over:
            winner = self.scoreboard.get_winner()
            self._draw_message(f"PLAYER {winner} WINS!",
                               sub="Press R to restart, ESC to quit")
        pygame.display.flip()
    def _draw_center_line(self):
        '''Draw a dashed line down the middle of the court.'''
        dash_height = 15
        gap = 10
        x = settings.SCREEN_WIDTH // 2 - 2
        y = 0
        while y < settings.SCREEN_HEIGHT:
            pygame.draw.rect(self.screen, settings.GREY, (x, y, 4, dash_height))
            y += dash_height + gap
    def _draw_message(self, text, sub=None):
        '''Draw a centered message (and optional sub-message) on screen.'''
        surface = self.message_font.render(text, True, settings.WHITE)
        rect = surface.get_rect(center=(settings.SCREEN_WIDTH // 2,
                                        settings.SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(surface, rect)
        if sub:
            sub_surface = self.message_font.render(sub, True, settings.GREY)
            sub_rect = sub_surface.get_rect(center=(settings.SCREEN_WIDTH // 2,
                                                    settings.SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(sub_surface, sub_rect)
    def run(self):
        '''Main game loop.'''
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)
        pygame.quit()