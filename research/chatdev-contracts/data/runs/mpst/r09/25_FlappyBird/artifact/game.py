'''
Main game orchestration: states, input, collisions, scoring, and rendering.
'''
import random
import pygame
import settings
from utils import draw_text, make_gradient
from bird import Bird
from pipe_manager import PipeManager
from ground import Ground
from sound import SoundKit
READY, PLAYING, GAME_OVER = "ready", "playing", "game_over"
class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.sound = SoundKit()
        self.background = make_gradient(settings.WIDTH, settings.HEIGHT, settings.SKY_TOP, settings.SKY_BOTTOM)
        self.clouds = [{"x": random.uniform(0, settings.WIDTH),
                        "y": random.uniform(40, settings.HEIGHT * 0.5),
                        "speed": random.uniform(8, 20),
                        "scale": random.uniform(0.7, 1.4)} for _ in range(5)]
        self.bird = Bird(settings.BIRD_X, settings.HEIGHT * 0.4)
        self.pipes = PipeManager()
        self.ground = Ground(settings.GROUND_Y)
        self.state = READY
        self.score = 0
        self.best = 0
        self.death_timer = 0.0
        self.flash = 0.0
        self.running = True
    def reset(self):
        self.bird.reset()
        self.pipes.reset()
        self.score = 0
        self.death_timer = 0.0
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if self.state == READY:
                        self.state = PLAYING
                        self.bird.flap()
                        self.sound.play("flap")
                    elif self.state == PLAYING:
                        self.bird.flap()
                        self.sound.play("flap")
                    elif self.state == GAME_OVER and self.death_timer <= 0:
                        self.reset()
                        self.state = READY
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == READY:
                    self.state = PLAYING
                    self.bird.flap()
                    self.sound.play("flap")
                elif self.state == PLAYING:
                    self.bird.flap()
                    self.sound.play("flap")
                elif self.state == GAME_OVER and self.death_timer <= 0:
                    self.reset()
                    self.state = READY
    def update(self, dt):
        self._update_clouds(dt)
        if self.state == READY:
            # gentle hover on the ready screen
            self.bird.anim_time += dt
            self.bird.y = settings.HEIGHT * 0.4 + math.sin(self.bird.anim_time * 3) * 8
            self.ground.update(dt, settings.BASE_SPEED)
        elif self.state == PLAYING:
            self.bird.update(dt)
            self.pipes.update(dt, self.score)
            self.ground.update(dt, self.pipes.speed_for(self.score))
            self._check_scoring()
            self._check_collisions()
        elif self.state == GAME_OVER:
            if self.death_timer > 0:
                self.death_timer = max(0.0, self.death_timer - dt)
            # bird falls to the ground after death
            if self.bird.y + self.bird.radius < self.ground.top():
                self.bird.update(dt)
            self.flash = max(0.0, self.flash - dt * 2)
    def _check_scoring(self):
        for pipe in self.pipes.pipes:
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1
                self.sound.play("score")
    def _check_collisions(self):
        if self.bird.y + self.bird.radius >= self.ground.top():
            self.bird.y = self.ground.top() - self.bird.radius
            self._die()
            return
        for pipe in self.pipes.pipes:
            if self.bird.hits_rect(pipe.top_rect) or self.bird.hits_rect(pipe.bottom_rect):
                self._die()
                return
    def _die(self):
        self.state = GAME_OVER
        self.death_timer = 0.6
        self.flash = 1.0
        self.best = max(self.best, self.score)
        self.sound.play("hit")
    def _update_clouds(self, dt):
        for c in self.clouds:
            c["x"] -= c["speed"] * dt
            if c["x"] < -80 * c["scale"]:
                c["x"] = settings.WIDTH + 60
                c["y"] = random.uniform(40, settings.HEIGHT * 0.5)
    def _draw_clouds(self, surface):
        for c in self.clouds:
            s = c["scale"]
            x, y = int(c["x"]), int(c["y"])
            r = int(18 * s)
            pygame.draw.circle(surface, settings.CLOUD, (x, y), r)
            pygame.draw.circle(surface, settings.CLOUD, (x + r, y + 4), int(r * 0.75))
            pygame.draw.circle(surface, settings.CLOUD, (x - r, y + 6), int(r * 0.7))
            pygame.draw.circle(surface, settings.CLOUD, (x + r // 2, y - r // 2), int(r * 0.7))
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self._draw_clouds(self.screen)
        self.pipes.draw(self.screen)
        self.ground.draw(self.screen)
        self.bird.draw(self.screen)
        if self.state == READY:
            draw_text(self.screen, "Flappy Bird", 48, settings.WIDTH // 2, settings.HEIGHT // 3,
                      color=settings.WHITE, outline_color=settings.BLACK, outline_width=3)
            draw_text(self.screen, "Press SPACE / Click to Flap", 22, settings.WIDTH // 2, settings.HEIGHT // 2,
                      color=settings.WHITE, outline_color=settings.BLACK)
        else:
            draw_text(self.screen, str(self.score), 44, settings.WIDTH // 2, 60,
                      color=settings.WHITE, outline_color=settings.BLACK, outline_width=3)
        if self.state == GAME_OVER:
            draw_text(self.screen, "Game Over", 40, settings.WIDTH // 2, settings.HEIGHT // 3,
                      color=settings.RED, outline_color=settings.BLACK, outline_width=3)
            draw_text(self.screen, "Score: {}  Best: {}".format(self.score, self.best), 24,
                      settings.WIDTH // 2, settings.HEIGHT // 3 + 44,
                      color=settings.WHITE, outline_color=settings.BLACK)
            if self.death_timer <= 0:
                draw_text(self.screen, "Press SPACE to Restart", 20, settings.WIDTH // 2, settings.HEIGHT // 2,
                          color=settings.WHITE, outline_color=settings.BLACK)
        if self.flash > 0:
            flash_surf = pygame.Surface((settings.WIDTH, settings.HEIGHT))
            flash_surf.fill(settings.WHITE)
            flash_surf.set_alpha(int(self.flash * 128))
            self.screen.blit(flash_surf, (0, 0))
        pygame.display.flip()
    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            dt = min(dt, 0.033)
            self.handle_events()
            self.update(dt)
            self.draw()