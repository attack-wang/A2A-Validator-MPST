'''
palindrome_detector.py
Core palindrome detection engine for the Palindrome Detector application.
...
'''
import re
from dataclasses import dataclass
@dataclass
class PalindromeMatch:
    """Container for a single palindrome occurrence found in the text."""
    original: str
    normalized: str
    line_number: int
    column: int
    length: int
    def __str__(self) -> str:
        return (f'"{self.original}" (line {self.line_number}, '
                f'column {self.column}, normalized "{self.normalized}", '
                f'length {self.length})')
class PalindromeDetector:
    """Detects palindromes in plain text at word, phrase, or line level."""
    _WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*")
    _SENTENCE_PATTERN = re.compile(r'[^.!?:\n]+[.!?:]?')
    def __init__(self, case_insensitive=True, ignore_punctuation=True, min_length=1):
        self.case_insensitive = case_insensitive
        self.ignore_punctuation = ignore_punctuation
        self.min_length = max(1, int(min_length))
    def normalize(self, text):
        if self.case_insensitive:
            text = text.lower()
        if self.ignore_punctuation:
            text = ''.join(ch for ch in text if ch.isalnum())
        return text
    def is_palindrome(self, text):
        """Return True if the normalized form of *text* reads the same
        forwards and backwards and meets the minimum length threshold."""
        normalized = self.normalize(text)
        if len(normalized) < self.min_length:
            return False
        return normalized == normalized[::-1]
    def detect(self, text, mode='word'):
        """Scan *text* and return a list of PalindromeMatch objects."""
        if mode == 'word':
            return self._detect_word_palindromes(text)
        if mode == 'phrase':
            return self._detect_phrase_palindromes(text)
        if mode == 'line':
            return self._detect_line_palindromes(text)
        if mode == 'all':
            matches = []
            matches.extend(self._detect_word_palindromes(text))
            matches.extend(self._detect_phrase_palindromes(text))
            matches.extend(self._detect_line_palindromes(text))
            return matches
        raise ValueError(f"Unknown detection mode: {mode!r}")
    def _detect_word_palindromes(self, text):
        """Find individual words that are palindromes once normalized."""
        matches = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in self._WORD_PATTERN.finditer(line):
                token = match.group(0)
                if self.is_palindrome(token):
                    normalized = self.normalize(token)
                    matches.append(PalindromeMatch(
                        original=token,
                        normalized=normalized,
                        line_number=line_number,
                        column=match.start(),
                        length=len(normalized),
                    ))
        return matches
    def _detect_phrase_palindromes(self, text):
        """Find sentence-like phrases that are palindromes once normalized."""
        matches = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in self._SENTENCE_PATTERN.finditer(line):
                phrase = match.group(0).strip()
                if not phrase:
                    continue
                if self.is_palindrome(phrase):
                    normalized = self.normalize(phrase)
                    # column of the first character of the phrase
                    column = match.start() + (len(match.group(0)) - len(match.group(0).lstrip()))
                    matches.append(PalindromeMatch(
                        original=phrase,
                        normalized=normalized,
                        line_number=line_number,
                        column=column,
                        length=len(normalized),
                    ))
        return matches
    def _detect_line_palindromes(self, text):
        """Find whole lines that are palindromes once normalized."""
        matches = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped:
                continue
            if self.is_palindrome(stripped):
                normalized = self.normalize(stripped)
                matches.append(PalindromeMatch(
                    original=stripped,
                    normalized=normalized,
                    line_number=line_number,
                    column=0,
                    length=len(normalized),
                ))
        return matches
    @staticmethod
    def build_statistics(matches, mode, source_name, total_lines, total_chars):
        """Assemble a dictionary of summary statistics for a scan."""
        return {
            'source': source_name,
            'mode': mode,
            'total_lines': total_lines,
            'total_characters': total_chars,
            'total_matches': len(matches),
            'longest': max((m.length for m in matches), default=0),
            'unique_normalized': len({m.normalized for m in matches}),
        }