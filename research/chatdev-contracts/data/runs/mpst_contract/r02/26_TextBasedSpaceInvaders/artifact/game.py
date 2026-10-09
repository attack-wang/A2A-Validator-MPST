import random
import pygame
from settings import (WIDTH, HEIGHT, FPS, PLAYER_SPEED, PLAYER_COOLDOWN,
                      BULLET_SPEED, ALIEN_BULLET_SPEED, ALIEN_ROWS, ALIEN_COLS,
                      ALIEN_WIDTH, ALIEN_HEIGHT, ALIEN_GAP_X, ALIEN_GAP_Y,
                      ALIEN_H_SPEED, ALIEN_V_STEP, ALIEN_FIRE_CHANCE,
                      START_LIVES, SCORE_PER_ALIEN)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 64)
        self.state = "play"
        self.reset()

    def reset(self):
        self.player = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 50, 40, 24)
        self.player_bullets = []
        self.alien_bullets = []
        self.last_shot = 0
        self.lives = START_LIVES
        self.score = 0
        self.dir = 1
        self.aliens = []
        grid_w = ALIEN_COLS * ALIEN_WIDTH + (ALIEN_COLS - 1) * ALIEN_GAP_X
        margin = (WIDTH - grid_w) // 2
        for r in range(ALIEN_ROWS):
            for c in range(ALIEN_COLS):
                x = margin + c * (ALIEN_WIDTH + ALIEN_GAP_X)
                y = 60 + r * (ALIEN_HEIGHT + ALIEN_GAP_Y)
                self.aliens.append(pygame.Rect(x, y, ALIEN_WIDTH, ALIEN_HEIGHT))
        self.state = "play"

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit
                if self.state != "play" and e.key == pygame.K_r:
                    self.reset()

    def update(self):
        if self.state != "play":
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.x += PLAYER_SPEED
        self.player.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot >= PLAYER_COOLDOWN:
            self.player_bullets.append(
                pygame.Rect(self.player.centerx - 2, self.player.top - 12, 4, 12))
            self.last_shot = now

        for b in self.player_bullets:
            b.y -= BULLET_SPEED
        self.player_bullets = [b for b in self.player_bullets if b.bottom > 0]
        for b in self.alien_bullets:
            b.y += ALIEN_BULLET_SPEED
        self.alien_bullets = [b for b in self.alien_bullets if b.top < HEIGHT]

        drop = False
        for a in self.aliens:
            nx = a.x + ALIEN_H_SPEED * self.dir
            if nx <= 0 or nx + ALIEN_WIDTH >= WIDTH:
                drop = True
        if drop:
            self.dir *= -1
            for a in self.aliens:
                a.y += ALIEN_V_STEP
        else:
            for a in self.aliens:
                a.x += ALIEN_H_SPEED * self.dir

        if self.aliens and random.random() < ALIEN_FIRE_CHANCE:
            bottom = {}
            for a in self.aliens:
                col = a.centerx
                if col not in bottom or a.bottom > bottom[col].bottom:
                    bottom[col] = a
            shooter = random.choice(list(bottom.values()))
            self.alien_bullets.append(
                pygame.Rect(shooter.centerx - 2, shooter.bottom, 4, 12))

        for b in self.player_bullets[:]:
            hit = b.collidelist(self.aliens)
            if hit != -1:
                self.aliens.pop(hit)
                self.score += SCORE_PER_ALIEN
                self.player_bullets.remove(b)

        for b in self.alien_bullets[:]:
            if b.colliderect(self.player):
                self.alien_bullets.remove(b)
                self.lives -= 1
                self.alien_bullets.clear()
                if self.lives <= 0:
                    self.state = "over"

        for a in self.aliens:
            if a.bottom >= self.player.top:
                self.state = "over"
                break

        if not self.aliens:
            self.state = "win"

    def draw(self):
        self.screen.fill((10, 10, 30))
        pygame.draw.rect(self.screen, (0, 200, 255), self.player)
        for b in self.player_bullets:
            pygame.draw.rect(self.screen, (255, 255, 0), b)
        for b in self.alien_bullets:
            pygame.draw.rect(self.screen, (255, 60, 60), b)
        for a in self.aliens:
            pygame.draw.rect(self.screen, (0, 230, 100), a)
        score_s = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_s = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(score_s, (10, 8))
        self.screen.blit(lives_s, (WIDTH - lives_s.get_width() - 10, 8))
        if self.state != "play":
            if self.state == "over":
                text = self.big_font.render("GAME OVER", True, (255, 80, 80))
            else:
                text = self.big_font.render("YOU WIN!", True, (80, 255, 80))
            hint = self.font.render("Press R to restart, ESC to quit", True, (255, 255, 255))
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)