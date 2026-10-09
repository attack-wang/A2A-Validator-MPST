import sys
try:
    import msvcrt
except ImportError:
    msvcrt = None
try:
    import termios
    import tty
    import select
except ImportError:
    termios = None
    tty = None
    select = None
def read_key():
    '''Read one key press. Returns a single-character string.'''
    if msvcrt is not None:
        # Windows console: single-key input without Enter.
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            # Function/arrow keys send a two-character sequence.
            ext = msvcrt.getwch()
            return {"H": "w", "P": "s", "K": "a", "M": "d"}.get(ext, "")
        return ch
    if termios is not None:
        # Unix-like terminals: raw single-key input without Enter.
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                # Escape or arrow key sequence: peek for the rest.
                if not _wait_readable(0.05):
                    return "\x1b"          # plain ESC -> quit
                seq = sys.stdin.read(1)
                if seq == "[" and _wait_readable(0.05):
                    final = sys.stdin.read(1)
                    return {"A": "w", "B": "s", "D": "a", "C": "d"}.get(final, "")
                return "\x1b"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    # Last resort: line-based input (requires Enter after each key).
    line = input()
    return line.strip()[:1] if line else ""
def _wait_readable(timeout):
    r, _, _ = select.select([sys.stdin], [], [], timeout)
    return bool(r)