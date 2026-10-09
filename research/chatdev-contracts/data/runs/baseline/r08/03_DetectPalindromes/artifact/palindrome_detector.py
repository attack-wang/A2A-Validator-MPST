'''
Core palindrome detection module.
Contains the PalindromeDetector class, which checks single strings for
the palindrome property, scans words (and optionally whole-line
phrases) of a text, and computes summary statistics about everything
that was found.
'''
import re
from collections import Counter
from config import (
    WORD_PATTERN,
    IGNORED_CHARS_PATTERN,
    DEFAULT_MIN_LENGTH,
    DEFAULT_CASE_SENSITIVE,
    DEFAULT_INCLUDE_PHRASES,
)
class PalindromeDetector:
    '''Detects palindromic words and phrases inside plain text.'''
    def __init__(self, min_length=DEFAULT_MIN_LENGTH,
                 case_sensitive=DEFAULT_CASE_SENSITIVE,
                 include_phrases=DEFAULT_INCLUDE_PHRASES):
        '''Configure the detector with its matching rules.'''
        self.min_length = min_length
        self.case_sensitive = case_sensitive
        self.include_phrases = include_phrases
        self._word_regex = re.compile(WORD_PATTERN)
        self._ignored_chars_regex = re.compile(IGNORED_CHARS_PATTERN)
    def is_palindrome(self, text):
        '''Return True when the normalized text reads the same backwards.'''
        normalized = self._normalize(text)
        if len(normalized) < self.min_length:
            return False
        return normalized == normalized[::-1]
    def _normalize(self, text):
        '''Strip ignored characters and apply the configured case rule.'''
        normalized = self._ignored_chars_regex.sub("", text)
        if not self.case_sensitive:
            normalized = normalized.lower()
        return normalized
    def detect_words(self, text):
        '''Scan the text word by word and describe every palindromic word.'''
        findings = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in self._word_regex.finditer(line):
                word = match.group(0)
                if self.is_palindrome(word):
                    findings.append({
                        "text": word,
                        "line": line_number,
                        "column": match.start() + 1,
                        "type": "word",
                    })
        return findings
    def detect_phrases(self, text):
        '''Scan the text line by line and report palindromic multi-word lines.'''
        findings = []
        if not self.include_phrases:
            return findings
        for line_number, line in enumerate(text.splitlines(), start=1):
            if len(self._word_regex.findall(line)) < 2:
                continue  # single-word lines are already covered by detect_words
            normalized = self._normalize(line)
            if len(normalized) >= self.min_length and normalized == normalized[::-1]:
                findings.append({
                    "text": line.strip(),
                    "line": line_number,
                    "column": 1,
                    "type": "phrase",
                })
        return findings
    def detect(self, text):
        '''Run the full detection and return all findings sorted by position.'''
        findings = self.detect_words(text)
        findings.extend(self.detect_phrases(text))
        findings.sort(key=lambda finding: (finding["line"], finding["column"]))
        return findings
    @staticmethod
    def compute_statistics(findings):
        '''Summarize a list of findings into a statistics dictionary.'''
        word_findings = [f for f in findings if f["type"] == "word"]
        phrase_findings = [f for f in findings if f["type"] == "phrase"]
        frequency = Counter(f["text"].lower() for f in word_findings)
        longest = max(word_findings, key=lambda f: len(f["text"]), default=None)
        most_frequent = frequency.most_common(1)
        return {
            "total_palindromes": len(findings),
            "total_words": len(word_findings),
            "total_phrases": len(phrase_findings),
            "unique_palindromes": len(frequency),
            "most_frequent": most_frequent[0] if most_frequent else None,
            "longest": longest["text"] if longest else None,
        }