'''
colors.py
ANSI escape codes used to paint terminal output.
'''
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
FG_WHITE = "\033[97m"
FG_BLACK = "\033[30m"
FG_GREEN = "\033[92m"
FG_YELLOW = "\033[93m"
FG_GREY = "\033[90m"
FG_RED = "\033[91m"
BG_GREEN = "\033[42m"  # bright? standard green bg is 42; bright is 102
BG_YELLOW = "\033[43m"
BG_GREY = "\033[100m"  # bright black bg = dark grey
BG_WHITE = "\033[107m"
def colorize(text, *codes):
    return "".join(codes) + text + RESET
def tile(letter, bg_code):
    return colorize(f" {letter.upper()} ", bg_code, BOLD, FG_WHITE)