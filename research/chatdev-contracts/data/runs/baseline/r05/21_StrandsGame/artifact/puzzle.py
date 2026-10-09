import random
def _normalize(text):
    """Uppercase a string and strip all whitespace so merges match robustly."""
    return "".join(text.split()).upper()
class Strand:
    """A single clickable text fragment that belongs to one target."""
    def __init__(self, strand_id, text, source_target):
        self.strand_id = strand_id
        self.text = text
        self.source_target = source_target  # canonical target this fragment came from
        self.used = False      # True once merged into a confirmed target
        self.hinted = False    # True once revealed by a hint
    @property
    def display_text(self):
        """Text shown to the player."""
        return self.text
    def __repr__(self):
        return f"Strand({self.strand_id}, '{self.text}')"
class Puzzle:
    """Theme, target list, fragment pool, and validation helpers."""
    def __init__(self, theme, targets_with_fragments, seed=None):
        """
        targets_with_fragments: list of (target_text, [fragment strings]) where
        the fragments concatenate exactly to the target text.
        """
        self.theme = theme
        self.targets = [t for t, _ in targets_with_fragments]  # canonical order
        self.target_fragments = {t: list(frags) for t, frags in targets_with_fragments}
        self.strands = []
        self._build_strands(seed)
    @staticmethod
    def _normalize(text):
        return "".join(text.split()).upper()
    def _build_strands(self, seed):
        """Create one Strand per fragment, validate the data, then shuffle."""
        rng = random.Random(seed)
        pieces = []
        sid = 0
        for target in self.targets:  # iterate canonical order, not dict order
            frags = self.target_fragments[target]
            # Data-integrity guard: fragments must concatenate exactly to target.
            joined = self._normalize("".join(frags))
            assert joined == self._normalize(target), (
                f"Fragments {frags} do not concatenate to target '{target}'"
            )
            for frag in frags:
                pieces.append(Strand(sid, frag, target))
                sid += 1
        rng.shuffle(pieces)
        self.strands = pieces
    def available_strands(self):
        """Strands not yet merged into a confirmed target."""
        return [s for s in self.strands if not s.used]
    def unfound_targets(self, found):
        """Canonical targets not yet merged, in original order."""
        found_set = {self._normalize(t) for t in found}
        return [t for t in self.targets if self._normalize(t) not in found_set]
    def match_target(self, text, found):
        """Return the matching unfound target for merged text, else None."""
        candidate = self._normalize(text)
        for t in self.unfound_targets(found):
            if self._normalize(t) == candidate:
                return t
        return None
    def total_targets(self):
        return len(self.targets)