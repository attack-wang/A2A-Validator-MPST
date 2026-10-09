import random


def safe_input(prompt=""):
    try:
        return input(prompt)
    except EOFError:
        print("\nInput stream closed (EOF). Exiting.")
        return "quit"
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        return "quit"


def ok(board, r, c, v):
    for i in range(9):
        if board[r][i] == v or board[i][c] == v:
            return False
    br, bc = 3 * (r // 3), 3 * (c // 3)
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if board[i][j] == v:
                return False
    return True


def solve(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for v in nums:
                    if ok(board, r, c, v):
                        board[r][c] = v
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True


def make_puzzle(holes=40):
    board = [[0] * 9 for _ in range(9)]
    solve(board)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for r, c in cells[:holes]:
        board[r][c] = 0
    return board


def display(board):
    print("    1 2 3   4 5 6   7 8 9")
    for r in range(9):
        if r % 3 == 0 and r:
            print("  ------+-------+------")
        row = []
        for c in range(9):
            if c % 3 == 0 and c:
                row.append("|")
            row.append(str(board[r][c]) if board[r][c] else ".")
        print(f"{r + 1}  " + " ".join(row))


def complete(board):
    return all(board[r][c] != 0 for r in range(9) for c in range(9))


def valid(board):
    target = list(range(1, 10))
    for r in range(9):
        if sorted(board[r]) != target:
            return False
    for c in range(9):
        if sorted(board[r][c] for r in range(9)) != target:
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            vals = [board[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)]
            if sorted(vals) != target:
                return False
    return True


def check_mistakes(board, fixed):
    mistakes = []
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v and (r, c) not in fixed:
                board[r][c] = 0
                if not ok(board, r, c, v):
                    mistakes.append((r + 1, c + 1, v))
                board[r][c] = v
    return mistakes


def main():
    board = make_puzzle()
    fixed = {(r, c) for r in range(9) for c in range(9) if board[r][c]}
    print("=== Classic Sudoku ===")
    print("Moves: row column value (e.g. 3 5 7) | 'check' | 'quit'")
    while True:
        display(board)
        if complete(board):
            if valid(board):
                print("Congratulations! Puzzle completed correctly!")
                break
            print("Board is full but contains mistakes. Fix them!")
        cmd = safe_input("> ").strip().lower()
        if cmd == "quit":
            print("Thanks for playing!")
            break
        if cmd == "check":
            mistakes = check_mistakes(board, fixed)
            if mistakes:
                for r, c, v in mistakes:
                    print(f"Mistake at row {r}, col {c}: {v} conflicts.")
            else:
                print("No mistakes so far.")
            continue
        parts = cmd.split()
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            print("Invalid input. Use: row column value")
            continue
        r, c, v = (int(p) for p in parts)
        if not (1 <= r <= 9 and 1 <= c <= 9 and 1 <= v <= 9):
            print("Row, column and value must be 1-9.")
            continue
        r -= 1
        c -= 1
        if (r, c) in fixed:
            print("That cell is a fixed clue and cannot be changed.")
            continue
        old = board[r][c]
        board[r][c] = 0
        conflict = not ok(board, r, c, v)
        board[r][c] = old
        if conflict:
            print(f"Warning: {v} conflicts with row/column/box. Place anyway? (y/n)")
            if safe_input("> ").strip().lower() != "y":
                continue
        board[r][c] = v


if __name__ == "__main__":
    main()