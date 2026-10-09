'''
colors.py
ANSI escape-code constants and small helpers used to paint terminal
output with the Wordle feedback colors (green / yellow / grey) plus a
few utility styles (bold, dim, reset).
'''
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
GREY = "\033[90m"
CYAN = "\033[96m"
RED = "\033[91m"
WHITE = "\033[97m"
def colorize(text, color):
    '''Wrap `text` in the given ANSI `color` code and reset afterwards.'''
    return f"{color}{text}{RESET}"
def green(text): return colorize(text, GREEN)
def yellow(text): return colorize(text, YELLOW)
def grey(text): return colorize(text, GREY)
def bold(text): return colorize(text, BOLD)
def dim(text): return colorize(text, DIM)
def cyan(text): return colorize(text, CYAN)
def red(text): return colorize(text, RED)