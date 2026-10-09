import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 480, 640
GROUND_H = 80
PIPE_W = 70
GRAVITY = 0.45
FLAP_V = -8.5
MAX_FALL = 12
SKY = (113, 197, 240)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 36, bold=True)
SMALL = pygame.font.SysFont("arial", 20)


def difficulty(score):
    """Gradual difficulty: pipes speed up and gaps shrink as score grows."""
    speed = min(3.0 + score * 0.06, 6.5)
    gap = max(175 - score * 2.5, 115)
    return speed, gap


class Bird:
    def __init__(self):
        self.x = 110.0
        self.y = HEIGHT / 2
        self.vel = 0.0
        self.r = 14

    def flap(self):
        self.vel = FLAP_V

    def update(self):
        self.vel = min(self.vel + GRAVITY, MAX_FALL)
        self.y += self.vel
        if self.y - self.r < 0:  # soft ceiling; only pipes/ground end the run
            self.y = self.r
            self.vel = 0

    def rect(self):
        return pygame.Rect(int(self.x - self.r), int(self.y - self.r),
                           self.r * 2, self.r * 2)

    def draw(self, surf):
        x, y, r = int(self.x), int(self.y), self.r
        pygame.draw.circle(surf, (255, 221, 64), (x, y), r)
        pygame.draw.circle(surf, (40, 40, 40), (x + 6, y - 5), 3)
        pygame.draw.polygon(surf, (255, 140, 0),
                            [(x + r - 2, y), (x + r + 8, y + 3), (x + r - 2, y + 7)])
        pygame.draw.ellipse(surf, (250, 250, 250), (x - 10, y - 2, 14, 9))


class Pipe:
    def __init__(self, x, gap_y, gap_h, speed):
        self.x = float(x)
        self.gap_y = gap_y
        self.gap_h = gap_h
        self.speed = speed
        self.passed = False

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x + PIPE_W < -10

    def rects(self):
        ground_y = HEIGHT - GROUND_H
        top = pygame.Rect(int(self.x), 0, PIPE_W, self.gap_y)
        bottom = pygame.Rect(int(self.x), self.gap_y + self.gap_h, PIPE_W,
                             ground_y - (self.gap_y + self.gap_h))
        return top, bottom

    def draw(self, surf):
        top, bottom = self.rects()
        for r in (top, bottom):
            pygame.draw.rect(surf, (96, 200, 96), r)
            pygame.draw.rect(surf, (56, 150, 70), r, 4)
        for lip in ((top.x - 4, top.bottom - 22), (bottom.x - 4, bottom.top)):
            lr = pygame.Rect(lip[0], lip[1], PIPE_W + 8, 22)
            pygame.draw.rect(surf, (110, 205, 110), lr)
            pygame.draw.rect(surf, (56, 150, 70), lr, 3)


def draw_ground(surf):
    gy = HEIGHT - GROUND_H
    pygame.draw.rect(surf, (222, 184, 110), (0, gy, WIDTH, GROUND_H))
    pygame.draw.rect(surf, (110, 180, 80), (0, gy, WIDTH, 14))


def center_text(surf, text, font, color, y):
    s = font.render(text, True, color)
    surf.blit(s, (WIDTH // 2 - s.get_width() // 2, y))


def main():
    bird = Bird()
    pipes = []
    score = 0
    best = 0
    spawn_timer = 0
    state = "ready"  # ready | play | over

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                if state == "ready":
                    state = "play"
                    bird.flap()
                elif state == "play":
                    bird.flap()
                else:
                    bird, pipes, score, spawn_timer = Bird(), [], 0, 0
                    state = "ready"

        if state == "play":
            speed, gap = difficulty(score)
            bird.update()
            spawn_timer -= 1
            if spawn_timer <= 0:
                gap_h = max(gap + random.randint(-12, 12), 100)  # varied gap sizes
                margin = 60
                gap_y = random.randint(margin, HEIGHT - GROUND_H - gap_h - margin)
                pipes.append(Pipe(WIDTH + 10, gap_y, gap_h,
                                  speed + random.uniform(-0.25, 0.25)))
                spawn_timer = max(int(270 / speed), 40)  # constant pipe spacing
            for p in pipes:
                p.update()
            pipes = [p for p in pipes if not p.offscreen()]
            for p in pipes:
                if not p.passed and p.x + PIPE_W < bird.x - bird.r:
                    p.passed = True
                    score += 1
                    best = max(best, score)
            if bird.y + bird.r >= HEIGHT - GROUND_H:
                bird.y = HEIGHT - GROUND_H - bird.r
                state = "over"
            else:
                br = bird.rect()
                for p in pipes:
                    top, bottom = p.rects()
                    if br.colliderect(top) or br.colliderect(bottom):
                        state = "over"
                        break
        elif state == "over":
            if bird.y + bird.r < HEIGHT - GROUND_H:
                bird.vel = min(bird.vel + GRAVITY, MAX_FALL)
                bird.y += bird.vel
                if bird.y + bird.r >= HEIGHT - GROUND_H:
                    bird.y = HEIGHT - GROUND_H - bird.r

        screen.fill(SKY)
        for p in pipes:
            p.draw(screen)
        draw_ground(screen)
        bird.draw(screen)
        center_text(screen, str(score), FONT, (255, 255, 255), 24)
        if state == "ready":
            center_text(screen, "Press SPACE / UP to flap", SMALL,
                        (255, 255, 255), HEIGHT // 2 - 70)
            center_text(screen, "Avoid the pipes and the ground!", SMALL,
                        (255, 255, 255), HEIGHT // 2 - 40)
        elif state == "over":
            center_text(screen, "Game Over", FONT, (200, 40, 40), HEIGHT // 2 - 90)
            center_text(screen, "Score: %d   Best: %d" % (score, best), SMALL,
                        (255, 255, 255), HEIGHT // 2 - 40)
            center_text(screen, "Press SPACE to restart", SMALL,
                        (255, 255, 255), HEIGHT // 2 - 10)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()