'''
game.py
Contains the Game class, the top-level controller of the Pong match.
It manages the game states (menu / playing / game over), handles
keyboard events, updates the simulation and renders every frame.
'''
import sys
import pygame
import settings
import ui
from paddle import Paddle
from ball import Ball
# ---------------------------------------------------------------------------
# Game states
# ---------------------------------------------------------------------------
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game_over'
class Game:
    '''Top-level controller: owns the window, the entities and the match flow.'''
    def __init__(self):
        '''Create the window, the entities and initialise the match state.'''
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        # Entities
        self.paddle_left = Paddle('left')
        self.paddle_right = Paddle('right')
        self.ball = Ball()          # Ball() serves towards a random side
        # Match state
        self.score_left = 0
        self.score_right = 0
        self.last_scorer = None     # 'left' / 'right', or None before first point
        self.winner = None          # 'left' / 'right', or None while playing
        self.state = STATE_MENU
    # ------------------------------------------------------------------
    # Match lifecycle
    # ------------------------------------------------------------------
    def _start_match(self):
        '''(Re)start a match: clear the scores and reset every entity.'''
        self.score_left = 0
        self.score_right = 0
        self.last_scorer = None
        self.winner = None
        self.paddle_left = Paddle('left')
        self.paddle_right = Paddle('right')
        self.ball = Ball()
        self.state = STATE_PLAYING
    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def _handle_events(self):
        '''Process window and keyboard events (quit / state transitions).'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    # SPACE starts the match from the menu or triggers a rematch.
                    if self.state in (STATE_MENU, STATE_GAME_OVER):
                        self._start_match()
    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------
    def _handle_paddle_input(self):
        '''Read the keyboard and move both paddles accordingly.'''
        keys = pygame.key.get_pressed()
        # Player 1 (left paddle): W / S
        if keys[pygame.K_w]:
            self.paddle_left.move_up()
        if keys[pygame.K_s]:
            self.paddle_left.move_down()
        # Player 2 (right paddle): Up / Down arrows
        if keys[pygame.K_UP]:
            self.paddle_right.move_up()
        if keys[pygame.K_DOWN]:
            self.paddle_right.move_down()
    # ------------------------------------------------------------------
    # Rules / collisions
    # ------------------------------------------------------------------
    def _check_paddle_collisions(self):
        '''Bounce the ball off either paddle when they overlap.'''
        ball = self.ball
        if ball.rect.colliderect(self.paddle_left.rect) and ball.velocity_x < 0:
            ball.bounce_off_paddle(self.paddle_left)
        elif ball.rect.colliderect(self.paddle_right.rect) and ball.velocity_x > 0:
            ball.bounce_off_paddle(self.paddle_right)
    def _check_scoring(self):
        '''Award a point when the ball leaves the playfield on either side.'''
        ball = self.ball
        if ball.rect.right < 0:
            # Ball left through the left edge -> right player scores.
            self.score_right += 1
            self.last_scorer = 'right'
            self._after_point(serve_towards='left')
        elif ball.rect.left > settings.SCREEN_WIDTH:
            # Ball left through the right edge -> left player scores.
            self.score_left += 1
            self.last_scorer = 'left'
            self._after_point(serve_towards='right')
    def _after_point(self, serve_towards):
        '''Handle the end of a point: reset the ball or finish the match.'''
        if self.score_left >= settings.WINNING_SCORE or self.score_right >= settings.WINNING_SCORE:
            self.winner = 'left' if self.score_left > self.score_right else 'right'
            self.state = STATE_GAME_OVER
        else:
            # Serve towards the player who just missed the ball.
            direction = -1 if serve_towards == 'left' else 1
            self.ball.reset(direction)
    # ------------------------------------------------------------------
    # Update / draw
    # ------------------------------------------------------------------
    def _update(self):
        '''Advance the simulation by one frame.'''
        self._handle_paddle_input()
        self.ball.update()
        if self.ball.serve_timer == 0:      # only collide while the ball is in flight
            self._check_paddle_collisions()
        self._check_scoring()
    def _draw_playfield(self):
        '''Draw everything that belongs to an active match.'''
        self.screen.fill(settings.COLOR_BACKGROUND)
        ui.draw_center_line(self.screen)
        ui.draw_score(self.screen, self.score_left, self.score_right)
        ui.draw_controls(self.screen)
        self.paddle_left.draw(self.screen)
        self.paddle_right.draw(self.screen)
        self.ball.draw(self.screen)
        # While the ball waits to be served, show who scored the last point.
        if self.ball.serve_timer > 0 and self.last_scorer is not None:
            scorer_name = 'Player 1' if self.last_scorer == 'left' else 'Player 2'
            ui.draw_centered_text(self.screen, f'{scorer_name} scores!', y_offset=-80)
    def _draw_menu(self):
        '''Draw the start screen.'''
        self.screen.fill(settings.COLOR_BACKGROUND)
        ui.draw_center_line(self.screen)
        ui.draw_centered_text(self.screen, 'P O N G', size='score', y_offset=-120)
        ui.draw_centered_text(
            self.screen,
            f'First player to {settings.WINNING_SCORE} points wins the match',
            size='small', y_offset=-60)
        ui.draw_centered_text(
            self.screen,
            'Player 1: W / S      Player 2: Up / Down arrows',
            size='small', y_offset=0)
        ui.draw_centered_text(self.screen, 'Press SPACE to start',
                              color=settings.COLOR_ACCENT, y_offset=70)
    def _draw_game_over(self):
        '''Draw the end-of-match screen.'''
        self._draw_playfield()
        winner_name = 'Player 1' if self.winner == 'left' else 'Player 2'
        ui.draw_centered_text(self.screen, f'{winner_name} wins!',
                              size='message', color=settings.COLOR_ACCENT, y_offset=-40)
        ui.draw_centered_text(self.screen, 'Press SPACE for a rematch - ESC to quit',
                              size='small', y_offset=20)
    def _draw(self):
        '''Render the current state of the game.'''
        if self.state == STATE_MENU:
            self._draw_menu()
        elif self.state == STATE_PLAYING:
            self._draw_playfield()
        else:
            self._draw_game_over()
        pygame.display.flip()
    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        '''Run the game until the window is closed.'''
        while True:
            self._handle_events()
            if self.state == STATE_PLAYING:
                self._update()
            self._draw()
            self.clock.tick(settings.FPS)