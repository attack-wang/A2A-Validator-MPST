'''
Palindrome detection logic.
This module provides the PalindromeDetector class, which:
- checks whether a single word or phrase is a palindrome,
- scans a block of text and collects every unique palindromic word,
  together with the line of its first occurrence and its total count,
- optionally identifies whole lines that are palindromes.
Detection rules (case sensitivity, punctuation handling, minimum length)
are configurable at construction time.
'''
import re
from collections import Counter
class PalindromeDetector:
    """Detects palindromic words and palindromic lines inside text."""
    def __init__(self, case_sensitive=False, ignore_punctuation=True, min_length=1):
        """
        Initialize the detector with its matching rules.
        :param case_sensitive: If True, 'Anna' and 'anna' are different.
        :param ignore_punctuation: If True, punctuation/spaces are removed
                                   before comparing characters.
        :param min_length: Minimum cleaned length for a candidate to count.
        """
        self.case_sensitive = case_sensitive
        self.ignore_punctuation = ignore_punctuation
        self.min_length = min_length
    def normalize(self, text):
        """Return `text` cleaned according to the detector's rules."""
        if self.ignore_punctuation:
            text = re.sub(r"[^A-Za-z0-9]", "", text)
        if not self.case_sensitive:
            text = text.lower()
        return text
    def is_palindrome(self, text):
        """Return True if `text` reads the same forwards and backwards."""
        normalized = self.normalize(text)
        if len(normalized) < self.min_length:
            return False
        return normalized == normalized[::-1]
    def find_palindrome_words(self, text):
        """
        Scan `text` and collect every unique palindromic word.
        :return: List of dicts (ordered by first appearance):
                 'word'  - the word exactly as it first appears in the text,
                 'clean' - its normalized form,
                 'line'  - 1-based line number of the first occurrence,
                 'count' - total number of occurrences in the whole text.
        """
        first_seen = {}   # normalized word -> info about first occurrence
        counts = Counter()  # normalized word -> total occurrences
        for line_number, line in enumerate(text.splitlines(), start=1):
            for word in self._extract_words(line):
                cleaned = self.normalize(word)
                if not cleaned or len(cleaned) < self.min_length:
                    continue
                counts[cleaned] += 1
                if cleaned not in first_seen and self.is_palindrome(word):
                    first_seen[cleaned] = {
                        "word": word,
                        "clean": cleaned,
                        "line": line_number,
                    }
        results = []
        for cleaned, info in first_seen.items():
            info["count"] = counts[cleaned]
            results.append(info)
        return results
    def find_palindrome_lines(self, text):
        """
        Find whole lines that are palindromes.
        :return: List of dicts with keys 'line_number' (1-based) and 'text'.
        """
        results = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped:
                continue
            if self.is_palindrome(stripped):
                results.append({"line_number": line_number, "text": stripped})
        return results
    @staticmethod
    def _extract_words(line):
        """Split a line into candidate words (runs of letters/digits)."""
        return re.findall(r"[A-Za-z0-9]+", line)