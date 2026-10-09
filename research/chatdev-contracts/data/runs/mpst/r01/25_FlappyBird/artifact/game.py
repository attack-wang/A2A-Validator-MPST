"""Core game logic: state machine, spawning, scoring, collisions, rendering."""
import math
import random
import pygame
import settings
from bird import Bird
from pipe import Pipe
from background import Background
class Game:
    """Coordinates the Flappy Bird game loop and all subsystems."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("arial", 48, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 28, bold=True)
        self.font_small = pygame.font.SysFont("arial", 20)
        self.bird = Bird(settings.BIRD_START_X, settings.BIRD_START_Y)
        self.background = Background()
        self.pipes = []
        self.state = "ready"  # ready | playing | game_over
        self.score = 0
        self.best_score = self._load_best_score()
        self.death_flash = 0.0
        self.shake = 0.0
        self.bob_timer = 0.0
    # --- difficulty -------------------------------------------------
    def current_gap_size(self):
        """Gap size shrinks with score, plus random variation; never below MIN_GAP_SIZE."""
        base = settings.BASE_GAP_SIZE - self.score * settings.GAP_SHRINK_PER_POINT
        gap = base + random.uniform(-settings.GAP_RANDOM_VARIATION, settings.GAP_RANDOM_VARIATION)
        return max(settings.MIN_GAP_SIZE, gap)
    def current_pipe_speed(self):
        """Pipe speed grows with score, capped at the maximum."""
        return min(settings.MAX_PIPE_SPEED,
                   settings.BASE_PIPE_SPEED + self.score * settings.SPEED_INCREASE_PER_POINT)
    # --- pipes ------------------------------------------------------
    def spawn_pipe(self):
        """Create a new pipe at the right edge with a randomized gap."""
        margin = 60
        playable_top = margin
        playable_bottom = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT - margin
        gap_size = self.current_gap_size()
        half = gap_size / 2
        gap_center = random.uniform(playable_top + half, playable_bottom - half)
        pipe = Pipe(settings.SCREEN_WIDTH + settings.PIPE_CAP_OVERHANG,
                    gap_center, gap_size, self.current_pipe_speed())
        self.pipes.append(pipe)
    def _should_spawn(self):
        """Spawn when the rightmost pipe is far enough away."""
        if not self.pipes:
            return True
        rightmost = max(p.x for p in self.pipes)
        return settings.SCREEN_WIDTH - rightmost >= settings.PIPE_SPACING
    # --- collisions -------------------------------------------------
    def check_collisions(self):
        """Return True if the bird hits a pipe or the ground."""
        hitbox = self.bird.get_hitbox()
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        if hitbox.bottom >= ground_top:
            return True
        return any(pipe.collides_with(hitbox) for pipe in self.pipes)
    # --- persistence ------------------------------------------------
    def _load_best_score(self):
        """Read the best score from disk; return 0 if unavailable."""
        try:
            with open(settings.BEST_SCORE_FILE, "r") as f:
                return int(f.read().strip() or 0)
        except (OSError, ValueError):
            return 0
    def _save_best_score(self):
        """Persist the best score when it has been beaten."""
        if self.score > self.best_score:
            self.best_score = self.score
            try:
                with open(settings.BEST_SCORE_FILE, "w") as f:
                    f.write(str(self.best_score))
            except OSError:
                pass
    # --- main loop --------------------------------------------------
    def run(self):
        """Run the game until the window is closed."""
        running = True
        while running:
            dt = min(self.clock.tick(settings.FPS) / 1000.0, 1.0 / 30.0)
            running = self._handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
    def _handle_events(self):
        """Process input; return False when the game should exit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if self.state == "ready":
                        self.state = "playing"
                        self.bird.flap()
                    elif self.state == "playing":
                        self.bird.flap()
                    else:
                        self.reset()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    # --- update -----------------------------------------------------
    def update(self, dt):
        """Advance the simulation one frame."""
        ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        if self.state == "playing":
            self.bird.update(dt)
            for pipe in self.pipes:
                pipe.update(dt)
                if pipe.check_score(self.bird.x):
                    self.score += 1
            self.pipes = [p for p in self.pipes if not p.is_offscreen()]
            if self._should_spawn():
                self.spawn_pipe()
            if self.check_collisions():
                self.state = "game_over"
                self.shake = 0.4
                self.death_flash = 0.6
                self._save_best_score()
        elif self.state == "ready":
            # gentle hover animation before the game starts
            self.bob_timer += dt
            self.bird.y = self.bird.start_y + math.sin(self.bob_timer * 3.0) * 8.0
        else:  # game_over: let the bird tumble down to the ground
            floor = ground_top - settings.BIRD_HEIGHT / 2
            if self.bird.y < floor:
                self.bird.update(dt)
                if self.bird.y > floor:
                    self.bird.y = floor
                    self.bird.velocity = 0.0
        self.shake = max(0.0, self.shake - dt)
        self.death_flash = max(0.0, self.death_flash - dt)
        world_speed = self.current_pipe_speed() if self.state == "playing" else settings.BASE_PIPE_SPEED
        self.background.update(dt, world_speed)
    # --- rendering --------------------------------------------------
    def _shake_offset(self):
        """Random blit offset while the death shake is active."""
        if self.shake > 0:
            magnitude = int(self.shake * 12)
            return (random.randint(-magnitude, magnitude),
                    random.randint(-magnitude, magnitude))
        return (0, 0)
    def draw(self):
        """Render the full frame and flip it to the display."""
        scene = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.background.draw(scene)
        for pipe in self.pipes:
            pipe.draw(scene)
        self.bird.draw(scene)
        self._draw_hud()
        if self.state == "ready":
            self._draw_ready_prompt()
        elif self.state == "game_over":
            self._draw_game_over()
        offset = self._shake_offset()
        self.screen.fill(settings.BLACK)
        self.screen.blit(scene, offset)
        if self.death_flash > 0:
            alpha = int(180 * (self.death_flash / 0.6))
            flash = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
            flash.fill((255, 255, 255, alpha))
            self.screen.blit(flash, (0, 0))
        pygame.display.flip()
    def _draw_hud(self):
        """Draw the outlined score at the top of the screen."""
        score_text = self.font_large.render(str(self.score), True, settings.WHITE)
        outline = self.font_large.render(str(self.score), True, settings.BLACK)
        pos = score_text.get_rect(center=(settings.SCREEN_WIDTH // 2, 70))
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            self.screen.blit(outline, pos.move(dx, dy))
        self.screen.blit(score_text, pos)
    def _draw_ready_prompt(self):
        """Show the start hint on the ready screen."""
        text = self.font_medium.render("Press SPACE to flap", True, settings.WHITE)
        outline = self.font_medium.render("Press SPACE to flap", True, settings.BLACK)
        pos = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 90))
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            self.screen.blit(outline, pos.move(dx, dy))
        self.screen.blit(text, pos)
    def _draw_game_over(self):
        """Show the game-over panel with score, best, and restart hint."""
        panel = pygame.Rect(0, 0, 320, 190)
        panel.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 40)
        pygame.draw.rect(self.screen, settings.WHITE, panel, border_radius=12)
        pygame.draw.rect(self.screen, settings.BLACK, panel, 3, border_radius=12)
        title = self.font_medium.render("GAME OVER", True, settings.RED)
        self.screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 38)))
        score_text = self.font_medium.render(f"Score: {self.score}", True, settings.BLACK)
        self.screen.blit(score_text, score_text.get_rect(center=(panel.centerx, panel.y + 84)))
        best_text = self.font_small.render(f"Best: {self.best_score}", True, settings.BLACK)
        self.screen.blit(best_text, best_text.get_rect(center=(panel.centerx, panel.y + 118)))
        hint = self.font_small.render("Press SPACE to restart", True, settings.BLACK)
        self.screen.blit(hint, hint.get_rect(center=(panel.centerx, panel.y + 152)))
    # --- reset ------------------------------------------------------
    def reset(self):
        """Return the game to its initial ready state."""
        self.bird.reset()
        self.pipes = []
        self.score = 0
        self.state = "ready"
        self.bob_timer = 0.0
        self.shake = 0.0
        self.death_flash = 0.0