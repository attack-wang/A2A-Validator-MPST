import pygame
import sys
import random

pygame.init()

W, H = 640, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
bigfont = pygame.font.SysFont(None, 48)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 128, 255)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
ROW_COLORS = [RED, ORANGE, YELLOW, GREEN]


class Player:
    def __init__(self):
        self.rect = pygame.Rect(W // 2 - 20, H - 40, 40, 20)
        self.speed = 5
        self.cooldown = 0
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.clamp_ip(screen.get_rect())
        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self, bullets):
        if self.cooldown == 0:
            bullets.append(pygame.Rect(self.rect.centerx - 2, self.rect.top - 10, 4, 10))
            self.cooldown = 20


class Alien:
    def __init__(self, x, y, row):
        self.rect = pygame.Rect(x, y, 30, 20)
        self.row = row
        self.points = (5 - row) * 10


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = Player()
        self.bullets = []
        self.bombs = []
        self.aliens = []
        self.dir = 1
        self.score = 0
        self.state = "play"
        self.frame = 0
        for r in range(4):
            for c in range(8):
                self.aliens.append(Alien(60 + c * 60, 60 + r * 45, r))

    def alien_shoot(self):
        if self.aliens and random.random() < 0.02:
            a = random.choice(self.aliens)
            self.bombs.append(pygame.Rect(a.rect.centerx - 2, a.rect.bottom, 4, 10))

    def update(self):
        if self.state != "play":
            return
        self.frame += 1
        self.player.update()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.player.shoot(self.bullets)
        self.alien_shoot()

        if self.frame % 30 == 0:
            edge = False
            for a in self.aliens:
                a.rect.x += self.dir * 8
                if a.rect.right > W or a.rect.left < 0:
                    edge = True
            if edge:
                self.dir *= -1
                for a in self.aliens:
                    a.rect.x += self.dir * 8
                    a.rect.y += 15

        for b in self.bullets[:]:
            b.y -= 8
            if b.bottom < 0:
                self.bullets.remove(b)

        for b in self.bombs[:]:
            b.y += 5
            if b.top > H:
                self.bombs.remove(b)
            elif b.colliderect(self.player.rect):
                self.bombs.remove(b)
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.state = "lose"

        for b in self.bullets[:]:
            for a in self.aliens[:]:
                if b.colliderect(a.rect):
                    self.bullets.remove(b)
                    self.aliens.remove(a)
                    self.score += a.points
                    break

        for a in self.aliens:
            if a.rect.bottom >= self.player.rect.top:
                self.state = "lose"
                break
        if not self.aliens and self.state == "play":
            self.state = "win"

    def draw(self):
        screen.fill(BLACK)
        for a in self.aliens:
            pygame.draw.rect(screen, ROW_COLORS[a.row], a.rect)
        pygame.draw.rect(screen, BLUE, self.player.rect)
        for b in self.bullets:
            pygame.draw.rect(screen, WHITE, b)
        for b in self.bombs:
            pygame.draw.rect(screen, RED, b)
        screen.blit(font.render("Score: %d" % self.score, True, WHITE), (10, 10))
        screen.blit(font.render("Lives: %d" % self.player.lives, True, WHITE), (W - 90, 10))
        if self.state != "play":
            msg = "YOU WIN!" if self.state == "win" else "GAME OVER"
            t = bigfont.render(msg, True, WHITE)
            screen.blit(t, (W // 2 - t.get_width() // 2, H // 2 - 30))
            p = font.render("Press R to restart, Q to quit", True, WHITE)
            screen.blit(p, (W // 2 - p.get_width() // 2, H // 2 + 20))
        pygame.display.flip()


def main():
    game = Game()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if e.key == pygame.K_r and game.state != "play":
                    game.reset()
        game.update()
        game.draw()
        clock.tick(60)


if __name__ == "__main__":
    main()