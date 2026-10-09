'''
ui.py
Terminal presentation helpers for the interactive storytelling game.
Provides wrapped text printing, decorative separators, a typewriter-style
slow reveal for dramatic moments, and choice prompting utilities so that
every narrative segment is presented consistently.
'''
import textwrap
import sys
import time
import os
class UI:
    """Static helper class that renders narrative text in the terminal."""
    WIDTH = 78
    ENABLE_TYPING = True
    TYPE_DELAY = 0.015
    @staticmethod
    def clear():
        """Clear the terminal screen on Windows and POSIX systems."""
        os.system('cls' if os.name == 'nt' else 'clear')
    @staticmethod
    def separator(char='-', width=None):
        """Print a horizontal separator line."""
        width = width or UI.WIDTH
        print(char * width)
    @staticmethod
    def title(text):
        """Print a centred, boxed section title."""
        UI.separator('=')
        print(text.center(UI.WIDTH))
        UI.separator('=')
    @staticmethod
    def print_wrapped(text, indent=''):
        """Print text with word wrapping, preserving blank-line paragraphs."""
        for line in text.split('\n'):
            if not line.strip():
                print()
                continue
            print(textwrap.fill(line, width=UI.WIDTH,
                                initial_indent=indent,
                                subsequent_indent=indent))
    @staticmethod
    def type_out(text, delay=None):
        """
        Typewriter effect that PRESERVES paragraph structure.
        Each source line is wrapped independently so blank lines
        (paragraph breaks) survive the animation.
        """
        if not UI.ENABLE_TYPING:
            UI.print_wrapped(text)
            return
        delay = delay if delay is not None else UI.TYPE_DELAY
        for line in text.split('\n'):
            if not line.strip():
                print()
                continue
            wrapped = textwrap.wrap(line, width=UI.WIDTH) or ['']
            for chunk in wrapped:
                for ch in chunk:
                    sys.stdout.write(ch)
                    sys.stdout.flush()
                    time.sleep(delay)
                sys.stdout.write('\n')
    @staticmethod
    def show_choices(options):
        """Display a numbered list of choices plus meta commands."""
        UI.separator()
        for i, opt in enumerate(options, 1):
            print(textwrap.fill(opt, width=UI.WIDTH,
                                initial_indent=f"  [{i}] ",
                                subsequent_indent="      "))
        print("  [s] status   [q] save & quit")
        UI.separator()