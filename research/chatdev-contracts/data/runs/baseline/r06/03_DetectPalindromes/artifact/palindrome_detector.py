'''
palindrome_detector.py
Core palindrome detection logic.
Contains:
- DetectionSettings: configuration dataclass for detection behaviour.
- PalindromeResult: dataclass describing one detected palindrome.
- PalindromeDetector: finds palindromic words and lines/phrases in text.
'''
import re
from dataclasses import dataclass
@dataclass
class DetectionSettings:
    """Configuration options controlling how palindromes are detected."""
    case_sensitive: bool = False
    ignore_punctuation: bool = True
    min_length: int = 3
@dataclass
class PalindromeResult:
    """A single detected palindrome together with its location."""
    original: str
    normalized: str
    line_number: int
    column: int
    kind: str
class PalindromeDetector:
    """Detects palindromic words and lines/phrases inside text."""
    WORD_PATTERN = re.compile(r"[A-Za-z0-9']+")
    def __init__(self, settings=None):
        self.settings = settings if settings is not None else DetectionSettings()
    def normalize(self, text):
        """Lowercase (unless case-sensitive) and strip non-alphanumerics."""
        normalized = text
        if self.settings.ignore_punctuation:
            normalized = re.sub(r"[^A-Za-z0-9]", "", normalized)
        if not self.settings.case_sensitive:
            normalized = normalized.lower()
        return normalized
    def is_palindrome(self, text):
        """Return True when the normalized text reads the same in reverse."""
        normalized = self.normalize(text)
        if len(normalized) < self.settings.min_length:
            return False
        return normalized == normalized[::-1]
    def detect(self, text, mode="both"):
        """Scan `text` and return a list of PalindromeResult objects."""
        results = []
        if mode in ("words", "both"):
            results.extend(self._detect_words(text))
        if mode in ("lines", "both"):
            line_results = self._detect_lines(text)
            if mode == "both":
                # Skip single-word lines already covered by word detection
                line_results = [
                    r for r in line_results if " " in r.original.strip()
                ]
            results.extend(line_results)
        return results
    def _detect_words(self, text):
        """Find palindromic individual words with their positions."""
        results = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in self.WORD_PATTERN.finditer(line):
                word = match.group(0)
                if self.is_palindrome(word):
                    results.append(PalindromeResult(
                        original=word,
                        normalized=self.normalize(word),
                        line_number=line_number,
                        column=match.start() + 1,
                        kind="word",
                    ))
        return results
    def _detect_lines(self, text):
        """Find palindromic whole lines (ignoring spaces/punctuation)."""
        results = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if self.is_palindrome(line):
                results.append(PalindromeResult(
                    original=line.strip(),
                    normalized=self.normalize(line),
                    line_number=line_number,
                    column=1,
                    kind="line",
                ))
        return results