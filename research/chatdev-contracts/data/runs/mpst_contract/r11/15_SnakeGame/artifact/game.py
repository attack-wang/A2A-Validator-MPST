import random

import pygame

from settings import CELL, COLS, ROWS, HUD, WIDTH, COLORS

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
KEY_DIRS = {
    pygame.K_UP: UP,
    pygame.K_w: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_d: RIGHT,
}


class Snake:
    def __init__(self):
        self.body = [(COLS // 2, ROWS // 2)]
        self.direction = RIGHT
        self.grow = 0
        self.queue = []

    def turn(self, direction):
        last = self.queue[-1] if self.queue else self.direction
        if direction != last and (direction[0] * -1, direction[1] * -1) != last:
            if len(self.queue) < 2:
                self.queue.append(direction)

    def step(self):
        if self.queue:
            self.direction = self.queue.pop(0)
        head = self.body[0]
        nxt = (head[0] + self.direction[0], head[1] + self.direction[1])
        blocked = self.body if self.grow else self.body[:-1]
        if not (0 <= nxt[0] < COLS and 0 <= nxt[1] < ROWS) or nxt in blocked:
            return False
        self.body.insert(0, nxt)
        if self.grow:
            self.grow -= 1
        else:
            self.body.pop()
        return True


class Food:
    def __init__(self, snake):
        self.respawn(snake)

    def respawn(self, snake):
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in snake.body]
        self.pos = random.choice(free) if free else None


class Game:
    def __init__(self, screen, speed):
        self.screen = screen
        self.speed = speed
        self.font = pygame.font.SysFont(None, 30)
        self.big = pygame.font.SysFont(None, 52)
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.food = Food(self.snake)
        self.score = 0
        self.alive = True
        self.paused = False
        self.running = True
        self.quit_app = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.quit_app = True
            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRS:
                    self.snake.turn(KEY_DIRS[event.key])
                elif event.key == pygame.K_SPACE and self.alive:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and not self.alive:
                    self.reset()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        if not self.alive or self.paused:
            return
        if not self.snake.step():
            self.alive = False
            return
        if self.food.pos and self.snake.body[0] == self.food.pos:
            self.snake.grow += 1
            self.score += 1
            self.food.respawn(self.snake)

    def draw_cell(self, pos, color):
        rect = (pos[0] * CELL + 1, HUD + pos[1] * CELL + 1, CELL - 2, CELL - 2)
        pygame.draw.rect(self.screen, color, rect, border_radius=4)

    def draw(self):
        self.screen.fill(COLORS["bg"])
        pygame.draw.rect(self.screen, COLORS["board"], (0, HUD, WIDTH, ROWS * CELL))
        pygame.draw.rect(self.screen, COLORS["border"], (0, HUD, WIDTH, ROWS * CELL), 2)
        if self.food.pos:
            self.draw_cell(self.food.pos, COLORS["food"])
        for i, seg in enumerate(self.snake.body):
            self.draw_cell(seg, COLORS["head"] if i == 0 else COLORS["snake"])
        self.screen.blit(self.font.render(f"Score: {self.score}", True, COLORS["text"]), (10, 8))
        hint = self.font.render("WASD/Arrows move | Space pause | Esc menu", True, COLORS["text"])
        self.screen.blit(hint, (WIDTH - hint.get_width() - 10, 8))
        cy = HUD + ROWS * CELL // 2
        if not self.alive:
            over = self.big.render("GAME OVER", True, COLORS["text"])
            again = self.font.render("Press R to restart", True, COLORS["text"])
            self.screen.blit(over, over.get_rect(center=(WIDTH // 2, cy - 20)))
            self.screen.blit(again, again.get_rect(center=(WIDTH // 2, cy + 20)))
        elif self.paused:
            pause = self.big.render("Paused", True, COLORS["text"])
            self.screen.blit(pause, pause.get_rect(center=(WIDTH // 2, cy)))
        pygame.display.flip()

    def run(self):
        interval = 1000 // self.speed
        last_move = pygame.time.get_ticks()
        while self.running:
            self.handle_events()
            now = pygame.time.get_ticks()
            if now - last_move >= interval:
                last_move = now
                self.update()
            self.draw()
            self.clock.tick(60)
        return self.quit_app