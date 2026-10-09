#!/usr/bin/env python3
"""Connect Four - two-player console game."""

import sys

ROWS, COLS = 6, 7
EMPTY = "."

def new_board():
    return [[EMPTY] * COLS for _ in range(ROWS)]

def print_board(board):
    print()
    for row in board:
        print(" ".join(row))
    print(" ".join(str(c) for c in range(1, COLS + 1)))
    print()

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
        for s in (1, -1):
            rr, cc = r + s * dr, c + s * dc
            while 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == disc:
                count += 1
                rr += s * dr
                cc += s * dc
        if count >= 4:
            return True
    return False

def get_move(board, player):
    while True:
        try:
            choice = input(f"Player {player}, choose a column (1-{COLS}): ").strip()
        except EOFError:
            print("\nInput stream closed. Ending game.")
            sys.exit(0)
        except KeyboardInterrupt:
            print("\nGame interrupted. Ending game.")
            sys.exit(0)
        try:
            col = int(choice) - 1
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if not 0 <= col < COLS:
            print(f"Column must be between 1 and {COLS}.")
        elif board[0][col] != EMPTY:
            print("That column is full. Choose another.")
        else:
            return col

def main():
    board = new_board()
    players = ("X", "O")
    turn = 0
    print("Welcome to Connect Four!")
    print_board(board)
    while True:
        player = players[turn % 2]
        col = get_move(board, player)
        r = drop_disc(board, col, player)
        print_board(board)
        if winning_line(board, r, col, player):
            print(f"Player {player} wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break
        turn += 1

if __name__ == "__main__":
    main()