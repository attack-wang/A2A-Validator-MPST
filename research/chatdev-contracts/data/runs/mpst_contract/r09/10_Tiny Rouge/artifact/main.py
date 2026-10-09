import pygame, random, sys

TILE, GRID, INFO = 12, 80, 48
WALL, FLOOR, DOOR = 0, 1, 2
NAMES = ["Slime", "Bat", "Skeleton", "Ghost", "Wizard"]


def carve(g, sx, sy, tx, ty):
    # Biased random walk: always leaves a connected floor path from start to target.
    x, y = sx, sy
    g[y][x] = FLOOR
    while (x, y) != (tx, ty):
        if random.random() < 0.8:
            dx, dy = tx - x, ty - y
            if dx and (not dy or random.random() < abs(dx) / (abs(dx) + abs(dy))):
                x += 1 if dx > 0 else -1
            else:
                y += 1 if dy > 0 else -1
        else:
            ddx, ddy = random.choice(((0, 1), (0, -1), (1, 0), (-1, 0)))
            nx, ny = x + ddx, y + ddy
            if 1 <= nx < GRID - 1 and 1 <= ny < GRID - 1:
                x, y = nx, ny
        g[y][x] = FLOOR


class Game:
    def __init__(self):
        self.level, self.maxhp, self.hp = 1, 100, 100
        self.mon = None
        self.msg = "W/A/S/D to move. Reach the green door!"
        self.new_level()

    def new_level(self):
        g = [[WALL] * GRID for _ in range(GRID)]
        carve(g, 1, 1, GRID - 2, GRID - 2)
        for y in range(1, GRID - 1):
            for x in range(1, GRID - 1):
                if g[y][x] == WALL and random.random() < 0.32:
                    g[y][x] = FLOOR
        g[GRID - 2][GRID - 2] = DOOR
        self.grid = g
        self.px = self.py = 1
        self.monsters = {}
        floors = [(x, y) for y in range(GRID) for x in range(GRID)
                  if g[y][x] == FLOOR and (x, y) != (1, 1)]
        random.shuffle(floors)
        n = 6 + self.level * 2
        for x, y in floors[:n]:
            self.monsters[(x, y)] = [random.choice(NAMES),
                                     random.randint(4, 10) + self.level * 3]
        self.chests = set(floors[n:n + 3 + self.level // 2])
        self.msg = f"Floor {self.level}. Monsters: {n}, Chests: {len(self.chests)}"

    def move(self, dx, dy):
        if self.hp <= 0:
            return
        nx, ny = self.px + dx, self.py + dy
        if not (0 <= nx < GRID and 0 <= ny < GRID) or self.grid[ny][nx] == WALL:
            self.msg = "Blocked by wall."
            return
        self.px, self.py = nx, ny
        if (nx, ny) in self.monsters:
            name, mhp = self.monsters.pop((nx, ny))
            self.hp -= mhp
            self.mon = (name, mhp)
            self.msg = f"Fought {name} (HP {mhp})! Lost {mhp} HP."
            if self.hp <= 0:
                self.msg = "You died! Press R to restart."
        elif (nx, ny) in self.chests:
            self.chests.discard((nx, ny))
            heal = random.randint(20, 30)
            self.hp = min(self.maxhp, self.hp + heal)
            self.msg = f"Treasure chest! Restored {heal} HP."
        elif self.grid[ny][nx] == DOOR:
            self.level += 1
            self.new_level()


def draw(screen, game, font):
    screen.fill((25, 25, 35))
    for y in range(GRID):
        for x in range(GRID):
            t = game.grid[y][x]
            c = (60, 60, 80) if t == WALL else (205, 205, 205) if t == FLOOR else (40, 180, 60)
            pygame.draw.rect(screen, c, (x * TILE, INFO + y * TILE, TILE, TILE))
    for (x, y) in game.chests:
        pygame.draw.rect(screen, (230, 180, 30), (x * TILE + 1, INFO + y * TILE + 1, TILE - 2, TILE - 2))
    for (x, y) in game.monsters:
        pygame.draw.rect(screen, (200, 40, 40), (x * TILE + 1, INFO + y * TILE + 1, TILE - 2, TILE - 2))
    pygame.draw.rect(screen, (30, 90, 220), (game.px * TILE, INFO + game.py * TILE, TILE, TILE))
    pygame.draw.rect(screen, (245, 245, 245), (0, 0, GRID * TILE, INFO))
    hp = max(0, game.hp)
    mon = f"Last monster: {game.mon[0]} (HP {game.mon[1]})" if game.mon else "No monster encountered yet"
    screen.blit(font.render(f"HP: {hp}/{game.maxhp}   Level: {game.level}   |   {mon}", True, (0, 0, 0)), (8, 4))
    screen.blit(font.render(game.msg, True, (140, 0, 0)), (8, 26))


def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID * TILE, GRID * TILE + INFO))
    pygame.display.set_caption("Tower of the Sorcerer - Roguelike")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)
    game = Game()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                k = e.key
                if k in (pygame.K_w, pygame.K_UP):
                    game.move(0, -1)
                elif k in (pygame.K_s, pygame.K_DOWN):
                    game.move(0, 1)
                elif k in (pygame.K_a, pygame.K_LEFT):
                    game.move(-1, 0)
                elif k in (pygame.K_d, pygame.K_RIGHT):
                    game.move(1, 0)
                elif k == pygame.K_r and game.hp <= 0:
                    game.__init__()
        draw(screen, game, font)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()