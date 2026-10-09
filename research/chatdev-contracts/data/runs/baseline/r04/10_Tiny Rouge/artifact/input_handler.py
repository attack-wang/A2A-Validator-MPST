'''Cross-platform, dependency-free single-keypress reader.'''
import sys
def read_key():
    '''Return a single lowercase key character, or '' on EOF/interrupt.'''
    # Windows
    try:
        import msvcrt
    except ImportError:
        msvcrt = None
    if msvcrt is not None:
        try:
            ch = msvcrt.getwch()
            if ch in ('\x00', '\xe0'):  # arrow/special keys: consume second code
                ch = msvcrt.getwch()
            return ch.lower()
        except (EOFError, KeyboardInterrupt):
            return '\x03'
    # POSIX
    try:
        import termios, tty
    except ImportError:
        # Last resort: line-based input
        line = sys.stdin.readline()
        return line.strip()[:1].lower() if line else '\x03'
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    except (EOFError, KeyboardInterrupt):
        ch = '\x03'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch.lower() if ch else '\x03'