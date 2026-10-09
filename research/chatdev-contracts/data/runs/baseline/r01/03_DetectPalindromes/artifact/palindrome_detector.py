'''
Core palindrome detection logic for the Palindrome Detector application.
Contains the PalindromeDetector class and PalindromeMatch dataclass.
'''
import re
from dataclasses import dataclass
@dataclass
class PalindromeMatch:
    '''Represents a single palindrome found in the text.'''
    text: str            # The palindrome text as it appears (normalized)
    original: str        # The original raw text
    line_number: int     # 1-based line number where it was found
    start_index: int     # Character index in the line where match starts
    end_index: int       # Character index in the line where match ends (exclusive)
    mode: str            # 'word', 'phrase', or 'line'
class PalindromeDetector:
    '''Detects palindromes in text at word, phrase, and line level.'''
    def __init__(self, case_sensitive=False, ignore_non_alphanumeric=True,
                 min_word_length=2, detect_phrases=True, max_phrase_words=10,
                 detect_lines=True):
        self.case_sensitive = case_sensitive
        self.ignore_non_alphanumeric = ignore_non_alphanumeric
        self.min_word_length = min_word_length
        self.detect_phrases = detect_phrases
        self.max_phrase_words = max_phrase_words
        self.detect_lines = detect_lines
    def _normalize(self, text):
        '''Normalize text according to settings (case, non-alphanumeric removal).'''
        result = text if self.case_sensitive else text.lower()
        if self.ignore_non_alphanumeric:
            result = ''.join(ch for ch in result if ch.isalnum())
        return result
    def is_palindrome(self, text):
        '''Check whether the given text is a palindrome under current settings.'''
        normalized = self._normalize(text)
        if not normalized:
            return False
        return normalized == normalized[::-1]
    def _iter_tokens(self, line):
        '''Yield (start_index, token) pairs for whitespace-separated tokens.'''
        for m in re.finditer(r'\S+', line):
            yield m.start(), m.group()
    def find_palindromic_words(self, line, line_number):
        '''Find palindromic words in a single line.'''
        matches = []
        for start, token in self._iter_tokens(line):
            normalized = self._normalize(token)
            if len(normalized) < self.min_word_length:
                continue
            if normalized == normalized[::-1]:
                matches.append(PalindromeMatch(
                    text=normalized,
                    original=token,
                    line_number=line_number,
                    start_index=start,
                    end_index=start + len(token),
                    mode='word'
                ))
        return matches
    def find_palindromic_phrases(self, line, line_number):
        '''Find palindromic word sequences (phrases) in a single line.'''
        matches = []
        tokens = [(m.start(), m.group()) for m in re.finditer(r'\S+', line)]
        n = len(tokens)
        if n < 2:
            return matches
        consumed = [False] * n
        max_w = min(self.max_phrase_words, n)
        for width in range(max_w, 1, -1):
            for i in range(0, n - width + 1):
                window = range(i, i + width)
                if any(consumed[j] for j in window):
                    continue
                phrase = ' '.join(tokens[j][1] for j in window)
                normalized = self._normalize(phrase)
                if len(normalized) < self.min_word_length:
                    continue
                if normalized == normalized[::-1]:
                    matches.append(PalindromeMatch(
                        text=normalized,
                        original=phrase,
                        line_number=line_number,
                        start_index=tokens[i][0],
                        end_index=tokens[i + width - 1][0] + len(tokens[i + width - 1][1]),
                        mode='phrase'
                    ))
                    for j in window:
                        consumed[j] = True
        return matches
    def find_palindromic_lines(self, line, line_number):
        '''Check whether an entire line is a palindrome; return match list.'''
        matches = []
        if not self.detect_lines:
            return matches
        stripped = line.strip()
        if not stripped:
            return matches
        normalized = self._normalize(stripped)
        if len(normalized) < self.min_word_length:
            return matches
        if normalized == normalized[::-1]:
            # FIX: compute correct start/end columns instead of the broken
            # 'line.find(stripped[0])' / Ellipsis placeholder.
            start = line.find(stripped)
            matches.append(PalindromeMatch(
                text=normalized,
                original=stripped,
                line_number=line_number,
                start_index=start,
                end_index=start + len(stripped),
                mode='line'
            ))
        return matches
    def detect(self, text):
        '''Run full detection over multi-line text. Returns list of PalindromeMatch.'''
        matches = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            # Line-level detection
            line_matches = self.find_palindromic_lines(line, line_number)
            matches.extend(line_matches)
            # Phrase-level detection (skip if the whole line is already a palindrome
            # to avoid duplicate reporting of the same content)
            if self.detect_phrases and not line_matches:
                matches.extend(self.find_palindromic_phrases(line, line_number))
            # Word-level detection
            matches.extend(self.find_palindromic_words(line, line_number))
        return matches