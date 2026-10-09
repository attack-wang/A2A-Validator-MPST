'''
config.py
Central configuration: ANSI escape codes, color palette definitions,
and difficulty presets.
'''
class Ansi:
    """ANSI escape sequences used by the console UI."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
COLOR_SYMBOLS = ['R', 'G', 'B', 'Y', 'O', 'P']
COLOR_NAMES = {'R': 'Red', 'G': 'Green', 'B': 'Blue',
               'Y': 'Yellow', 'O': 'Orange', 'P': 'Purple'}
COLOR_ANSI = {'R': Ansi.RED, 'G': Ansi.GREEN, 'B': Ansi.BLUE,
              'Y': Ansi.YELLOW, 'O': Ansi.MAGENTA, 'P': Ansi.CYAN}
# key -> (label, code_length, max_attempts, palette_size)
DIFFICULTIES = {
    '1': ('Easy', 4, 12, 6),
    '2': ('Medium', 4, 10, 6),
    '3': ('Hard', 5, 8, 6),
}