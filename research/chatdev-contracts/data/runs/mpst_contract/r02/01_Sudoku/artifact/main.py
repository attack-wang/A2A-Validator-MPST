import random


def make_empty_board():
    return [[0] * 9 for _ in range(9)]


def is_valid(board, row, col, val):
    if val in board[row]:
        return False
    for r in range(9):
        if board[r][col] == val:
            return False
    br, bc = 3 * (row // 3), 3 * (col // 3)
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if board[r][c] == val:
                return False
    return True


def solve(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for v in nums:
                    if is_valid(board, r, c, v):
                        board[r][c] = v
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True


def count_solutions(board, limit=2):
    count = 0

    def backtrack():
        nonlocal count
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    for v in range(1, 10):
                        if is_valid(board, r, c, v):
                            board[r][c] = v
                            backtrack()
                            board[r][c] = 0
                            if count >= limit:
                                return
                    return
        count += 1

    backtrack()
    return count


def generate_puzzle(holes=45):
    full = make_empty_board()
    solve(full)
    puzzle = [row[:] for row in full]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    removed = 0
    for r, c in cells:
        if removed >= holes:
            break
        backup = puzzle[r][c]
        puzzle[r][c] = 0
        if count_solutions([row[:] for row in puzzle]) != 1:
            puzzle[r][c] = backup
        else:
            removed += 1
    return puzzle, full


def find_conflicts(board):
    conflicts = set()

    def scan(cells):
        seen = {}
        for pos, v in cells:
            if v:
                if v in seen:
                    conflicts.add(pos)
                    conflicts.add(seen[v])
                seen[v] = pos

    for r in range(9):
        scan([((r, c), board[r][c]) for c in range(9)])
    for c in range(9):
        scan([((r, c), board[r][c]) for r in range(9)])
    for br in (0, 3, 6):
        for bc in (0, 3, 6):
            scan([((r, c), board[r][c])
                  for r in range(br, br + 3) for c in range(bc, bc + 3)])
    return conflicts


def print_board(board):
    print("\n    1 2 3   4 5 6   7 8 9")
    for r in range(9):
        if r in (3, 6):
            print("    ------+-------+------")
        line = f"  {r + 1} "
        for c in range(9):
            if c in (3, 6):
                line += "| "
            line += (str(board[r][c]) if board[r][c] else ".") + " "
        print(line)
    print()


def new_game():
    puzzle, solution = generate_puzzle()
    board = [row[:] for row in puzzle]
    fixed = {(r, c) for r in range(9) for c in range(9) if puzzle[r][c]}
    return board, solution, fixed


def main():
    print("=== Classic Sudoku (9x9) ===")
    print("Fill the grid so every row, column and 3x3 box has digits 1-9 once.")
    print("Place a value:  <row> <col> <value>   (e.g. 3 7 5; value 0 clears a cell)")
    print("Commands: check | hint | solve | new | quit")
    board, solution, fixed = new_game()
    while True:
        print_board(board)
        if all(board[r][c] for r in range(9) for c in range(9)) and not find_conflicts(board):
            print("Congratulations! The puzzle is complete and correct!")
            break
        cmd = input("> ").strip().lower()
        if cmd == "quit":
            print("Thanks for playing!")
            break
        if cmd == "new":
            board, solution, fixed = new_game()
            continue
        if cmd == "solve":
            board = [row[:] for row in solution]
            continue
        if cmd == "hint":
            empties = [(r, c) for r in range(9) for c in range(9) if not board[r][c]]
            if empties:
                r, c = random.choice(empties)
                board[r][c] = solution[r][c]
                print(f"Hint: ({r + 1},{c + 1}) = {board[r][c]}")
            else:
                print("No empty cells left.")
            continue
        if cmd == "check":
            conflicts = find_conflicts(board)
            if conflicts:
                spots = ", ".join(f"({r + 1},{c + 1})" for r, c in sorted(conflicts))
                print(f"Mistakes found at: {spots}")
            else:
                print("No mistakes so far. Keep going!")
            continue
        parts = cmd.split()
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            r, c, v = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
            if not (0 <= r <= 8 and 0 <= c <= 8 and 0 <= v <= 9):
                print("Row and column must be 1-9; value must be 0-9.")
                continue
            if (r, c) in fixed:
                print("That cell is a fixed clue and cannot be changed.")
                continue
            board[r][c] = v
        else:
            print("Invalid input. Use '<row> <col> <value>' or a command.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nThanks for playing!")