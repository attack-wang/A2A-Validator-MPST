import pygame
import random
import sys

CELL = 20
COLS, ROWS = 30, 20
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + 40
DIFFICULTIES = {"Easy": 8, "Medium": 12, "Hard": 18}


def draw_text(surf, text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    surf.blit(font.render(text, True, color), (x, y))


def spawn_food(snake):
    while True:
        p = (random.randrange(COLS), random.randrange(ROWS))
        if p not in snake:
            return p


def choose_difficulty(screen):
    screen.fill((0, 0, 0))
    draw_text(screen, "SNAKE - Select Difficulty", 40, (0, 255, 0), 140, 100)
    names = list(DIFFICULTIES)
    for i, name in enumerate(names):
        draw_text(screen, "%d. %s" % (i + 1, name), 32, (255, 255, 255), 250, 180 + i * 50)
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if pygame.K_1 <= e.key <= pygame.K_3:
                    return DIFFICULTIES[names[e.key - pygame.K_1]]
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def game_loop(fps):
    screen = pygame.display.get_surface()
    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    pending = []
    food = spawn_food(snake)
    score = 0
    clock = pygame.time.Clock()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None
            if e.type == pygame.KEYDOWN:
                new_dir = None
                if e.key == pygame.K_UP:
                    new_dir = (0, -1)
                elif e.key == pygame.K_DOWN:
                    new_dir = (0, 1)
                elif e.key == pygame.K_LEFT:
                    new_dir = (-1, 0)
                elif e.key == pygame.K_RIGHT:
                    new_dir = (1, 0)
                elif e.key == pygame.K_ESCAPE:
                    return None
                if new_dir is not None and len(pending) < 2:
                    last = pending[-1] if pending else direction
                    if new_dir != last and (new_dir[0] + last[0], new_dir[1] + last[1]) != (0, 0):
                        pending.append(new_dir)
        if pending:
            direction = pending.pop(0)
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if head[0] < 0 or head[0] >= COLS or head[1] < 0 or head[1] >= ROWS or head in snake:
            return score
        snake.insert(0, head)
        if head == food:
            score += 1
            if len(snake) >= COLS * ROWS:
                return score
            food = spawn_food(snake)
        else:
            snake.pop()
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (60, 60, 60), (0, 0, COLS * CELL, ROWS * CELL), 2)
        pygame.draw.rect(screen, (255, 0, 0), (food[0] * CELL, food[1] * CELL, CELL, CELL))
        for seg in snake:
            pygame.draw.rect(screen, (0, 255, 0), (seg[0] * CELL, seg[1] * CELL, CELL - 1, CELL - 1))
        draw_text(screen, "Score: %d" % score, 28, (255, 255, 255), 10, ROWS * CELL + 8)
        pygame.display.flip()
        clock.tick(fps)


def game_over_screen(screen, score):
    screen.fill((0, 0, 0))
    draw_text(screen, "Game Over! Score: %d" % score, 40, (255, 0, 0), 160, 200)
    draw_text(screen, "Press R to restart, Q to quit", 28, (255, 255, 255), 190, 260)
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return True
                if e.key in (pygame.K_q, pygame.K_ESCAPE):
                    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    while True:
        fps = choose_difficulty(screen)
        score = game_loop(fps)
        if score is None or not game_over_screen(screen, score):
            break
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()