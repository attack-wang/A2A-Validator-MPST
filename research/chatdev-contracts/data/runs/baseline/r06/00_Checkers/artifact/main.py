def parse_move(text):
    text = text.strip().lower()
    if not text:
        raise NotationError("Empty input. Enter a move like 'b6-a5'.")
    # Validate the raw text: only position tokens separated by '-', 'x', spaces, or 'to'.
    normalized = re.sub(r"\s*to\s*", "-", text)  # hmm, 'to' contains letters that could clash
    ...