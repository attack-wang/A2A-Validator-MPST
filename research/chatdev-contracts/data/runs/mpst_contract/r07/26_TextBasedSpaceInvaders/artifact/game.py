import pygame
import random

W, H = 480, 640
ROWS, COLS = 4, 8
COLORS = [(90, 230, 110), (90, 200, 230), (230, 200, 90), (230, 120, 200)]


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 26)
        self.big = pygame.font.SysFont(None, 52)
        self.reset()

    def reset(self):
        self.player = pygame.Rect(W // 2 - 20, H - 44, 40, 22)
        self.lives = 3
        self.score = 0
        self.bullets = []
        self.bombs = []
        self.cool = 0
        self.fire_timer = 1000
        self.dir = 1
        self.base_speed = 25.0
        self.state = "play"
        self.aliens = [[pygame.Rect(40 + c * 50, 70 + r * 40, 32, 22), r]
                       for r in range(ROWS) for c in range(COLS)]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.state == "play" and self.cool <= 0:
                self.bullets.append(pygame.Rect(self.player.centerx - 2,
                                                self.player.top - 12, 4, 12))
                self.cool = 300
            elif event.key == pygame.K_r and self.state != "play":
                self.reset()

    def update(self, dt):
        if self.state != "play":
            return
        s = dt / 1000.0
        self.cool = max(0, self.cool - dt)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= 300 * s
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += 300 * s
        self.player.clamp_ip(pygame.Rect(0, 0, W, H))

        step = self.base_speed * s * (1 + (ROWS * COLS - len(self.aliens)) * 0.06)
        edge = False
        for rect, _ in self.aliens:
            rect.x += self.dir * step
            if rect.right >= W - 4 or rect.left <= 4:
                edge = True
        if edge:
            self.dir *= -1
            for rect, _ in self.aliens:
                rect.y += 18
        for rect, _ in self.aliens:
            if rect.bottom >= self.player.top:
                self.state = "over"
                return

        self.fire_timer -= dt
        if self.fire_timer <= 0 and self.aliens:
            rect, _ = random.choice(self.aliens)
            self.bombs.append(pygame.Rect(rect.centerx - 2, rect.bottom, 4, 12))
            self.fire_timer = max(350, 1200 - self.score)

        for b in self.bullets[:]:
            b.y -= 500 * s
            if b.bottom < 0:
                self.bullets.remove(b)
                continue
            for pair in self.aliens[:]:
                if b.colliderect(pair[0]):
                    self.aliens.remove(pair)
                    self.bullets.remove(b)
                    self.score += 10
                    break

        for bo in self.bombs[:]:
            bo.y += 350 * s
            if bo.top > H:
                self.bombs.remove(bo)
            elif bo.colliderect(self.player):
                self.bombs.remove(bo)
                self.lives -= 1
                if self.lives <= 0:
                    self.state = "over"

        if not self.aliens and self.state == "play":
            self.state = "win"

    def draw(self):
        self.screen.fill((8, 10, 28))
        for rect, row in self.aliens:
            pygame.draw.rect(self.screen, COLORS[row], rect)
        pygame.draw.rect(self.screen, (90, 180, 255), self.player)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.player.centerx - 2, self.player.top - 6, 4, 6))
        for b in self.bullets:
            pygame.draw.rect(self.screen, (255, 255, 255), b)
        for bo in self.bombs:
            pygame.draw.rect(self.screen, (255, 90, 90), bo)
        hud = self.font.render("Score: %d   Lives: %d" % (self.score, self.lives),
                               True, (255, 255, 255))
        self.screen.blit(hud, (10, 8))
        if self.state == "over":
            self._center(self.big.render("GAME OVER", True, (255, 70, 70)))
            self._center(self.font.render("Press R to restart", True, (230, 230, 230)), 60)
        elif self.state == "win":
            self._center(self.big.render("YOU WIN!", True, (110, 255, 120)))
            self._center(self.font.render("Press R to restart", True, (230, 230, 230)), 60)

    def _center(self, surf, dy=0):
        self.screen.blit(surf, surf.get_rect(center=(W // 2, H // 2 + dy)))