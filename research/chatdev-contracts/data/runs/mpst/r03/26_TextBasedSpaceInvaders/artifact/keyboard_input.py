'''
keyboard_input.py
Cross-platform, non-blocking keyboard helper used by the game loop.
Provides read_key(), which returns a symbolic key name ('left',
'right', 'space', 'quit', ...) for a pressed key, or None when no
key is waiting. Uses msvcrt on Windows and termios/select on Unix,
so no third-party dependency is required.
'''
import sys
KEY_LEFT = 'left'
KEY_RIGHT = 'right'
KEY_SPACE = 'space'
KEY_QUIT = 'quit'
KEY_RESTART = 'r'
if sys.platform == 'win32':
    import msvcrt
    _ARROWS = {'K': KEY_LEFT, 'M': KEY_RIGHT, 'H': 'up', 'P': 'down'}
    def read_key():
        '''Return the symbolic name of a pressed key, or None if none waiting.'''
        while msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch in ('\x00', '\xe0'):            # extended (arrow) key prefix
                if msvcrt.kbhit():
                    return _ARROWS.get(msvcrt.getwch())
                return None
            if ch == ' ':
                return KEY_SPACE
            if ch in ('q', 'Q', '\x1b'):
                return KEY_QUIT
            return ch.lower()
        return None
else:
    import termios
    import tty
    import select
    import atexit
    _ARROWS = {'D': KEY_LEFT, 'C': KEY_RIGHT, 'A': 'up', 'B': 'down'}
    _old_termios = None
    def _enable_raw():
        global _old_termios
        if _old_termios is None:
            fd = sys.stdin.fileno()
            _old_termios = termios.tcgetattr(fd)
            tty.setcbreak(fd)
            atexit.register(_restore)
    def _restore():
        global _old_termios
        if _old_termios is not None:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, _old_termios)
            _old_termios = None
    def read_key():
        '''Return the symbolic name of a pressed key, or None if none waiting.'''
        _enable_raw()
        while select.select([sys.stdin], [], [], 0)[0]:
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                if select.select([sys.stdin], [], [], 0.01)[0]:
                    if sys.stdin.read(1) == '[' and select.select([sys.stdin], [], [], 0.01)[0]:
                        return _ARROWS.get(sys.stdin.read(1))
                return KEY_QUIT
            if ch == ' ':
                return KEY_SPACE
            if ch in ('q', 'Q'):
                return KEY_QUIT
            return ch.lower()
        return None