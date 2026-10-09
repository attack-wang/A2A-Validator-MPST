import random
import sys

try:
    import pygame
except ImportError:
    sys.exit("pygame is required. Install it with: pip install pygame")

pygame.init()

W, H = 480, 640
FPS = 60
GRAVITY = 0.45
FLAP_VEL = -8.5
MAX_FALL = 12
PIPE_W = 70
PIPE_SPACING = 240
GROUND_H = 80
SKY = (113, 197, 207)
GROUND_C = (222, 184, 135)
PIPE_C = (111, 196, 69)
PIPE_EDGE = (60, 140, 40)
PIPE_LIP = (86, 170, 50)
BIRD_C = (255, 204, 0)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Bird - ChatDev")
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("arial", 48, bold=True)
font = pygame.font.SysFont("arial", 26, bold=True)


def difficulty(score):
    """Difficulty ramps up: pipe speed rises and gap shrinks with score."""
    speed = min(3.0 + score * 0.06, 7.5)
    gap = max(175 - score * 2, 115)
    return speed, gap


class Bird:
    def __init__(self):
        self.x = 110.0
        self.y = float(H // 2 - 60)
        self.vel = 0.0
        self.r = 14

    def flap(self):
        self.vel = FLAP_VEL

    def update(self):
        self.vel = min(self.vel + GRAVITY, MAX_FALL)
        self.y += self.vel
        if self.y < self.r:
            self.y = self.r
            self.vel = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.r), int(self.y - self.r),
                           self.r * 2, self.r * 2)

    def draw(self, surf):
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(surf, BIRD_C, (x, y), self.r)
        pygame.draw.circle(surf, (255, 255, 255), (x + 5, y - 4), 4)
        pygame.draw.circle(surf, (0, 0, 0), (x + 6, y - 4), 2)
        pygame.draw.polygon(surf, (255, 120, 0),
                            [(x + self.r - 2, y),
                             (x + self.r + 8, y + 2),
                             (x + self.r - 2, y + 5)])
        pygame.draw.ellipse(surf, (255, 255, 255), (x - 11, y + 2, 14, 8))


class Pipe:
    def __init__(self, x, gap_center, gap_size):
        self.x = float(x)
        self.w = PIPE_W
        self.gap_center = gap_center
        self.gap_size = gap_size
        self.passed = False

    def update(self, speed):
        self.x -= speed

    def offscreen(self):
        return self.x + self.w < -20

    def rects(self):
        top_h = int(self.gap_center - self.gap_size // 2)
        bot_y = int(self.gap_center + self.gap_size // 2)
        top = pygame.Rect(int(self.x), 0, self.w, top_h)
        bottom = pygame.Rect(int(self.x), bot_y, self.w, H - GROUND_H - bot_y)
        return top, bottom

    def draw(self, surf):
        top, bottom = self.rects()
        for r in (top, bottom):
            pygame.draw.rect(surf, PIPE_C, r)
            pygame.draw.rect(surf, PIPE_EDGE, r, 3)
        pygame.draw.rect(surf, PIPE_LIP, (top.x - 4, top.bottom - 22, top.w + 8, 22))
        pygame.draw.rect(surf, PIPE_EDGE, (top.x - 4, top.bottom - 22, top.w + 8, 22), 3)
        pygame.draw.rect(surf, PIPE_LIP, (bottom.x - 4, bottom.y, bottom.w + 8, 22))
        pygame.draw.rect(surf, PIPE_EDGE, (bottom.x - 4, bottom.y, bottom.w + 8, 22), 3)


class Game:
    def __init__(self):
        self.best = 0
        self.reset()

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.speed, self.gap = difficulty(0)
        self.spawn_timer = 0
        self.spawn_pipe()
        self.state = "play"

    def spawn_pipe(self):
        margin = 60
        lo = margin + self.gap // 2
        hi = H - GROUND_H - margin - self.gap // 2
        center = random.randint(int(lo), int(hi))
        gap_size = int(self.gap + random.randint(-12, 12))
        self.pipes.append(Pipe(W + 40, center, gap_size))

    def flap(self):
        if self.state == "play":
            self.bird.flap()

    def game_over(self):
        self.best = max(self.best, self.score)
        self.state = "over"

    def update(self):
        if self.state != "play":
            return
        self.speed, self.gap = difficulty(self.score)
        self.bird.update()
        self.spawn_timer += 1
        if self.spawn_timer >= PIPE_SPACING / self.speed:
            self.spawn_timer = 0
            self.spawn_pipe()
        for p in self.pipes:
            p.update(self.speed)
            if not p.passed and p.x + p.w < self.bird.x - self.bird.r:
                p.passed = True
                self.score += 1
        self.pipes = [p for p in self.pipes if not p.offscreen()]
        if self.bird.y + self.bird.r >= H - GROUND_H:
            self.game_over()
            return
        bird_rect = self.bird.rect
        for p in self.pipes:
            top, bottom = p.rects()
            if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
                self.game_over()
                return

    def draw(self):
        screen.fill(SKY)
        for p in self.pipes:
            p.draw(screen)
        pygame.draw.rect(screen, GROUND_C, (0, H - GROUND_H, W, GROUND_H))
        pygame.draw.rect(screen, (180, 140, 100), (0, H - GROUND_H, W, 10))
        self.bird.draw(screen)
        score_s = font_big.render(str(self.score), True, (255, 255, 255))
        screen.blit(score_s, score_s.get_rect(center=(W // 2, 60)))
        if self.state == "over":
            self.draw_overlay()

    def draw_overlay(self):
        shade = pygame.Surface((W, H), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 140))
        screen.blit(shade, (0, 0))
        t1 = font_big.render("GAME OVER", True, (255, 80, 80))
        t2 = font.render("Score: %d   Best: %d" % (self.score, self.best), True, (255, 255, 255))
        t3 = font.render("Press SPACE to restart", True, (255, 255, 255))
        screen.blit(t1, t1.get_rect(center=(W // 2, H // 2 - 60)))
        screen.blit(t2, t2.get_rect(center=(W // 2, H // 2)))
        screen.blit(t3, t3.get_rect(center=(W // 2, H // 2 + 50)))


def main():
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if game.state == "play":
                        game.flap()
                    else:
                        game.reset()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and game.state == "play":
                game.flap()
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()