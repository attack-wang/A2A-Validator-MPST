import pygame
import random
import sys

WIDTH, HEIGHT = 400, 600
GROUND_Y = HEIGHT - 60
GRAVITY = 0.45
FLAP = -8.5
PIPE_W = 60

SKY = (113, 197, 207)
GREEN = (76, 175, 80)
DARK = (55, 120, 55)
SAND = (222, 216, 149)
YELLOW = (255, 200, 40)
ORANGE = (230, 126, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 60, 60)


class Bird:
    def __init__(self):
        self.x = 90
        self.y = HEIGHT // 2
        self.vel = 0
        self.r = 14

    def flap(self):
        self.vel = FLAP

    def update(self):
        self.vel = min(self.vel + GRAVITY, 12)
        self.y += self.vel

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)


class Pipe:
    def __init__(self, gap_h):
        self.x = WIDTH + 40
        self.gap_h = gap_h
        self.gap_y = random.randint(80, GROUND_Y - 80 - gap_h)
        self.passed = False

    def rects(self):
        top = pygame.Rect(self.x, 0, PIPE_W, self.gap_y)
        bottom = pygame.Rect(self.x, self.gap_y + self.gap_h, PIPE_W,
                             GROUND_Y - (self.gap_y + self.gap_h))
        return top, bottom


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 32, bold=True)
        self.small = pygame.font.SysFont("arial", 20)
        self.reset()

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.speed = 3.0
        self.gap_h = 170
        self.spawn_timer = 0
        self.spawn_interval = 90
        self.over = False
        self.started = False

    def adjust_difficulty(self):
        self.speed = min(3.0 + self.score * 0.06, 7.0)
        self.gap_h = max(170 - self.score * 2.5, 110)
        self.spawn_interval = max(90 - self.score, 55)

    def spawn_pipe(self):
        jitter = random.randint(-15, 15)
        self.pipes.append(Pipe(max(100, self.gap_h + jitter)))

    def update(self):
        if not self.started:
            return
        self.adjust_difficulty()
        self.bird.update()
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_pipe()
        for p in self.pipes:
            p.x -= self.speed
            if not p.passed and p.x + PIPE_W < self.bird.x - self.bird.r:
                p.passed = True
                self.score += 1
        self.pipes = [p for p in self.pipes if p.x + PIPE_W > 0]
        if self.bird.y + self.bird.r >= GROUND_Y:
            self.bird.y = GROUND_Y - self.bird.r
            self.over = True
        if self.bird.y - self.bird.r < 0:
            self.bird.y = self.bird.r
            self.bird.vel = 0
        for p in self.pipes:
            top, bottom = p.rects()
            if self.bird.rect().colliderect(top) or self.bird.rect().colliderect(bottom):
                self.over = True
                break

    def draw(self):
        self.screen.fill(SKY)
        pygame.draw.rect(self.screen, SAND, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        for p in self.pipes:
            top, bottom = p.rects()
            pygame.draw.rect(self.screen, GREEN, top)
            pygame.draw.rect(self.screen, GREEN, bottom)
            pygame.draw.rect(self.screen, DARK, top, 3)
            pygame.draw.rect(self.screen, DARK, bottom, 3)
        b = self.bird
        pygame.draw.circle(self.screen, YELLOW, (b.x, int(b.y)), b.r)
        pygame.draw.circle(self.screen, ORANGE, (b.x + 10, int(b.y)), 4)
        pygame.draw.circle(self.screen, BLACK, (b.x + 5, int(b.y) - 4), 2)
        s = self.font.render(str(self.score), True, WHITE)
        self.screen.blit(s, (WIDTH // 2 - s.get_width() // 2, 20))
        if not self.started:
            m = self.small.render("Press SPACE to flap and start", True, BLACK)
            self.screen.blit(m, (WIDTH // 2 - m.get_width() // 2, HEIGHT // 2 - 60))
        if self.over:
            go = self.font.render("Game Over!", True, RED)
            rs = self.small.render("Press R to restart, ESC to quit", True, BLACK)
            self.screen.blit(go, (WIDTH // 2 - go.get_width() // 2, HEIGHT // 2 - 50))
            self.screen.blit(rs, (WIDTH // 2 - rs.get_width() // 2, HEIGHT // 2 - 10))
        pygame.display.flip()

    def run(self, clock):
        while True:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_SPACE, pygame.K_UP) and not self.over:
                        self.started = True
                        self.bird.flap()
                    elif e.key == pygame.K_r and self.over:
                        self.reset()
                    elif e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            if not self.over:
                self.update()
            self.draw()