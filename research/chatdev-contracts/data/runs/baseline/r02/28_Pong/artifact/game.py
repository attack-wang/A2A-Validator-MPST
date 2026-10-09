'''
game.py
Core game orchestration: window creation, main loop, state machine
(menu -> playing -> game over), collision handling, scoring, ball
resetting after each point and rendering of every on-screen element.
'''
import random
import pygame
import sys
import settings
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
class Game:
    """State-machine driven two-player Pong game."""
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    def __init__(self):
        """Initialise pygame, the window, entities and the menu state."""
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("consolas", 64, bold=True)
        self.font_medium = pygame.font.SysFont("consolas", 30)
        self.font_small = pygame.font.SysFont("consolas", 22)
        self.left_paddle = Paddle("left", settings.KEY_LEFT_UP, settings.KEY_LEFT_DOWN)
        self.right_paddle = Paddle("right", settings.KEY_RIGHT_UP, settings.KEY_RIGHT_DOWN)
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.state = self.MENU
        self.serve_timer = 0
        self.running = True
    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def handle_events(self):
        """Process the event queue: quit, start/restart and pause-to-menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == self.MENU and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.start_game()
                elif self.state == self.GAME_OVER:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                elif self.state == self.PLAYING and event.key == pygame.K_ESCAPE:
                    # back to menu
                    self.state = self.MENU
    def start_game(self):
        """Reset scores, paddles and ball, then enter PLAYING with a serve delay."""
        self.scoreboard.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.reset(random.choice([-1, 1]))
        self.serve_timer = settings.SERVE_DELAY_FRAMES
        self.state = self.PLAYING
    # ------------------------------------------------------------------
    # Update logic
    # ------------------------------------------------------------------
    def handle_collisions(self):
        """Bounce the ball off either paddle and push it clear of the paddle."""
        ball_rect = self.ball.rect
        if self.ball.dx < 0 and ball_rect.colliderect(self.left_paddle.rect):
            offset = self.left_paddle.hit_offset(ball_rect)
            self.ball.bounce_off_paddle(offset)
            ball_rect.left = self.left_paddle.rect.right
            self.ball.x = float(ball_rect.x)
        elif self.ball.dx > 0 and ball_rect.colliderect(self.right_paddle.rect):
            offset = self.right_paddle.hit_offset(ball_rect)
            self.ball.bounce_off_paddle(offset)
            ball_rect.right = self.right_paddle.rect.left
            self.ball.x = float(ball_rect.x)
    def check_scoring(self):
        """Award a point when a player misses; end the match on a win."""
        if self.ball.rect.right < 0:                       # ball passed left edge
            self.scoreboard.increment("right")             # right player scores
            self._after_point(serve_direction=-1)          # serve toward conceder
        elif self.ball.rect.left > settings.SCREEN_WIDTH:  # passed right edge
            self.scoreboard.increment("left")
            self._after_point(serve_direction=1)
    def _after_point(self, serve_direction):
        """Reset the ball with a serve delay, or switch to GAME_OVER."""
        if self.scoreboard.get_winner():
            self.state = self.GAME_OVER
            return
        self.ball.reset(serve_direction)
        self.serve_timer = settings.SERVE_DELAY_FRAMES
    def update(self):
        """Advance the game one frame (only while PLAYING)."""
        if self.state != self.PLAYING:
            return
        self.left_paddle.update()
        self.right_paddle.update()
        if self.serve_timer > 0:          # ball frozen during serve delay
            self.serve_timer -= 1
            return
        self.ball.update()
        self.handle_collisions()
        self.check_scoring()
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def draw(self):
        """Render one frame according to the current state."""
        self.screen.fill(settings.COLOR_BACKGROUND)
        self._draw_center_line()
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.scoreboard.draw(self.screen)
        if self.state == self.MENU:
            self._draw_text("PONG", self.font_large, settings.COLOR_ACCENT, -70)
            self._draw_text("Player 1: W / S    Player 2: Up / Down",
                            self.font_small, settings.COLOR_TEXT, 0)
            self._draw_text("First to %d points wins - press SPACE to start"
                            % settings.WINNING_SCORE,
                            self.font_small, settings.COLOR_TEXT, 40)
        elif self.state == self.GAME_OVER:
            winner = self.scoreboard.get_winner()
            label = "Player 1 wins!" if winner == "left" else "Player 2 wins!"
            self._draw_text(label, self.font_large, settings.COLOR_ACCENT, -70)
            self._draw_text("SPACE: play again    ESC: quit",
                            self.font_small, settings.COLOR_TEXT, 0)
        pygame.display.flip()
    def _draw_center_line(self):
        """Dashed vertical line splitting the two halves."""
        for y in range(0, settings.SCREEN_HEIGHT, 30):
            pygame.draw.rect(self.screen, settings.COLOR_FOREGROUND,
                             (settings.SCREEN_WIDTH // 2 - 2, y, 4, 15))
    def _draw_text(self, text, font, color, y_offset):
        """Blit text horizontally centred, offset vertically from mid-screen."""
        rendered = font.render(text, True, color)
        pos = (settings.SCREEN_WIDTH // 2 - rendered.get_width() // 2,
               settings.SCREEN_HEIGHT // 2 + y_offset - rendered.get_height() // 2)
        self.screen.blit(rendered, pos)
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        """Run the main loop until the window is closed."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)
        pygame.quit()