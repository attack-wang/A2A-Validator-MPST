'''
Terminal UI helpers: banner, board, keyboard, messages.
'''
from colors import (BOLD, DIM, RESET, CYAN, YELLOW, GREY, GREEN, RED, colorize, supports_color)
from feedback import LetterResult, render_feedback
USE_COLOR = supports_color()
BANNER = r"""
 __          __  _                            _         
 \ \        / / | |                          | |        
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ _   _ 
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __| | | |
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | |_| |_| |
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__|\__, |
                                                   __/ |
                                                  |___/ 
"""
def print_banner(use_color=None):
    use = USE_COLOR if use_color is None else use_color
    print(colorize(BANNER, CYAN) if use else BANNER)
def print_board(history, use_color=None):
    use = USE_COLOR if use_color is None else use_color
    print()
    print(colorize("BOARD", BOLD) if use else "BOARD")
    if not history:
        msg = "  (no guesses yet — 6 attempts remaining)"
        print(colorize(msg, DIM) if use else msg)
    for guess, results in history:
        print("   " + render_feedback(guess, results, use_color=use))
    print()
def print_keyboard(status, use_color=None):
    use = USE_COLOR if use_color is None else use_color
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    precedence = {LetterResult.ABSENT: 0, LetterResult.PRESENT: 1, LetterResult.CORRECT: 2}
    if use:
        style_map = {
            LetterResult.CORRECT: GREEN_BG,
            LetterResult.PRESENT: YELLOW_BG,
            LetterResult.ABSENT: GREY_BG,
        }
    else:
        style_map = {}
    indent = "     "
    for row in rows:
        line = indent
        for ch in row:
            result = status.get(ch)
            if use and result is not None:
                line += colorize(ch.upper(), style_map[result]) + " "
            elif result is not None:
                marker_map = {
                    LetterResult.CORRECT: "[G]",
                    LetterResult.PRESENT: "[Y]",
                    LetterResult.ABSENT: "[.]",
                }
                line += ch.upper() + marker_map[result] + " "
            else:
                line += ch.upper() + " "
        print(line)
    print()
def keyboard_status_from_history(history):
    status = {}
    precedence = {LetterResult.ABSENT: 0, LetterResult.PRESENT: 1, LetterResult.CORRECT: 2}
    for guess, results in history:
        for ch, r in zip(guess, results):
            current = status.get(ch)
            if current is None or precedence[r] > precedence[current]:
                status[ch] = r
    return status
def print_message(text, style=None, use_color=None):
    use = USE_COLOR if use_color is None else use_color
    print(colorize(text, style) if use else text)