'''Utility helpers for text normalization and safe user input.'''
import re
import config
def normalize(text):
    '''Normalize an answer string for tolerant comparison.
    Lowercases the text, collapses internal whitespace, strips surrounding
    punctuation, and (optionally) removes leading articles such as "the".
    '''
    cleaned = (text or "").strip().lower()
    # Collapse any run of whitespace into a single space.
    cleaned = re.sub(r"\s+", " ", cleaned)
    # Strip punctuation from the ends so "Nile." matches "nile".
    cleaned = cleaned.strip(" .,!?'\";:")
    if config.STRIP_ARTICLES:
        # Remove a single leading article so "the nile" matches "nile".
        cleaned = re.sub(r"^(the|a|an)\s+", "", cleaned)
    return cleaned
def ask(prompt):
    '''Prompt the user until a non-empty answer is entered; returns the raw string.'''
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Please enter an answer.")
def ask_int(prompt, default=None, low=None, high=None):
    '''Prompt the user for a whole number, re-prompting on invalid input.
    If the user presses Enter and a default is provided, the default is
    returned. Optional low/high bounds constrain the accepted values.
    '''
    while True:
        raw = input(prompt).strip()
        if not raw:
            if default is not None:
                return default
            print("Please enter a whole number.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if low is not None and value < low:
            print("Please enter a number >= {}.".format(low))
            continue
        if high is not None and value > high:
            print("Please enter a number <= {}.".format(high))
            continue
        return value