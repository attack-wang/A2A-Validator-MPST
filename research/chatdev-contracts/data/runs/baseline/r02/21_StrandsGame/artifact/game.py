def validate(self, merge_text, puzzle, found_targets):
    text = normalize_text(merge_text)
    if not text:
        return (self.INVALID, 'Empty merge — nothing submitted.')
    if text in found_targets:
        return (self.DUPLICATE, f"'{display}' was already found. Try a new combination.")
    if text in puzzle.targets:
        return (self.VALID, f"'{display}' is a theme word! Excellent merge!")
    if text in self.dictionary:
        return (self.BONUS, f"'{display}' is a bonus word!")
    unfound = [t for t in puzzle.targets if t not in found_targets]
    if any(t.startswith(text) and t != text for t in unfound):
        return (self.PARTIAL, f"'{display}' is a great start — it begins a theme word. Keep going!")
    return (self.INVALID, f"'{display}' is not part of this puzzle. Strands returned.")