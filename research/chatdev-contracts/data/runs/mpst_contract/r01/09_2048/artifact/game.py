"""Core 2048 logic: 4x4 grid, slides, merges, spawns, and game-over checks."""
import random

SIZE = 4


def new_board():
    """Return a fresh board with two starting tiles."""
    board = [[0] * SIZE for _ in range(SIZE)]
    add_tile(board)
    add_tile(board)
    return board


def add_tile(board):
    """Spawn a 2 (90%) or 4 (10%) in a random empty cell."""
    empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if not empty:
        return False
    r, c = random.choice(empty)
    board[r][c] = 2 if random.random() < 0.9 else 4
    return True


def _slide(values):
    """Slide a line left, merging equal neighbours once; return (line, gained)."""
    tiles = [v for v in values if v]
    line, gained, i = [], 0, 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            merged = tiles[i] * 2
            line.append(merged)
            gained += merged
            i += 2
        else:
            line.append(tiles[i])
            i += 1
    line += [0] * (SIZE - len(line))
    return line, gained


def move(board, direction):
    """Apply 'up'/'down'/'left'/'right'; return (moved, score_gained)."""
    moved, gained = False, 0
    if direction in ('left', 'right'):
        for r in range(SIZE):
            row = board[r][::-1] if direction == 'right' else list(board[r])
            line, s = _slide(row)
            if direction == 'right':
                line = line[::-1]
            if line != board[r]:
                moved = True
                board[r] = line
            gained += s
    else:
        for c in range(SIZE):
            col = [board[r][c] for r in range(SIZE)]
            if direction == 'down':
                col.reverse()
            line, s = _slide(col)
            if direction == 'down':
                line.reverse()
            for r in range(SIZE):
                if board[r][c] != line[r]:
                    moved = True
                board[r][c] = line[r]
            gained += s
    return moved, gained


def can_move(board):
    """True while any cell is empty or any adjacent pair is equal."""
    for r in range(SIZE):
        for c in range(SIZE):
            v = board[r][c]
            if v == 0:
                return True
            if c + 1 < SIZE and board[r][c + 1] == v:
                return True
            if r + 1 < SIZE and board[r + 1][c] == v:
                return True
    return False


def highest_tile(board):
    """Largest tile currently on the board."""
    return max(max(row) for row in board)