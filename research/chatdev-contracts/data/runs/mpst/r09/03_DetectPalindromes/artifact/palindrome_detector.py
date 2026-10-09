'''
Core palindrome detection logic.
This module provides the PalindromeDetector class, which can:
- Normalize text (case folding, punctuation removal).
- Check whether a given string is a palindrome.
- Find palindromic words, phrases (multi-word sequences), and whole lines
  within a larger body of text.
'''
import re
# Pattern used to tokenize raw text into word-like tokens (letters, digits,
# and apostrophes inside words). Covers ASCII plus common Latin, Greek and
# Cyrillic ranges.
WORD_PATTERN = r"[A-Za-z\u00C0-\u024F\u0370-\u03FF\u0400-\u04FF0-9']+"
class PalindromeDetector:
    """Detects palindromic words, phrases, and lines within text."""
    def __init__(self, min_length=1, case_insensitive=True, ignore_punctuation=True):
        """
        Initialize the detector.
        :param min_length: Minimum normalized length for a candidate to be considered.
        :param case_insensitive: If True, ignore letter case when checking.
        :param ignore_punctuation: If True, strip punctuation/whitespace before checking.
        """
        self.min_length = min_length
        self.case_insensitive = case_insensitive
        self.ignore_punctuation = ignore_punctuation
    def normalize(self, text):
        """Normalize a string according to detector settings."""
        if self.case_insensitive:
            text = text.lower()
        if self.ignore_punctuation:
            # Keep only alphanumeric characters
            text = re.sub(r"[^0-9a-zA-Z\u00C0-\u024F\u0370-\u03FF\u0400-\u04FF]+", "", text)
        else:
            # Only remove whitespace so phrases can still be checked
            text = re.sub(r"\s+", "", text)
        return text
    def is_palindrome(self, text):
        """Return True if the normalized text reads the same forwards and backwards."""
        normalized = self.normalize(text)
        if len(normalized) < self.min_length:
            return False
        return normalized == normalized[::-1]
    def find_palindrome_words(self, text):
        """
        Find unique palindromic single words in the text (in order of first appearance).
        Single-character words are trivially palindromes and are always skipped,
        so the effective minimum length for words is max(min_length, 2).
        """
        seen = set()
        palindromes = []
        min_word_length = max(self.min_length, 2)
        for word in re.findall(WORD_PATTERN, text):
            normalized = self.normalize(word)
            if len(normalized) < min_word_length:
                continue
            if normalized == normalized[::-1] and normalized not in seen:
                seen.add(normalized)
                palindromes.append(word)
        return palindromes
    def find_palindrome_phrases(self, text, max_words=10):
        """
        Find palindromic multi-word phrases in the text.
        A phrase is a contiguous sequence of at least two words on the same line.
        Phrases are never built across line boundaries, which avoids nonsensical
        candidates that span separate sentences. Each word is normalized only
        once and candidates are extended incrementally, keeping detection fast
        even for large files. Duplicates (by normalized form) are removed.
        :param max_words: Maximum number of words in a phrase candidate.
                          The default (10) is large enough to catch classic
                          long palindromes such as "Was it a car or a cat I saw?"
        """
        seen = set()
        phrases = []
        min_norm_length = max(self.min_length, 3)
        for line in text.splitlines():
            tokens = re.findall(WORD_PATTERN, line)
            normalized_tokens = [self.normalize(token) for token in tokens]
            count = len(tokens)
            for start in range(count):
                concatenated = ""
                for end in range(start, min(start + max_words, count)):
                    concatenated += normalized_tokens[end]
                    if end - start + 1 < 2:
                        # A phrase must contain at least two words.
                        continue
                    if len(concatenated) < min_norm_length:
                        continue
                    if concatenated == concatenated[::-1] and concatenated not in seen:
                        seen.add(concatenated)
                        phrases.append(" ".join(tokens[start:end + 1]))
        return phrases
    def find_palindrome_lines(self, text):
        """Find whole lines that are palindromes (after normalization)."""
        palindromic_lines = []
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            normalized = self.normalize(stripped)
            if len(normalized) >= max(self.min_length, 2) and normalized == normalized[::-1]:
                palindromic_lines.append(stripped)
        return palindromic_lines
    def detect(self, text, max_phrase_words=10):
        """Run all detections and return a dictionary of results."""
        palindrome_words = self.find_palindrome_words(text)
        palindrome_phrases = self.find_palindrome_phrases(text, max_words=max_phrase_words)
        palindrome_lines = self.find_palindrome_lines(text)
        return {
            "words": palindrome_words,
            "phrases": palindrome_phrases,
            "lines": palindrome_lines,
            "statistics": {
                "total_palindromes": len(palindrome_words) + len(palindrome_phrases) + len(palindrome_lines),
                "unique_palindrome_words": len(palindrome_words),
                "unique_palindrome_phrases": len(palindrome_phrases),
                "palindrome_lines": len(palindrome_lines),
            },
        }