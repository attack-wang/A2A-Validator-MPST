'''
Game module: main game loop, event handling, collision detection,
scoring with ball reset after each point, and rendering.
'''
import pygame
import sys
import random
import settings
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
class Game:
    '''Manages the Pong game state, loop, and rendering.'''
    def __init__(self):
        '''Set up the window, paddles, ball, scoreboard, and game state.'''
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.CAPTION)
        self.clock = pygame.time.Clock()
        self.hint_font = pygame.font.Font(settings.FONT_NAME, settings.HINT_FONT_SIZE)
        self.paddle_left = Paddle(
            x=settings.PADDLE_MARGIN,
            up_key=pygame.K_w,
            down_key=pygame.K_s,
            color=settings.WHITE,
        )
        self.paddle_right = Paddle(
            x=settings.SCREEN_WIDTH - settings.PADDLE_MARGIN - settings.PADDLE_WIDTH,
            up_key=pygame.K_UP,
            down_key=pygame.K_DOWN,
            color=settings.WHITE,
        )
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.game_over = False
    def handle_events(self):
        '''Process quit, restart (R when game over), and exit (ESC) events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.restart()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    def update(self):
        '''Update paddles, ball, collisions, and scoring each frame.'''
        keys = pygame.key.get_pressed()
        self.paddle_left.update(keys)
        self.paddle_right.update(keys)
        if not self.game_over:
            self.ball.update()
            self.check_paddle_collisions()
            self.check_scoring()
    def check_paddle_collisions(self):
        '''Bounce the ball off a paddle only when moving toward it.'''
        if self.ball.rect.colliderect(self.paddle_left.rect) and self.ball.speed_x < 0:
            self.ball.bounce_off_paddle(self.paddle_left)
        if self.ball.rect.colliderect(self.paddle_right.rect) and self.ball.speed_x > 0:
            self.ball.bounce_off_paddle(self.paddle_right)
    def check_scoring(self):
        '''Award a point when the ball exits an edge, then reset ball or end game.'''
        # Ball passed the left edge -> Player 2 (right) scores
        if self.ball.rect.right <= 0:
            self.scoreboard.score_point('right')
            self.after_point(serve_direction=-1)  # serve toward the player who missed (left)
        # Ball passed the right edge -> Player 1 (left) scores
        elif self.ball.rect.left >= settings.SCREEN_WIDTH:
            self.scoreboard.score_point('left')
            self.after_point(serve_direction=1)   # serve toward the player who missed (right)
    def after_point(self, serve_direction):
        '''Reset the ball after each point, or switch to the game-over state.
        Resetting immediately guarantees check_scoring() fires exactly once
        per point, so scores cannot run up while the ball is off-screen.
        '''
        if self.scoreboard.has_winner():
            self.game_over = True
        else:
            self.ball.reset(direction=serve_direction)
    def draw(self):
        '''Render the court, paddles, ball, score, and any overlay messages.'''
        self.screen.fill(settings.BLACK)
        self.draw_center_line()
        self.paddle_left.draw(self.screen)
        self.paddle_right.draw(self.screen)
        self.ball.draw(self.screen)
        self.scoreboard.draw(self.screen)
        if self.game_over:
            self.scoreboard.draw_winner(self.screen)
        else:
            # Controls hint at the bottom of the screen
            hint = self.hint_font.render(
                "Player 1: W/S   Player 2: Up/Down   First to "
                + str(settings.WINNING_SCORE) + " wins", True, settings.GRAY)
            hint_rect = hint.get_rect(center=(settings.SCREEN_WIDTH // 2,
                                              settings.SCREEN_HEIGHT - 20))
            self.screen.blit(hint, hint_rect)
    def draw_center_line(self):
        '''Draw a dashed vertical line at the middle of the screen.'''
        dash_height = 15
        gap = 10
        x = settings.SCREEN_WIDTH // 2 - 1
        y = 0
        while y < settings.SCREEN_HEIGHT:
            pygame.draw.rect(self.screen, settings.GRAY, (x, y, 2, dash_height))
            y += dash_height + gap
    def run(self):
        '''Run the main game loop until the player quits.'''
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(settings.FPS)
    def restart(self):
        '''Reset scores, ball, and state so a new match can begin.'''
        self.scoreboard.reset_scores()
        self.ball.reset(direction=random.choice([-1, 1]))
        self.game_over = False