import random
import sys

try:
    import pygame
except ImportError:
    print("pygame is required. Install it with: pip install pygame")
    sys.exit(1)

W, H = 800, 600
FPS = 60
PLAYER_SPEED = 6
BULLET_SPEED = 9
ALIEN_BULLET_SPEED = 5
ROWS, COLS = 4, 8
START_LIVES = 3
MAX_P_BULLETS = 3


class Player:
    def __init__(self):
        self.rect = pygame.Rect(W // 2 - 20, H - 60, 40, 22)
        self.lives = START_LIVES
        self.cooldown = 0

    def move(self, dx):
        self.rect.x = max(10, min(W - 10 - self.rect.width, self.rect.x + dx))


class Bullet:
    def __init__(self, x, y, dy, color):
        self.rect = pygame.Rect(x - 2, y, 4, 12)
        self.dy = dy
        self.color = color


class Alien:
    def __init__(self, col, row):
        self.rect = pygame.Rect(70 + col * 78, 70 + row * 52, 40, 26)
        self.row = row
        self.points = (ROWS - row) * 10


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = Player()
        self.aliens = [Alien(c, r) for r in range(ROWS) for c in range(COLS)]
        self.pbullets = []
        self.abullets = []
        self.dir = 1
        self.score = 0
        self.fire_timer = 70
        self.state = "play"
        self.message = ""
        self.stars = [(random.randint(0, W - 1), random.randint(0, H - 1),
                       random.choice((1, 1, 2))) for _ in range(70)]

    def fleet_speed(self):
        return 0.6 + (ROWS * COLS - len(self.aliens)) * 0.035

    def update(self):
        if self.state != "play":
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-PLAYER_SPEED)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(PLAYER_SPEED)
        if self.player.cooldown > 0:
            self.player.cooldown -= 1
        if keys[pygame.K_SPACE] and self.player.cooldown == 0 \
                and len(self.pbullets) < MAX_P_BULLETS:
            self.pbullets.append(Bullet(self.player.rect.centerx,
                                        self.player.rect.top - 12,
                                        -BULLET_SPEED, (80, 255, 120)))
            self.player.cooldown = 18

        # Fleet movement: slide sideways, drop and reverse at edges
        dx = int(round(self.dir * self.fleet_speed()))
        if dx:
            edge = False
            for a in self.aliens:
                a.rect.x += dx
                if a.rect.right > W - 10 or a.rect.left < 10:
                    edge = True
            if edge:
                self.dir *= -1
                for a in self.aliens:
                    a.rect.x -= dx
                    a.rect.y += 18

        # Alien fire: bottom-most alien of a random column shoots
        self.fire_timer -= 1
        if self.fire_timer <= 0 and self.aliens:
            cols = {}
            for a in self.aliens:
                cols.setdefault(a.rect.x, []).append(a)
            shooter = max(random.choice(list(cols.values())),
                          key=lambda a: a.rect.y)
            self.abullets.append(Bullet(shooter.rect.centerx,
                                        shooter.rect.bottom,
                                        ALIEN_BULLET_SPEED, (255, 90, 90)))
            destroyed = ROWS * COLS - len(self.aliens)
            self.fire_timer = max(22, 70 - destroyed)

        # Move bullets and cull off-screen ones
        for b in self.pbullets:
            b.rect.y += b.dy
        for b in self.abullets:
            b.rect.y += b.dy
        self.pbullets = [b for b in self.pbullets if b.rect.bottom > 0]
        self.abullets = [b for b in self.abullets if b.rect.top < H]

        # Player bullets vs aliens
        for b in list(self.pbullets):
            for a in list(self.aliens):
                if b.rect.colliderect(a.rect):
                    self.aliens.remove(a)
                    if b in self.pbullets:
                        self.pbullets.remove(b)
                    self.score += a.points
                    break

        # Alien bullets vs player
        for b in list(self.abullets):
            if b.rect.colliderect(self.player.rect):
                self.abullets.remove(b)
                self.player.lives -= 1
                self.abullets.clear()
                if self.player.lives <= 0:
                    self.state = "over"
                    self.message = "GAME OVER"

        # Aliens reaching the bottom end the game
        for a in self.aliens:
            if a.rect.bottom >= self.player.rect.top:
                self.state = "over"
                self.message = "GAME OVER - INVASION!"
                break

        # All aliens destroyed: victory
        if self.state == "play" and not self.aliens:
            self.state = "win"
            self.message = "YOU WIN!"

    def draw(self, screen, font, big):
        screen.fill((8, 10, 28))
        for x, y, s in self.stars:
            screen.fill((200, 200, 220), (x, y, s, s))
        pygame.draw.rect(screen, (0, 190, 255), self.player.rect)
        pygame.draw.rect(screen, (0, 190, 255),
                         (self.player.rect.centerx - 4,
                          self.player.rect.top - 8, 8, 8))
        colors = [(255, 90, 90), (255, 170, 60), (120, 230, 120), (190, 130, 255)]
        for a in self.aliens:
            c = colors[a.row % len(colors)]
            pygame.draw.rect(screen, c, a.rect)
            pygame.draw.rect(screen, (8, 10, 28),
                             (a.rect.x + 8, a.rect.y + 7, 7, 7))
            pygame.draw.rect(screen, (8, 10, 28),
                             (a.rect.right - 15, a.rect.y + 7, 7, 7))
        for b in self.pbullets:
            pygame.draw.rect(screen, b.color, b.rect)
        for b in self.abullets:
            pygame.draw.rect(screen, b.color, b.rect)
        hud = font.render("Score: %d   Lives: %d   Aliens: %d" %
                          (self.score, self.player.lives, len(self.aliens)),
                          True, (255, 255, 255))
        screen.blit(hud, (12, 10))
        if self.state != "play":
            t = big.render(self.message, True, (255, 230, 80))
            screen.blit(t, t.get_rect(center=(W // 2, H // 2 - 20)))
            s = font.render("Press R to restart - Q to quit", True, (255, 255, 255))
            screen.blit(s, s.get_rect(center=(W // 2, H // 2 + 30)))
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    big = pygame.font.SysFont(None, 56)
    game = Game()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif e.key == pygame.K_r:
                    game.reset()
        game.update()
        game.draw(screen, font, big)
        clock.tick(FPS)


if __name__ == "__main__":
    main()