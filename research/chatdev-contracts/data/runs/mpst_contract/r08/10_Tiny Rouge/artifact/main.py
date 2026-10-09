import os
import random

W = H = 80
VIEW = 25


def gen_map(level):
    g = [['#' if random.random() < 0.26 else '.' for _ in range(W)] for _ in range(H)]
    sx, sy, dx, dy = 1, 1, W - 2, H - 2
    g[sy][sx] = g[dy][dx] = '.'
    if random.random() < 0.5:
        for x in range(sx, dx + 1):
            g[sy][x] = '.'
        for y in range(sy, dy + 1):
            g[y][dx] = '.'
    else:
        for y in range(sy, dy + 1):
            g[y][sx] = '.'
        for x in range(sx, dx + 1):
            g[dy][x] = '.'
    floors = [(x, y) for y in range(H) for x in range(W)
              if g[y][x] == '.' and (x, y) not in ((sx, sy), (dx, dy))]
    random.shuffle(floors)
    n = 14 + level * 2
    monsters = {(x, y): random.randint(5, 15) + level * 3 for x, y in floors[:n]}
    chests = set(floors[n:n + 8])
    return g, (sx, sy), (dx, dy), monsters, chests


def draw(g, p, door, monsters, chests, hp, level, msg):
    px, py = p
    half = VIEW // 2
    lines = [f"Tower of the Sorcerer-like | Level {level} | HP: {hp}",
             f"Move: W/A/S/D  Quit: Q | {msg}",
             "-" * VIEW]
    for y in range(max(0, py - half), min(H, py + half + 1)):
        row = []
        for x in range(max(0, px - half), min(W, px + half + 1)):
            if (x, y) == p:
                row.append('@')
            elif (x, y) == door:
                row.append('D')
            elif (x, y) in monsters:
                row.append('M')
            elif (x, y) in chests:
                row.append('C')
            else:
                row.append(g[y][x])
        lines.append(''.join(row))
    print("\033[2J\033[H" + "\n".join(lines))


def main():
    if os.name == 'nt':
        os.system('')
    level, hp = 1, 100
    g, start, door, monsters, chests = gen_map(level)
    p = start
    msg = "Reach the door D. Fight monsters M, open chests C."
    while True:
        draw(g, p, door, monsters, chests, hp, level, msg)
        try:
            cmd = input("Move (W/A/S/D, Q quit): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return
        if cmd == 'q':
            print("\nThanks for playing!")
            return
        d = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}.get(cmd)
        if not d:
            msg = "Invalid key. Use W/A/S/D or Q."
            continue
        nx, ny = p[0] + d[0], p[1] + d[1]
        if not (0 <= nx < W and 0 <= ny < H) or g[ny][nx] == '#':
            msg = "A wall blocks your way."
            continue
        if (nx, ny) in monsters:
            mhp = monsters.pop((nx, ny))
            hp -= mhp
            msg = f"Monster encountered (HP {mhp})! You take {mhp} damage."
            if hp <= 0:
                draw(g, (nx, ny), door, monsters, chests, 0, level, msg)
                print("\nYou died. Game over.")
                return
        elif (nx, ny) in chests:
            heal = random.randint(20, 30)
            hp += heal
            chests.discard((nx, ny))
            msg = f"Treasure chest! HP +{heal} (now {hp})."
        elif (nx, ny) == door:
            level += 1
            g, start, door, monsters, chests = gen_map(level)
            p = start
            msg = f"You reached the door! Descended to level {level}."
            continue
        else:
            msg = ""
        p = (nx, ny)


if __name__ == '__main__':
    main()