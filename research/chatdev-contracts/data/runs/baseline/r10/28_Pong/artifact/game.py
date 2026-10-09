'''
game.py
Main Game class: wires together paddles, ball, and scoreboard; handles
events, updates game state each frame, and renders the court and overlays.
'''
import random
import pygame
import settings
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
class Game:
    """Coordinates the two-player Pong match from start to win."""
    def __init__(self):
        """Initialize pygame, the window, and all game objects."""
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(settings.CAPTION)
        self.clock = pygame.time.Clock()
        self.running = False
        self.game_over = False
        # Left paddle: Player 1 (W/S keys); Right paddle: Player 2 (arrows)
        self.paddle_left = Paddle(
            settings.PADDLE_MARGIN,
            pygame.K_w, pygame.K_s, settings.GREEN,
        )
        self.paddle_right = Paddle(
            settings.SCREEN_WIDTH - settings.PADDLE_MARGIN - settings.PADDLE_WIDTH,
            pygame.K_UP, pygame.K_DOWN, settings.BLUE,
        )
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.message_font = pygame.font.Font(
            settings.FONT_NAME, settings.MESSAGE_FONT_SIZE
        )
        self.small_font = pygame.font.Font(
            settings.FONT_NAME, settings.SMALL_FONT_SIZE
        )
    def handle_events(self):
        """Process quit, restart, and exit requests."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.restart()
    def restart(self):
        """Reset scores and ball for a fresh match."""
        self.scoreboard.reset()
        self.ball.reset(direction=random.choice([-1, 1]))
        self.game_over = False
    def run(self):
        """Run the main game loop until the player quits."""
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)
        pygame.quit()
    def update(self):
        """Update paddles, ball, collisions, and scoring for one frame."""
        keys = pygame.key.get_pressed()
        self.paddle_left.update(keys)
        self.paddle_right.update(keys)
        if not self.game_over:
            self.ball.update()
            self.check_paddle_collisions()
            self.check_scoring()
    def check_paddle_collisions(self):
        """Bounce the ball off either paddle when it reaches its face."""
        ball = self.ball
        # Left paddle: ball must be moving left toward it
        left = self.paddle_left
        if ball.speed_x < 0:
            crossed = (ball.prev_rect.left >= left.rect.right and
                       ball.rect.left <= left.rect.right)
            overlapping = ball.rect.colliderect(left.rect)
            if (crossed or overlapping) and \
               ball.rect.bottom >= left.rect.top and \
               ball.rect.top <= left.rect.bottom:
                ball.bounce_off_paddle(left)
        # Right paddle: ball must be moving right toward it
        right = self.paddle_right
        if ball.speed_x > 0:
            crossed = (ball.prev_rect.right <= right.rect.left and
                       ball.rect.right >= right.rect.left)
            overlapping = ball.rect.colliderect(right.rect)
            if (crossed or overlapping) and \
               ball.rect.bottom >= right.rect.top and \
               ball.rect.top <= right.rect.bottom:
                ball.bounce_off_paddle(right)
    def check_scoring(self):
        """Award a point when the ball passes a side edge, then reset the ball
        or finish the match if the winning score has been reached."""
        if self.ball.rect.right < 0:
            # Ball passed the left edge: right player scores
            self.scoreboard.increase_score('right')
            self.after_point('right')
        elif self.ball.rect.left > settings.SCREEN_WIDTH:
            # Ball passed the right edge: left player scores
            self.scoreboard.increase_score('left')
            self.after_point('left')
    def after_point(self, scorer):
        """Handle post-point logic: reset the ball or end the match."""
        winner = self.scoreboard.get_winner()
        if winner is not None:
            self.game_over = True
        else:
            # Serve toward the player who missed the ball (the non-scorer)
            direction = -1 if scorer == 'right' else 1
            self.ball.reset(direction=direction)
    def draw(self):
        """Render the court, objects, scores, and any overlay messages."""
        self.screen.fill(settings.BLACK)
        self.draw_center_line()
        self.paddle_left.draw(self.screen)
        self.paddle_right.draw(self.screen)
        self.ball.draw(self.screen)
        self.scoreboard.draw(self.screen)
        if self.game_over:
            self.draw_game_over()
        elif self.ball.serve_timer > 0:
            self.draw_serve_hint()
        pygame.display.flip()
    def draw_center_line(self):
        """Draw the dashed center line dividing the two court halves."""
        line_width = 4
        segment_height = 20
        gap = 14
        x = settings.SCREEN_WIDTH // 2 - line_width // 2
        y = 0
        while y < settings.SCREEN_HEIGHT:
            pygame.draw.rect(
                self.screen, settings.GREY,
                (x, y, line_width, segment_height),
            )
            y += segment_height + gap
    def draw_serve_hint(self):
        """Show a short countdown hint while the ball waits to be served."""
        seconds_left = self.ball.serve_timer // settings.FPS + 1
        text = f"Serving in {seconds_left}..."
        surface = self.small_font.render(text, True, settings.WHITE)
        rect = surface.get_rect(
            center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 40)
        )
        self.screen.blit(surface, rect)
    def draw_game_over(self):
        """Display the winner and restart instructions."""
        winner = self.scoreboard.get_winner()
        if winner == 'left':
            message = "Player 1 (left) wins!"
        else:
            message = "Player 2 (right) wins!"
        surface = self.message_font.render(message, True, settings.WHITE)
        rect = surface.get_rect(
            center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 30)
        )
        self.screen.blit(surface, rect)
        hint = "Press SPACE to play again - ESC to quit"
        surface = self.small_font.render(hint, True, settings.WHITE)
        rect = surface.get_rect(
            center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 20)
        )
        self.screen.blit(surface, rect)