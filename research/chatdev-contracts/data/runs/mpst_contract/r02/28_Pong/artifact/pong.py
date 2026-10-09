import random

import pygame

WIDTH, HEIGHT = 800, 600
PADDLE_W, PADDLE_H = 12, 100
PADDLE_SPEED = 7
BALL_SIZE = 14
BALL_BASE_SPEED = 6.0
BALL_MAX_SPEED = 13.0
WIN_SCORE = 5
FPS = 60
WHITE = (235, 235, 235)
BLACK = (18, 18, 18)
GREY = (100, 100, 100)


class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, (HEIGHT - PADDLE_H) // 2, PADDLE_W, PADDLE_H)

    def move(self, direction):
        self.rect.y = max(0, min(HEIGHT - PADDLE_H, self.rect.y + direction * PADDLE_SPEED))

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.reset(random.choice((-1, 1)))

    def reset(self, direction):
        self.x = WIDTH / 2 - BALL_SIZE / 2
        self.y = HEIGHT / 2 - BALL_SIZE / 2
        self.vx = BALL_BASE_SPEED * direction
        self.vy = random.choice((-1, 1)) * random.uniform(2.0, 4.0)
        self.rect = pygame.Rect(int(self.x), int(self.y), BALL_SIZE, BALL_SIZE)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.y <= 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y >= HEIGHT - BALL_SIZE:
            self.y = HEIGHT - BALL_SIZE
            self.vy = -abs(self.vy)
        self.rect.topleft = (int(self.x), int(self.y))

    def bounce(self, paddle):
        self.vx = -self.vx * 1.05
        if abs(self.vx) > BALL_MAX_SPEED:
            self.vx = BALL_MAX_SPEED if self.vx > 0 else -BALL_MAX_SPEED
        offset = (self.rect.centery - paddle.rect.centery) / (PADDLE_H / 2)
        self.vy = max(-6.0, min(6.0, offset * 5.5))
        if self.vx > 0:
            self.x = float(paddle.rect.right)
        else:
            self.x = float(paddle.rect.left - BALL_SIZE)
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong - First to %d" % WIN_SCORE)
        self.clock = pygame.time.Clock()
        self.big_font = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 28)
        self.reset()

    def reset(self):
        self.p1 = Paddle(30)
        self.p2 = Paddle(WIDTH - 30 - PADDLE_W)
        self.ball = Ball()
        self.score1 = 0
        self.score2 = 0
        self.winner = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.p1.move(-1)
        if keys[pygame.K_s]:
            self.p1.move(1)
        if keys[pygame.K_UP]:
            self.p2.move(-1)
        if keys[pygame.K_DOWN]:
            self.p2.move(1)

    def update(self):
        if self.winner:
            return
        ball = self.ball
        ball.update()
        p1, p2 = self.p1.rect, self.p2.rect
        if ball.vx < 0 and ball.rect.right >= p1.left and ball.rect.left <= p1.right \
                and ball.rect.bottom >= p1.top and ball.rect.top <= p1.bottom:
            ball.bounce(self.p1)
        elif ball.vx > 0 and ball.rect.left <= p2.right and ball.rect.right >= p2.left \
                and ball.rect.bottom >= p2.top and ball.rect.top <= p2.bottom:
            ball.bounce(self.p2)
        if ball.x + BALL_SIZE < 0:
            self.score2 += 1
            self.check_winner()
            ball.reset(-1)
        elif ball.x > WIDTH:
            self.score1 += 1
            self.check_winner()
            ball.reset(1)

    def check_winner(self):
        if self.score1 >= WIN_SCORE:
            self.winner = "Player 1"
        elif self.score2 >= WIN_SCORE:
            self.winner = "Player 2"

    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, GREY, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        self.p1.draw(self.screen)
        self.p2.draw(self.screen)
        self.ball.draw(self.screen)
        self.screen.blit(self.font.render(str(self.score1), True, WHITE), (WIDTH // 2 - 70, 15))
        self.screen.blit(self.font.render(str(self.score2), True, WHITE), (WIDTH // 2 + 40, 15))
        hint = self.small_font.render(
            "P1: W/S    P2: Up/Down    First to %d    ESC: quit" % WIN_SCORE, True, GREY)
        self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 20)))
        if self.winner:
            msg = self.big_font.render("%s wins!  R: restart" % self.winner, True, WHITE)
            self.screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    if event.key == pygame.K_r and self.winner:
                        self.reset()
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)