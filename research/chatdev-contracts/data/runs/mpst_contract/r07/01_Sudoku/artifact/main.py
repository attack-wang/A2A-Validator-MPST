import random


def valid(board, r, c, v):
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
                    if valid(board, r, c, v):
                        board[r][c] = v
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True


def count_solutions(board, limit=2):
    count = 0

    def bt():
        nonlocal count
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    for v in range(1, 10):
                        if valid(board, r, c, v):
                            board[r][c] = v
                            bt()
                            board[r][c] = 0
                            if count >= limit:
                                return
                    return
        count += 1

    bt()
    return count


def make_puzzle():
    solution = [[0] * 9 for _ in range(9)]
    solve(solution)
    puzzle = [row[:] for row in solution]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    removed = 0
    for r, c in cells:
        if removed >= 45:
            break
        backup = puzzle[r][c]
        puzzle[r][c] = 0
        if count_solutions(puzzle) != 1:
            puzzle[r][c] = backup
        else:
            removed += 1
    return solution, puzzle


def has_conflict(puzzle, r, c):
    v = puzzle[r][c]
    if v == 0:
        return False
    for i in range(9):
        if i != c and puzzle[r][i] == v:
            return True
        if i != r and puzzle[i][c] == v:
            return True
    br, bc = 3 * (r // 3), 3 * (c // 3)
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if (i, j) != (r, c) and puzzle[i][j] == v:
                return True
    return False


def display(puzzle):
    print("\n    1 2 3 | 4 5 6 | 7 8 9")
    print("   " + "-" * 22)
    for r in range(9):
        if r in (3, 6):
            print("    " + "-" * 21)
        row = []
        for c in range(9):
            if c in (3, 6):
                row.append("|")
            row.append(str(puzzle[r][c]) if puzzle[r][c] else ".")
        print("  %d %s" % (r + 1, " ".join(row)))
    print()


def main():
    print("=" * 30)
    print("        SUDOKU (9x9)")
    print("=" * 30)
    print("Each row, column and 3x3 box must contain digits 1-9 exactly once.")
    print("Commands:")
    print("  <row> <col> <value>   place a value, e.g. 3 4 5")
    print("  erase <row> <col>     clear a cell")
    print("  check                 list mistakes")
    print("  hint                  reveal one correct value")
    print("  solve                 reveal the full solution")
    print("  new                   start a new puzzle")
    print("  quit                  exit the game")
    solution, puzzle = make_puzzle()
    fixed = {(r, c) for r in range(9) for c in range(9) if puzzle[r][c]}
    while True:
        display(puzzle)
        parts = input("> ").strip().lower().split()
        if not parts:
            continue
        try:
            cmd = parts[0]
            if cmd == "quit":
                print("Thanks for playing!")
                break
            if cmd == "new":
                solution, puzzle = make_puzzle()
                fixed = {(r, c) for r in range(9) for c in range(9) if puzzle[r][c]}
                print("New puzzle generated!")
                continue
            if cmd == "check":
                bad = [(r + 1, c + 1) for r in range(9) for c in range(9)
                       if puzzle[r][c] and (has_conflict(puzzle, r, c)
                                            or puzzle[r][c] != solution[r][c])]
                if bad:
                    print("Mistakes at: " + ", ".join(f"({r},{c})" for r, c in bad))
                else:
                    print("No mistakes so far. Keep going!")
                continue
            if cmd == "hint":
                empty = [(r, c) for r in range(9) for c in range(9) if puzzle[r][c] == 0]
                if not empty:
                    print("No empty cells left.")
                    continue
                r, c = random.choice(empty)
                puzzle[r][c] = solution[r][c]
                print(f"Hint: ({r + 1},{c + 1}) = {solution[r][c]}")
            elif cmd == "solve":
                puzzle = [row[:] for row in solution]
                print("Solution revealed.")
            elif cmd == "erase" and len(parts) == 3:
                r, c = int(parts[1]) - 1, int(parts[2]) - 1
                if not (0 <= r < 9 and 0 <= c < 9):
                    print("Row and column must be 1-9.")
                    continue
                if (r, c) in fixed:
                    print("That cell is a given clue and cannot be erased.")
                    continue
                puzzle[r][c] = 0
            else:
                if len(parts) != 3:
                    print("Unknown command.")
                    continue
                r, c, v = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
                if not (0 <= r < 9 and 0 <= c < 9):
                    print("Row and column must be 1-9.")
                    continue
                if not (1 <= v <= 9):
                    print("Value must be 1-9.")
                    continue
                if (r, c) in fixed:
                    print("That cell is a given clue and cannot be changed.")
                    continue
                puzzle[r][c] = v
                if has_conflict(puzzle, r, c):
                    print(f"Mistake: {v} conflicts with a digit in its row, column or box.")
                else:
                    print(f"Placed {v} at ({r + 1},{c + 1}).")
            if puzzle == solution:
                display(puzzle)
                print("Congratulations! You completed the puzzle correctly!")
                break
        except (ValueError, IndexError):
            print("Invalid input. Use: <row> <col> <value>")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")