'''
game.py
Defines the Game class: owns the pygame window, the main loop, event
handling, state updates (paddles, ball, scoring) and rendering, plus
the serve/reset flow and the win/restart screen.
'''
import random
import pygame
import constants as c
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
class Game:
    '''Two-player Pong game: loop, input, physics, scoring and rendering.'''
    SERVE_DELAY_FRAMES = 45  # frames to wait before the ball moves after a point
    def __init__(self):
        '''Create the window, game objects and initial state.'''
        pygame.init()
        self.screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
        pygame.display.set_caption("Pong - Two Player")
        self.clock = pygame.time.Clock()
        self.left_paddle = Paddle("left", pygame.K_w, pygame.K_s)
        self.right_paddle = Paddle("right", pygame.K_UP, pygame.K_DOWN)
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.font_message = pygame.font.Font(None, c.FONT_SIZE_MESSAGE)
        self.font_hint = pygame.font.Font(None, c.FONT_SIZE_HINT)
        self.serve_timer = self.SERVE_DELAY_FRAMES
        self.game_over = False
        self.running = True
    def run(self):
        '''Main game loop: events, update, render, tick.'''
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(c.FPS)
        pygame.quit()
    def handle_events(self):
        '''Process window close events and restart key when game is over.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_SPACE:
                    self.restart()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    def update(self):
        '''Advance the game state one frame.'''
        if self.game_over:
            return
        keys = pygame.key.get_pressed()
        self.left_paddle.update(keys)
        self.right_paddle.update(keys)
        if self.serve_timer > 0:
            self.serve_timer -= 1
        else:
            self.ball.update(self.left_paddle, self.right_paddle)
            self.check_point()
    def check_point(self):
        '''Award a point when the ball passes a paddle, then reset the ball.'''
        if self.ball.is_out_left():
            self.scoreboard.increment_right()
            self.after_point(serve_direction=1)
        elif self.ball.is_out_right():
            self.scoreboard.increment_left()
            self.after_point(serve_direction=-1)
        if self.scoreboard.has_winner():
            self.game_over = True
    def after_point(self, serve_direction):
        '''Reset the ball after a point and start a short serve delay.'''
        self.ball.reset(serve_direction)
        self.serve_timer = self.SERVE_DELAY_FRAMES
    def restart(self):
        '''Start a fresh match after someone has won.'''
        self.scoreboard.reset()
        self.ball.reset(random.choice([-1, 1]))
        self.serve_timer = self.SERVE_DELAY_FRAMES
        self.game_over = False
    def render(self):
        '''Draw background, center line, paddles, ball, scores and messages.'''
        self.screen.fill(c.COLOR_BACKGROUND)
        self.draw_center_line()
        self.scoreboard.draw(self.screen)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        if self.game_over:
            winner = self.scoreboard.get_winner()
            self.draw_message(f"{winner.capitalize()} player wins!", c.WINDOW_HEIGHT // 2 - 40)
            self.draw_hint("Press SPACE to play again  |  ESC to quit", c.WINDOW_HEIGHT // 2 + 20)
        elif self.serve_timer > 0:
            self.draw_hint(f"First to {c.WINNING_SCORE} points wins!", c.WINDOW_HEIGHT - 60)
            self.draw_hint("Left: W / S      Right: UP / DOWN arrows", c.WINDOW_HEIGHT - 35)
        pygame.display.flip()
    def draw_center_line(self):
        '''Draw a dashed vertical line separating the two halves.'''
        dash_height = 15
        gap = 10
        x = c.WINDOW_WIDTH // 2 - 2
        y = 0
        while y < c.WINDOW_HEIGHT:
            pygame.draw.rect(self.screen, c.COLOR_CENTER_LINE, (x, y, 4, dash_height))
            y += dash_height + gap
    def draw_message(self, text, y):
        '''Render a large centered message at the given vertical position.'''
        surface = self.font_message.render(text, True, c.COLOR_TEXT)
        rect = surface.get_rect(center=(c.WINDOW_WIDTH // 2, y))
        self.screen.blit(surface, rect)
    def draw_hint(self, text, y):
        '''Render a small centered hint line at the given vertical position.'''
        surface = self.font_hint.render(text, True, c.COLOR_TEXT)
        rect = surface.get_rect(center=(c.WINDOW_WIDTH // 2, y))
        self.screen.blit(surface, rect)