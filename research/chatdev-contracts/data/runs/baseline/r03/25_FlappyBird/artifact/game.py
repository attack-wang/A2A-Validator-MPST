"""Game loop, states, scoring, difficulty ramp and rendering for Flappy Bird."""
import math
import random
import sys
import pygame
import settings
from bird import Bird
from pipe import Pipe
class Game:
    """Owns the game loop, game states, scoring, difficulty and rendering."""
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("arial", settings.FONT_LARGE, bold=True)
        self.font_medium = pygame.font.SysFont("arial", settings.FONT_MEDIUM, bold=True)
        self.font_small = pygame.font.SysFont("arial", settings.FONT_SMALL)
        self.clouds = [
            (random.randint(0, settings.SCREEN_WIDTH), random.randint(40, 220), random.randint(18, 30))
            for _ in range(5)
        ]
        self.high_score = 0
        self.state = self.MENU
        self.frames = 0
        self.scroll_x = 0.0
        self.reset()
    def reset(self):
        """Reset the round: fresh bird, no pipes, base difficulty."""
        self.bird = Bird(settings.BIRD_X, settings.SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.speed = settings.BASE_PIPE_SPEED
        self.distance_since_spawn = 0.0
        self.flash_timer = 0
        self.new_best = False
    # ----- difficulty -----
    def difficulty_progress(self):
        """0..1 ramp based on the current score."""
        return min(self.score / settings.DIFFICULTY_RAMP_SCORE, 1.0)
    def current_gap_size(self):
        """Gap shrinks with progress, plus random jitter."""
        progress = self.difficulty_progress()
        base = settings.BASE_GAP_SIZE - progress * (settings.BASE_GAP_SIZE - settings.MIN_GAP_SIZE)
        return random.uniform(base - settings.GAP_VARIANCE, base + settings.GAP_VARIANCE)
    def current_speed(self):
        """Scroll speed grows with progress."""
        progress = self.difficulty_progress()
        return settings.BASE_PIPE_SPEED + progress * (settings.MAX_PIPE_SPEED - settings.BASE_PIPE_SPEED)
    # ----- round flow -----
    def spawn_pipe(self):
        """Create a pipe pair just off the right edge with a random gap."""
        gap_size = self.current_gap_size()
        ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        min_center = settings.PIPE_MARGIN + gap_size / 2
        max_center = ground_y - settings.PIPE_MARGIN - gap_size / 2
        gap_center = random.uniform(min_center, max_center)
        self.pipes.append(Pipe(settings.SCREEN_WIDTH + settings.PIPE_WIDTH,
                               gap_center, gap_size, self.speed))
    def game_over(self):
        """Switch to GAME_OVER once, record the high score and flash."""
        if self.state != self.PLAYING:
            return
        self.state = self.GAME_OVER
        self.flash_timer = 20
        if self.score > self.high_score:
            self.high_score = self.score
            self.new_best = True
    # ----- per-frame logic -----
    def update(self):
        """Advance the current state by one frame."""
        for i, (cx, cy, r) in enumerate(self.clouds):
            cx -= 0.3
            if cx + r < 0:
                cx = settings.SCREEN_WIDTH + r
                cy = random.randint(40, 220)
            self.clouds[i] = (cx, cy, r)
        if self.state == self.MENU:
            self.bird.y = self.bird.start_y + math.sin(self.frames * 0.08) * 8
            self.bird.rotation = 0
        elif self.state == self.PLAYING:
            self.speed = self.current_speed()
            self.scroll_x += self.speed
            self.bird.update()
            self.distance_since_spawn += self.speed
            if self.distance_since_spawn >= settings.PIPE_SPAWN_DISTANCE:
                self.distance_since_spawn = 0.0
                self.spawn_pipe()
            bird_rect = self.bird.get_rect()
            for pipe in self.pipes:
                pipe.update()
                if pipe.collides(bird_rect):
                    self.game_over()
                elif pipe.has_passed(settings.BIRD_X):
                    self.score += 1
            self.pipes = [p for p in self.pipes if not p.offscreen()]
            ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
            if self.bird.y + self.bird.radius >= ground_y:
                self.bird.y = ground_y - self.bird.radius
                self.game_over()
            elif self.bird.y - self.bird.radius < 0:
                self.bird.y = self.bird.radius
                self.bird.velocity = 0.0
        elif self.state == self.GAME_OVER:
            ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
            if self.bird.y + self.bird.radius < ground_y:
                self.bird.velocity = min(self.bird.velocity + self.bird.gravity, settings.MAX_FALL_SPEED)
                self.bird.y += self.bird.velocity
                if self.bird.y + self.bird.radius > ground_y:
                    self.bird.y = ground_y - self.bird.radius
            if self.flash_timer > 0:
                self.flash_timer -= 1
        self.frames += 1
    # ----- input -----
    def handle_events(self):
        """Process quit/flap/restart input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if self.state == self.MENU:
                        self.reset()
                        self.state = self.PLAYING
                        self.bird.flap()
                    elif self.state == self.PLAYING:
                        self.bird.flap()
                    elif self.state == self.GAME_OVER and self.flash_timer <= 0:
                        self.reset()
                        self.state = self.PLAYING
                        self.bird.flap()
                elif event.key == pygame.K_ESCAPE and self.state == self.GAME_OVER:
                    self.state = self.MENU
                    self.reset()
    # ----- rendering -----
    def draw(self):
        """Render background, pipes, ground, bird and HUD."""
        self.screen.fill(settings.SKY_BLUE)
        for cx, cy, r in self.clouds:
            pygame.draw.circle(self.screen, settings.CLOUD_COLOR, (int(cx), int(cy)), r)
            pygame.draw.circle(self.screen, settings.CLOUD_COLOR,
                               (int(cx) + r, int(cy) + 3), int(r * 0.7))
        for pipe in self.pipes:
            pipe.draw(self.screen)
        ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        pygame.draw.rect(self.screen, settings.GROUND_COLOR,
                         (0, ground_y, settings.SCREEN_WIDTH, settings.GROUND_HEIGHT))
        offset = int(self.scroll_x) % 24
        for x in range(-24, settings.SCREEN_WIDTH + 24, 24):
            pygame.draw.rect(self.screen, settings.GROUND_DARK, (x - offset, ground_y, 12, 12))
        self.bird.draw(self.screen)
        self.draw_hud()
        if self.state == self.GAME_OVER and self.flash_timer > 18:
            overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            overlay.fill(settings.WHITE)
            overlay.set_alpha(150)
            self.screen.blit(overlay, (0, 0))
    def draw_hud(self):
        """Score / menu / game-over text."""
        if self.state == self.PLAYING:
            score_surf = self.font_large.render(str(self.score), True, settings.WHITE)
            outline = self.font_large.render(str(self.score), True, settings.BLACK)
            rect = score_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, 50))
            for off in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                self.screen.blit(outline, rect.move(off))
            self.screen.blit(score_surf, rect)
        elif self.state == self.MENU:
            title = self.font_large.render("Flappy Bird", True, settings.WHITE)
            trect = title.get_rect(center=(settings.SCREEN_WIDTH // 2, 180))
            self.screen.blit(title, trect)
            prompt = self.font_small.render("Press SPACE / UP to flap", True, settings.BLACK)
            prect = prompt.get_rect(center=(settings.SCREEN_WIDTH // 2, 380))
            self.screen.blit(prompt, prect)
        elif self.state == self.GAME_OVER:
            over = self.font_large.render("Game Over", True, settings.RED)
            orect = over.get_rect(center=(settings.SCREEN_WIDTH // 2, 200))
            self.screen.blit(over, orect)
            score_text = self.font_medium.render(f"Score: {self.score}", True, settings.BLACK)
            srect = score_text.get_rect(center=(settings.SCREEN_WIDTH // 2, 260))
            self.screen.blit(score_text, srect)
            best_text = self.font_medium.render(f"Best: {self.high_score}", True, settings.BLACK)
            brect = best_text.get_rect(center=(settings.SCREEN_WIDTH // 2, 300))
            self.screen.blit(best_text, brect)
            if self.new_best:
                best_label = self.font_small.render("NEW BEST!", True, settings.ORANGE)
                blrect = best_label.get_rect(center=(settings.SCREEN_WIDTH // 2, 335))
                self.screen.blit(best_label, blrect)
            retry = self.font_small.render("Press SPACE to retry - ESC for menu", True, settings.BLACK)
            rrect = retry.get_rect(center=(settings.SCREEN_WIDTH // 2, 380))
            self.screen.blit(retry, rrect)
    # ----- main loop -----
    def run(self):
        """Main game loop: events, update, render at fixed FPS."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(settings.FPS)