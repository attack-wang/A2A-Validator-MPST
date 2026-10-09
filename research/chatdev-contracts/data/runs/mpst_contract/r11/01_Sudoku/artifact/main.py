import random


def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None


def valid(board, r, c, v):
    if any(board[r][x] == v for x in range(9)):
        return False
    if any(board[x][c] == v for x in range(9)):
        return False
    br, bc = 3 * (r // 3), 3 * (c // 3)
    return all(board[i][j] != v
               for i in range(br, br + 3)
               for j in range(bc, bc + 3))


def solve(board):
    pos = find_empty(board)
    if pos is None:
        return True
    r, c = pos
    for v in random.sample(range(1, 10), 9):
        if valid(board, r, c, v):
            board[r][c] = v
            if solve(board):
                return True
            board[r][c] = 0
    return False


def make_puzzle(holes=45):
    full = [[0] * 9 for _ in range(9)]
    solve(full)
    puzzle = [row[:] for row in full]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for r, c in cells[:holes]:
        puzzle[r][c] = 0
    return full, puzzle


def display(board, fixed):
    print("    1 2 3   4 5 6   7 8 9")
    print("  +-------+-------+-------+")
    for r in range(9):
        if r in (3, 6):
            print("  +-------+-------+-------+")
        cells = []
        for c in range(9):
            v = board[r][c]
            if v == 0:
                cells.append(".")
            elif fixed[r][c]:
                cells.append("\033[94m%d\033[0m" % v)
            else:
                cells.append("\033[92m%d\033[0m" % v)
        print("%d | " % (r + 1) + " ".join(cells[:3]) + " | "
              + " ".join(cells[3:6]) + " | " + " ".join(cells[6:]) + " |")
    print("  +-------+-------+-------+")


def find_mistakes(board):
    bad = []
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v:
                board[r][c] = 0
                if not valid(board, r, c, v):
                    bad.append((r, c))
                board[r][c] = v
    return bad


def is_complete(board):
    return all(board[r][c] != 0 for r in range(9) for c in range(9))


def main():
    solution, puzzle = make_puzzle()
    board = [row[:] for row in puzzle]
    fixed = [[puzzle[r][c] != 0 for c in range(9)] for r in range(9)]
    print("=== Classic Sudoku ===")
    print("Moves: 'row col value' (e.g. '1 5 7'); value 0 erases a cell.")
    print("Commands: check | hint | solve | quit")
    display(board, fixed)
    while True:
        try:
            raw = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return
        if raw == "quit":
            print("Bye!")
            return
        if raw == "solve":
            display(solution, [[True] * 9 for _ in range(9)])
            print("Solution shown. Game over.")
            return
        if raw == "hint":
            empties = [(r, c) for r in range(9) for c in range(9)
                       if board[r][c] == 0]
            if empties:
                r, c = random.choice(empties)
                board[r][c] = solution[r][c]
                display(board, fixed)
            else:
                print("No empty cells left.")
            continue
        parts = raw.split()
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            print("Invalid input. Use: row col value")
            continue
        r, c, v = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
        if not (0 <= r < 9 and 0 <= c < 9 and 0 <= v <= 9):
            print("Row/col must be 1-9 and value 0-9 (0 erases).")
            continue
        if fixed[r][c]:
            print("That cell is a given clue and cannot be changed.")
            continue
        board[r][c] = 0
        conflict = v and not valid(board, r, c, v)
        board[r][c] = v
        display(board, fixed)
        if conflict:
            print("Mistake! %d conflicts in its row, column, or 3x3 box." % v)
        if is_complete(board):
            if not find_mistakes(board):
                print("Congratulations! The puzzle is completed correctly!")
                return
            print("Board is full but contains mistakes. Use 'check' to fix.")


if __name__ == "__main__":
    main()