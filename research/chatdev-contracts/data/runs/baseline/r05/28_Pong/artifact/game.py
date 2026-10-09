'''
game.py
Defines the Game class: owns the pygame window, both paddles, the ball,
the fonts and the main loop. Handles per-frame updates, wall/paddle
collisions, scoring, win detection, restart (SPACE) and quit (ESC).
Fixes applied: complete __init__ and main loop, event handling for
SPACE-restart and ESC-quit, winner stored as "left"/"right" so the
game-over message matches, update() guarded to stop infinite scoring
after a win, and pygame.display.flip() added to render frames.
'''
import pygame
import settings
from paddle import Paddle
from ball import Ball
class Game:
    '''Runs one match of two-player Pong and renders every frame.'''
    def __init__(self):
        '''Create the window, fonts, paddles, ball and initial game state.'''
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.CAPTION)
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.Font(None, 72)
        self.message_font = pygame.font.Font(None, 36)
        self.left_paddle = Paddle(
            settings.PADDLE_MARGIN,
            pygame.K_w, pygame.K_s, settings.GREEN)
        self.right_paddle = Paddle(
            settings.SCREEN_WIDTH - settings.PADDLE_MARGIN - settings.PADDLE_WIDTH,
            pygame.K_UP, pygame.K_DOWN, settings.BLUE)
        self.ball = Ball()
        self.winner = None  # None while playing; "left" or "right" after a win
    def run(self):
        '''Main loop: tick at FPS, handle events, update (while playing), draw.'''
        while True:
            self.clock.tick(settings.FPS)
            self.handle_events()
            if self.winner is None:
                self.update()
            self.draw()
    def handle_events(self):
        '''Process window close, ESC (quit) and SPACE (restart after a win).'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit
                if event.key == pygame.K_SPACE and self.winner is not None:
                    self.restart()
    def restart(self):
        '''Start a fresh match: clear scores, re-center paddles, reset ball.'''
        self.left_paddle.score = 0
        self.right_paddle.score = 0
        self.left_paddle.reset_position()
        self.right_paddle.reset_position()
        self.ball.reset()
        self.winner = None
    def update(self):
        '''Advance the game state by one frame (skipped once a winner exists).'''
        if self.winner is not None:
            return
        keys = pygame.key.get_pressed()
        self.left_paddle.move(keys)
        self.right_paddle.move(keys)
        self.ball.move()
        self.check_wall_collisions()
        self.check_paddle_collisions()
        self.check_scoring()
    def check_wall_collisions(self):
        '''Bounce the ball off the top and bottom screen edges.'''
        ball_rect = self.ball.get_rect()
        if ball_rect.top <= 0 and self.ball.speed_y < 0:
            self.ball.bounce_vertical()
            self.ball.y = 0
        elif ball_rect.bottom >= settings.SCREEN_HEIGHT and self.ball.speed_y > 0:
            self.ball.bounce_vertical()
            self.ball.y = settings.SCREEN_HEIGHT - self.ball.size
    def check_paddle_collisions(self):
        '''Bounce the ball off either paddle, preventing tunneling/sticking.'''
        ball_rect = self.ball.get_rect()
        left_rect = self.left_paddle.get_rect()
        right_rect = self.right_paddle.get_rect()
        if ball_rect.colliderect(left_rect) and self.ball.speed_x < 0:
            self.ball.x = left_rect.right
            self.ball.bounce_horizontal(self.left_paddle)
        elif ball_rect.colliderect(right_rect) and self.ball.speed_x > 0:
            self.ball.x = right_rect.left - self.ball.size
            self.ball.bounce_horizontal(self.right_paddle)
    def check_scoring(self):
        '''Award a point when the ball passes a side edge, reset ball, check win.'''
        ball_rect = self.ball.get_rect()
        if ball_rect.right < 0:
            # Ball exited on the left: right player scores
            self.right_paddle.score += 1
            self.after_point()
        elif ball_rect.left > settings.SCREEN_WIDTH:
            # Ball exited on the right: left player scores
            self.left_paddle.score += 1
            self.after_point()
    def after_point(self):
        '''Handle post-point logic: reset the ball or record the winner.'''
        if self.left_paddle.score >= settings.WINNING_SCORE:
            self.winner = "left"
        elif self.right_paddle.score >= settings.WINNING_SCORE:
            self.winner = "right"
        else:
            self.ball.reset()
    def draw(self):
        '''Render the current frame: background, line, paddles, ball, scores.'''
        self.screen.fill(settings.BLACK)
        self.draw_center_line()
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_scores()
        self.draw_controls()
        if self.winner is not None:
            self.draw_game_over()
        pygame.display.flip()
    def draw_center_line(self):
        '''Draw the dashed center line dividing the two halves of the court.'''
        dash_height, gap, y = 20, 12, 0
        x = settings.SCREEN_WIDTH // 2 - 2
        while y < settings.SCREEN_HEIGHT:
            pygame.draw.rect(self.screen, settings.GRAY, (x, y, 4, dash_height))
            y += dash_height + gap
    def draw_scores(self):
        '''Render both players' scores at the top of the screen.'''
        left_text = self.score_font.render(
            str(self.left_paddle.score), True, settings.GREEN)
        right_text = self.score_font.render(
            str(self.right_paddle.score), True, settings.BLUE)
        self.screen.blit(left_text, left_text.get_rect(
            center=(settings.SCREEN_WIDTH // 4, 50)))
        self.screen.blit(right_text, right_text.get_rect(
            center=(3 * settings.SCREEN_WIDTH // 4, 50)))
    def draw_controls(self):
        '''Show the control hints along the bottom of the court.'''
        hint_text = self.message_font.render(
            "Left paddle: W / S    Right paddle: Arrow Up / Arrow Down    "
            "First to {} wins".format(settings.WINNING_SCORE),
            True, settings.GRAY)
        self.screen.blit(hint_text, hint_text.get_rect(
            midbottom=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 10)))
    def draw_game_over(self):
        '''Overlay the winner announcement and restart instructions.'''
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(160)
        overlay.fill(settings.BLACK)
        self.screen.blit(overlay, (0, 0))
        if self.winner == "left":
            message, color = "Left player wins!", settings.GREEN
        else:
            message, color = "Right player wins!", settings.BLUE
        winner_text = self.score_font.render(message, True, color)
        self.screen.blit(winner_text, winner_text.get_rect(
            center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 30)))
        restart_text = self.message_font.render(
            "Press SPACE to play again - ESC to quit", True, settings.WHITE)
        self.screen.blit(restart_text, restart_text.get_rect(
            center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 30)))