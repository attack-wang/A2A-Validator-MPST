'''
Terminal UI helpers: screen clearing, word-wrapped printing, dividers,
a skippable typewriter effect, and a safe input pause.
'''
import os
import sys
import textwrap
import time
WIDTH = 80
TYPE_DELAY = 0.01
def clear_screen():
    os.system("cls" if os.name == "nt" else "printf '\\033[2J\\033[H'")
def wrap(text, width=WIDTH):
    return textwrap.fill(textwrap.dedent(text).strip(), width=width)
def print_wrapped(text, width=WIDTH):
    print(wrap(text, width))
def divider(char='-', length=WIDTH):
    print(char * length)
def _flush_stdin():
    """Discard any pending keyboard input (best effort, cross-platform)."""
    try:
        if os.name == "nt":
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            import termios
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except Exception:
        pass
def _enter_pressed():
    """Non-blocking check: has Enter been pressed? (best effort)."""
    try:
        if os.name == "nt":
            import msvcrt
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                return ch in (b'\r', b'\n')
            return False
        else:
            import select
            dr, _, _ = select.select([sys.stdin], [], [], 0)
            if dr:
                ch = sys.stdin.read(1)
                return ch in ('\n', '\r')
            return False
    except Exception:
        return False
def type_print(text, delay=TYPE_DELAY, skip_hint=True):
    """Print text with a typewriter effect. Press Enter to skip."""
    if skip_hint:
        print("(press Enter to skip typing)", flush=True)
    skipped = False
    for ch in text:
        if not skipped and _enter_pressed():
            skipped = True
            _flush_stdin()
        if skipped:
            sys.stdout.write(text[text.index(ch):] if False else ch)
            ...