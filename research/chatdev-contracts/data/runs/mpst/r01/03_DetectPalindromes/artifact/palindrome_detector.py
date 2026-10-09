'''
palindrome_detector.py
Core palindrome detection logic for the Palindrome Detector application.
Provides the PalindromeDetector class, which can:
  * Check whether a single word or phrase is a palindrome.
  * Scan a list of word tokens and find every palindromic word.
  * Scan raw text and find palindromic phrases (multi-word palindromes).
  * Produce summary statistics about the analysis.
A palindrome is a sequence of characters that reads the same forward and
backward. By default, detection is case-insensitive and ignores all
non-alphanumeric characters, so "Madam, I'm Adam" style phrases are handled
correctly.
'''
import re
from collections import Counter
class PalindromeDetector:
    """Detects palindromic words and phrases inside text."""
    def __init__(self, ignore_case=True, ignore_non_alphanumeric=True, min_length=1):
        """
        Configure the detector.
        :param ignore_case: If True, 'Level' and 'level' are both palindromes.
        :param ignore_non_alphanumeric: If True, punctuation/spaces are stripped
                                        before checking.
        :param min_length: Minimum length (in characters, after normalization)
                           a candidate must have to be considered a palindrome.
        """
        if min_length < 1:
            raise ValueError("min_length must be at least 1")
        self.ignore_case = ignore_case
        self.ignore_non_alphanumeric = ignore_non_alphanumeric
        self.min_length = min_length
    def _normalize(self, text):
        """Lowercase and strip non-alphanumeric characters according to settings."""
        if self.ignore_non_alphanumeric:
            text = re.sub(r"[^0-9A-Za-z]", "", text)
        if self.ignore_case:
            text = text.lower()
        return text
    def is_palindrome(self, text):
        """
        Return True if `text` is a palindrome under the current settings.
        Single characters are only palindromes when min_length == 1.
        """
        normalized = self._normalize(text)
        if len(normalized) < self.min_length:
            return False
        return normalized == normalized[::-1]
    def detect_words(self, tokens):
        """Return the list of tokens (in order) that are palindromes."""
        return [token for token in tokens if self.is_palindrome(token)]
    def analyze(self, tokens):
        """
        Full analysis of a token list.
        Returns a dictionary:
            {
                'palindromes': Counter mapping palindrome -> occurrence count,
                'statistics': {
                    'total_tokens': int,
                    'total_palindromes': int,
                    'unique_palindromes': int,
                    'palindrome_ratio': float
                }
            }
        """
        found = self.detect_words(tokens)
        counts = Counter(found)
        total_tokens = len(tokens)
        total_palindromes = len(found)
        unique = len(counts)
        ratio = (total_palindromes / total_tokens) if total_tokens else 0.0
        statistics = {
            'total_tokens': total_tokens,
            'total_palindromes': total_palindromes,
            'unique_palindromes': unique,
            'palindrome_ratio': ratio,
        }
        return {'palindromes': counts, 'statistics': statistics}
    def detect_phrases(self, text, max_phrase_length=6):
        """
        Find palindromic phrases (sequences of 2..max_phrase_length words).
        Text is split into sentences; within each sentence a sliding window
        over the word tokens is checked. Returns a list of dictionaries:
            {'phrase': str, 'length': int, 'sentence': int}
        sorted by phrase length (longest first).
        """
        sentences = re.split(r"[.!?;\n]+", text)
        results = []
        for index, sentence in enumerate(sentences, start=1):
            words = re.findall(r"[A-Za-z0-9']+", sentence)
            if len(words) < 2:
                continue
            seen = set()
            for size in range(min(max_phrase_length, len(words)), 1, -1):
                for start in range(0, len(words) - size + 1):
                    window = words[start:start + size]
                    normalized = self._normalize(" ".join(window))
                    if len(normalized) < max(self.min_length, 3):
                        continue
                    if normalized == normalized[::-1]:
                        phrase = " ".join(window)
                        key = normalized
                        if key not in seen:
                            seen.add(key)
                            results.append({
                                'phrase': phrase,
                                'length': size,
                                'sentence': index,
                            })
        results.sort(key=lambda item: (-item['length'], item['sentence']))
        return results