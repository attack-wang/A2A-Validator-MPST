'''
palindrome_detector.py
Core module containing the PalindromeDetector class, which provides
functionality to detect palindromic words, lines, and phrases within
a given text.
'''
import re
from collections import Counter
class PalindromeDetector:
    '''
    A detector that identifies palindromes within text at different
    granularities: individual words, whole lines, and phrases/sentences.
    '''
    def __init__(self, min_length=1, case_sensitive=False):
        '''
        Initialize the detector.
        Args:
            min_length (int): Minimum length (of the normalized text) for a
                              candidate to be considered a palindrome.
                              Note: with the default of 1, every single
                              alphanumeric character (e.g. "a", "I") is
                              treated as a palindromic word; raise this
                              value (e.g. --min-length 3) to filter out
                              short candidates.
            case_sensitive (bool): If True, comparison is case-sensitive.
        '''
        self.min_length = max(1, min_length)
        self.case_sensitive = case_sensitive
    def _normalize(self, text):
        '''
        Normalize text for palindrome comparison.
        Keeps only alphanumeric characters and lowercases them unless
        the detector is case-sensitive.
        Args:
            text (str): The raw text to normalize.
        Returns:
            str: The normalized text.
        '''
        cleaned = re.sub(r'[^A-Za-z0-9]', '', text)
        if not self.case_sensitive:
            cleaned = cleaned.lower()
        return cleaned
    def is_palindrome(self, text):
        '''
        Check whether the given text is a palindrome.
        A palindrome reads the same forwards and backwards after
        normalization (ignoring punctuation, spaces, and case by default).
        Args:
            text (str): The text to check.
        Returns:
            bool: True if the normalized text is a palindrome, False otherwise.
        '''
        normalized = self._normalize(text)
        if len(normalized) < self.min_length:
            return False
        return normalized == normalized[::-1]
    def find_palindrome_words(self, text):
        '''
        Find all palindromic words in the given text.
        Args:
            text (str): The text to scan.
        Returns:
            dict: Mapping of palindrome word -> number of occurrences.
        '''
        words = re.findall(r"[A-Za-z0-9']+", text)
        palindromes = Counter()
        for word in words:
            if self.is_palindrome(word):
                palindromes[word] += 1
        return dict(palindromes)
    def find_palindrome_lines(self, text):
        '''
        Find all lines that are palindromes when considered as a whole.
        Args:
            text (str): The text to scan.
        Returns:
            list: List of tuples (line_number, line_content) for palindromic lines.
        '''
        results = []
        for index, line in enumerate(text.splitlines(), start=1):
            if self.is_palindrome(line):
                results.append((index, line.strip()))
        return results
    def find_palindrome_phrases(self, text):
        '''
        Find all sentences/phrases in the text that are palindromes.
        Sentences are split on common punctuation delimiters (. ! ? ;).
        Args:
            text (str): The text to scan.
        Returns:
            list: List of palindromic phrase strings.
        '''
        phrases = re.split(r'[.!?;]+', text)
        results = []
        for phrase in phrases:
            stripped = phrase.strip()
            if stripped and self.is_palindrome(stripped):
                results.append(stripped)
        return results