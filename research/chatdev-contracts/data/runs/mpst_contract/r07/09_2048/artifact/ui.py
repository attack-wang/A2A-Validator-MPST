import os
import sys

if sys.platform == "win32":
    os.system("")  # enable ANSI escape sequence processing on Windows consoles

COLORS = {
    2: "242", 4: "230", 8: "222", 16: "208", 32: "203", 64: "196",
    128: "51", 256: "50", 512: "49", 1024: "48", 2048: "47",
}

ARROWS = {"A": "up", "B": "down", "C": "right", "D": "left"}


def _map_escape(seq):
    if len(seq) == 2:
        return ARROWS.get(seq[1], "")
    return ""


def get_key():
    """Return 'up'/'down'/'left'/'right'/'quit', or '' for ignored keys."""
    if sys.platform == "win32" and sys.stdin.isatty():
        import msvcrt
        try:
            ch = msvcrt.getwch()
            if ch in ("\x00", "\xe0"):
                ch = msvcrt.getwch()
                return {"H": "up", "P": "down", "K": "left", "M": "right"}.get(ch, "")
        except (EOFError, OSError):
            return "quit"
        return "quit" if ch in ("q", "Q", "\x03") else ""
    if sys.stdin.isatty():
        import termios
        import tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                return _map_escape(sys.stdin.read(2))
        except (EOFError, OSError):
            return "quit"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    else:
        # Non-interactive stdin (e.g., piped/scripted input): plain reads so
        # input like "q" or end-of-stream exits promptly.
        try:
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                return _map_escape(sys.stdin.read(2))
        except (EOFError, OSError):
            return "quit"
    if ch == "":
        return "quit"
    return "quit" if ch in ("q", "Q", "\x03") else ""