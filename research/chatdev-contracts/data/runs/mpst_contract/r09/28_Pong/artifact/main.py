import sys

try:
    import pygame
except ImportError:
    print("pygame is required to run this game. Install it with: pip install pygame")
    sys.exit(1)

import random

pygame.init()

WIDTH, HEIGHT = 800, 600
PADDLE_W, PADDLE_H = 12, 100
BALL_SIZE = 12
PADDLE_SPEED = 7
BALL_SPEED_X, BALL_SPEED_Y = 6, 4
WIN_SCORE = 5
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Player Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)


class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)

    def move(self, dy):
        self.rect.y = max(0, min(HEIGHT - PADDLE_H, self.rect.y + dy))

    def reset(self):
        self.rect.y = HEIGHT // 2 - PADDLE_H // 2

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    def __init__(self):
        self.reset(random.choice([-1, 1]))

    def reset(self, direction):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2,
                                HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.vx = BALL_SPEED_X * direction
        self.vy = random.choice([-1, 1]) * BALL_SPEED_Y

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)


def main():
    left = Paddle(20)
    right = Paddle(WIDTH - 20 - PADDLE_W)
    ball = Ball()
    score_left = 0
    score_right = 0
    winner = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and winner:
                score_left = score_right = 0
                winner = None
                left.reset()
                right.reset()
                ball.reset(random.choice([-1, 1]))

        keys = pygame.key.get_pressed()
        if not winner:
            if keys[pygame.K_w]:
                left.move(-PADDLE_SPEED)
            if keys[pygame.K_s]:
                left.move(PADDLE_SPEED)
            if keys[pygame.K_UP]:
                right.move(-PADDLE_SPEED)
            if keys[pygame.K_DOWN]:
                right.move(PADDLE_SPEED)

            ball.rect.x += ball.vx
            ball.rect.y += ball.vy

            if ball.rect.top <= 0:
                ball.rect.top = 0
                ball.vy = -ball.vy
            if ball.rect.bottom >= HEIGHT:
                ball.rect.bottom = HEIGHT
                ball.vy = -ball.vy

            if ball.rect.colliderect(left.rect) and ball.vx < 0:
                ball.rect.left = left.rect.right
                ball.vx = -ball.vx
                ball.vy += int((ball.rect.centery - left.rect.centery) / (PADDLE_H / 2) * 3)
            if ball.rect.colliderect(right.rect) and ball.vx > 0:
                ball.rect.right = right.rect.left
                ball.vx = -ball.vx
                ball.vy += int((ball.rect.centery - right.rect.centery) / (PADDLE_H / 2) * 3)
            ball.vy = max(-10, min(10, ball.vy))

            if ball.rect.right < 0:
                score_right += 1
                ball.reset(-1)
            elif ball.rect.left > WIDTH:
                score_left += 1
                ball.reset(1)

            if score_left >= WIN_SCORE:
                winner = "Left Player"
            elif score_right >= WIN_SCORE:
                winner = "Right Player"

        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        left.draw()
        right.draw()
        ball.draw()
        score_text = font.render(f"{score_left}    {score_right}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        if winner:
            win_text = font.render(f"{winner} wins! Press R to restart", True, WHITE)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 24))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()