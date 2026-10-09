'''
Game class for the Pong game.
Owns the pygame window and main loop, and coordinates all gameplay:
player input, paddle/ball updates, paddle collisions, scoring with
serve delays, the winning-score threshold, restart handling and the
rendering of every on-screen element.
'''
import random
import pygame
import settings
from ball import Ball
from paddle import Paddle
class Game:
    """Two-player Pong match controller and renderer."""
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        """Initialise pygame, the window, fonts, entities and match state."""
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(settings.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_score = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_SCORE)
        self.font_message = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_MESSAGE)
        self.font_small = pygame.font.Font(settings.FONT_NAME, settings.FONT_SIZE_SMALL)
        self.left_paddle = Paddle(
            settings.PADDLE_MARGIN,
            settings.KEY_LEFT_UP,
            settings.KEY_LEFT_DOWN,
            settings.COLOR_PADDLE_LEFT,
        )
        self.right_paddle = Paddle(
            settings.WINDOW_WIDTH - settings.PADDLE_MARGIN - settings.PADDLE_WIDTH,
            settings.KEY_RIGHT_UP,
            settings.KEY_RIGHT_DOWN,
            settings.COLOR_PADDLE_RIGHT,
        )
        self.ball = Ball()
        self.score_left = 0
        self.score_right = 0
        self.serve_timer = 0.0  # ms remaining before the next serve
        self.state = Game.STATE_PLAYING
        self.winner_text = ""
        self._serve_ball(random.choice((-1, 1)))
    # ------------------------------------------------------------------ #
    # Main loop                                                          #
    # ------------------------------------------------------------------ #
    def run(self):
        """Run the game loop until the player quits."""
        running = True
        while running:
            delta_ms = self.clock.tick(settings.FPS)
            running = self._handle_events()
            self._update(delta_ms)
            self._render()
        pygame.quit()
    # ------------------------------------------------------------------ #
    # Internal helpers                                                   #
    # ------------------------------------------------------------------ #
    def _serve_ball(self, direction):
        """Reset the ball toward `direction` and arm the serve delay timer."""
        self.ball.reset(direction)
        self.serve_timer = settings.SERVE_DELAY_MS
    def _restart_match(self):
        """Reset scores and state, then serve a fresh ball for a new match."""
        self.score_left = 0
        self.score_right = 0
        self.state = Game.STATE_PLAYING
        self.winner_text = ""
        self._serve_ball(random.choice((-1, 1)))
    def _handle_events(self):
        """Process the event queue; return False when the game should exit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if self.state == Game.STATE_GAME_OVER and event.key == settings.KEY_RESTART:
                    self._restart_match()
        return True
    def _update(self, delta_ms):
        """Advance one frame: paddles always move; ball only while playing."""
        keys = pygame.key.get_pressed()
        self.left_paddle.update(keys)
        self.right_paddle.update(keys)
        if self.state == Game.STATE_GAME_OVER:
            return
        if self.serve_timer > 0:          # ball frozen during serve delay
            self.serve_timer -= delta_ms
            return
        self.ball.update()
        self._handle_paddle_collisions()
        self._check_scoring()
    def _handle_paddle_collisions(self):
        """Bounce the ball off a paddle when it intersects one, moving toward it."""
        if (self.ball.speed_x < 0 and self.ball.rect.colliderect(self.left_paddle.rect)):
            self.ball.bounce_off_paddle(self.left_paddle, +1)
        elif (self.ball.speed_x > 0 and self.ball.rect.colliderect(self.right_paddle.rect)):
            self.ball.bounce_off_paddle(self.right_paddle, -1)
    def _check_scoring(self):
        """Award a point when the ball exits a side; handle win or re-serve."""
        if self.ball.rect.right < 0:                       # left player missed
            self.score_right += 1
            if self.score_right >= settings.WINNING_SCORE:
                self.state = Game.STATE_GAME_OVER
                self.winner_text = "Player 2 wins!"
            else:
                self._serve_ball(-1)                       # re-serve toward loser
        elif self.ball.rect.left > settings.WINDOW_WIDTH:  # right player missed
            self.score_left += 1
            if self.score_left >= settings.WINNING_SCORE:
                self.state = Game.STATE_GAME_OVER
                self.winner_text = "Player 1 wins!"
            else:
                self._serve_ball(+1)                       # re-serve toward loser
    def _render(self):
        """Draw the current frame: field, scores, entities, overlays."""
        self.screen.fill(settings.COLOR_BACKGROUND)
        self._draw_center_line()
        self._draw_scores()
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        if self.state == Game.STATE_PLAYING:
            self.ball.draw(self.screen)
            if self.serve_timer > 0:
                self._draw_controls_hint()
        else:
            self._draw_game_over()
        pygame.display.flip()
    def _draw_center_line(self):
        """Draw a dashed vertical line dividing the two playfields."""
        for y in range(0, settings.WINDOW_HEIGHT, 30):
            pygame.draw.rect(
                self.screen,
                settings.COLOR_CENTER_LINE,
                (settings.WINDOW_WIDTH // 2 - 2, y, 4, 15),
            )
    def _draw_scores(self):
        """Render both players' scores near the top of the window."""
        left = self.font_score.render(str(self.score_left), True, settings.COLOR_SCORE)
        right = self.font_score.render(str(self.score_right), True, settings.COLOR_SCORE)
        self.screen.blit(left, left.get_rect(center=(settings.WINDOW_WIDTH // 4, 60)))
        self.screen.blit(right, right.get_rect(center=(3 * settings.WINDOW_WIDTH // 4, 60)))
    def _draw_controls_hint(self):
        """Show the control legend while the ball waits to be served."""
        controls = self.font_small.render(
            "Player 1: W / S      Player 2: UP / DOWN", True, settings.COLOR_MESSAGE
        )
        self.screen.blit(
            controls,
            controls.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 40)),
        )
    def _draw_game_over(self):
        """Overlay the winner banner and restart instructions."""
        overlay = pygame.Surface(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        winner = self.font_message.render(self.winner_text, True, settings.COLOR_MESSAGE)
        final = self.font_small.render(
            f"Final score  {self.score_left} : {self.score_right}", True, settings.COLOR_MESSAGE
        )
        prompt = self.font_small.render(
            f"Press {settings.KEY_RESTART_NAME} to play again  |  ESC to quit",
            True,
            settings.COLOR_MESSAGE,
        )
        center = settings.WINDOW_WIDTH // 2
        middle = settings.WINDOW_HEIGHT // 2
        self.screen.blit(winner, winner.get_rect(center=(center, middle - 50)))
        self.screen.blit(final, final.get_rect(center=(center, middle)))
        self.screen.blit(prompt, prompt.get_rect(center=(center, middle + 50)))