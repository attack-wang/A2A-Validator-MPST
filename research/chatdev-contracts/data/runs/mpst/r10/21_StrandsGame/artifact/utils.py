def normalize(text):
    """Uppercase and keep only alphabetic characters."""
    return "".join(ch for ch in text.upper() if ch.isalpha())