'''
game.py
Defines the Game class that orchestrates the Pong game loop, states,
collisions, scoring, and rendering.
'''
import random
import pygame
import settings
from paddle import Paddle
from ball import Ball
class Game:
    '''Manages game states (menu, playing, paused, game over), the loop, and scoring.'''
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_score = pygame.font.SysFont("consolas", settings.FONT_SIZE_SCORE, bold=True)
        self.font_text = pygame.font.SysFont("consolas", settings.FONT_SIZE_TEXT)
        self.font_title = pygame.font.SysFont("consolas", settings.FONT_SIZE_TITLE, bold=True)
        self.paddle_left = Paddle(
            x=settings.PADDLE_MARGIN,
            up_key=pygame.K_w,
            down_key=pygame.K_s,
            color=settings.BLUE,
        )
        self.paddle_right = Paddle(
            x=settings.SCREEN_WIDTH - settings.PADDLE_MARGIN - settings.PADDLE_WIDTH,
            up_key=pygame.K_UP,
            down_key=pygame.K_DOWN,
            color=settings.RED,
        )
        self.ball = Ball()
        self.score_left = 0
        self.score_right = 0
        self.state = self.STATE_MENU
        self.winner_text = ""
        self.running = True
    def handle_events(self):
        '''Process input events: quit, start, pause toggle, and restart.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.state == self.STATE_MENU and event.key == pygame.K_SPACE:
                    self.start_game()
                elif self.state == self.STATE_PLAYING and event.key == pygame.K_p:
                    self.state = self.STATE_PAUSED
                elif self.state == self.STATE_PAUSED and event.key == pygame.K_p:
                    self.state = self.STATE_PLAYING
                elif self.state == self.STATE_GAME_OVER and event.key == pygame.K_r:
                    self.start_game()
    def start_game(self):
        '''Reset scores, paddles, and ball, then begin a new match.'''
        self.score_left = 0
        self.score_right = 0
        self.paddle_left.reset()
        self.paddle_right.reset()
        self.ball.reset(direction=random.choice([-1, 1]))
        self.state = self.STATE_PLAYING
    def update(self):
        '''Update paddles, ball, collisions, scoring, and win condition.'''
        if self.state != self.STATE_PLAYING:
            return
        self.paddle_left.update()
        self.paddle_right.update()
        self.ball.update()
        # Paddle collision (only when ball moves toward that paddle)
        if (self.ball.speed_x < 0
                and self.ball.rect.colliderect(self.paddle_left.rect)):
            self.ball.bounce_off_paddle(self.paddle_left)
        elif (self.ball.speed_x > 0
                and self.ball.rect.colliderect(self.paddle_right.rect)):
            self.ball.bounce_off_paddle(self.paddle_right)
        # Scoring: a player misses -> opponent scores, then reset ball for next serve
        if self.ball.rect.right < 0:
            self.score_right += 1
            self.ball.reset(direction=1)
        elif self.ball.rect.left > settings.SCREEN_WIDTH:
            self.score_left += 1
            self.ball.reset(direction=-1)
        # Winning score threshold
        if self.score_left >= settings.WINNING_SCORE:
            self.winner_text = "Left player (Blue) wins!"
            self.state = self.STATE_GAME_OVER
        elif self.score_right >= settings.WINNING_SCORE:
            self.winner_text = "Right player (Red) wins!"
            self.state = self.STATE_GAME_OVER
    def draw(self):
        '''Render scores, paddles, ball, and state overlays.'''
        self.screen.fill(settings.BLACK)
        # Center dashed line
        for y in range(0, settings.SCREEN_HEIGHT, 40):
            pygame.draw.rect(self.screen, settings.GREY,
                             (settings.SCREEN_WIDTH // 2 - 2, y, 4, 20))
        # Scores
        self.screen.blit(
            self.font_score.render(str(self.score_left), True, settings.BLUE),
            (settings.SCREEN_WIDTH // 2 - 100, 20))
        self.screen.blit(
            self.font_score.render(str(self.score_right), True, settings.RED),
            (settings.SCREEN_WIDTH // 2 + 60, 20))
        # Entities
        self.paddle_left.draw(self.screen)
        self.paddle_right.draw(self.screen)
        self.ball.draw(self.screen)
        # State overlays
        if self.state == self.STATE_MENU:
            self._draw_center_text("CHATDEV PONG", settings.YELLOW,
                                   settings.FONT_SIZE_TITLE, -60)
            self._draw_center_text("Left: W/S  |  Right: UP/DOWN arrows",
                                   settings.WHITE, settings.FONT_SIZE_TEXT, 20)
            self._draw_center_text(
                "First to %d points wins. Press SPACE to start."
                % settings.WINNING_SCORE, settings.WHITE,
                settings.FONT_SIZE_TEXT, 60)
        elif self.state == self.STATE_PAUSED:
            self._draw_center_text("PAUSED - press P to resume", settings.YELLOW,
                                   settings.FONT_SIZE_TEXT, 0)
        elif self.state == self.STATE_GAME_OVER:
            self._draw_center_text(self.winner_text, settings.YELLOW,
                                   settings.FONT_SIZE_TITLE, -40)
            self._draw_center_text("Press R to play again, ESC to quit.",
                                   settings.WHITE, settings.FONT_SIZE_TEXT, 30)
        pygame.display.flip()
    def _draw_center_text(self, text, color, size, y_offset):
        '''Draw a text line horizontally centered with a vertical offset.'''
        font = pygame.font.SysFont("consolas", size, bold=True)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(settings.SCREEN_WIDTH // 2,
                                     settings.SCREEN_HEIGHT // 2 + y_offset))
        self.screen.blit(surf, rect)
    def run(self):
        '''Main game loop: events, update, draw, and frame pacing.'''
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)
        pygame.quit()