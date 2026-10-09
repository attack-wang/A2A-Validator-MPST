'''
utils.py
Utility helper functions for validated console input used throughout
the Monopoly Go! game. These helpers guarantee that every interactive
prompt returns a usable value, so the Game class can rely on them for
player setup, buy/rent decisions, jail choices, and chance handling.
'''
def ask_yes_no(prompt):
    """Prompt the user with a yes/no question until a valid answer is given.
    Accepts 'y', 'yes', 'n', or 'no' (case-insensitive, whitespace-tolerant).
    Args:
        prompt (str): The question to display to the user.
    Returns:
        bool: True if the user answered yes, False if the user answered no.
    """
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ('y', 'yes'):
            return True
        if ans in ('n', 'no'):
            return False
        print("Please answer 'y' or 'n'.")
def ask_int(prompt, lo, hi):
    """Prompt the user for an integer within an inclusive range until valid.
    Re-prompts with an error message when the input is non-numeric or
    outside the [lo, hi] bounds.
    Args:
        prompt (str): The message displayed before reading input.
        lo (int): The minimum acceptable value.
        hi (int): The maximum acceptable value.
    Returns:
        int: A validated integer in the range [lo, hi].
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print(f"Please enter a number between {lo} and {hi}.")
            continue
        if lo <= value <= hi:
            return value
        print(f"Please enter a number between {lo} and {hi}.")