import random


def valid(board, r, c, v):
    if any(board[r][j] == v for j in range(9) if j != c):
        return False
    if any(board[i][c] == v for i in range(9) if i != r):
        return False
    br, bc = 3 * (r // 3), 3 * (c // 3)
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if (i != r or j != c) and board[i][j] == v:
                return False
    return True


def solve(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for v in nums:
                    if valid(board, r, c, v):
                        board[r][c] = v
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True


def count_solutions(board, limit=2):
    count = 0

    def find_empty():
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return r, c
        return None

    def bt():
        nonlocal count
        pos = find_empty()
        if pos is None:
            count += 1
            return
        r, c = pos
        for v in range(1, 10):
            if valid(board, r, c, v):
                board[r][c] = v
                bt()
                board[r][c] = 0
                if count >= limit:
                    return

    bt()
    return count


def generate(clues=32):
    full = [[0] * 9 for _ in range(9)]
    solve(full)
    puzzle = [row[:] for row in full]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    removed = 0
    for r, c in cells:
        if removed >= 81 - clues:
            break
        backup = puzzle[r][c]
        puzzle[r][c] = 0
        if count_solutions([row[:] for row in puzzle]) != 1:
            puzzle[r][c] = backup
        else:
            removed += 1
    return full, puzzle


def display(board):
    print("\n    1 2 3   4 5 6   7 8 9")
    for r in range(9):
        if r % 3 == 0 and r > 0:
            print("   " + "-" * 21)
        row = []
        for c in range(9):
            if c % 3 == 0 and c > 0:
                row.append("|")
            row.append(str(board[r][c]) if board[r][c] else ".")
        print(f"{r + 1}  " + " ".join(row))
    print()


def read_command(prompt="> "):
    try:
        return input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt, OSError):
        print()
        return "quit"


def main():
    solution, puzzle = generate()
    board = [row[:] for row in puzzle]
    print("=== SUDOKU ===")
    print("Enter moves as: row col value  (e.g. '1 5 7'; value 0 erases).")
    print("Commands: 'check' shows mistakes, 'quit' exits.")
    while True:
        display(board)
        if all(board[r][c] != 0 for r in range(9) for c in range(9)):
            if all(board[r][c] == solution[r][c] for r in range(9) for c in range(9)):
                print("Congratulations! Puzzle completed correctly!")
                break
            print("Board is full but contains mistakes. Type 'check' or fix entries (0 erases).")
        cmd = read_command()
        if cmd == "quit":
            print("Thanks for playing!")
            break
        if cmd == "check":
            mistakes = [(r + 1, c + 1) for r in range(9) for c in range(9)
                        if board[r][c] != 0 and board[r][c] != solution[r][c]]
            if mistakes:
                print("Mistakes at: " + ", ".join(f"({r},{c})" for r, c in mistakes))
            else:
                print("No mistakes so far!")
            continue
        parts = cmd.split()
        if len(parts) != 3:
            print("Invalid input. Use 'row col value'.")
            continue
        try:
            r, c, v = int(parts[0]), int(parts[1]), int(parts[2])
        except ValueError:
            print("Numbers only, please.")
            continue
        if not (1 <= r <= 9 and 1 <= c <= 9 and 0 <= v <= 9):
            print("Row/col must be 1-9, value 0-9.")
            continue
        r -= 1
        c -= 1
        if puzzle[r][c] != 0:
            print("That cell is a fixed clue and cannot be changed.")
            continue
        if v != 0 and not valid(board, r, c, v):
            print(f"Warning: {v} conflicts with its row, column, or 3x3 box (placed anyway).")
        board[r][c] = v


if __name__ == "__main__":
    main()