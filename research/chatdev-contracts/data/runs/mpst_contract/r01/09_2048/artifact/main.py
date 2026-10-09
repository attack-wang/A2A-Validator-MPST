"""Terminal 2048: arrow keys slide tiles; merge equal tiles to reach 2048."""
import os
import sys

from game import add_tile, can_move, highest_tile, move, new_board

CLEAR = "\033[2J\033[H"
BORDER = "+" + "-----+" * 4
DIRECTIONS = ('up', 'down', 'left', 'right')
WASD = {'w': 'up', 's': 'down', 'a': 'left', 'd': 'right'}

if sys.platform == 'win32':
    try:
        os.system("")  # Enable ANSI escape processing on Windows consoles.
    except OSError:
        pass


def read_key():
    """Return 'up'/'down'/'left'/'right', 'quit', or '' for ignored keys."""
    try:
        import msvcrt
        ch = msvcrt.getwch()
        if ch in ('\x00', '\xe0'):
            ch = msvcrt.getwch()
            return {'H': 'up', 'P': 'down', 'K': 'left', 'M': 'right'}.get(ch, '')
        return WASD.get(ch.lower(), 'quit' if ch.lower() == 'q' else '')
    except ImportError:
        import select
        import termios
        import tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                if ready:
                    seq = sys.stdin.read(2)
                    if len(seq) == 2 and seq[0] == '[':
                        return {'A': 'up', 'B': 'down',
                                'C': 'right', 'D': 'left'}.get(seq[1], '')
                return ''
            if ch in WASD:
                return WASD[ch]
            return 'quit' if ch.lower() == 'q' else ''
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def render(board, score, best):
    print(CLEAR, end="")
    print("2048 | Score: {} | Highest tile: {}".format(score, best))
    print(BORDER)
    for row in board:
        cells = ["{:>4} ".format(v) if v else "  .  " for v in row]
        print("|" + "|".join(cells) + "|")
        print(BORDER)
    print("Move: arrow keys (or WASD). Quit: q.", flush=True)


def main():
    board = new_board()
    score = 0
    best = highest_tile(board)
    render(board, score, best)
    while True:
        key = read_key()
        if key == 'quit':
            print("Bye! Score: {} | Highest tile: {}".format(score, best))
            return
        if key not in DIRECTIONS:
            continue
        moved, gained = move(board, key)
        if not moved:
            continue
        score += gained
        add_tile(board)
        best = max(best, highest_tile(board))
        render(board, score, best)
        if not can_move(board):
            print("Game over! Final score: {} | Highest tile: {}".format(score, best))
            return


if __name__ == '__main__':
    main()