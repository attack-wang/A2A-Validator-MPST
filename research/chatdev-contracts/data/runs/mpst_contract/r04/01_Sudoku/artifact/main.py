#!/usr/bin/env python3
"""Classic 9x9 Sudoku: generates puzzles, accepts player moves, checks mistakes, confirms completion."""

import random

N = 9


def is_valid(board, r, c, v):
    if any(board[r][x] == v for x in range(N)):
        return False
    if any(board[x][c] == v for x in range(N)):
        return False
    br, bc = 3 * (r // 3), 3 * (c // 3)
    return all(board[i][j] != v
               for i in range(br, br + 3)
               for j in range(bc, bc + 3))


def find_empty(board):
    for r in range(N):
        for c in range(N):
            if board[r][c] == 0:
                return r, c
    return None


def count_solutions(board, limit, shuffled):
    """Count solutions up to `limit`; leaves the board filled when a solution is found."""
    if limit <= 0:
        return 0
    pos = find_empty(board)
    if pos is None:
        return 1
    r, c = pos
    nums = list(range(1, N + 1))
    if shuffled:
        random.shuffle(nums)
    total = 0
    for v in nums:
        if is_valid(board, r, c, v):
            board[r][c] = v
            total += count_solutions(board, limit - total, shuffled)
            if total >= limit:
                return total
            board[r][c] = 0
    return total


def generate(clues):
    """Return (puzzle, solution) with a unique solution and the requested clue count."""
    board = [[0] * N for _ in range(N)]
    count_solutions(board, 1, True)
    solution = [row[:] for row in board]
    cells = [(r, c) for r in range(N) for c in range(N)]
    random.shuffle(cells)
    removed, target = 0, N * N - clues
    for r, c in cells:
        if removed >= target:
            break
        backup = board[r][c]
        board[r][c] = 0
        if count_solutions([row[:] for row in board], 2, False) != 1:
            board[r][c] = backup
        else:
            removed += 1
    return board, solution


def conflicts(board):
    """Return the set of (r, c) cells involved in row/column/box duplicates."""
    bad = set()

    def scan(cells):
        seen = {}
        for r, c in cells:
            v = board[r][c]
            if v:
                if v in seen:
                    bad.add((r, c))
                    bad.add(seen[v])
                seen[v] = (r, c)

    for r in range(N):
        scan([(r, c) for c in range(N)])
    for c in range(N):
        scan([(r, c) for r in range(N)])
    for br in range(0, N, 3):
        for bc in range(0, N, 3):
            scan([(br + i, bc + j) for i in range(3) for j in range(3)])
    return bad


def is_complete(board):
    return (all(board[r][c] != 0 for r in range(N) for c in range(N))
            and not conflicts(board))


def print_board(board, given, bad):
    print("\n    1 2 3 | 4 5 6 | 7 8 9")
    for r in range(N):
        if r in (3, 6):
            print("  ------+-------+------")
        cells = []
        for c in range(N):
            v = board[r][c]
            if v == 0:
                cells.append(".")
            elif (r, c) in bad:
                cells.append("\033[31m%d\033[0m" % v)
            elif (r, c) in given:
                cells.append(str(v))
            else:
                cells.append("\033[36m%d\033[0m" % v)
            if c in (2, 5):
                cells.append("|")
        print("%d | %s" % (r + 1, " ".join(cells)))


def parse_cell(rs, cs):
    if rs.isdigit() and cs.isdigit():
        r, c = int(rs) - 1, int(cs) - 1
        if 0 <= r < N and 0 <= c < N:
            return r, c
    print("Row and column must be numbers 1-9.")
    return None


def main():
    print("=== Classic Sudoku (9x9) ===")
    print("Fill the grid so every row, column and 3x3 box contains digits 1-9 exactly once.")
    while True:
        puzzle, solution = generate(clues=38)
        given = {(r, c) for r in range(N) for c in range(N) if puzzle[r][c]}
        board = [row[:] for row in puzzle]
        print("\nCommands: 'row col value' | 'clear row col' | 'check' | "
              "'reveal row col' | 'new' | 'quit'")
        solved = False
        while True:
            print_board(board, given, conflicts(board))
            if is_complete(board):
                print("\n*** Congratulations! The puzzle is complete and correct! ***")
                solved = True
                break
            try:
                move = input("\nMove: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                return
            parts = move.split()
            if not parts:
                continue
            cmd = parts[0]
            if cmd == "quit":
                print("Bye!")
                return
            if cmd == "new":
                break
            if cmd == "check":
                bad = conflicts(board)
                if bad:
                    print("Mistakes at: " + ", ".join(
                        "(%d,%d)" % (r + 1, c + 1) for r, c in sorted(bad)))
                else:
                    print("No mistakes so far.")
                continue
            if cmd in ("clear", "reveal", "hint") and len(parts) == 3:
                cell = parse_cell(parts[1], parts[2])
                if cell is None:
                    continue
                r, c = cell
                if (r, c) in given:
                    print("That cell is a given clue and cannot be changed.")
                    continue
                board[r][c] = 0 if cmd == "clear" else solution[r][c]
                continue
            if len(parts) == 3 and cmd.isdigit():
                cell = parse_cell(cmd, parts[1])
                if cell is None:
                    continue
                r, c = cell
                if not parts[2].isdigit() or not 1 <= int(parts[2]) <= 9:
                    print("Value must be a digit 1-9.")
                    continue
                if (r, c) in given:
                    print("That cell is a given clue and cannot be changed.")
                    continue
                board[r][c] = int(parts[2])
                continue
            print("Unknown command. Use: 'row col value', 'clear row col', "
                  "'check', 'reveal row col', 'new', 'quit'.")
        if solved:
            try:
                again = input("Play again? (y/n): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                return
            if again != "y":
                print("Thanks for playing!")
                return


if __name__ == "__main__":
    main()