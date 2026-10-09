'''
utils.py
Utility helper functions for the simplified Monopoly Go! game.
Provides input validation helpers and text formatting utilities used
across the game modules.
'''
def ask_yes_no(prompt):
    """Prompt the user for a yes/no answer, returns True for yes."""
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Invalid input. Please enter 'y' or 'n'.")
def ask_int(prompt, minimum=None, maximum=None):
    """Prompt for an integer within optional bounds."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Value must be at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Value must be at most {maximum}.")
            continue
        return value
def format_money(amount):
    """Format an integer amount of money as a dollar string."""
    return f"${amount}"
def divider(title=""):
    """Return a horizontal divider line, optionally with a centered title."""
    width = 70
    if title:
        pad = max(0, (width - len(title) - 2) // 2)
        return "-" * pad + f" {title} " + "-" * (width - pad - len(title) - 2)
    return "-" * width
def press_enter(prompt="Press ENTER to continue..."):
    """Pause execution until the user presses ENTER."""
    input(prompt)