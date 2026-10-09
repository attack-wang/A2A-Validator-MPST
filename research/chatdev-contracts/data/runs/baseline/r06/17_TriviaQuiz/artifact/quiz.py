def _describe_answer(self, question, raw):
    """Human-readable version of the user's answer for the review section."""
    text = (raw or "").strip()
    if not text:
        return "(skipped)"
    choices = getattr(question, "choices", None)
    if choices is not None:
        letters = getattr(question, "LETTERS", "ABCDEFGH")
        if len(text) == 1 and text.upper() in letters[:len(choices)]:
            return f"{text.upper()} ({choices[letters.index(text.upper())]})"
        if text.isdigit() and 1 <= int(text) <= len(choices):
            return f"{text} ({choices[int(text) - 1]})"
    return text