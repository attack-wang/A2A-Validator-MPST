import random, os, time

SIZE, KINDS, TARGET, MAX_MOVES = 8, 6, 1500, 25
ICONS = "RGBYPO"
ANSI = ["\033[91m", "\033[92m", "\033[94m", "\033[93m", "\033[95m", "\033[38;5;208m"]
RESET = "\033[0m"
DIRS = {"u": (-1, 0), "d": (1, 0), "l": (0, -1), "r": (0, 1)}


def find_matches(b):
    m = set()
    for r in range(SIZE):
        c = 0
        while c < SIZE - 2:
            if b[r][c] == b[r][c + 1] == b[r][c + 2]:
                v, k = b[r][c], c
                while k < SIZE and b[r][k] == v:
                    m.add((r, k)); k += 1
                c = k
            else:
                c += 1
    for c in range(SIZE):
        r = 0
        while r < SIZE - 2:
            if b[r][c] == b[r + 1][c] == b[r + 2][c]:
                v, k = b[r][c], r
                while k < SIZE and b[k][c] == v:
                    m.add((k, c)); k += 1
                r = k
            else:
                r += 1
    return m


def has_move(b):
    for r in range(SIZE):
        for c in range(SIZE):
            for dr, dc in ((0, 1), (1, 0)):
                r2, c2 = r + dr, c + dc
                if r2 < SIZE and c2 < SIZE:
                    b[r][c], b[r2][c2] = b[r2][c2], b[r][c]
                    ok = bool(find_matches(b))
                    b[r][c], b[r2][c2] = b[r2][c2], b[r][c]
                    if ok:
                        return True
    return False


def new_board():
    while True:
        b = [[random.randrange(KINDS) for _ in range(SIZE)] for _ in range(SIZE)]
        if not find_matches(b) and has_move(b):
            return b


def drop(b):
    for c in range(SIZE):
        col = [b[r][c] for r in range(SIZE) if b[r][c] >= 0]
        missing = SIZE - len(col)
        col = [random.randrange(KINDS) for _ in range(missing)] + col
        for r in range(SIZE):
            b[r][c] = col[r]


def resolve(b):
    total, chain = 0, 0
    while True:
        m = find_matches(b)
        if not m:
            return total, chain
        chain += 1
        pts = 10 * len(m) * chain
        total += pts
        for r, c in m:
            b[r][c] = -1
        drop(b)
        show(b, "Chain x%d: +%d" % (chain, pts))
        time.sleep(0.4)


def reshuffle(b):
    vals = [b[r][c] for r in range(SIZE) for c in range(SIZE)]
    while True:
        random.shuffle(vals)
        i = 0
        for r in range(SIZE):
            for c in range(SIZE):
                b[r][c] = vals[i]; i += 1
        if not find_matches(b) and has_move(b):
            return


def show(b, msg=""):
    os.system("cls" if os.name == "nt" else "clear")
    print("=== Match-3 (Candy Crush style) ===")
    print("   " + " ".join(str(c) for c in range(SIZE)))
    for r in range(SIZE):
        row = " ".join(ANSI[v] + ICONS[v] + RESET if v >= 0 else " " for v in b[r])
        print(" %d %s" % (r, row))
    print(msg)


def main():
    b = new_board()
    score, moves = 0, MAX_MOVES
    show(b, "Score %d/%d | Moves left %d | Swap: 'row col u/d/l/r' | q=quit" % (score, TARGET, moves))
    while moves > 0:
        try:
            cmd = input("swap> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return
        if cmd in ("q", "quit"):
            print("Bye!")
            return
        parts = cmd.split()
        if len(parts) != 3 or parts[2] not in DIRS or not all(p.isdigit() for p in parts[:2]):
            show(b, "Invalid input. Use: row col u/d/l/r")
            continue
        r, c, d = int(parts[0]), int(parts[1]), parts[2]
        dr, dc = DIRS[d]
        r2, c2 = r + dr, c + dc
        if not (0 <= r < SIZE and 0 <= c < SIZE and 0 <= r2 < SIZE and 0 <= c2 < SIZE):
            show(b, "Swap out of bounds.")
            continue
        b[r][c], b[r2][c2] = b[r2][c2], b[r][c]
        if not find_matches(b):
            b[r][c], b[r2][c2] = b[r2][c2], b[r][c]
            show(b, "No match there — move not used.")
            continue
        moves -= 1
        gained, chain = resolve(b)
        score += gained
        while not has_move(b):
            show(b, "No possible moves — reshuffling!")
            time.sleep(0.6)
            reshuffle(b)
        show(b, "+%d (chain x%d) | Score %d/%d | Moves left %d" % (gained, chain, score, TARGET, moves))
        if score >= TARGET:
            show(b, "YOU WIN! Final score %d in %d moves." % (score, MAX_MOVES - moves))
            return
    show(b, "GAME OVER. Final score %d (target %d)." % (score, TARGET))


if __name__ == "__main__":
    main()