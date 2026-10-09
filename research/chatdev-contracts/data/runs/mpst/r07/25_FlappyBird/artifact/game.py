"""
game.py
Core orchestration of the Flappy Bird clone: the main loop, the state
machine (menu / playing / game over), difficulty scaling, pipe spawning,
scoring, collision handling, high-score persistence and every piece of
background / HUD rendering.
"""
import json
import math
import random
import pygame
import settings
from bird import Bird
from ground import Ground
from pipe import Pipe
from sounds import create_sounds
# The three states of the game.
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
class Game:
    """Owns the window, all entities and the frame-by-frame game loop."""
    def __init__(self):
        # Mixer settings must be prepared before pygame.init() starts audio.
        pygame.mixer.pre_init(22050, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("arial", 52, bold=True)
        self.font_med = pygame.font.SysFont("arial", 30, bold=True)
        self.font_small = pygame.font.SysFont("arial", 22, bold=True)
        self.sounds = create_sounds()
        self.highscore = self._load_highscore()
        self.clouds = self._make_clouds()
        self.reset()
        self.state = MENU
    # ------------------------------------------------------- persistence
    def _load_highscore(self):
        """Read the persisted best score; 0 when missing or corrupt."""
        try:
            with open(settings.HIGHSCORE_FILE, "r") as fh:
                return int(json.load(fh).get("highscore", 0))
        except (OSError, ValueError, TypeError):
            return 0
    def _save_highscore(self):
        """Persist the best score; failures are silently ignored."""
        try:
            with open(settings.HIGHSCORE_FILE, "w") as fh:
                json.dump({"highscore": self.highscore}, fh)
        except OSError:
            pass
    # ----------------------------------------------------------- helpers
    def _make_clouds(self):
        """Create a handful of decorative clouds at random positions."""
        return [{"x": random.uniform(0, settings.SCREEN_WIDTH),
                 "y": random.uniform(40, 260),
                 "speed": random.uniform(0.1, 0.4),
                 "scale": random.uniform(0.7, 1.5)}
                for _ in range(6)]
    def _drift_clouds(self):
        """Move clouds leftwards, recycling them once they leave the screen."""
        for cloud in self.clouds:
            cloud["x"] -= cloud["speed"]
            if cloud["x"] < -140:
                cloud["x"] = settings.SCREEN_WIDTH + 140
                cloud["y"] = random.uniform(40, 260)
    def reset(self):
        """(Re)initialise everything needed for a fresh run."""
        self.bird = Bird(settings.BIRD_X, settings.SCREEN_HEIGHT // 2)
        self.pipes = []
        self.ground = Ground()
        self.score = 0
        self.frames_since_pipe = 0
        self.distance_since_spawn = 0.0
        self.flash_timer = 0
        self.menu_timer = 0
        self.menu_base_y = settings.SCREEN_HEIGHT // 2
        self.game_over_timer = 0
    def current_difficulty(self):
        """Return (pipe_speed, gap_height) scaled by the current score."""
        speed = min(settings.PIPE_SPEED_START
                    + self.score * settings.PIPE_SPEED_PER_POINT,
                    settings.PIPE_SPEED_MAX)
        gap = max(settings.PIPE_GAP_START
                  - self.score * settings.PIPE_GAP_PER_POINT,
                  settings.PIPE_GAP_MIN)
        return speed, gap
    def _spawn_pipe(self):
        """Add a new pipe pair just off the right edge with a random gap."""
        _speed, gap = self.current_difficulty()
        margin = settings.GAP_CENTER_MARGIN
        min_center = margin + gap / 2
        max_center = (settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
                      - margin - gap / 2)
        gap_center = random.uniform(min_center, max_center)
        self.pipes.append(Pipe(settings.SCREEN_WIDTH + settings.PIPE_CAP_OVERHANG,
                               gap_center, gap))
    def _game_over(self, grounded):
        """Switch to the game-over state, play sounds and store the score."""
        self.state = GAME_OVER
        self.flash_timer = 8
        self.game_over_timer = 45  # brief lockout so a held key cannot skip
        self.sounds.play("hit")
        if not grounded:
            self.sounds.play("swoosh")
        if self.score > self.highscore:
            self.highscore = self.score
            self._save_highscore()
    # ------------------------------------------------------------ events
    def handle_events(self):
        """Process the event queue; return False when the game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if self.state == MENU:
                        self.state = PLAYING
                        self.bird.flap()
                        self.sounds.play("flap")
                    elif self.state == PLAYING:
                        self.bird.flap()
                        self.sounds.play("flap")
                    elif self.state == GAME_OVER and self.game_over_timer <= 0:
                        self.reset()
                        self.state = MENU
        return True
    # ------------------------------------------------------------ update
    def update(self):
        """Advance the simulation by exactly one frame."""
        if self.state == PLAYING:
            speed, _gap = self.current_difficulty()
            self._drift_clouds()
            self.bird.update()
            self.ground.update(speed)
            self._update_pipes(speed)
            self._check_collisions()
        elif self.state == MENU:
            self.menu_timer += 1
            self._drift_clouds()
            self.bird.y = self.menu_base_y + math.sin(self.menu_timer * 0.08) * 8
            self.bird.anim_timer += 0.18  # gentle idle wing flapping
            self.ground.update(settings.PIPE_SPEED_START)
        else:  # GAME_OVER
            if self.flash_timer > 0:
                self.flash_timer -= 1
            if self.game_over_timer > 0:
                self.game_over_timer -= 1
            self._tumble_bird()
    def _update_pipes(self, speed):
        """Move pipes, spawn new ones and award points for passes."""
        if self.pipes:
            # Spawn by travelled distance so spacing stays constant at any speed.
            self.distance_since_spawn += speed
            if self.distance_since_spawn >= settings.PIPE_SPACING:
                self._spawn_pipe()
                self.distance_since_spawn = 0.0
        else:
            # Delay before the very first pipe appears.
            self.frames_since_pipe += 1
            if self.frames_since_pipe >= settings.FIRST_PIPE_DELAY:
                self._spawn_pipe()
                self.frames_since_pipe = 0
        for pipe in self.pipes:
            pipe.update(speed)
            if pipe.has_passed(self.bird.x):
                pipe.mark_passed()
                self.score += 1
                self.sounds.play("score")
        self.pipes = [p for p in self.pipes if not p.is_offscreen()]
    def _check_collisions(self):
        """End the run when the bird touches a pipe or the ground."""
        rect = self.bird.get_collision_rect()
        if self.bird.hits_ground() or self.ground.collide(rect):
            self._game_over(grounded=True)
            return
        for pipe in self.pipes:
            if pipe.collides(rect):
                self._game_over(grounded=False)
                return
    def _tumble_bird(self):
        """Let the dead bird fall and rotate nose-down until it lands."""
        ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT - 10
        if self.bird.y < ground_y:
            self.bird.velocity = min(self.bird.velocity + settings.GRAVITY,
                                     settings.MAX_FALL_SPEED)
            self.bird.y += self.bird.velocity
            self.bird.rotation = max(-90.0, self.bird.rotation - 6.0)
        else:
            self.bird.y = ground_y
    # ------------------------------------------------------------- draw
    def draw(self):
        """Render one full frame: sky, clouds, pipes, ground, bird, HUD."""
        self._draw_background()
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.ground.draw(self.screen)
        self.bird.draw(self.screen)
        self._draw_hud()
        if self.flash_timer > 0:
            flash = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            flash.set_alpha(120)
            flash.fill((255, 255, 255))
            self.screen.blit(flash, (0, 0))
        pygame.display.flip()
    def _draw_background(self):
        """Vertical sky gradient plus drifting clouds."""
        sky_height = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        steps = 30
        top, bottom = settings.SKY_TOP, settings.SKY_BOTTOM
        for i in range(steps):
            t = i / (steps - 1)
            colour = (int(top[0] + (bottom[0] - top[0]) * t),
                      int(top[1] + (bottom[1] - top[1]) * t),
                      int(top[2] + (bottom[2] - top[2]) * t))
            pygame.draw.rect(self.screen, colour,
                             (0, sky_height * i // steps,
                              settings.SCREEN_WIDTH,
                              sky_height // steps + 1))
        for cloud in self.clouds:
            self._draw_cloud(cloud["x"], cloud["y"], cloud["scale"])
    def _draw_cloud(self, x, y, scale):
        """A fluffy cloud built from overlapping circles."""
        r = int(20 * scale)
        puffs = ((0, 0, 1.0), (r, -r * 0.35, 0.75), (-r, -r * 0.25, 0.7),
                 (r * 1.7, r * 0.15, 0.55), (-r * 1.6, r * 0.2, 0.5))
        for dx, dy, factor in puffs:
            pygame.draw.circle(self.screen, settings.CLOUD,
                               (int(x + dx), int(y + dy)), int(r * factor))
    def _draw_text(self, text, font, colour, center, outlined=True):
        """Blit centred text, optionally with a hard outline for readability."""
        surface = font.render(text, True, colour)
        if outlined:
            border = font.render(text, True, settings.TEXT_OUTLINE)
            for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                self.screen.blit(border, (center[0] - border.get_width() // 2 + dx,
                                          center[1] - border.get_height() // 2 + dy))
        self.screen.blit(surface, (center[0] - surface.get_width() // 2,
                                   center[1] - surface.get_height() // 2))
    def _draw_panel(self, rect):
        """Rounded panel used by the game-over dialog."""
        pygame.draw.rect(self.screen, settings.PANEL, rect, border_radius=14)
        pygame.draw.rect(self.screen, settings.PANEL_OUTLINE, rect,
                         3, border_radius=14)
    def _draw_hud(self):
        """State-dependent heads-up display."""
        if self.state == PLAYING:
            self._draw_text(str(self.score), self.font_big,
                            settings.TEXT_WHITE,
                            (settings.SCREEN_WIDTH // 2, 70))
        elif self.state == MENU:
            self._draw_text(settings.TITLE, self.font_big, settings.TEXT_GOLD,
                            (settings.SCREEN_WIDTH // 2, 150))
            self._draw_text("Press SPACE or UP to flap", self.font_med,
                            settings.TEXT_WHITE,
                            (settings.SCREEN_WIDTH // 2, 250))
            self._draw_text("Slip through the pipe gaps!", self.font_small,
                            settings.TEXT_WHITE,
                            (settings.SCREEN_WIDTH // 2, 300))
            self._draw_text(f"Best: {self.highscore}", self.font_med,
                            settings.TEXT_GOLD,
                            (settings.SCREEN_WIDTH // 2, 380))
            self._draw_text("ESC to quit", self.font_small, settings.TEXT_WHITE,
                            (settings.SCREEN_WIDTH // 2,
                             settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT - 30))
        else:  # GAME_OVER
            panel = pygame.Rect(0, 0, 320, 190)
            panel.center = (settings.SCREEN_WIDTH // 2,
                            settings.SCREEN_HEIGHT // 2 - 40)
            self._draw_panel(panel)
            self._draw_text("GAME OVER", self.font_med, settings.TEXT_RED,
                            (panel.centerx, panel.top + 35))
            self._draw_text(f"Score: {self.score}", self.font_med,
                            settings.TEXT_OUTLINE,
                            (panel.centerx, panel.top + 85), outlined=False)
            self._draw_text(f"Best: {self.highscore}", self.font_med,
                            settings.TEXT_OUTLINE,
                            (panel.centerx, panel.top + 125), outlined=False)
            self._draw_text("Press SPACE for menu", self.font_small,
                            settings.TEXT_WHITE,
                            (panel.centerx, panel.bottom + 30))
    # -------------------------------------------------------------- loop
    def run(self):
        """The main loop: events, update, draw, tick."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)
        pygame.quit()