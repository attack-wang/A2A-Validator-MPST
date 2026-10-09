import pygame, random

pygame.init()
CELL, COLS, ROWS, PANEL = 30, 10, 20, 200
W, H = COLS * CELL + PANEL, ROWS * CELL
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
big = pygame.font.SysFont("arial", 40, bold=True)

COLORS = {'I': (0, 200, 255), 'O': (255, 200, 0), 'T': (170, 0, 220),
          'S': (0, 220, 0), 'Z': (230, 0, 0), 'J': (0, 60, 230), 'L': (255, 140, 0)}

BASE = {
    'I': ([(0, 1), (1, 1), (2, 1), (3, 1)], 4),
    'O': ([(0, 0), (1, 0), (0, 1), (1, 1)], 2),
    'T': ([(0, 1), (1, 1), (2, 1), (1, 0)], 3),
    'S': ([(1, 0), (2, 0), (0, 1), (1, 1)], 3),
    'Z': ([(0, 0), (1, 0), (1, 1), (2, 1)], 3),
    'J': ([(0, 0), (0, 1), (1, 1), (2, 1)], 3),
    'L': ([(2, 0), (0, 1), (1, 1), (2, 1)], 3),
}

def rot(cells, n):
    return [(n - 1 - y, x) for x, y in cells]

SHAPES = {}
for k, (cells, n) in BASE.items():
    states, cur = [], cells
    for _ in range(4):
        if cur in states:
            break
        states.append(cur)
        cur = rot(cur, n)
    SHAPES[k] = states

class Piece:
    def __init__(self, kind):
        self.kind, self.r, self.x, self.y = kind, 0, COLS // 2 - 2, 0

    def cells(self, r=None, x=None, y=None):
        r = self.r if r is None else r
        x = self.x if x is None else x
        y = self.y if y is None else y
        states = SHAPES[self.kind]
        return [(cx + x, cy + y) for cx, cy in states[r % len(states)]]

class Game:
    def __init__(self):
        self.grid = [[None] * COLS for _ in range(ROWS)]
        self.bag, self.score, self.lines = [], 0, 0
        self.over, self.acc, self.interval = False, 0, 800
        self.next = self.pull()
        self.spawn()

    def pull(self):
        if not self.bag:
            self.bag = list(SHAPES)
            random.shuffle(self.bag)
        return self.bag.pop()

    def spawn(self):
        self.cur = Piece(self.next)
        self.next = self.pull()
        if self.hit(self.cur.cells()):
            self.over = True

    def hit(self, cells):
        return any(x < 0 or x >= COLS or y >= ROWS or (y >= 0 and self.grid[y][x]) for x, y in cells)

    def move(self, dx, dy):
        p = self.cur
        c = p.cells(x=p.x + dx, y=p.y + dy)
        if not self.hit(c):
            p.x += dx
            p.y += dy
            return True
        return False

    def rotate(self):
        p = self.cur
        n = len(SHAPES[p.kind])
        for k in (0, -1, 1, -2, 2):
            if not self.hit(p.cells(r=(p.r + 1) % n, x=p.x + k)):
                p.r = (p.r + 1) % n
                p.x += k
                return True
        return False

    def lock(self):
        for x, y in self.cur.cells():
            if y >= 0:
                self.grid[y][x] = self.cur.kind
        full = [i for i, row in enumerate(self.grid) if all(row)]
        for i in full:
            del self.grid[i]
            self.grid.insert(0, [None] * COLS)
        if full:
            lvl = self.lines // 10 + 1
            self.lines += len(full)
            self.score += {1: 100, 2: 300, 3: 500, 4: 800}[len(full)] * lvl
        self.spawn()

    def soft(self):
        if self.move(0, 1):
            self.score += 1
        else:
            self.lock()

    def hard(self):
        n = 0
        while self.move(0, 1):
            n += 1
        self.score += n * 2
        self.lock()

    def update(self, dt):
        self.interval = max(80, 800 - (self.lines // 10) * 70)
        self.acc += dt
        if self.acc >= self.interval:
            self.acc = 0
            if not self.move(0, 1):
                self.lock()

def draw_cell(surf, x, y, color):
    r = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
    pygame.draw.rect(surf, color, r)
    pygame.draw.rect(surf, (20, 20, 30), r, 1)

def draw(g, paused):
    screen.fill((15, 15, 25))
    for y in range(ROWS):
        for x in range(COLS):
            if g.grid[y][x]:
                draw_cell(screen, x, y, COLORS[g.grid[y][x]])
    if g.cur and not g.over:
        for x, y in g.cur.cells():
            if y >= 0:
                draw_cell(screen, x, y, COLORS[g.cur.kind])
    px = COLS * CELL
    pygame.draw.rect(screen, (40, 40, 55), (px, 0, PANEL, H))
    for i, txt in enumerate(["Score: %d" % g.score, "Lines: %d" % g.lines, "Level: %d" % (g.lines // 10 + 1)]):
        screen.blit(font.render(txt, True, (255, 255, 255)), (px + 20, 20 + i * 30))
    screen.blit(font.render("Next:", True, (255, 255, 255)), (px + 20, 120))
    off = SHAPES[g.next][0]
    minx = min(c[0] for c in off)
    miny = min(c[1] for c in off)
    for cx, cy in off:
        r = pygame.Rect(px + 20 + (cx - minx) * CELL, 150 + (cy - miny) * CELL, CELL, CELL)
        pygame.draw.rect(screen, COLORS[g.next], r)
        pygame.draw.rect(screen, (20, 20, 30), r, 1)
    for i, s in enumerate(["Arrows: move/rotate", "Down: soft drop", "Space: hard drop", "P: pause", "R: restart"]):
        screen.blit(font.render(s, True, (180, 180, 190)), (px + 20, H - 140 + i * 24))
    if g.over:
        ov = pygame.Surface((COLS * CELL, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 180))
        screen.blit(ov, (0, 0))
        screen.blit(big.render("GAME OVER", True, (255, 60, 60)), (20, H // 2 - 40))
        screen.blit(font.render("Press R to restart", True, (255, 255, 255)), (20, H // 2 + 10))
    elif paused:
        screen.blit(big.render("PAUSED", True, (255, 255, 255)), (60, H // 2 - 20))

def main():
    game = Game()
    paused = False
    while True:
        dt = clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    game = Game()
                    paused = False
                if game.over:
                    continue
                if e.key == pygame.K_p:
                    paused = not paused
                if paused:
                    continue
                if e.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif e.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif e.key == pygame.K_DOWN:
                    game.soft()
                elif e.key == pygame.K_UP:
                    game.rotate()
                elif e.key == pygame.K_SPACE:
                    game.hard()
        if not game.over and not paused:
            game.update(dt)
        draw(game, paused)
        pygame.display.flip()

if __name__ == "__main__":
    main()