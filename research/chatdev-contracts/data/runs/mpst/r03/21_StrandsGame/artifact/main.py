def unmerge(self, word=None):
    """Undo a merge. If word is None, undo the most recent merge.
    Returns (success, message)."""
    if not self._history:
        return False, "Nothing to undo - no merges have been made yet."
    if word is None:
        pretty, strands_used = self._history[-1]
        label = pretty
    else:
        key = normalize(word)  # hmm, puzzle.py doesn't import normalize
        ...