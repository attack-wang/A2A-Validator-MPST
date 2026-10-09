'''
palindrome_detector.py
Core detection module for the Palindrome Detector application.
Contains the PalindromeMatch data class, which represents a single
palindrome discovered in a text, and the PalindromeDetector class,
which implements the algorithms used to find palindromic words and
sentences within arbitrary text.
'''
import re
from dataclasses import dataclass
from typing import List, Dict
@dataclass
class PalindromeMatch:
    """Represents one palindrome found in the source text."""
    text: str            # The original text as it appeared in the file
    normalized: str      # The normalized (cleaned) form used for comparison
    line_number: int     # 1-based line number where the match was found
    start_index: int     # 0-based character offset within the line
    length: int          # Length of the normalized palindrome
    def __str__(self) -> str:
        """Return a compact, human-readable description of the match."""
        return '"{0}" (line {1}, {2} chars)'.format(
            self.text, self.line_number, self.length
        )
class PalindromeDetector:
    """
    Detects palindromic words and sentences inside plain text.
    The detector is configurable:
      * min_length          -- minimum normalized length for a match
      * case_sensitive      -- whether letter case matters
      * ignore_punctuation  -- whether punctuation/spaces are stripped
    """
    # A "word" is a run of letters, digits or apostrophes.
    WORD_PATTERN = re.compile(r"[A-Za-z0-9']+")
    # A "sentence" is a run of characters ending with . ! ? or end-of-line.
    SENTENCE_PATTERN = re.compile(r"[^.!?\n]+[.!?]?")
    def __init__(self, min_length: int = 2,
                 case_sensitive: bool = False,
                 ignore_punctuation: bool = True) -> None:
        if min_length < 1:
            raise ValueError("min_length must be at least 1")
        self.min_length = min_length
        self.case_sensitive = case_sensitive
        self.ignore_punctuation = ignore_punctuation
        # Statistics filled in by the most recent detect() call.
        self.last_scan_stats: Dict[str, int] = {}
    # ------------------------------------------------------------------
    # Normalization helpers
    # ------------------------------------------------------------------
    def normalize(self, text: str) -> str:
        """
        Clean a piece of text so it can be compared against its reverse.
        Punctuation and whitespace are removed when ignore_punctuation is
        enabled, and the text is lower-cased unless case_sensitive is set.
        """
        if self.ignore_punctuation:
            text = re.sub(r"[^A-Za-z0-9]", "", text)
        if not self.case_sensitive:
            text = text.lower()
        return text
    def is_palindrome(self, text: str) -> bool:
        """
        Return True if `text` reads the same forwards and backwards
        after normalization and satisfies the minimum length rule.
        """
        normalized = self.normalize(text)
        if len(normalized) < self.min_length:
            return False
        return normalized == normalized[::-1]
    # ------------------------------------------------------------------
    # Detection routines
    # ------------------------------------------------------------------
    def detect_words(self, text: str) -> List[PalindromeMatch]:
        """Scan the text word by word and collect palindromic words."""
        matches: List[PalindromeMatch] = []
        tokens_scanned = 0
        for line_number, line in enumerate(text.splitlines(), start=1):
            for found in self.WORD_PATTERN.finditer(line):
                tokens_scanned += 1
                word = found.group(0)
                if self.is_palindrome(word):
                    normalized = self.normalize(word)
                    matches.append(PalindromeMatch(
                        text=word,
                        normalized=normalized,
                        line_number=line_number,
                        start_index=found.start(),
                        length=len(normalized),
                    ))
        self.last_scan_stats = {
            "lines": len(text.splitlines()),
            "tokens_scanned": tokens_scanned,
            "matches": len(matches),
        }
        return matches
    def detect_sentences(self, text: str) -> List[PalindromeMatch]:
        """Scan the text sentence by sentence and collect palindromes."""
        matches: List[PalindromeMatch] = []
        tokens_scanned = 0
        for line_number, line in enumerate(text.splitlines(), start=1):
            for raw in self.SENTENCE_PATTERN.findall(line):
                sentence = raw.strip()
                if not sentence:
                    continue
                tokens_scanned += 1
                if self.is_palindrome(sentence):
                    normalized = self.normalize(sentence)
                    start = line.find(sentence)
                    matches.append(PalindromeMatch(
                        text=sentence,
                        normalized=normalized,
                        line_number=line_number,
                        start_index=start if start >= 0 else 0,
                        length=len(normalized),
                    ))
        self.last_scan_stats = {
            "lines": len(text.splitlines()),
            "tokens_scanned": tokens_scanned,
            "matches": len(matches),
        }
        return matches
    def detect(self, text: str, mode: str = "words") -> List[PalindromeMatch]:
        """
        Run detection over `text` using the requested mode:
          * "words"     -- check individual words
          * "sentences" -- check whole sentences / phrases
        """
        if mode == "sentences":
            return self.detect_sentences(text)
        if mode == "words":
            return self.detect_words(text)
        raise ValueError("mode must be either 'words' or 'sentences'")
    # ------------------------------------------------------------------
    # Post-processing helpers
    # ------------------------------------------------------------------
    @staticmethod
    def unique_matches(matches: List[PalindromeMatch]) -> List[PalindromeMatch]:
        """
        Collapse repeated matches so each palindrome appears once.
        The key includes the line number, so the same palindrome found
        on different lines is still reported for each line.
        """
        seen = set()
        unique = []
        for match in matches:
            key = (match.normalized, match.line_number)
            if key not in seen:
                seen.add(key)
                unique.append(match)
        return unique