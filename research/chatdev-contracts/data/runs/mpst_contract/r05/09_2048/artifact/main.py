"""2048 - terminal game on a 4x4 grid (arrow keys to play, q to quit)."""
import os
import random
import sys

SIZE = 4
DIRECTIONS = ('UP', 'DOWN', 'LEFT', 'RIGHT')


def read_key():
    """Read one key press cross-platform; map arrow keys to direction names."""
    try:
        if os.name == 'nt':
            import msvcrt
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ch = msvcrt.getch()
            return {b'H': 'UP', b'P': 'DOWN', b'K': 'LEFT', b'M': 'RIGHT'}.get(
                ch, ch.decode(errors='ignore').lower())
        import termios
        import tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return {'\x1b[A': 'UP', '\x1b[B': 'DOWN', '\x1b[C': 'RIGHT',
                '\x1b[D': 'LEFT'}.get(ch, ch.lower())
    except (EOFError, KeyboardInterrupt, OSError):
        return 'q'


def slide_left(line):
    """Slide one line left, merging equal neighbours once. -> (line, gained, moved)"""
    tiles = [v for v in line if v]
    out = []
    gained = 0
    i = 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            out.append(tiles[i] * 2)
            gained += tiles[i] * 2
            i += 2
        else:
            out.append(tiles[i])
            i += 1
    out += [0] * (SIZE - len(out))
    return out, gained, out != line


def orient(grid, direction):
    """Return the grid as lines that slide 'left' for the given direction."""
    if direction in ('LEFT', 'RIGHT'):
        lines = [list(row) for row in grid]
    else:
        lines = [[grid[r][c] for r in range(SIZE)] for c in range(SIZE)]
    if direction in ('RIGHT', 'DOWN'):
        lines = [line[::-1] for line in lines]
    return lines


def unorient(grid, direction, lines):
    """Write oriented (already slid) lines back into the grid."""
    if direction in ('RIGHT', 'DOWN'):
        lines = [line[::-1] for line in lines]
    if direction in ('LEFT', 'RIGHT'):
        grid[:] = [list(line) for line in lines]
    else:
        for c in range(SIZE):
            for r in range(SIZE):
                grid[r][c] = lines[c][r]


def move(grid, direction):
    """Apply one move; returns (moved, gained_score)."""
    results = [slide_left(line) for line in orient(grid, direction)]
    if not any(res[2] for res in results):
        return False, 0
    unorient(grid, direction, [res[0] for res in results])
    return True, sum(res[1] for res in results)


def spawn(grid):
    """Place a new 2 (90%) or 4 (10%) tile in a random empty cell."""
    empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if grid[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        grid[r][c] = 2 if random.random() < 0.9 else 4


def can_move(grid):
    """True while any move is possible (empty cell or equal neighbours)."""
    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] == 0:
                return True
            if c + 1 < SIZE and grid[r][c] == grid[r][c + 1]:
                return True
            if r + 1 < SIZE and grid[r][c] == grid[r + 1][c]:
                return True
    return False


def display(grid, score, best, message=''):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('2048 | Score: {} | Highest tile: {}'.format(score, best))
    print('+' + '------+' * SIZE)
    for row in grid:
        print(''.join('|{:>5} '.format(v if v else '') for v in row) + '|')
        print('+' + '------+' * SIZE)
    print('Arrow keys: move | q: quit')
    if message:
        print(message)
    sys.stdout.flush()


def main():
    grid = [[0] * SIZE for _ in range(SIZE)]
    spawn(grid)
    spawn(grid)
    score = 0
    best = max(v for row in grid for v in row)
    won = False
    message = ''
    while True:
        display(grid, score, best, message)
        message = ''
        key = read_key()
        if key in ('q', '\x03'):
            print('Thanks for playing! Score: {} | Highest tile: {}'.format(score, best))
            break
        if key not in DIRECTIONS:
            message = 'Unknown key: use arrow keys or q.'
            continue
        moved, gained = move(grid, key)
        if not moved:
            message = 'No tiles can slide that way.'
            continue
        score += gained
        spawn(grid)
        best = max(best, max(v for row in grid for v in row))
        if best >= 2048 and not won:
            won = True
            message = 'You made the 2048 tile! Keep going or press q.'
        if not can_move(grid):
            display(grid, score, best)
            print('GAME OVER - no moves left. Score: {} | Highest tile: {}'.format(score, best))
            break


if __name__ == '__main__':
    main()