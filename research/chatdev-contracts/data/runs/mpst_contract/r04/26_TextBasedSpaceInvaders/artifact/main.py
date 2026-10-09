import sys
import random

try:
    import pygame
except ImportError:
    sys.exit("pygame is required to run Space Invaders. Install it with: pip install pygame")

WIDTH, HEIGHT = 800, 600
FPS = 60
BG = (8, 10, 22)
WHITE = (235, 235, 235)
GREEN = (70, 220, 130)
RED = (230, 80, 80)
BLUE = (90, 170, 255)
YELLOW = (250, 215, 90)

ALIEN_ROWS, ALIEN_COLS = 4, 8
ALIEN_SPEED = 1.2
ALIEN_DESCENT = 18
PLAYER_SPEED = 6
BULLET_SPEED = 9
ENEMY_BULLET_SPEED = 5
START_LIVES = 3


class Ship:
    def __init__(self):
        self.w, self.h = 48, 24
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 60
        self.lives = START_LIVES
        self.cooldown = 0
        self.invuln = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), self.y, self.w, self.h)

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += PLAYER_SPEED
        self.x = max(0, min(WIDTH - self.w, self.x))
        self.cooldown = max(0, self.cooldown - 1)
        self.invuln = max(0, self.invuln - 1)

    def draw(self, surf):
        if self.invuln and (self.invuln // 4) % 2 == 0:
            return
        r = self.rect
        pygame.draw.polygon(surf, WHITE, [
            (r.centerx, r.top), (r.right, r.bottom),
            (r.right - 9, r.bottom), (r.centerx, r.bottom - 11),
            (r.left + 9, r.bottom), (r.left, r.bottom)])


class Alien:
    COLORS = [RED, BLUE, GREEN, YELLOW]

    def __init__(self, col, row):
        self.w, self.h = 36, 24
        self.x = 90 + col * 78
        self.y = 70 + row * 55
        self.row = row
        self.wobble = random.randrange(2)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def draw(self, surf, frame):
        r = self.rect
        c = self.COLORS[self.row % len(self.COLORS)]
        pygame.draw.rect(surf, c, (r.x, r.y + 6, r.w, r.h - 6), border_radius=7)
        pygame.draw.rect(surf, c, (r.x + 7, r.y + 2, r.w - 14, 8), border_radius=4)
        off = 2 if (frame // 20 + self.wobble) % 2 else -2
        pygame.draw.circle(surf, BG, (r.centerx - 8 + off, r.y + 13), 3)
        pygame.draw.circle(surf, BG, (r.centerx + 8 + off, r.y + 13), 3)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.big = pygame.font.SysFont(None, 64)
        self.stars = [(random.randrange(WIDTH), random.randrange(HEIGHT),
                       random.choice((1, 1, 2))) for _ in range(90)]
        self.reset()

    def reset(self):
        self.ship = Ship()
        self.aliens = [Alien(c, r) for r in range(ALIEN_ROWS) for c in range(ALIEN_COLS)]
        self.bullets = []
        self.bombs = []
        self.dir = 1
        self.score = 0
        self.state = "play"
        self.fire_timer = 60
        self.frame = 0

    def march(self):
        speed = ALIEN_SPEED + (ALIEN_ROWS * ALIEN_COLS - len(self.aliens)) * 0.05
        if any(a.x <= 0 or a.x + a.w >= WIDTH for a in self.aliens):
            self.dir *= -1
            for a in self.aliens:
                a.y += ALIEN_DESCENT
        else:
            for a in self.aliens:
                a.x += self.dir * speed

    def update(self):
        self.frame += 1
        self.ship.update(pygame.key.get_pressed())

        for b in self.bullets[:]:
            b.y -= BULLET_SPEED
            if b.bottom < 0:
                self.bullets.remove(b)

        if self.frame % 2 == 0:
            self.march()

        self.fire_timer -= 1
        if self.fire_timer <= 0 and self.aliens:
            s = random.choice(self.aliens).rect
            self.bombs.append(pygame.Rect(s.centerx - 2, s.bottom, 4, 12))
            self.fire_timer = random.randint(40, 90)

        for b in self.bombs[:]:
            b.y += ENEMY_BULLET_SPEED
            if b.top > HEIGHT:
                self.bombs.remove(b)

        for b in self.bullets[:]:
            for a in self.aliens:
                if b.colliderect(a.rect):
                    self.aliens.remove(a)
                    self.bullets.remove(b)
                    self.score += 10 + (ALIEN_ROWS - 1 - a.row) * 5
                    break

        if self.ship.invuln == 0:
            for b in self.bombs[:]:
                if b.colliderect(self.ship.rect):
                    self.bombs.remove(b)
                    self.ship.lives -= 1
                    self.ship.invuln = 90
                    if self.ship.lives <= 0:
                        self.state = "over"
                    break

        if any(a.rect.bottom >= self.ship.rect.top for a in self.aliens):
            self.state = "over"
        elif not self.aliens:
            self.state = "win"

    def draw(self):
        self.screen.fill(BG)
        for x, y, s in self.stars:
            pygame.draw.circle(self.screen, (70, 75, 95), (x, y), s)
        for a in self.aliens:
            a.draw(self.screen, self.frame)
        self.ship.draw(self.screen)
        for b in self.bullets:
            pygame.draw.rect(self.screen, YELLOW, b)
        for b in self.bombs:
            pygame.draw.rect(self.screen, RED, b)
        pygame.draw.rect(self.screen, (40, 45, 60), (0, HEIGHT - 26, WIDTH, 26))
        hud = self.font.render(f"SCORE {self.score}    LIVES {self.ship.lives}", True, WHITE)
        self.screen.blit(hud, (14, 8))
        if self.state != "play":
            win = self.state == "win"
            t = self.big.render("YOU WIN!" if win else "GAME OVER", True, GREEN if win else RED)
            sub = self.font.render(f"Final score: {self.score}  |  R = restart, ESC = quit", True, WHITE)
            self.screen.blit(t, t.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 24)))
            self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 34)))

    def run(self):
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if self.state == "play" and e.key == pygame.K_SPACE and self.ship.cooldown == 0:
                        r = self.ship.rect
                        self.bullets.append(pygame.Rect(r.centerx - 2, r.top - 12, 4, 14))
                        self.ship.cooldown = 18
                    elif self.state != "play" and e.key == pygame.K_r:
                        self.reset()
            if self.state == "play":
                self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()