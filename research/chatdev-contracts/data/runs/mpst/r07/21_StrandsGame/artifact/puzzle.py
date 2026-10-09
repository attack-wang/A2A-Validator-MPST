'''
puzzle.py
Defines the Puzzle data model for the Strands game.
A Puzzle holds a list of text strands and a mapping from every target
word to the exact ordered tuple of strand indices that spell it.
`__post_init__` guarantees the puzzle is well-formed: every strand is
used exactly once across all words, strands are non-empty, and no
duplicate target words exist.
'''
from dataclasses import dataclass
@dataclass
class Puzzle:
    """Container for one Strands board: strands plus the word solutions."""
    title: str
    theme: str
    strands: list          # list[str]: the text fragments to merge
    words: dict            # word -> tuple of strand indices (canonical order)
    key_word: str = ""     # optional special word (like NYT's spangram)
    hint_text: str = ""
    def __post_init__(self):
        """Validate the puzzle: non-empty strands, no dup words, each strand used exactly once."""
        # All strands must be non-empty strings.
        for i, s in enumerate(self.strands):
            if not isinstance(s, str) or not s.strip():
                raise ValueError(f"Strand {i} must be a non-empty string, got {s!r}")
        # No duplicate target words.
        if len(set(self.words)) != len(self.words):
            raise ValueError("Puzzle contains duplicate target words")
        # Every strand index must be used exactly once across all words.
        usage = [0] * len(self.strands)
        for word, idxs in self.words.items():
            for i in idxs:
                if not 0 <= i < len(self.strands):
                    raise ValueError(f"Word {word!r} references out-of-range strand {i}")
                usage[i] += 1
        bad = [i for i, n in enumerate(usage) if n != 1]
        if bad:
            raise ValueError(f"Strands must each be used exactly once; problem at {bad}")
        # The key word, if given, must be one of the target words.
        if self.key_word and self.key_word not in self.words:
            raise ValueError(f"key_word {self.key_word!r} is not among the target words")
    @property
    def word_list(self):
        """Return the target words in a stable order (longest first, then alphabetical)."""
        return sorted(self.words.keys(), key=lambda w: (-len(w), w))
    def strands_for_word(self, word):
        """Return the ordered tuple of strand indices that spell `word`."""
        return self.words[word]
    def word_for_strands(self, indices):
        """Return the word formed by concatenating strands in the given order, else None."""
        merged = "".join(self.strands[i] for i in indices)
        for word, idxs in self.words.items():
            if sorted(idxs) == sorted(indices) and word == merged:
                return word
        return None
    def is_key_word(self, word):
        """Return True if `word` is this puzzle's special key word."""
        return bool(self.key_word) and word.upper() == self.key_word.upper()