import random

SIZE = 4
DIRECTIONS = ('up', 'down', 'left', 'right')
KEYMAP = {
    'w': 'up', 'up': 'up', '\x1b[a': 'up',
    's': 'down', 'down': 'down', '\x1b[b': 'down',
    'a': 'left', 'left': 'left', '\x1b[d': 'left',
    'd': 'right', 'right': 'right', '\x1b[c': 'right',
}


def new_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_tile(board)
    add_tile(board)
    return board


def add_tile(board):
    empties = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if not empties:
        return
    r, c = random.choice(empties)
    board[r][c] = 2 if random.random() < 0.9 else 4


def slide_left(row):
    tiles = [v for v in row if v]
    out, score, i = [], 0, 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            merged = tiles[i] * 2
            out.append(merged)
            score += merged
            i += 2
        else:
            out.append(tiles[i])
            i += 1
    return out + [0] * (SIZE - len(out)), score


def transpose(board):
    return [list(col) for col in zip(*board)]


def reverse(board):
    return [row[::-1] for row in board]


def move(board, direction):
    b = [row[:] for row in board]
    if direction in ('up', 'down'):
        b = transpose(b)
    if direction in ('right', 'down'):
        b = reverse(b)
    score, moved = 0, False
    for idx, row in enumerate(b):
        new_row, gained = slide_left(row)
        b[idx] = new_row
        score += gained
        if new_row != row:
            moved = True
    if direction in ('right', 'down'):
        b = reverse(b)
    if direction in ('up', 'down'):
        b = transpose(b)
    return b, score, moved


def can_move(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return True
            if c + 1 < SIZE and board[r][c] == board[r][c + 1]:
                return True
            if r + 1 < SIZE and board[r][c] == board[r + 1][c]:
                return True
    return False


def highest_tile(board):
    return max(max(row) for row in board)


def render(board, score):
    line = "+" + "------+" * SIZE
    print("\n 2048 | Score: %d | Highest tile: %d" % (score, highest_tile(board)))
    print(line)
    for row in board:
        print("|" + "|".join("%4d  " % v if v else "  .   " for v in row) + "|")
        print(line)


def read_command():
    try:
        raw = input("Move (w/a/s/d or arrow keys, q=quit): ")
    except EOFError:
        return None
    cmd = raw.strip().lower()
    if cmd in ('q', 'quit', 'exit'):
        return None
    return KEYMAP.get(cmd, '')


def main():
    board, score = new_board(), 0
    while True:
        render(board, score)
        if not can_move(board):
            print("Game over! Final score: %d | Highest tile: %d" % (score, highest_tile(board)))
            break
        cmd = read_command()
        if cmd is None:
            print("Thanks for playing! Score: %d | Highest tile: %d" % (score, highest_tile(board)))
            break
        if cmd not in DIRECTIONS:
            print("Invalid input. Use w/a/s/d or arrow keys.")
            continue
        new_board_state, gained, moved = move(board, cmd)
        if not moved:
            print("No tiles moved in that direction; try another.")
            continue
        board = new_board_state
        score += gained
        add_tile(board)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame exited.")