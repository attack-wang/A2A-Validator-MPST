'''
palindrome_detector.py
Core palindrome detection logic for the application.
The PalindromeDetector class checks whether individual strings are
palindromes and scans larger bodies of text for palindromic words,
lines, and sentences. Detection is configurable: it can be made
case-sensitive, punctuation can be kept or ignored, and a minimum
length threshold can be enforced.
'''
import re
class PalindromeDetector:
    '''
    Detects palindromes within text at word, line, and sentence level.
    A palindrome is a string that reads the same forward and backward.
    By default, comparison is case-insensitive and ignores characters
    that are not letters or digits (spaces, punctuation, etc.), which
    allows phrase palindromes such as "A man, a plan, a canal: Panama"
    to be recognized.
    '''
    def __init__(self, case_sensitive=False, ignore_non_alphanumeric=True, min_length=1):
        '''
        Initialize the detector with configurable behavior.
        Args:
            case_sensitive (bool): If True, 'Level' and 'level' are
                treated as different strings.
            ignore_non_alphanumeric (bool): If True, spaces and
                punctuation are stripped before comparison, enabling
                phrase-level palindrome detection.
            min_length (int): Minimum cleaned length for a string to be
                considered a palindrome candidate.
        '''
        self.case_sensitive = case_sensitive
        self.ignore_non_alphanumeric = ignore_non_alphanumeric
        self.min_length = max(1, min_length)
    def normalize(self, text):
        '''
        Normalize a string for palindrome comparison.
        Lowercases the text (unless case-sensitive mode is active) and
        removes non-alphanumeric characters when configured to do so.
        Args:
            text (str): The raw input string.
        Returns:
            str: The normalized string used for comparison.
        '''
        if not self.case_sensitive:
            text = text.lower()
        if self.ignore_non_alphanumeric:
            text = ''.join(char for char in text if char.isalnum())
        return text
    def is_palindrome(self, text):
        '''
        Check whether a single string is a palindrome.
        Args:
            text (str): The string to check.
        Returns:
            bool: True if the normalized string reads the same in both
            directions and meets the minimum length requirement.
        '''
        cleaned = self.normalize(text)
        if len(cleaned) < self.min_length:
            return False
        return cleaned == cleaned[::-1]
    def detect_word_palindromes(self, text):
        '''
        Scan text word-by-word and collect palindromic words.
        Words are whitespace-separated tokens. Punctuation attached to
        a word (e.g., "madam,") is handled by the normalization step.
        Words are grouped by their normalized form, so variants such as
        "Madam," and "madam" count as one unique word; the first-seen
        raw form is kept for display.
        Args:
            text (str): The text to scan.
        Returns:
            list: Dictionaries describing each unique palindromic word,
            in order of first appearance, with occurrence counts:
            [{'word': 'Madam,', 'count': 2}, ...]
        '''
        found = {}
        order = []
        for word in text.split():
            if self.is_palindrome(word):
                key = self.normalize(word)
                if key not in found:
                    found[key] = {'word': word, 'count': 0}
                    order.append(key)
                found[key]['count'] += 1
        return [found[key] for key in order]
    def detect_line_palindromes(self, text):
        '''
        Scan text line-by-line and collect palindromic lines.
        A line counts as a palindrome when its normalized content reads
        the same forward and backward. Empty lines are skipped.
        Args:
            text (str): The text to scan (may contain multiple lines).
        Returns:
            list: Dictionaries with the 1-based line number, the
            original line text, and its cleaned form:
            [{'line_number': 3, 'line': 'Never odd or even', 'cleaned': '...'}, ...]
        '''
        results = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped:
                continue
            if self.is_palindrome(stripped):
                results.append({
                    'line_number': line_number,
                    'line': stripped,
                    'cleaned': self.normalize(stripped)
                })
        return results
    def detect_sentence_palindromes(self, text):
        '''
        Scan text sentence-by-sentence and collect palindromic sentences.
        Sentences are split on '.', '!' and '?' boundaries followed by
        whitespace. This enables detection of phrase palindromes such
        as "A man, a plan, a canal: Panama".
        Args:
            text (str): The text to scan.
        Returns:
            list: Dictionaries with the 1-based sentence number, the
            original sentence text, and its cleaned form:
            [{'sentence_number': 1, 'sentence': '...', 'cleaned': '...'}, ...]
        '''
        sentences = re.split(r'(?<=[.!?])\s+', text)
        results = []
        sentence_number = 0
        for sentence in sentences:
            stripped = sentence.strip()
            if not stripped:
                continue
            sentence_number += 1
            if self.is_palindrome(stripped):
                results.append({
                    'sentence_number': sentence_number,
                    'sentence': stripped,
                    'cleaned': self.normalize(stripped)
                })
        return results