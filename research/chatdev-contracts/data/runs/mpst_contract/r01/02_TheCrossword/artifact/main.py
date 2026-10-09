"""Console crossword puzzle: fill words by clue number and direction."""

ROWS, COLS = 5, 6

# (number, direction, row, col, answer, clue)
PUZZLE = [
    (1, "across", 0, 0, "PYTHON", "Programming language named after a comedy troupe"),
    (4, "across", 2, 0, "PIANO", "Keyboard with black and white keys"),
    (5, "across", 3, 2, "MAR", "To damage or spoil"),
    (1, "down", 0, 0, "PUP", "Young dog"),
    (2, "down", 0, 2, "TRAM", "Streetcar"),
    (3, "down", 0, 4, "ODOR", "Distinctive smell"),
]

grid = [[None] * COLS for _ in range(ROWS)]
STARTS = {}


def cells(p):
    _, d, r, c, w, _ = p
    dr, dc = (0, 1) if d == "across" else (1, 0)
    return [(r + dr * i, c + dc * i) for i in range(len(w))]


def build():
    for p in PUZZLE:
        n, _, r, c, _, _ = p
        STARTS[(r, c)] = n
        for (rr, cc) in cells(p):
            if grid[rr][cc] is None:
                grid[rr][cc] = ""


def lookup(num, d):
    for p in PUZZLE:
        if p[0] == num and p[1] == d:
            return p
    return None


def solved(p):
    return all(grid[r][c] == ch for (r, c), ch in zip(cells(p), p[4]))


def done():
    return all(solved(p) for p in PUZZLE)


def show():
    print("    " + "".join(f"{c:^4}" for c in range(COLS)))
    for r in range(ROWS):
        line = f"{r:>3} "
        for c in range(COLS):
            v = grid[r][c]
            if v is None:
                line += " ## "
            elif v:
                line += f" {v}  "
            else:
                n = STARTS.get((r, c))
                label = str(n) if n else "_"
                line += f" {label:<2} "
        print(line)


def show_clues():
    for d in ("across", "down"):
        print(d.upper() + ":")
        for p in sorted((q for q in PUZZLE if q[1] == d), key=lambda q: q[0]):
            print(f"  {p[0]}. {p[5]} ({len(p[4])})")


def parse_dir(s):
    s = s.lower()
    if s in ("a", "across"):
        return "across"
    if s in ("d", "down"):
        return "down"
    return None


def fill(num, d, word):
    p = lookup(num, d)
    if not p:
        print("No such clue.")
        return
    word = word.upper()
    if not word.isalpha():
        print("Use letters only.")
        return
    if len(word) != len(p[4]):
        print(f"Expected {len(p[4])} letters.")
        return
    for i, (r, c) in enumerate(cells(p)):
        cur = grid[r][c]
        if cur and cur != word[i]:
            print(f"'{word[i]}' conflicts with '{cur}' already on the grid.")
            return
    if word != p[4]:
        print("Those letters fit the grid but are not correct for this clue.")
        return
    for i, (r, c) in enumerate(cells(p)):
        grid[r][c] = word[i]
    print("Accepted.")


def clear(num, d):
    p = lookup(num, d)
    if not p:
        print("No such clue.")
        return
    for (r, c) in cells(p):
        if grid[r][c] is None:
            continue
        shared = any(q is not p and solved(q) and (r, c) in cells(q) for q in PUZZLE)
        if not shared:
            grid[r][c] = ""
    print("Cleared.")


def main():
    build()
    print("Crossword! Enter a word as: <clue number> <across|down> <word>")
    print("Other commands: clear <num> <across|down> | quit")
    show_clues()
    show()
    while True:
        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not cmd:
            continue
        parts = cmd.split()
        low = parts[0].lower()
        if low in ("quit", "exit"):
            break
        if low == "clear":
            if len(parts) < 3 or not parts[1].isdigit() or not parse_dir(parts[2]):
                print("Usage: clear <num> <across|down>")
                continue
            clear(int(parts[1]), parse_dir(parts[2]))
        elif len(parts) >= 3 and parts[0].isdigit():
            d = parse_dir(parts[1])
            if not d:
                print("Direction must be across or down.")
                continue
            fill(int(parts[0]), d, "".join(parts[2:]))
        else:
            print("Usage: <clue number> <across|down> <word>")
        show()
        if done():
            print("Congratulations - the puzzle is complete!")
            break


if __name__ == "__main__":
    main()