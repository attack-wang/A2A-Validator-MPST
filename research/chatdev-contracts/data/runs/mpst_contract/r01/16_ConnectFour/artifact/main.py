"""Connect Four: two-player console game."""

import sys

ROWS, COLS = 6, 7
EMPTY = "."
DISCS = {1: "X", 2: "O"}


def new_board():
    return [[EMPTY] * COLS for _ in range(ROWS)]


def print_board(board):
    for row in board:
        print(" ".join(row))
    print(" ".join(str(c + 1) for c in range(COLS)))


def drop_disc(board, col, disc):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = disc
            return r
    return -1


def is_full(board):
    return all(board[0][c] != EMPTY for c in range(COLS))


def winning_line(board, r, c, disc):
    for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
        count = 1
        for sign in (1, -1):
            nr, nc = r + dr * sign, c + dc * sign
            while 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == disc:
                count += 1
                nr += dr * sign
                nc += dc * sign
        if count >= 4:
            return True
    return False


def get_move(board, player):
    while True:
        try:
            raw = input(f"Player {player} ({DISCS[player]}), choose a column (1-{COLS}): ").strip()
        except EOFError:
            print("\nInput stream closed. Exiting Connect Four.")
            sys.exit(0)
        if not raw.isdigit():
            print("Invalid input: please enter a number.")
            continue
        col = int(raw) - 1
        if not 0 <= col < COLS:
            print(f"Column must be between 1 and {COLS}.")
            continue
        if board[0][col] != EMPTY:
            print("That column is full. Choose another.")
            continue
        return col


def main():
    board = new_board()
    player = 1
    print("Welcome to Connect Four! Form a line of four to win.")
    print_board(board)
    while True:
        col = get_move(board, player)
        r = drop_disc(board, col, DISCS[player])
        print_board(board)
        if winning_line(board, r, col, DISCS[player]):
            print(f"Player {player} ({DISCS[player]}) wins!")
            break
        if is_full(board):
            print("The grid is full. It's a draw!")
            break
        player = 2 if player == 1 else 1


if __name__ == "__main__":
    main()