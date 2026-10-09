'''
palindrome_detector.py
Core module containing the PalindromeDetector class, which finds
palindromic words and phrases in a given block of text.
Words are extracted as sequences of letters/digits (optionally with
internal apostrophes). Each candidate is normalized according to the
detector's configuration (case folding, stripping non-alphanumeric
characters) and then checked against its reverse.
'''
import re
# Tokens are sequences of letters/digits, optionally containing
# internal apostrophes (e.g., "madam's" -> token "madam's").
WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*")
class PalindromeDetector:
    '''
    Detects palindromic words and phrases within a block of text.
    '''
    def __init__(self, ignore_case=True, ignore_non_alphanumeric=True, min_length=3):
        '''
        Initialize the detector with normalization options.
        :param ignore_case: if True, letter casing is ignored during checks.
        :param ignore_non_alphanumeric: if True, spaces/punctuation are ignored.
        :param min_length: minimum normalized length for a token to be considered.
        '''
        self.ignore_case = ignore_case
        self.ignore_non_alphanumeric = ignore_non_alphanumeric
        self.min_length = min_length
    def _normalize(self, text):
        '''
        Normalize a candidate string according to detector settings.
        :param text: raw candidate string.
        :return: normalized string used for palindrome checking.
        '''
        if self.ignore_case:
            text = text.lower()
        if self.ignore_non_alphanumeric:
            text = ''.join(ch for ch in text if ch.isalnum())
        return text
    def _is_palindrome(self, normalized):
        '''
        Check whether a normalized string qualifies as a palindrome.
        :param normalized: normalized candidate string.
        :return: True if the string is a palindrome of sufficient length.
        '''
        return len(normalized) >= self.min_length and normalized == normalized[::-1]
    def analyze(self, text):
        '''
        Analyze text for palindromic words and phrases, line by line.
        :param text: full text content to analyze.
        :return: dict with 'word_palindromes' and 'phrase_palindromes',
                 each a list of (candidate, line_number) tuples.
        '''
        word_palindromes = []
        phrase_palindromes = []
        seen_words = set()
        seen_phrases = set()
        for line_number, line in enumerate(text.splitlines(), start=1):
            words = WORD_PATTERN.findall(line)
            # --- Word-level detection ---
            for word in words:
                normalized = self._normalize(word)
                if self._is_palindrome(normalized) and normalized not in seen_words:
                    seen_words.add(normalized)
                    word_palindromes.append((word, line_number))
            # --- Phrase-level detection (multi-word palindromes) ---
            for start in range(len(words)):
                for end in range(start + 2, len(words) + 1):
                    phrase = ' '.join(words[start:end])
                    normalized = self._normalize(phrase)
                    if self._is_palindrome(normalized) and normalized not in seen_phrases:
                        seen_phrases.add(normalized)
                        phrase_palindromes.append((phrase, line_number))
        return {
            'word_palindromes': word_palindromes,
            'phrase_palindromes': phrase_palindromes,
        }