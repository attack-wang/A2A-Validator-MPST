"""Connect Four - two players alternate dropping discs into a 7x6 grid."""


ROWS = 6
COLS = 7
EMPTY = "."

def new_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print()
    for row in board:
        print(" ".join(row))
    print(" ".join(str(c + 1) for c in range(COLS)))
    print()

def drop_disc(board, col, disc):
    """Drop a disc into the chosen column; return the row index or None if full."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = disc
            return r
    return None

def is_winning_move(board, row, col, disc):
    """Check all four directions from the last placed disc for a line of four."""
    directions = ((0, 1), (1, 0), (1, 1), (1, -1))
    for dr, dc in directions:
        count = 1
        for sign in (1, -1):
            r, c = row + dr * sign, col + dc * sign
            while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == disc:
                count += 1
                if count >= 4:
                    return True
                r += dr * sign
                c += dc * sign
    return False

def board_full(board):
    return all(board[0][c] != EMPTY for c in range(COLS))

def get_valid_column(board, player):
    """Prompt until the player enters a valid, non-full column number (1-7)."""
    while True:
        raw = input(f"Player {player}, choose a column (1-{COLS}): ").strip()
        if not raw.isdigit():
            print("Invalid input: please enter a number.")
            continue
        col = int(raw) - 1
        if not 0 <= col < COLS:
            print(f"Invalid column: choose between 1 and {COLS}.")
            continue
        if board[0][col] != EMPTY:
            print("That column is full. Choose another.")
            continue
        return col

def play():
    board = new_board()
    players = ("X", "O")
    turn = 0
    print("Welcome to Connect Four!")
    print_board(board)

    while True:
        player = players[turn % 2]
        col = get_valid_column(board, player)
        row = drop_disc(board, col, player)
        print_board(board)

        if is_winning_move(board, row, col, player):
            print(f"Player {player} wins! Four in a row!")
            break
        if board_full(board):
            print("It's a draw! The board is full.")
            break
        turn += 1

if __name__ == "__main__":
    play()