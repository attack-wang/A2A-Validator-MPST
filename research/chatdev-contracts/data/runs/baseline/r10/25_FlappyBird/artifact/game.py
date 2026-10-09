'''
game.py
Core game loop, state management, scoring and difficulty scaling.
States: menu -> playing -> game_over -> (restart) -> playing ...
Fixes applied from the test report:
- completed the truncated handle_events() (unclosed parenthesis -> SyntaxError)
- restored all missing methods (run, update, draw, _play, difficulty/spawn/cloud helpers)
- initialized self.clouds so _update_clouds/_draw_clouds cannot raise AttributeError
'''
import random
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    BASE_SPEED, MAX_SPEED, SPEED_GAIN_PER_POINT,
    BASE_GAP, MIN_GAP, GAP_SHRINK_PER_POINT, GAP_VARIATION,
    PIPE_WIDTH, PIPE_SPACING,
    BIRD_START_X, BIRD_START_Y, BIRD_HEIGHT,
    GROUND_HEIGHT, SKY_COLOR, CLOUD_COLOR,
    RESTART_DELAY_FRAMES,
)
from bird import Bird
from pipe import Pipe
from ground import Ground
import ui
from sounds import create_sounds
from highscore import load_high_score, save_high_score
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
class Game:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 1, 512)
        pygame.init()
        if pygame.mixer.get_init() is None:
            try:
                pygame.mixer.init()
            except pygame.error:
                pass
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("arial", 48, bold=True)
        self.font_small = pygame.font.SysFont("arial", 24, bold=True)
        self.sounds = create_sounds()
        self.best_score = load_high_score()
        self.death_timer = 0
        self.reset()
        self.state = STATE_MENU
    # ------------------------------------------------------------------ #
    # Setup / state transitions
    # ------------------------------------------------------------------ #
    def reset(self):
        self.bird = Bird(BIRD_START_X, BIRD_START_Y)
        self.pipes = []
        self.ground = Ground()
        self.clouds = self._make_clouds()
        self.score = 0
        self.speed = BASE_SPEED
        self.gap_size = BASE_GAP
        self.distance_since_spawn = 0
    def _make_clouds(self):
        return [
            {"x": random.randint(0, SCREEN_WIDTH),
             "y": random.randint(60, 260),
             "s": random.uniform(0.2, 0.8)}
            for _ in range(4)
        ]
    def start(self):
        self.reset()
        self.state = STATE_PLAYING
    def game_over(self):
        self.bird.alive = False
        self.state = STATE_GAME_OVER
        self.death_timer = RESTART_DELAY_FRAMES
        self._play("hit")
        if self.score > self.best_score:
            self.best_score = self.score
            save_high_score(self.best_score)
    def _play(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.play()
    # ------------------------------------------------------------------ #
    # Events (previously truncated at line 75 — now complete)
    # ------------------------------------------------------------------ #
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if self.state == STATE_MENU:
                        self.start()
                        self.bird.flap()
                        self._play("flap")
                    elif self.state == STATE_PLAYING:
                        self.bird.flap()
                        self._play("flap")
                    elif self.state == STATE_GAME_OVER and self.death_timer <= 0:
                        self.start()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit
    # ------------------------------------------------------------------ #
    # Difficulty & pipe spawning
    # ------------------------------------------------------------------ #
    def update_difficulty(self):
        self.speed = min(MAX_SPEED, BASE_SPEED + self.score * SPEED_GAIN_PER_POINT)
        self.gap_size = max(MIN_GAP, BASE_GAP - self.score * GAP_SHRINK_PER_POINT)
    def spawn_pipe_if_needed(self):
        if not self.pipes:
            self._spawn_pipe(SCREEN_WIDTH + PIPE_WIDTH)
            self.distance_since_spawn = 0
            return
        self.distance_since_spawn += self.speed
        if self.distance_since_spawn >= PIPE_SPACING:
            self._spawn_pipe(SCREEN_WIDTH + PIPE_WIDTH)
            self.distance_since_spawn = 0
    def _spawn_pipe(self, x):
        variation = random.randint(-GAP_VARIATION, GAP_VARIATION)
        gap = max(MIN_GAP, self.gap_size + variation)
        self.pipes.append(Pipe(x, gap))
    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #
    def update(self):
        self._update_clouds()
        if self.state == STATE_PLAYING:
            self.bird.update()
            self.update_difficulty()
            self.spawn_pipe_if_needed()
            for pipe in self.pipes:
                pipe.update(self.speed)
            self.pipes = [p for p in self.pipes if not p.offscreen()]
            self.ground.update(self.speed)
            # scoring: pipe fully passed the bird
            for pipe in self.pipes:
                if not pipe.scored and pipe.x + PIPE_WIDTH < self.bird.x:
                    pipe.scored = True
                    self.score += 1
                    self._play("point")
            # collisions
            bird_box = self.bird.hitbox
            hit_pipe = any(p.collides(bird_box) for p in self.pipes)
            hit_ground = self.bird.y + BIRD_HEIGHT / 2 >= SCREEN_HEIGHT - GROUND_HEIGHT
            if hit_pipe or hit_ground:
                self.game_over()
        elif self.state == STATE_GAME_OVER:
            # let the dead bird tumble to the ground
            self.bird.update()
            ground_top = SCREEN_HEIGHT - GROUND_HEIGHT
            if self.bird.y + BIRD_HEIGHT / 2 >= ground_top:
                self.bird.y = ground_top - BIRD_HEIGHT / 2
                self.bird.velocity = 0.0
            if self.death_timer > 0:
                self.death_timer -= 1
    def _update_clouds(self):
        for cloud in self.clouds:
            cloud["x"] -= cloud["s"]
            if cloud["x"] < -80:
                cloud["x"] = SCREEN_WIDTH + 80
                cloud["y"] = random.randint(60, 260)
    # ------------------------------------------------------------------ #
    # Draw
    # ------------------------------------------------------------------ #
    def _draw_clouds(self):
        for cloud in self.clouds:
            x, y = int(cloud["x"]), int(cloud["y"])
            pygame.draw.ellipse(self.screen, CLOUD_COLOR, (x, y, 70, 28))
            pygame.draw.ellipse(self.screen, CLOUD_COLOR, (x + 18, y - 12, 50, 30))
            pygame.draw.ellipse(self.screen, CLOUD_COLOR, (x + 40, y + 2, 46, 24))
    def draw(self):
        self.screen.fill(SKY_COLOR)
        self._draw_clouds()
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.ground.draw(self.screen)
        self.bird.draw(self.screen)
        if self.state in (STATE_PLAYING, STATE_GAME_OVER):
            ui.draw_score(self.screen, self.score, self.font_big)
        if self.state == STATE_MENU:
            ui.draw_center_text(self.screen, "Flappy Bird", self.font_big, SCREEN_HEIGHT // 2 - 60)
            ui.draw_center_text(self.screen, "Press SPACE to start", self.font_small, SCREEN_HEIGHT // 2)
            ui.draw_center_text(self.screen, f"Best: {self.best_score}", self.font_small, SCREEN_HEIGHT // 2 + 40)
        elif self.state == STATE_GAME_OVER:
            ui.draw_game_over(self.screen, self.score, self.best_score, self.font_big, self.font_small)
        pygame.display.flip()
    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)