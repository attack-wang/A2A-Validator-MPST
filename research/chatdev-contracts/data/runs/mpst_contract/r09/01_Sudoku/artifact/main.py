import random


def find_empty(b):
    for r in range(9):
        for c in range(9):
            if b[r][c] == 0:
                return r, c
    return None


def ok(b, r, c, v):
    if any(b[r][j] == v for j in range(9)):
        return False
    if any(b[i][c] == v for i in range(9)):
        return False
    br, bc = 3 * (r // 3), 3 * (c // 3)
    return all(b[i][j] != v for i in range(br, br + 3) for j in range(bc, bc + 3))


def fill(b):
    pos = find_empty(b)
    if pos is None:
        return True
    r, c = pos
    nums = list(range(1, 10))
    random.shuffle(nums)
    for v in nums:
        if ok(b, r, c, v):
            b[r][c] = v
            if fill(b):
                return True
            b[r][c] = 0
    return False


def count_solutions(b, limit=2):
    cnt = 0

    def bt():
        nonlocal cnt
        pos = find_empty(b)
        if pos is None:
            cnt += 1
            return
        r, c = pos
        for v in range(1, 10):
            if ok(b, r, c, v):
                b[r][c] = v
                bt()
                b[r][c] = 0
                if cnt >= limit:
                    return

    bt()
    return cnt


def new_puzzle(target=36):
    b = [[0] * 9 for _ in range(9)]
    fill(b)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    givens = 81
    for r, c in cells:
        if givens <= target:
            break
        keep = b[r][c]
        b[r][c] = 0
        if count_solutions([row[:] for row in b]) != 1:
            b[r][c] = keep
        else:
            givens -= 1
    return b


def conflicts(b):
    bad = set()
    for r in range(9):
        seen = {}
        for c in range(9):
            v = b[r][c]
            if v:
                if v in seen:
                    bad.add((r, c))
                    bad.add((r, seen[v]))
                seen[v] = c
    for c in range(9):
        seen = {}
        for r in range(9):
            v = b[r][c]
            if v:
                if v in seen:
                    bad.add((r, c))
                    bad.add((seen[v], c))
                seen[v] = r
    for br in (0, 3, 6):
        for bc in (0, 3, 6):
            seen = {}
            for i in range(br, br + 3):
                for j in range(bc, bc + 3):
                    v = b[i][j]
                    if v:
                        if v in seen:
                            bad.add((i, j))
                            bad.add(seen[v])
                        seen[v] = (i, j)
    return bad


def render(b):
    print("\n   1 2 3 | 4 5 6 | 7 8 9")
    for r in range(9):
        if r in (3, 6):
            print("   ------+-------+------")
        row = []
        for c in range(9):
            if c in (3, 6):
                row.append("|")
            row.append(str(b[r][c]) if b[r][c] else ".")
        print(f"{r + 1}  " + " ".join(row))
    print()


HELP = """Commands:
  <row> <col> <value>   place a value, e.g. 3 5 7
  clear <row> <col>     erase a cell, e.g. clear 3 5
  check                 report mistake cells
  new                   start a fresh puzzle
  help                  show this help
  quit                  exit the game"""


def main():
    print("=== Classic Sudoku 9x9 ===")
    print("Fill the grid so every row, column and 3x3 box has digits 1-9 exactly once.")
    print(HELP)
    board = new_puzzle()
    given = [[board[r][c] != 0 for c in range(9)] for r in range(9)]
    while True:
        render(board)
        bad = conflicts(board)
        if bad:
            print("Mistakes (row,col): " + ", ".join(f"({r + 1},{c + 1})" for r, c in sorted(bad)))
        if all(board[r][c] != 0 for r in range(9) for c in range(9)) and not bad:
            print("Congratulations! The puzzle is completed correctly!")
            break
        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return
        parts = cmd.split()
        if cmd in ("quit", "exit"):
            print("Bye!")
            return
        if cmd == "help":
            print(HELP)
        elif cmd == "new":
            board = new_puzzle()
            given = [[board[r][c] != 0 for c in range(9)] for r in range(9)]
            print("New puzzle started.")
        elif cmd == "check":
            if bad:
                print("Mistakes (row,col): " + ", ".join(f"({r + 1},{c + 1})" for r, c in sorted(bad)))
            else:
                print("No mistakes so far.")
        elif parts and parts[0] == "clear" and len(parts) == 3 and all(p.isdigit() for p in parts[1:]):
            r, c = int(parts[1]) - 1, int(parts[2]) - 1
            if not (0 <= r < 9 and 0 <= c < 9):
                print("Row and column must be 1-9.")
            elif given[r][c]:
                print("That cell is a fixed clue and cannot be cleared.")
            else:
                board[r][c] = 0
        elif len(parts) == 3 and all(p.isdigit() for p in parts):
            r, c, v = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
            if not (0 <= r < 9 and 0 <= c < 9 and 1 <= v <= 9):
                print("Use row 1-9, column 1-9, value 1-9.")
            elif given[r][c]:
                print("That cell is a fixed clue.")
            else:
                board[r][c] = v
        else:
            print("Unknown command. Type 'help'.")


if __name__ == "__main__":
    main()