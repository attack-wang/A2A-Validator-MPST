import os
import random
import sys
from collections import deque

SIZE = 80
WALL, FLOOR, DOOR = '#', '.', 'D'
MAXHP = 100
VIEW = 33

if os.name == 'nt':
    os.system('')  # enable ANSI escape processing on Windows terminals

DIRS = {'w': (-1, 0), 'a': (0, -1), 's': (1, 0), 'd': (0, 1),
        'W': (-1, 0), 'A': (0, -1), 'S': (1, 0), 'D': (0, 1),
        'UP': (-1, 0), 'LEFT': (0, -1), 'DOWN': (1, 0), 'RIGHT': (0, 1)}


def read_key():
    if os.name == 'nt':
        import msvcrt
        ch = msvcrt.getwch()
        if ch in ('\x00', '\xe0'):
            ext = msvcrt.getwch()
            return {'\x48': 'UP', '\x50': 'DOWN', '\x4b': 'LEFT', '\x4d': 'RIGHT'}.get(ext)
        return ch
    import termios
    import tty
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            if sys.stdin.read(1) == '[':
                return {'A': 'UP', 'B': 'DOWN', 'C': 'RIGHT', 'D': 'LEFT'}.get(sys.stdin.read(1))
            return None
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


class Monster:
    def __init__(self, level):
        self.name = random.choice(("Slime", "Bat", "Skeleton", "Ghost", "Demon", "Golem"))
        self.hp = random.randint(8, 15) + 4 * level
        self.atk = random.randint(1, 4) + level


def bfs(grid, start, goal):
    q = deque([start])
    seen = {start}
    while q:
        y, x = q.popleft()
        if (y, x) == goal:
            return True
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < SIZE and 0 <= nx < SIZE and (ny, nx) not in seen and grid[ny][nx] != WALL:
                seen.add((ny, nx))
                q.append((ny, nx))
    return False


def gen_level(level):
    while True:
        g = [[FLOOR] * SIZE for _ in range(SIZE)]
        for i in range(SIZE):
            g[0][i] = g[SIZE - 1][i] = g[i][0] = g[i][SIZE - 1] = WALL
        for y in range(1, SIZE - 1):
            for x in range(1, SIZE - 1):
                if random.random() < 0.30:
                    g[y][x] = WALL
        start, door = (1, 1), (SIZE - 2, SIZE - 2)
        g[1][1] = FLOOR
        g[SIZE - 2][SIZE - 2] = DOOR
        if bfs(g, start, door):
            break
    monsters, chests = {}, set()
    floors = [(y, x) for y in range(1, SIZE - 1) for x in range(1, SIZE - 1)
              if g[y][x] == FLOOR and (y, x) != start and (y, x) != door]
    random.shuffle(floors)
    nm = min(len(floors), 8 + 2 * level)
    for y, x in floors[:nm]:
        monsters[(y, x)] = Monster(level)
    for y, x in floors[nm:nm + 4]:
        chests.add((y, x))
    return g, start, door, monsters, chests


def draw(grid, pos, hp, level, last, mstat, monsters, chests):
    py, px = pos
    y0 = max(0, min(SIZE - VIEW, py - VIEW // 2))
    x0 = max(0, min(SIZE - VIEW, px - VIEW // 2))
    lines = ['\033[H\033[2J']
    for vy in range(VIEW):
        row = []
        for vx in range(VIEW):
            y, x = y0 + vy, x0 + vx
            row.append('@' if (y, x) == pos else 'M' if (y, x) in monsters
                       else 'C' if (y, x) in chests else grid[y][x])
        lines.append(''.join(row))
    lines.append(f"HP: {hp}/{MAXHP}  Floor: {level}  [W/A/S/D move  Q quit]")
    lines.append(last)
    lines.append("@ you  M monster  C chest  D door  # wall")
    if mstat:
        lines.append(f"Last monster: {mstat.name}  HP {mstat.hp}  ATK {mstat.atk}")
    print('\n'.join(lines), flush=True)


def main():
    level, hp = 1, MAXHP
    last = "Welcome! Reach the door (D). WASD to move, Q to quit."
    mstat = None
    while True:
        grid, pos, door, monsters, chests = gen_level(level)
        last = f"-- Floor {level} --"
        dead = False
        while True:
            draw(grid, pos, hp, level, last, mstat, monsters, chests)
            key = read_key()
            if key in ('q', 'Q', '\x03'):
                return
            if key not in DIRS:
                continue
            dy, dx = DIRS[key]
            ny, nx = pos[0] + dy, pos[1] + dx
            if not (0 <= ny < SIZE and 0 <= nx < SIZE) or grid[ny][nx] == WALL:
                last = "A wall blocks your way."
                continue
            pos = (ny, nx)
            if (ny, nx) in monsters:
                m = monsters.pop((ny, nx))
                mstat = m
                hp -= m.hp
                last = f"Fought {m.name} (HP {m.hp}, ATK {m.atk}): -{m.hp} HP"
                if hp <= 0:
                    dead = True
                    break
            elif (ny, nx) in chests:
                chests.discard((ny, nx))
                heal = random.randint(20, 30)
                hp = min(MAXHP, hp + heal)
                last = f"Treasure chest: +{heal} HP"
            elif (ny, nx) == door:
                level += 1
                break
        if dead:
            draw(grid, pos, 0, level, last, mstat, monsters, chests)
            print(f"YOU DIED on floor {level}.  [R] restart  [Q] quit", flush=True)
            if read_key() in ('r', 'R'):
                level, hp, mstat = 1, MAXHP, None
                continue
            return


if __name__ == "__main__":
    main()