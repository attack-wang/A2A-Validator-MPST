'''
ui.py — Console input/output helpers for the game.
Handles printing narrative text with word wrapping, presenting
numbered choices, capturing special commands (status/quit),
and rendering the status panel.
'''
import textwrap
SPECIAL_STATUS = "s"
SPECIAL_QUIT = "q"
class ConsoleUI:
    def __init__(self, width=78):
        self.width = width
    def show_title(self, title):
        line = "=" * self.width
        print(line)
        print(title.center(self.width))
        print(line)
    def show_text(self, text):
        for paragraph in text.split("\n"):
            print(textwrap.fill(paragraph, width=self.width))
        print()
    def show_divider(self):
        print("-" * self.width)
    def show_choices(self, choices, locked_choices):
        """choices: list of (index, text); locked: list of (index, text, hint)"""
        for idx, text in choices:
            print(f"  [{idx}] {text}")
        for idx, text, hint in locked_choices:
            print(f"  [ ] {text}  (locked — {hint})")
        print()
    def get_command(self, valid_indices, prompt="Your choice"):
        """Returns ('choice', index) or ('status', None) or ('quit', None)."""
        while True:
            raw = input(f"{prompt} ").strip().lower()
            if raw == SPECIAL_STATUS:
                return ("status", None)
            if raw == SPECIAL_QUIT:
                return ("quit", None)
            if raw.isdigit():
                num = int(raw)
                if num in valid_indices:
                    return ("choice", num)
            print("  Please enter a listed number, 's' for status, or 'q' to save & quit.")
    def confirm(self, prompt):
        while True:
            raw = input(f"{prompt} [y/n] ").strip().lower()
            if raw in ("y", "yes"):
                return True
            if raw in ("n", "no"):
                return False
            print("  Please answer 'y' or 'n'.")
    def show_status(self, state):
        self.show_divider()
        print("STATUS".center(self.width))
        self.show_divider()
        rel = ", ".join(f"{k}: {v}" for k, v in sorted(state.relationships.items())) or "none"
        print(f"Relationships : {rel}")
        inv = ", ".join(state.inventory) if state.inventory else "empty"
        print(f"Inventory     : {inv}")
        flags = ", ".join(k for k, v in sorted(state.flags.items()) if v) or "none"
        print(f"Flags         : {flags}")
        var = ", ".join(f"{k}: {v}" for k, v in sorted(state.variables.items())) or "none"
        print(f"Variables     : {var}")
        self.show_divider()
    def show_ending_banner(self, title):
        print()
        print("*" * self.width)
        print(title.center(self.width))
        print("*" * self.width)
    def pause(self, message="Press Enter to continue..."):
        input(message)