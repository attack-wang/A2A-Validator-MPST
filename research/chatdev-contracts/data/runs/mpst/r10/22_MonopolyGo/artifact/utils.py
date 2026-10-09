'''
Utility helper functions for input validation and text formatting.
'''
def prompt_yes_no(message):
    """Prompt the user for a yes/no answer and return True/False."""
    while True:
        answer = input(f"{message} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")
def prompt_choice(message, options):
    """Prompt the user to choose one value from a list of allowed options."""
    options = [str(o) for o in options]
    while True:
        answer = input(f"{message} ({'/'.join(options)}): ").strip()
        if answer in options:
            return answer
        print(f"Please choose one of: {', '.join(options)}.")
def prompt_int(message, minimum=None, maximum=None):
    """Prompt the user for an integer within an optional inclusive range."""
    while True:
        raw = input(f"{message}: ").strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Value must be at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Value must be at most {maximum}.")
            continue
        return value
def format_money(amount):
    """Return a money string such as '$1,500'."""
    return f"${amount:,}"
def press_enter(message="Press Enter to continue..."):
    """Pause the game until the user presses Enter."""
    input(message)