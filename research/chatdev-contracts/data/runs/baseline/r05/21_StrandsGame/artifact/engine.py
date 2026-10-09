def take_hint(self):
    if self.state == COMPLETE:
        return self._feedback(False, "Puzzle already complete!", "info"), None
    unfound = self.puzzle.unfound_targets(self.found)
    if not unfound:
        return self._feedback(False, "No targets left.", "info"), None
    target = unfound[0]
    frags = self.puzzle.target_fragments[target]
    # find first unused strand whose text matches the first unhinted fragment
    ...