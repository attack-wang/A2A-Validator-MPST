'''
ui.py
User-interface helpers for Simplified Monopoly Go!.
Provides robust console input utilities used by game.py and main.py:
  - get_line:    safely read a line of input (handles EOF / Ctrl-C)
  - get_choice:  keep prompting until the user picks one of the valid options
  - ask_yes_no:  ask a yes/no question and return True/False
'''
def get_line(prompt):
    """Read a stripped line of input; exit cleanly on EOF or KeyboardInterrupt."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGame exited.")
        raise SystemExit
def get_choice(prompt, valid_options):
    """Prompt repeatedly until the user enters one of valid_options (case-insensitive)."""
    valid = [option.lower() for option in valid_options]
    while True:
        choice = get_line(prompt).lower()
        if choice in valid:
            return choice
        print(f"Invalid choice. Please enter one of: {', '.join(valid)}")
def ask_yes_no(prompt):
    """Ask a yes/no question; return True for 'y/yes' and False for 'n/no'."""
    while True:
        answer = get_line(prompt).lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")