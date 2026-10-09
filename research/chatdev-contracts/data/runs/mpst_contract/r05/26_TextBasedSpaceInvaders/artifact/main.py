import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 480, 640
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 100)
RED = (255, 80, 80)

PLAYER_SPEED = 5
BULLET_SPEED = 8
ALIEN_BULLET_SPEED = 4
ALIEN_STEP_X = 2
ALIEN_DROP = 12
FIRE_COOLDOWN = 18
START_LIVES = 3
ROWS, COLS = 4, 8
ALIEN_W, ALIEN_H = 32, 24
ALIEN_GAP_X, ALIEN_GAP_Y = 48, 40
ALIEN_MARGIN_X, ALIEN_TOP = 60, 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 26)
big_font = pygame.font.SysFont(None, 52)


class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 50, 40, 18)
        self.cooldown = 0

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED
        self.cooldown = max(0, self.cooldown - 1)

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)
        pygame.draw.polygon(screen, GREEN, [
            (self.rect.centerx, self.rect.top - 10),
            (self.rect.left + 6, self.rect.top),
            (self.rect.right - 6, self.rect.top)])


class Bullet:
    def __init__(self, x, y, speed, color):
        self.rect = pygame.Rect(x - 2, y, 4, 12)
        self.speed = speed
        self.color = color

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


class Alien:
    def __init__(self, x, y, points):
        self.rect = pygame.Rect(x, y, ALIEN_W, ALIEN_H)
        self.points = points
        self.alive = True

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        pygame.draw.rect(screen, WHITE, (self.rect.x + 7, self.rect.y + 8, 5, 5))
        pygame.draw.rect(screen, WHITE, (self.rect.x + 20, self.rect.y + 8, 5, 5))
        pygame.draw.rect(screen, WHITE, (self.rect.x + 12, self.rect.y + 16, 8, 3))


def make_aliens():
    aliens = []
    for row in range(ROWS):
        for col in range(COLS):
            points = (ROWS - row) * 10
            x = ALIEN_MARGIN_X + col * ALIEN_GAP_X
            y = ALIEN_TOP + row * ALIEN_GAP_Y
            aliens.append(Alien(x, y, points))
    return aliens


def draw_hud(score, lives):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 8))
    screen.blit(font.render(f"Lives: {lives}", True, WHITE), (WIDTH - 100, 8))


def draw_center(text, size_font, y, color=WHITE):
    surf = size_font.render(text, True, color)
    screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))


def main():
    player = Player()
    aliens = make_aliens()
    player_bullets = []
    alien_bullets = []
    score = 0
    lives = START_LIVES
    alien_dir = 1
    fire_timer = 60
    state = "play"
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and state != "play":
                player = Player()
                aliens = make_aliens()
                player_bullets, alien_bullets = [], []
                score, lives = 0, START_LIVES
                alien_dir, fire_timer = 1, 60
                state = "play"

        if state == "play":
            keys = pygame.key.get_pressed()
            player.update(keys)
            if keys[pygame.K_SPACE] and player.cooldown == 0:
                player_bullets.append(
                    Bullet(player.rect.centerx, player.rect.top - 12, -BULLET_SPEED, GREEN))
                player.cooldown = FIRE_COOLDOWN

            for b in player_bullets + alien_bullets:
                b.update()
            player_bullets = [b for b in player_bullets if b.rect.bottom > 0]
            alien_bullets = [b for b in alien_bullets if b.rect.top < HEIGHT]

            alive = [a for a in aliens if a.alive]
            if alive:
                leftmost = min(a.rect.left for a in alive)
                rightmost = max(a.rect.right for a in alive)
                if rightmost + alien_dir * ALIEN_STEP_X >= WIDTH or leftmost + alien_dir * ALIEN_STEP_X <= 0:
                    alien_dir *= -1
                    for a in alive:
                        a.rect.y += ALIEN_DROP
                else:
                    for a in alive:
                        a.rect.x += alien_dir * ALIEN_STEP_X

                fire_timer -= 1
                if fire_timer <= 0:
                    shooter = random.choice(alive)
                    alien_bullets.append(
                        Bullet(shooter.rect.centerx, shooter.rect.bottom, ALIEN_BULLET_SPEED, RED))
                    fire_timer = random.randint(40, 90)

            for b in player_bullets:
                for a in alive:
                    if a.alive and b.rect.colliderect(a.rect):
                        a.alive = False
                        b.rect.y = -100
                        score += a.points
                        break
            player_bullets = [b for b in player_bullets if b.rect.y > -60]

            for b in alien_bullets:
                if b.rect.colliderect(player.rect):
                    lives -= 1
                    b.rect.y = HEIGHT + 100
            alien_bullets = [b for b in alien_bullets if b.rect.y < HEIGHT + 60]

            if any(a.rect.bottom >= player.rect.top for a in alive if a.alive):
                state = "lose"
            elif not any(a.alive for a in aliens):
                state = "win"
            elif lives <= 0:
                state = "lose"

        screen.fill(BLACK)
        player.draw()
        for a in aliens:
            if a.alive:
                a.draw()
        for b in player_bullets + alien_bullets:
            b.draw()
        draw_hud(score, lives)
        if state == "win":
            draw_center("YOU WIN!", big_font, HEIGHT // 2 - 60)
            draw_center(f"Final Score: {score}", font, HEIGHT // 2)
            draw_center("Press R to restart", font, HEIGHT // 2 + 30)
        elif state == "lose":
            draw_center("GAME OVER", big_font, HEIGHT // 2 - 60)
            draw_center(f"Final Score: {score}", font, HEIGHT // 2)
            draw_center("Press R to restart", font, HEIGHT // 2 + 30)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()