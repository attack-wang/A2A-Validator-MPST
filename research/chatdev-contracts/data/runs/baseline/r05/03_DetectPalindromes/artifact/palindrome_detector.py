'''
palindrome_detector.py
Core palindrome detection logic for the Palindrome Detector application.
Provides the PalindromeDetector class, which determines whether strings
are palindromes and scans larger bodies of text for palindromic words,
phrases, and sentences.
'''
import re
import string
class PalindromeDetector:
    '''
    Detects palindromes within arbitrary text.
    A palindrome is a sequence that reads the same forward and backward.
    By default the detector ignores letter casing and non-alphanumeric
    characters (spaces, punctuation), so phrases such as
    "A man, a plan, a canal: Panama" are recognized as palindromes.
    Any non-empty normalized sequence counts, including single
    characters such as "a" or "I"; only empty strings are rejected.
    '''
    def __init__(self, ignore_case=True, ignore_non_alphanumeric=True):
        '''
        Initialize the detector with its matching behavior.
        Args:
            ignore_case (bool): If True, comparisons are case-insensitive.
            ignore_non_alphanumeric (bool): If True, spaces and punctuation
                are removed before comparison.
        '''
        self.ignore_case = ignore_case
        self.ignore_non_alphanumeric = ignore_non_alphanumeric
    def normalize(self, text):
        '''
        Normalize a string according to the detector configuration.
        Args:
            text (str): The raw string to normalize.
        Returns:
            str: The normalized string used for palindrome comparison.
        '''
        if text is None:
            return ""
        normalized = text
        if self.ignore_non_alphanumeric:
            normalized = "".join(ch for ch in normalized if ch.isalnum())
        if self.ignore_case:
            normalized = normalized.lower()
        return normalized
    def is_palindrome(self, text):
        '''
        Check whether the provided text is a palindrome.
        A palindrome is any non-empty sequence that equals its own
        reverse; single characters therefore qualify.
        Args:
            text (str): The word, phrase, or sentence to check.
        Returns:
            bool: True if the text is a palindrome, False otherwise.
        '''
        normalized = self.normalize(text)
        if not normalized:
            return False
        return normalized == normalized[::-1]
    @staticmethod
    def _clean_word(word):
        '''
        Strip surrounding punctuation from a single word token.
        Args:
            word (str): The raw word token.
        Returns:
            str: The word without leading/trailing punctuation.
        '''
        return word.strip(string.punctuation)
    def find_palindromic_words(self, text):
        '''
        Scan the text and collect all palindromic words.
        Args:
            text (str): The text to scan.
        Returns:
            list: Entries describing each palindromic word, containing the
                cleaned word, its token position, and the original token.
        '''
        results = []
        tokens = text.split()
        for position, token in enumerate(tokens):
            cleaned = self._clean_word(token)
            if cleaned and self.is_palindrome(cleaned):
                results.append({
                    "text": cleaned,
                    "position": position,
                    "original": token,
                })
        return results
    def find_palindromic_phrases(self, text, max_words=12):
        '''
        Find palindromic phrases made of consecutive words (3+ words).
        For every starting word, only the longest palindromic phrase is
        reported to avoid redundant nested matches.
        Args:
            text (str): The text to scan.
            max_words (int): Maximum phrase length (in words) to consider.
        Returns:
            list: Entries describing each palindromic phrase, containing
                the phrase text, its starting token index, and word count.
        '''
        results = []
        tokens = [self._clean_word(token) for token in text.split()]
        total = len(tokens)
        for start in range(total):
            longest = None
            max_length = min(max_words, total - start)
            for length in range(max_length, 2, -1):
                candidate = tokens[start:start + length]
                if any(not word for word in candidate):
                    continue
                phrase = " ".join(candidate)
                if self.is_palindrome(phrase):
                    longest = {
                        "text": phrase,
                        "start": start,
                        "word_count": length,
                    }
                    break
            if longest is not None:
                results.append(longest)
        return results
    def find_palindromic_sentences(self, text):
        '''
        Scan the text and collect all palindromic sentences.
        Args:
            text (str): The text to scan.
        Returns:
            list: Entries describing each palindromic sentence, containing
                the sentence text and its sentence index.
        '''
        results = []
        sentences = self.split_sentences(text)
        for index, sentence in enumerate(sentences):
            if sentence and self.is_palindrome(sentence):
                results.append({
                    "text": sentence,
                    "index": index,
                })
        return results
    @staticmethod
    def split_sentences(text):
        '''
        Split raw text into sentences on punctuation boundaries.
        Args:
            text (str): The text to split.
        Returns:
            list: Cleaned sentence strings.
        '''
        parts = re.split(r"(?<=[.!?])\s+", text)
        return [part.strip() for part in parts if part and part.strip()]
    def analyze(self, text):
        '''
        Perform a full palindrome analysis on the given text.
        Args:
            text (str): The text to analyze.
        Returns:
            dict: Summary containing total word/sentence counts and the
                lists of palindromic words, phrases, and sentences.
        '''
        palindromic_words = self.find_palindromic_words(text)
        palindromic_phrases = self.find_palindromic_phrases(text)
        palindromic_sentences = self.find_palindromic_sentences(text)
        return {
            "total_words": len(text.split()),
            "total_sentences": len(self.split_sentences(text)),
            "palindromic_words": palindromic_words,
            "palindromic_phrases": palindromic_phrases,
            "palindromic_sentences": palindromic_sentences,
            "palindrome_count": len(palindromic_words),
        }