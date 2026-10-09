import random


def ok(b, r, c, v):
    if v in b[r]:
        return False
    if any(b[i][c] == v for i in range(9)):
        return False
    br, bc = 3 * (r // 3), 3 * (c // 3)
    return all(b[i][j] != v for i in range(br, br + 3) for j in range(bc, bc + 3))


def fill(b):
    for r in range(9):
        for c in range(9):
            if b[r][c] == 0:
                vs = list(range(1, 10))
                random.shuffle(vs)
                for v in vs:
                    if ok(b, r, c, v):
                        b[r][c] = v
                        if fill(b):
                            return True
                        b[r][c] = 0
                return False
    return True


def new_puzzle(holes=45):
    b = [[0] * 9 for _ in range(9)]
    fill(b)
    sol = [row[:] for row in b]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for r, c in cells[:holes]:
        b[r][c] = 0
    return b, sol


def show(b):
    print("    1 2 3   4 5 6   7 8 9")
    for r in range(9):
        if r % 3 == 0 and r:
            print("   " + "-" * 21)
        row = []
        for c in range(9):
            if c % 3 == 0 and c:
                row.append("|")
            row.append(str(b[r][c]) if b[r][c] else ".")
        print(f"{r + 1}  " + " ".join(row))


def conflicts(b):
    bad = set()
    for r in range(9):
        for c in range(9):
            v = b[r][c]
            if v:
                for i in range(9):
                    if i != c and b[r][i] == v:
                        bad.add((r, c))
                    if i != r and b[i][c] == v:
                        bad.add((r, c))
                br, bc = 3 * (r // 3), 3 * (c // 3)
                for i in range(br, br + 3):
                    for j in range(bc, bc + 3):
                        if (i, j) != (r, c) and b[i][j] == v:
                            bad.add((r, c))
    return bad


def done(b):
    return all(b[r][c] != 0 for r in range(9) for c in range(9)) and not conflicts(b)


def main():
    puzzle, solution = new_puzzle()
    print("=== Sudoku ===")
    print("Moves: row col value (e.g. 3 4 7); value 0 clears a cell.")
    print("Commands: check | hint | quit")
    while True:
        show(puzzle)
        bad = conflicts(puzzle)
        if bad:
            print("Mistakes at: " + ", ".join(f"({r + 1},{c + 1})" for r, c in sorted(bad)))
        if done(puzzle):
            print("Congratulations! Puzzle completed correctly!")
            break
        try:
            s = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break
        if s == "quit":
            print("Bye.")
            break
        if s == "check":
            cur = conflicts(puzzle)
            print("Mistakes: " + (", ".join(f"({r + 1},{c + 1})" for r, c in sorted(cur)) or "none"))
            continue
        if s == "hint":
            empties = [(r, c) for r in range(9) for c in range(9) if puzzle[r][c] == 0]
            if empties:
                r, c = random.choice(empties)
                puzzle[r][c] = solution[r][c]
                print(f"Hint: ({r + 1},{c + 1}) = {solution[r][c]}")
            else:
                print("No empty cells.")
            continue
        parts = s.split()
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            print("Invalid input.")
            continue
        r, c, v = map(int, parts)
        if not (1 <= r <= 9 and 1 <= c <= 9 and 0 <= v <= 9):
            print("Out of range.")
            continue
        puzzle[r - 1][c - 1] = v


if __name__ == "__main__":
    main()