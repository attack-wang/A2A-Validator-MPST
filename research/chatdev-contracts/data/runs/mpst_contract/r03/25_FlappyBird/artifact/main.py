import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 480, 640
FPS = 60
GROUND_Y = HEIGHT - 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("arial", 48, bold=True)
font_small = pygame.font.SysFont("arial", 24)

WHITE = (255, 255, 255)
SKY = (113, 197, 207)
GREEN = (111, 196, 69)
DARK = (55, 120, 40)
YELLOW = (255, 204, 0)
ORANGE = (255, 140, 0)
BROWN = (120, 80, 40)

GRAVITY = 0.5
FLAP = -9
PIPE_W = 70
PIPE_SPACING = 220
BASE_SPEED = 3.0
MAX_SPEED = 6.0
BASE_GAP = 170
MIN_GAP = 110
MARGIN = 60


class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.vel = 0
        self.r = 15

    def flap(self):
        self.vel = FLAP

    def update(self):
        self.vel = min(self.vel + GRAVITY, 12)
        self.y += self.vel

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def draw(self, surf):
        pygame.draw.circle(surf, YELLOW, (int(self.x), int(self.y)), self.r)
        pygame.draw.circle(surf, (0, 0, 0), (int(self.x) + 6, int(self.y) - 5), 3)
        pygame.draw.circle(surf, ORANGE, (int(self.x) + 9, int(self.y) + 1), 5)


class Pipe:
    def __init__(self, x, gap_center, gap):
        self.x = x
        self.gap_center = gap_center
        self.gap = gap
        self.passed = False

    def update(self, speed):
        self.x -= speed

    def rects(self):
        top_h = self.gap_center - self.gap / 2
        bot_y = self.gap_center + self.gap / 2
        top = pygame.Rect(int(self.x), 0, PIPE_W, int(top_h))
        bot = pygame.Rect(int(self.x), int(bot_y), PIPE_W, GROUND_Y - int(bot_y))
        return top, bot

    def offscreen(self):
        return self.x + PIPE_W < 0


def difficulty(score):
    speed = min(BASE_SPEED + score * 0.05, MAX_SPEED)
    gap = max(BASE_GAP - score * 1.5, MIN_GAP)
    return speed, gap


def spawn_pipe(x, gap):
    half = int(gap / 2)
    center = random.randint(MARGIN + half, GROUND_Y - MARGIN - half)
    return Pipe(x, center, gap)


def draw_ground(surf, offset):
    pygame.draw.rect(surf, BROWN, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    pygame.draw.rect(surf, GREEN, (0, GROUND_Y, WIDTH, 10))
    for i in range(-1, WIDTH // 40 + 2):
        x = i * 40 - offset % 40
        pygame.draw.rect(surf, DARK, (x, GROUND_Y, 20, 10))


def reset():
    bird = Bird()
    gap = difficulty(0)[1]
    pipes = [spawn_pipe(WIDTH + 100, gap)]
    return bird, pipes, 0, difficulty(0)[0], gap, 0


def main():
    bird, pipes, score, speed, gap, ground_off = reset()
    alive = True
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP) and alive:
                    bird.flap()
                elif event.key == pygame.K_r and not alive:
                    bird, pipes, score, speed, gap, ground_off = reset()
                    alive = True
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if alive:
            speed, gap = difficulty(score)
            bird.update()
            ground_off = (ground_off + speed) % 40
            for p in pipes:
                p.update(speed)
            if pipes[-1].x < WIDTH - PIPE_SPACING:
                pipes.append(spawn_pipe(WIDTH, gap))
            if pipes[0].offscreen():
                pipes.pop(0)
            for p in pipes:
                if not p.passed and p.x + PIPE_W < bird.x - bird.r:
                    p.passed = True
                    score += 1
            if bird.y - bird.r <= 0:
                bird.y = bird.r
                bird.vel = 0
            if bird.y + bird.r >= GROUND_Y:
                alive = False
            for p in pipes:
                top, bot = p.rects()
                if bird.rect().colliderect(top) or bird.rect().colliderect(bot):
                    alive = False

        screen.fill(SKY)
        for p in pipes:
            top, bot = p.rects()
            pygame.draw.rect(screen, GREEN, top)
            pygame.draw.rect(screen, GREEN, bot)
            pygame.draw.rect(screen, DARK, top, 3)
            pygame.draw.rect(screen, DARK, bot, 3)
        draw_ground(screen, ground_off)
        bird.draw(screen)
        score_surf = font_big.render(str(score), True, WHITE)
        screen.blit(score_surf, (WIDTH // 2 - score_surf.get_width() // 2, 20))
        if not alive:
            go = font_big.render("Game Over", True, (200, 40, 40))
            screen.blit(go, (WIDTH // 2 - go.get_width() // 2, HEIGHT // 2 - 60))
            hint = font_small.render("Score: {}  -  Press R to restart".format(score), True, WHITE)
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()