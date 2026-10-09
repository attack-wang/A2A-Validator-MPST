'''
palindrome_detector.py
Core palindrome detection logic for the Palindrome Detector application.
A palindrome is a sequence that reads the same forward and backward.
By default the detector is case-insensitive and ignores punctuation,
spaces and other non-alphanumeric characters, so that classic
palindromic phrases such as "A man, a plan, a canal: Panama!" are
recognised correctly.
Classes:
    PalindromeDetector -- detects palindromic words and phrases in text.
'''
import re
# Words are extracted using this pattern: letters, digits and apostrophes.
WORD_PATTERN = re.compile(r"[A-Za-z0-9']+")
# Sentences/phrases are split after a sentence-ending punctuation mark.
SENTENCE_SPLIT_PATTERN = re.compile(r'(?<=[.!?])\s+')
class PalindromeDetector:
    """Detects palindromic words and palindromic phrases inside free text."""
    def __init__(self, min_length=2, case_sensitive=False, ignore_punctuation=True):
        """
        Initialise the detector.
        Args:
            min_length (int): Minimum normalized length for a candidate to be
                considered a palindrome (excludes single letters such as "a").
            case_sensitive (bool): When True, letter case matters.
            ignore_punctuation (bool): When True, non-alphanumeric characters
                are removed before testing.
        """
        self.min_length = min_length
        self.case_sensitive = case_sensitive
        self.ignore_punctuation = ignore_punctuation
    def normalize(self, text):
        """Return a cleaned version of *text* used for palindrome testing."""
        cleaned = text
        if self.ignore_punctuation:
            cleaned = ''.join(ch for ch in cleaned if ch.isalnum())
        if not self.case_sensitive:
            cleaned = cleaned.lower()
        return cleaned
    def is_palindrome(self, text):
        """Return True when the normalized text reads the same both ways."""
        normalized = self.normalize(text)
        if len(normalized) < self.min_length:
            return False
        return normalized == normalized[::-1]
    def find_palindromic_words(self, text):
        """
        Return every distinct word in *text* that is itself a palindrome.
        The original spelling of the first occurrence is preserved
        (e.g. "Racecar" is reported as "Racecar"). In case-sensitive mode
        the raw spelling is used as the dedup key, so "Anna" and "anna"
        are reported separately; otherwise matching ignores letter case.
        """
        found = []
        seen = set()
        for word in WORD_PATTERN.findall(text):
            if self.is_palindrome(word):
                key = word if self.case_sensitive else word.lower()
                if key not in seen:
                    seen.add(key)
                    found.append(word)
        return found
    def find_palindromic_phrases(self, text):
        """
        Return every sentence in *text* whose letters form a palindrome.
        Only multi-word sentences are considered here; single-word
        palindromic sentences are already covered by the word search.
        """
        found = []
        for phrase in SENTENCE_SPLIT_PATTERN.split(text):
            stripped = phrase.strip()
            if not stripped:
                continue
            if len(WORD_PATTERN.findall(stripped)) >= 2 and self.is_palindrome(stripped):
                found.append(stripped)
        return found
    def analyze(self, text):
        """
        Run a complete analysis of *text*.
        Returns:
            dict: A structured result containing the palindromic words,
            palindromic phrases and summary statistics.
        """
        words = self.find_palindromic_words(text)
        phrases = self.find_palindromic_phrases(text)
        return {
            'palindromic_words': words,
            'palindromic_phrases': phrases,
            'total_words': len(WORD_PATTERN.findall(text)),
            'word_count': len(words),
            'phrase_count': len(phrases),
        }