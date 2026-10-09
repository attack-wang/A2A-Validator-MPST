import random


def valid(board, r, c, n):
    if n in board[r]:
        return False
    if any(board[i][c] == n for i in range(9)):
        return False
    br, bc = 3 * (r // 3), 3 * (c // 3)
    return all(board[i][j] != n for i in range(br, br + 3) for j in range(bc, bc + 3))


def solve(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for n in nums:
                    if valid(board, r, c, n):
                        board[r][c] = n
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True


def make_puzzle():
    board = [[0] * 9 for _ in range(9)]
    solve(board)
    puzzle = [row[:] for row in board]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for r, c in cells[:45]:
        puzzle[r][c] = 0
    return board, puzzle


def display(puzzle):
    print("\n    1 2 3   4 5 6   7 8 9")
    for r in range(9):
        if r % 3 == 0 and r:
            print("  " + "-" * 21)
        row = []
        for c in range(9):
            if c % 3 == 0 and c:
                row.append("|")
            row.append(str(puzzle[r][c]) if puzzle[r][c] else ".")
        print(f"{r + 1}  " + " ".join(row))
    print()


def read_move():
    try:
        return input("Move (row col value) or 'q': ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"


def main():
    solution, puzzle = make_puzzle()
    fixed = {(r, c) for r in range(9) for c in range(9) if puzzle[r][c]}
    print("=== Classic Sudoku ===")
    print("Fill the grid so every row, column and 3x3 box has digits 1-9.")
    print("Enter moves as: row col value (e.g. 1 5 7). Enter 'q' to quit.")
    while True:
        display(puzzle)
        move = read_move()
        if move == "q":
            print("Thanks for playing! Goodbye.")
            break
        parts = move.split()
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            print("Invalid input. Use: row col value")
            continue
        r, c, v = (int(p) - 1 for p in parts)
        if not (0 <= r < 9 and 0 <= c < 9 and 0 <= v < 9):
            print("Row/col must be 1-9 and value must be 1-9.")
            continue
        if (r, c) in fixed:
            print("That cell is a given clue and cannot be changed.")
            continue
        if puzzle[r][c] != 0:
            print("That cell is already filled. Choose an empty cell ('.').")
            continue
        if solution[r][c] != v + 1:
            print(f"Mistake! {v + 1} is not correct for row {r + 1}, column {c + 1}.")
            continue
        puzzle[r][c] = v + 1
        if all(puzzle[i][j] != 0 for i in range(9) for j in range(9)):
            display(puzzle)
            print("Congratulations! The puzzle is complete and fully correct!")
            break


if __name__ == "__main__":
    main()