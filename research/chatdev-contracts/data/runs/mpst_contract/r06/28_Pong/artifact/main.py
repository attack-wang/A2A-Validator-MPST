import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
PADDLE_W, PADDLE_H = 12, 90
BALL_SIZE = 14
PADDLE_SPEED = 7
BALL_SPEED = 6
WINNING_SCORE = 5
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
big_font = pygame.font.SysFont(None, 64)
small_font = pygame.font.SysFont(None, 32)


class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)

    def move(self, dy):
        self.rect.y = max(0, min(HEIGHT - PADDLE_H, self.rect.y + dy))

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                                HEIGHT // 2 - BALL_SIZE // 2,
                                BALL_SIZE, BALL_SIZE)
        self.vx = BALL_SPEED * random.choice((1, -1))
        self.vy = BALL_SPEED * random.uniform(0.4, 0.9) * random.choice((1, -1))

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


def draw_center_line(surface):
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(surface, WHITE, (WIDTH // 2 - 2, y, 4, 10))


def blit_centered(surface, text, font, y):
    surf = font.render(text, True, WHITE)
    surface.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))


def main():
    left = Paddle(30)
    right = Paddle(WIDTH - 30 - PADDLE_W)
    ball = Ball()
    score = [0, 0]
    winner = None
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if winner is None:
            if keys[pygame.K_w]:
                left.move(-PADDLE_SPEED)
            if keys[pygame.K_s]:
                left.move(PADDLE_SPEED)
            if keys[pygame.K_UP]:
                right.move(-PADDLE_SPEED)
            if keys[pygame.K_DOWN]:
                right.move(PADDLE_SPEED)

            ball.rect.x += int(ball.vx)
            ball.rect.y += int(ball.vy)

            if ball.rect.top <= 0:
                ball.rect.top = 0
                ball.vy = abs(ball.vy)
            elif ball.rect.bottom >= HEIGHT:
                ball.rect.bottom = HEIGHT
                ball.vy = -abs(ball.vy)

            if ball.vx < 0 and ball.rect.colliderect(left.rect):
                ball.rect.left = left.rect.right
                ball.vx = abs(ball.vx)
                rel = (ball.rect.centery - left.rect.centery) / (PADDLE_H / 2)
                ball.vy = BALL_SPEED * max(-1.0, min(1.0, rel))
            elif ball.vx > 0 and ball.rect.colliderect(right.rect):
                ball.rect.right = right.rect.left
                ball.vx = -abs(ball.vx)
                rel = (ball.rect.centery - right.rect.centery) / (PADDLE_H / 2)
                ball.vy = BALL_SPEED * max(-1.0, min(1.0, rel))

            if ball.rect.right < 0:
                score[1] += 1
                ball.reset()
            elif ball.rect.left > WIDTH:
                score[0] += 1
                ball.reset()

            if score[0] >= WINNING_SCORE or score[1] >= WINNING_SCORE:
                winner = 0 if score[0] >= WINNING_SCORE else 1
        elif keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            score = [0, 0]
            left = Paddle(30)
            right = Paddle(WIDTH - 30 - PADDLE_W)
            ball.reset()
            winner = None

        screen.fill(BLACK)
        draw_center_line(screen)
        left.draw(screen)
        right.draw(screen)
        ball.draw(screen)
        s0 = big_font.render(str(score[0]), True, WHITE)
        s1 = big_font.render(str(score[1]), True, WHITE)
        screen.blit(s0, (WIDTH // 4 - s0.get_width() // 2, 20))
        screen.blit(s1, (3 * WIDTH // 4 - s1.get_width() // 2, 20))
        if winner is None:
            blit_centered(screen, "P1: W/S   P2: Up/Down   ESC: Quit", small_font, HEIGHT - 40)
        else:
            blit_centered(screen, "Player %d wins!" % (winner + 1), big_font, HEIGHT // 2 - 60)
            blit_centered(screen, "Press SPACE to play again", small_font, HEIGHT // 2 + 10)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()