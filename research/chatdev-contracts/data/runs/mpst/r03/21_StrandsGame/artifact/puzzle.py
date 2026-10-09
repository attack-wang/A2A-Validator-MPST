def unmerge(self, word=None):
    if not self._history:
        return False, "Nothing to undo - no merges have been made yet."
    if word is None:
        index = len(self._history) - 1
    else:
        key = normalize(word)
        index = next((i for i, (pretty, _) in enumerate(self._history)
                      if normalize(pretty) == key), None)
        if index is None:
            return False, f"'{word.upper()}' has not been merged, so it cannot be undone."
    pretty, strands_used = self._history.pop(index)
    for s in strands_used:
        s.used = False
        s.used_in = None
    # remove from found list
    if pretty in self.found:
        self.found.remove(pretty)
    self.completed = False
    return True, f"Undone: {pretty} - strands {', '.join(str(s.id) for s in strands_used)} are available again."