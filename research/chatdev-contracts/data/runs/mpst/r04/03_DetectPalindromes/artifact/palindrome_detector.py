'''
palindrome_detector.py
Core palindrome detection module.
Defines the single authoritative PalindromeMatch dataclass used across the
project, and the PalindromeDetector class, which scans plain text for
single-word and multi-word palindromes. Detection behaviour is configurable
via case-insensitivity, ignoring non-alphanumeric characters, a minimum
normalized length, and a maximum phrase length (in words).
'''
import re
from dataclasses import dataclass
@dataclass
class PalindromeMatch:
    """A palindrome found in the source text."""
    text: str             # raw text as it appears in the source
    normalized: str       # normalized form used for the palindrome test
    line_number: int      # 1-based line number of first occurrence
    column: int           # 0-based character offset of first occurrence
    word_count: int       # 1 for single words, >1 for multi-word phrases
    occurrences: int = 1  # total number of occurrences in the text
class PalindromeDetector:
    """Detects single-word and multi-word palindromes in plain text."""
    # Matches words, allowing internal apostrophes (e.g. "madam", "i'm").
    WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
    def __init__(self, ignore_case=True, ignore_non_alphanumeric=True,
                 min_length=2, max_phrase_words=6, find_phrases=True):
        """Store and validate detection settings."""
        self.ignore_case = ignore_case
        self.ignore_non_alphanumeric = ignore_non_alphanumeric
        self.min_length = max(1, min_length)
        self.max_phrase_words = max(2, max_phrase_words)
        self.find_phrases = find_phrases
    def normalize(self, text):
        """Lowercase and strip non-alphanumerics according to settings."""
        result = re.sub(r"[^A-Za-z0-9]+", "", text) if self.ignore_non_alphanumeric else text
        return result.lower() if self.ignore_case else result
    def _is_palindrome_normalized(self, normalized):
        """True if the normalized string meets min_length and reads the same reversed."""
        return len(normalized) >= self.min_length and normalized == normalized[::-1]
    def is_palindrome(self, text):
        """Public helper: test a single string for palindrome-ness."""
        return self._is_palindrome_normalized(self.normalize(text))
    def detect(self, text):
        """Scan text line by line; return (word_matches, phrase_matches, stats)."""
        word_matches, phrase_matches = {}, {}
        total_words = 0
        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            words = [(m.group(), m.start()) for m in self.WORD_PATTERN.finditer(line)]
            total_words += len(words)
            # Single-word palindromes.
            for raw, start in words:
                norm = self.normalize(raw)
                if self._is_palindrome_normalized(norm):
                    if norm in word_matches:
                        word_matches[norm].occurrences += 1
                    else:
                        word_matches[norm] = PalindromeMatch(raw, norm, line_number, start, 1)
            # Multi-word phrase palindromes (consecutive word windows).
            if self.find_phrases:
                for size in range(2, min(self.max_phrase_words, len(words)) + 1):
                    for i in range(len(words) - size + 1):
                        window = words[i:i + size]
                        raw = " ".join(w for w, _ in window)
                        norm = self.normalize(raw)
                        if self._is_palindrome_normalized(norm):
                            if norm in phrase_matches:
                                phrase_matches[norm].occurrences += 1
                            else:
                                phrase_matches[norm] = PalindromeMatch(
                                    raw, norm, line_number, window[0][1], size)
        word_list = sorted(word_matches.values(), key=lambda m: (-m.occurrences, m.normalized))
        phrase_list = sorted(phrase_matches.values(), key=lambda m: (-m.occurrences, m.normalized))
        longest = max((m.normalized for m in word_list + phrase_list), key=len, default="")
        stats = {
            "total_lines": len(lines),
            "total_words": total_words,
            "total_characters": len(text),
            "unique_palindrome_words": len(word_list),
            "palindrome_word_occurrences": sum(m.occurrences for m in word_list),
            "unique_palindrome_phrases": len(phrase_list),
            "palindrome_phrase_occurrences": sum(m.occurrences for m in phrase_list),
            "longest_palindrome": longest,
        }
        return word_list, phrase_list, stats