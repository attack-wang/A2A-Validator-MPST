import random
import sys

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 24)
SMALL = pygame.font.SysFont("consolas", 16)
BIG = pygame.font.SysFont("consolas", 48, bold=True)

WHITE = (240, 240, 240)
GREEN = (0, 210, 90)
RED = (230, 70, 70)
BLUE = (80, 140, 240)
YELLOW = (245, 220, 70)
BG = (12, 12, 24)

ROWS, COLS = 4, 10
ALIEN_W, ALIEN_H = 40, 28
H_GAP, V_GAP = 22, 24
PLAYER_SPEED = 6
BULLET_SPEED = 10
ALIEN_BULLET_SPEED = 5
START_LIVES = 3
STEP_FRAMES = 24
DROP = 20


class Player:
    def __init__(self):
        self.w, self.h = 60, 24
        self.x = WIDTH // 2 - self.w // 2
        self.y = HEIGHT - 60
        self.cooldown = 0

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += PLAYER_SPEED
        self.x = max(0, min(WIDTH - self.w, self.x))
        self.cooldown = max(0, self.cooldown - 1)

    def center(self):
        self.x = WIDTH // 2 - self.w // 2

    def draw(self):
        pygame.draw.polygon(screen, GREEN, [
            (self.x + self.w // 2, self.y),
            (self.x + self.w, self.y + self.h),
            (self.x + self.w - 12, self.y + self.h - 7),
            (self.x + 12, self.y + self.h - 7),
            (self.x, self.y + self.h),
        ])


class Bullet:
    def __init__(self, x, y, vy, color):
        self.rect = pygame.Rect(x - 2, y, 4, 12)
        self.vy = vy
        self.color = color

    def update(self):
        self.rect.y += self.vy

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


class Alien:
    def __init__(self, row, x, y):
        self.rect = pygame.Rect(x, y, ALIEN_W, ALIEN_H)
        self.points = (ROWS - row) * 10
        self.color = YELLOW if row == 0 else BLUE

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        pygame.draw.rect(screen, BG, self.rect.inflate(-18, -10), border_radius=4)


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = Player()
        self.player_bullets = []
        self.alien_bullets = []
        self.aliens = []
        self.direction = 1
        self.score = 0
        self.lives = START_LIVES
        self.state = "play"
        self.frame = 0
        grid_w = COLS * ALIEN_W + (COLS - 1) * H_GAP
        start_x = (WIDTH - grid_w) // 2
        for r in range(ROWS):
            for c in range(COLS):
                x = start_x + c * (ALIEN_W + H_GAP)
                y = 60 + r * (ALIEN_H + V_GAP)
                self.aliens.append(Alien(r, x, y))

    def alien_step(self):
        if not self.aliens:
            return
        left = min(a.rect.left for a in self.aliens)
        right = max(a.rect.right for a in self.aliens)
        speed = min(6 + (ROWS * COLS - len(self.aliens)) * 0.25, 18)
        dx = self.direction * speed
        if right + dx > WIDTH - 10 or left + dx < 10:
            self.direction *= -1
            for a in self.aliens:
                a.rect.y += DROP
        else:
            for a in self.aliens:
                a.rect.x += dx

    def alien_fire(self):
        if self.aliens and random.random() < 0.03:
            shooter = random.choice(self.aliens)
            self.alien_bullets.append(
                Bullet(shooter.rect.centerx, shooter.rect.bottom, ALIEN_BULLET_SPEED, RED))

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = "lose"
        else:
            self.alien_bullets.clear()
            self.player.center()

    def update(self):
        if self.state != "play":
            return
        self.frame += 1
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.player.cooldown == 0:
            self.player_bullets.append(
                Bullet(self.player.rect().centerx, self.player.rect().top, -BULLET_SPEED, GREEN))
            self.player.cooldown = 18

        if self.frame % STEP_FRAMES == 0:
            self.alien_step()
        self.alien_fire()

        for b in self.player_bullets:
            b.update()
        self.player_bullets = [b for b in self.player_bullets if b.rect.bottom > 0]

        for b in self.alien_bullets:
            b.update()
        self.alien_bullets = [b for b in self.alien_bullets if b.rect.top < HEIGHT]

        for b in self.player_bullets[:]:
            hit = b.rect.collidelist(self.aliens)
            if hit != -1:
                self.score += self.aliens[hit].points
                self.aliens.pop(hit)
                self.player_bullets.remove(b)

        for b in self.alien_bullets[:]:
            if b.rect.colliderect(self.player.rect()):
                self.alien_bullets.remove(b)
                self.lose_life()
                if self.state != "play":
                    return

        for a in self.aliens:
            if a.rect.bottom >= self.player.rect().top:
                self.state = "lose"
                return

        if not self.aliens:
            self.state = "win"

    def draw(self):
        screen.fill(BG)
        self.player.draw()
        for b in self.player_bullets + self.alien_bullets:
            b.draw()
        for a in self.aliens:
            a.draw()
        hud = FONT.render(f"SCORE: {self.score}    LIVES: {self.lives}", True, WHITE)
        screen.blit(hud, (16, 12))
        hint = SMALL.render("Move: A/D or Arrows    Fire: SPACE    Restart: R    Quit: ESC", True, WHITE)
        screen.blit(hint, hint.get_rect(midbottom=(WIDTH // 2, HEIGHT - 8)))
        if self.state != "play":
            msg = "YOU WIN!" if self.state == "win" else "GAME OVER"
            color = GREEN if self.state == "win" else RED
            t1 = BIG.render(msg, True, color)
            t2 = FONT.render(f"Final Score: {self.score}   Press R to restart", True, WHITE)
            screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
            screen.blit(t2, t2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
        pygame.display.flip()


def main():
    game = Game()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if e.key == pygame.K_r and game.state != "play":
                    game.reset()
        game.update()
        game.draw()
        clock.tick(60)


if __name__ == "__main__":
    main()