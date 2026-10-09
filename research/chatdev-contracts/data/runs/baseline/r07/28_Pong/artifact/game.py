'''
game.py
Defines the Game class: game states, main loop, scoring, and rendering.
Rebuilt from fragments: the bare "if self.state == STATE_SERVING" snippet
belongs inside Game.update, "_after_point" and "run/handle_events" belong
to the Game class, and the score must actually be incremented per point.
'''
import pygame
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS,
                       COLOR_BACKGROUND, COLOR_TEXT, COLOR_CENTER_LINE,
                       COLOR_WINNER, COLOR_PADDLE_LEFT, COLOR_PADDLE_RIGHT,
                       PADDLE_MARGIN, PADDLE_WIDTH, POINT_PAUSE_SECONDS,
                       FONT_MAIN_SIZE, FONT_SMALL_SIZE)
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
# Game states
STATE_SERVING = "serving"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
class Game:
    '''Coordinates paddles, ball, scoreboard, and the main game loop.'''
    def __init__(self):
        '''Create the window, clock, fonts, paddles, ball, and scoreboard.'''
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_main = pygame.font.SysFont("consolas", FONT_MAIN_SIZE, bold=True)
        self.font_small = pygame.font.SysFont("consolas", FONT_SMALL_SIZE)
        self.paddle_left = Paddle(PADDLE_MARGIN,
                                  pygame.K_w, pygame.K_s, COLOR_PADDLE_LEFT)
        self.paddle_right = Paddle(WINDOW_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH,
                                   pygame.K_UP, pygame.K_DOWN, COLOR_PADDLE_RIGHT)
        self.paddles = [self.paddle_left, self.paddle_right]
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.serve_direction = 1
        self.state = STATE_SERVING
        self.state_timer = 0.0
        self.running = False
    def run(self):
        '''Run the main loop until the player quits, then shut down pygame.'''
        self.running = True
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(delta_time)
            self.render()
        pygame.quit()
    def handle_events(self):
        '''Process quit and restart input.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.state == STATE_GAME_OVER and event.key == pygame.K_r:
                    self._restart_match()
    def update(self, delta_time):
        '''Advance the state machine and game objects one frame.'''
        self.state_timer += delta_time
        if self.state == STATE_SERVING:
            if self.state_timer >= POINT_PAUSE_SECONDS:
                self._enter_state(STATE_PLAYING)
        elif self.state == STATE_PLAYING:
            keys = pygame.key.get_pressed()
            for paddle in self.paddles:
                paddle.update(keys)
            self.ball.update(self.paddles)
            side = self.ball.out_of_bounds()
            if side != 0:
                self._after_point(side)
        # STATE_GAME_OVER: wait for R (restart) or ESC/quit
    def _after_point(self, conceding_side):
        '''Award the point, then end the match or prepare the next serve.'''
        if conceding_side > 0:
            self.scoreboard.score_left()
        else:
            self.scoreboard.score_right()
        if self.scoreboard.has_winner():
            self._enter_state(STATE_GAME_OVER)
        else:
            self.serve_direction = conceding_side
            self.ball.reset(self.serve_direction)
            self._enter_state(STATE_SERVING)
    def _restart_match(self):
        '''Reset scores, ball, and paddles for a new match.'''
        self.scoreboard.reset()
        for paddle in self.paddles:
            paddle.reset_position()
        self.serve_direction = 1
        self.ball.reset(self.serve_direction)
        self._enter_state(STATE_SERVING)
    def _enter_state(self, new_state):
        '''Switch state and restart the state timer.'''
        self.state = new_state
        self.state_timer = 0.0
    def render(self):
        '''Draw one frame: background, center line, paddles, ball, score, text.'''
        self.window.fill(COLOR_BACKGROUND)
        pygame.draw.rect(self.window, COLOR_CENTER_LINE,
                         (WINDOW_WIDTH // 2 - 2, 0, 4, WINDOW_HEIGHT))
        for paddle in self.paddles:
            paddle.draw(self.window)
        self.ball.draw(self.window)
        self.scoreboard.draw(self.window)
        self._draw_status_text()
        pygame.display.flip()
    def _draw_status_text(self):
        '''Show the serve hint or the winner banner.'''
        if self.state == STATE_SERVING:
            text = self.font_small.render("Get ready...", True, COLOR_TEXT)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
            self.window.blit(text, rect)
        elif self.state == STATE_GAME_OVER:
            winner = self.scoreboard.get_winner()
            title = self.font_main.render(f"{winner} WINS!", True, COLOR_WINNER)
            rect = title.get_rect(center=(WINDOW_WIDTH // 2,
                                          WINDOW_HEIGHT // 2 - 30))
            self.window.blit(title, rect)
            hint = self.font_small.render("Press R to play again - ESC to quit",
                                          True, COLOR_TEXT)
            hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2,
                                              WINDOW_HEIGHT // 2 + 20))
            self.window.blit(hint, hint_rect)