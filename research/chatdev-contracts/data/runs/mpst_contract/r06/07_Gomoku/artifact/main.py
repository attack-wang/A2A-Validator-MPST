#!/usr/bin/env python3
"""Gomoku: 15x15 board, two players (Black=X, White=O); five in a row wins."""

SIZE = 15
EMPTY = "."
STONES = ("X", "O")
NAMES = ("Black", "White")
DIRS = ((0, 1), (1, 0), (1, 1), (1, -1))


def new_board():
    return [[EMPTY] * SIZE for _ in range(SIZE)]


def print_board(board):
    print("    " + " ".join("%2d" % c for c in range(SIZE)))
    for r in range(SIZE):
        print("%2d  " % r + " ".join("%2s" % cell for cell in board[r]))
    print()


def in_bounds(r, c):
    return 0 <= r < SIZE and 0 <= c < SIZE


def is_win(board, r, c):
    stone = board[r][c]
    for dr, dc in DIRS:
        count = 1
        for sign in (1, -1):
            nr, nc = r + sign * dr, c + sign * dc
            while in_bounds(nr, nc) and board[nr][nc] == stone:
                count += 1
                nr += sign * dr
                nc += sign * dc
        if count >= 5:
            return True
    return False


def board_full(board):
    return all(cell != EMPTY for row in board for cell in row)


def read_move(name, stone):
    while True:
        try:
            raw = input("%s (%s) move - 'row col' (0-14), or 'q' to quit: "
                        % (name, stone)).strip().lower()
        except (EOFError, KeyboardInterrupt):
            # stdin closed or interrupted: treat as a clean quit.
            print()
            return None
        if raw in ("q", "quit", "exit"):
            return None
        parts = raw.replace(",", " ").split()
        if len(parts) == 2:
            try:
                r, c = int(parts[0]), int(parts[1])
                if in_bounds(r, c):
                    return r, c
            except ValueError:
                pass
        print("Invalid input. Enter two numbers between 0 and 14.")


def main():
    board = new_board()
    turn = 0
    print("=== Gomoku (15x15) ===")
    print("Black=X, White=O. Five in a row (horizontal, vertical or diagonal) wins.")
    print_board(board)
    while True:
        idx = turn % 2
        move = read_move(NAMES[idx], STONES[idx])
        if move is None:
            print("Game aborted.")
            break
        r, c = move
        if board[r][c] != EMPTY:
            print("Cell already occupied. Try again.")
            continue
        board[r][c] = STONES[idx]
        print_board(board)
        if is_win(board, r, c):
            print("%s (%s) wins with five in a row!" % (NAMES[idx], STONES[idx]))
            break
        if board_full(board):
            print("Draw - the board is full.")
            break
        turn += 1


if __name__ == "__main__":
    main()