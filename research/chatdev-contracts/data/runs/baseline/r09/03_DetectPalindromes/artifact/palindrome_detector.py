'''
palindrome_detector.py
Core palindrome detection logic for the application.
This module provides the PalindromeDetector class, which identifies
palindromic words and sentences within a body of text. Normalization is
configurable (case-insensitivity and punctuation stripping) so classic
palindromes such as "A man, a plan, a canal: Panama" are recognized
correctly.
'''
import re
class PalindromeDetector:
    """Detects palindromic words and sentences in free-form text."""
    SENTENCE_SPLIT_PATTERN = re.compile(r'[.!?;]+')
    def __init__(self, ignore_case=True, ignore_punctuation=True, min_length=1):
        """
        Initialize the detector with its comparison settings.
        :param ignore_case: If True, letter casing is ignored when comparing.
        :param ignore_punctuation: If True, non-alphanumeric characters are
                                   stripped before comparing.
        :param min_length: Minimum normalized length for a candidate to be
                           accepted as a palindrome.
        """
        self.ignore_case = ignore_case
        self.ignore_punctuation = ignore_punctuation
        self.min_length = max(int(min_length), 1)
    def normalize(self, text):
        """
        Normalize a string for palindrome comparison.
        :param text: The raw string to normalize.
        :return: The normalized string (lowercased and stripped of
                 non-alphanumeric characters, according to configuration).
        """
        if self.ignore_case:
            text = text.lower()
        if self.ignore_punctuation:
            text = ''.join(ch for ch in text if ch.isalnum())
        return text
    def is_palindrome(self, text):
        """
        Determine whether a single string is a palindrome.
        :param text: The string to test.
        :return: True if the normalized string reads the same forwards and
                 backwards and meets the minimum length requirement.
        """
        normalized = self.normalize(text)
        if len(normalized) < self.min_length:
            return False
        return normalized == normalized[::-1]
    def find_word_palindromes(self, text):
        """
        Find every palindromic word (whitespace-separated token) in text.
        :param text: The text to scan.
        :return: A list of dictionaries with keys 'word', 'line' and
                 'position' describing each palindromic token found.
        """
        results = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            for position, token in enumerate(line.split(), start=1):
                if self.is_palindrome(token):
                    results.append({
                        'word': token,
                        'line': line_number,
                        'position': position
                    })
        return results
    def find_sentence_palindromes(self, text):
        """
        Find every palindromic sentence or phrase in text.
        Lines are split into sentence-like chunks on common terminators
        (. ! ? ;) and each chunk is tested as a whole after normalization.
        :param text: The text to scan.
        :return: A list of dictionaries with keys 'sentence' and 'line'.
        """
        results = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            for sentence in self.split_sentences(line):
                if self.is_palindrome(sentence):
                    results.append({
                        'sentence': sentence.strip(),
                        'line': line_number
                    })
        return results
    @classmethod
    def split_sentences(cls, line):
        """
        Split a single line of text into sentence-like chunks.
        :param line: One line of text (no newlines).
        :return: A list of non-empty sentence strings.
        """
        chunks = cls.SENTENCE_SPLIT_PATTERN.split(line)
        return [chunk for chunk in chunks if chunk.strip()]
    def analyze(self, text):
        """
        Perform a complete palindrome analysis of the given text.
        :param text: The full text to analyze.
        :return: A dictionary containing:
                 - 'whole_text_is_palindrome': bool
                 - 'word_palindromes': list of word match dictionaries
                 - 'sentence_palindromes': list of sentence match dictionaries
                 - 'unique_word_palindromes': sorted list of unique matches
                 - 'total_words_scanned': int
                 - 'total_sentences_scanned': int
        """
        word_palindromes = self.find_word_palindromes(text)
        sentence_palindromes = self.find_sentence_palindromes(text)
        unique_words = sorted({
            self.normalize(item['word']) for item in word_palindromes
        })
        total_words = sum(len(line.split()) for line in text.splitlines())
        total_sentences = sum(
            len(self.split_sentences(line)) for line in text.splitlines()
        )
        return {
            'whole_text_is_palindrome': self.is_palindrome(text),
            'word_palindromes': word_palindromes,
            'sentence_palindromes': sentence_palindromes,
            'unique_word_palindromes': unique_words,
            'total_words_scanned': total_words,
            'total_sentences_scanned': total_sentences
        }