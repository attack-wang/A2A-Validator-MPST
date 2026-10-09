'''
Main game class: game loop, states, difficulty scaling, and rendering.
'''
import random
import pygame
import settings
from bird import Bird
from pipe import Pipe
class Game:
    '''Runs the Flappy Bird game loop and manages game state.'''
    STATE_START = 'start'
    STATE_PLAYING = 'playing'
    STATE_GAME_OVER = 'game_over'
    def __init__(self):
        '''Initialize pygame, window, fonts, and initial game state.'''
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.Font(settings.FONT_NAME, 48)
        self.font_medium = pygame.font.Font(settings.FONT_NAME, 28)
        self.font_small = pygame.font.Font(settings.FONT_NAME, 20)
        self.best_score = 0
        self.running = True
        self.reset()
        self.state = self.STATE_START
    def reset(self):
        '''Reset the round: bird, pipes, score, and scroll offset.'''
        self.bird = Bird(settings.BIRD_START_X, settings.BIRD_START_Y)
        self.pipes = []
        self.score = 0
        self.ground_offset = 0.0
        self.death_timer = 0.0
    # ------------------------------------------------------------------
    # Difficulty scaling
    # ------------------------------------------------------------------
    def current_gap_size(self):
        '''Gap shrinks as score rises, with random variation, bounded below.'''
        base = settings.BASE_GAP_SIZE - self.score * settings.GAP_DECREASE_PER_POINT
        base = max(settings.MIN_GAP_SIZE, base)
        variation = random.uniform(-settings.GAP_RANDOM_VARIATION,
                                   settings.GAP_RANDOM_VARIATION)
        return max(settings.MIN_GAP_SIZE, base + variation)
    def current_pipe_speed(self):
        '''Pipe speed rises as score rises, bounded above.'''
        speed = settings.BASE_PIPE_SPEED + self.score * settings.SPEED_INCREASE_PER_POINT
        return min(settings.MAX_PIPE_SPEED, speed)
    # ------------------------------------------------------------------
    # Game loop
    # ------------------------------------------------------------------
    def run(self):
        '''Main loop: process events, update, and render each frame.'''
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
    def handle_events(self):
        '''Process keyboard and mouse input per state.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.action()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.action()
    def action(self):
        '''Flap, start, or restart depending on the current state.'''
        if self.state == self.STATE_START:
            self.state = self.STATE_PLAYING
            self.bird.flap()
        elif self.state == self.STATE_PLAYING:
            self.bird.flap()
        elif self.state == self.STATE_GAME_OVER and self.death_timer <= 0.0:
            self.reset()
            self.state = self.STATE_PLAYING
            self.bird.flap()
    def update(self, dt):
        '''Advance the simulation for one frame.'''
        if self.state == self.STATE_PLAYING:
            self.bird.update(dt)
            self.update_pipes(dt)
            self.update_score()
            self.check_collisions()
            self.ground_offset -= self.current_pipe_speed() * dt
        elif self.state == self.STATE_GAME_OVER:
            self.death_timer = max(0.0, self.death_timer - dt)
            ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
            if self.bird.y < ground_top - settings.BIRD_RADIUS:
                self.bird.update(dt)  # let the bird fall after a crash
                # Clamp so the bird rests on the ground instead of tunneling
                if self.bird.y > ground_top - settings.BIRD_RADIUS:
                    self.bird.y = ground_top - settings.BIRD_RADIUS
                    self.bird.velocity = 0.0
    def update_pipes(self, dt):
        '''Move pipes, spawn new ones, and cull offscreen ones.'''
        speed = self.current_pipe_speed()
        for pipe in self.pipes:
            pipe.update(dt, speed)
        if not self.pipes:
            self.spawn_pipe()
        else:
            last = self.pipes[-1]
            if last.x <= settings.SCREEN_WIDTH - settings.PIPE_SPAWN_DISTANCE:
                self.spawn_pipe()
        self.pipes = [p for p in self.pipes if not p.is_offscreen()]
    def spawn_pipe(self, x=None):
        '''Create a new pipe pair with a randomized gap.'''
        gap_size = self.current_gap_size()
        gap_center = Pipe.random_gap_center(gap_size)
        if x is None:
            x = settings.SCREEN_WIDTH + settings.PIPE_CAP_OVERHANG
        self.pipes.append(Pipe(x, gap_center, gap_size))
    def update_score(self):
        '''Award points for pipes the bird has passed.'''
        for pipe in self.pipes:
            if pipe.has_passed(self.bird.x):
                pipe.mark_scored()
                self.score += settings.SCORE_PER_PIPE
                if self.score > self.best_score:
                    self.best_score = self.score
    def check_collisions(self):
        '''End the game on pipe or ground collision.'''
        bird_rect = self.bird.get_rect()
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        if bird_rect.bottom >= ground_top:
            self.game_over()
            return
        for pipe in self.pipes:
            if pipe.collides_with(bird_rect):
                self.game_over()
                return
    def game_over(self):
        '''Switch to the game-over state and record the best score.'''
        self.state = self.STATE_GAME_OVER
        self.death_timer = 0.6  # brief pause before restart is allowed
        if self.score > self.best_score:
            self.best_score = self.score
    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def draw(self):
        '''Render the current frame.'''
        self.screen.fill(settings.SKY_BLUE)
        self.draw_clouds()
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.draw_ground()
        self.bird.draw(self.screen)
        if self.state == self.STATE_START:
            self.draw_start_screen()
        elif self.state == self.STATE_PLAYING:
            self.draw_score()
        else:
            self.draw_game_over_screen()
        pygame.display.flip()
    def draw_clouds(self):
        '''Draw a few static decorative clouds.'''
        for cx, cy, r in ((90, 110, 26), (300, 70, 32), (400, 170, 22), (180, 220, 20)):
            pygame.draw.circle(self.screen, settings.CLOUD_COLOR, (cx, cy), r)
            pygame.draw.circle(self.screen, settings.CLOUD_COLOR,
                               (cx + r, cy + 4), int(r * 0.75))
            pygame.draw.circle(self.screen, settings.CLOUD_COLOR,
                               (cx - r, cy + 6), int(r * 0.7))
    def draw_ground(self):
        '''Render the scrolling ground band.'''
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        pygame.draw.rect(self.screen, settings.GROUND_COLOR,
                         (0, ground_top, settings.SCREEN_WIDTH, settings.GROUND_HEIGHT))
        pygame.draw.rect(self.screen, settings.GROUND_DARK,
                         (0, ground_top, settings.SCREEN_WIDTH, 10))
        stripe_w = 24
        offset = int(self.ground_offset) % stripe_w
        for x in range(-stripe_w, settings.SCREEN_WIDTH + stripe_w, stripe_w):
            pygame.draw.polygon(self.screen, settings.GROUND_DARK, [
                (x + offset, ground_top + 10),
                (x + offset + stripe_w // 2, ground_top + 10),
                (x + offset, ground_top + 22),
            ])
    def draw_text_with_outline(self, text, font, color, outline_color, center, outline_width=2):
        '''Render text with a simple outline for readability.'''
        surf = font.render(text, True, outline_color)
        rect = surf.get_rect(center=center)
        for dx, dy in ((-outline_width, 0), (outline_width, 0),
                       (0, -outline_width), (0, outline_width)):
            self.screen.blit(surf, rect.move(dx, dy))
        surf = font.render(text, True, color)
        self.screen.blit(surf, rect)
    def draw_score(self):
        '''Show the current score at the top of the screen.'''
        self.draw_text_with_outline(str(self.score), self.font_big,
                                    settings.WHITE, settings.BLACK,
                                    (settings.SCREEN_WIDTH // 2, 60))
    def draw_start_screen(self):
        '''Title screen with instructions and best score.'''
        cx = settings.SCREEN_WIDTH // 2
        self.draw_text_with_outline('FLAPPY BIRD', self.font_big,
                                    settings.WHITE, settings.BLACK, (cx, 150))
        self.draw_text_with_outline('Press SPACE or CLICK to flap', self.font_small,
                                    settings.WHITE, settings.BLACK, (cx, 230))
        self.draw_text_with_outline('Avoid the pipes!', self.font_small,
                                    settings.WHITE, settings.BLACK, (cx, 265))
        self.draw_text_with_outline('Difficulty rises with your score', self.font_small,
                                    settings.WHITE, settings.BLACK, (cx, 300))
        self.draw_text_with_outline('Best: {}'.format(self.best_score), self.font_medium,
                                    settings.WHITE, settings.BLACK, (cx, 360))
    def draw_game_over_screen(self):
        '''Game-over panel with final score, best score, and restart hint.'''
        cx = settings.SCREEN_WIDTH // 2
        panel = pygame.Rect(0, 0, 320, 220)
        panel.center = (cx, settings.SCREEN_HEIGHT // 2 - 20)
        pygame.draw.rect(self.screen, settings.WHITE, panel, border_radius=12)
        pygame.draw.rect(self.screen, settings.BLACK, panel, 3, border_radius=12)
        self.draw_text_with_outline('GAME OVER', self.font_big,
                                    settings.RED, settings.BLACK, (cx, panel.top + 45))
        self.draw_text_with_outline('Score: {}'.format(self.score), self.font_medium,
                                    settings.BLACK, settings.WHITE, (cx, panel.top + 105))
        self.draw_text_with_outline('Best: {}'.format(self.best_score), self.font_medium,
                                    settings.BLACK, settings.WHITE, (cx, panel.top + 140))
        if self.death_timer <= 0.0:
            self.draw_text_with_outline('Press SPACE to restart', self.font_small,
                                        settings.BLACK, settings.WHITE,
                                        (cx, panel.bottom - 30))