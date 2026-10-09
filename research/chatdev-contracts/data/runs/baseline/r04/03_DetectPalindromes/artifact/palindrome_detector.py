'''
palindrome_detector.py
Core palindrome detection logic for the Palindrome Detector application.
This module provides the PalindromeDetector class, which identifies
palindromic single words and palindromic multi-word phrases inside
arbitrary text. Detection is configurable (minimum length, maximum
phrase size, case sensitivity, and whether non-alphanumeric characters
are ignored).
'''
import re
class PalindromeDetector:
    '''
    Detects palindromic words and phrases within text.
    A palindrome is a sequence that reads the same forward and backward.
    By default, comparisons are case-insensitive and ignore punctuation,
    so classics such as "A man, a plan, a canal: Panama" are recognized.
    '''
    # Tokens are runs of letters/digits (ASCII); punctuation acts as a separator.
    WORD_PATTERN = re.compile(r'[A-Za-z0-9]+')
    def __init__(self, min_length=2, max_phrase_words=10,
                 case_sensitive=False, ignore_non_alphanumeric=True):
        '''
        Initialize the detector with configurable behavior.
        :param min_length: minimum normalized character length for a palindrome
        :param max_phrase_words: maximum number of words in a phrase to check
        :param case_sensitive: whether comparison is case-sensitive
        :param ignore_non_alphanumeric: strip non-alphanumeric chars before comparing
        '''
        if min_length < 1:
            raise ValueError('min_length must be at least 1')
        if max_phrase_words < 1:
            raise ValueError('max_phrase_words must be at least 1')
        self.min_length = min_length
        self.max_phrase_words = max_phrase_words
        self.case_sensitive = case_sensitive
        self.ignore_non_alphanumeric = ignore_non_alphanumeric
    def _normalize(self, text):
        '''
        Normalize a text fragment for palindrome comparison.
        :param text: raw text fragment
        :return: normalized string used for comparison
        '''
        if self.ignore_non_alphanumeric:
            text = re.sub(r'[^A-Za-z0-9]', '', text)
        if not self.case_sensitive:
            text = text.lower()
        return text
    def _is_palindrome(self, normalized):
        '''
        Check whether a normalized string is a palindrome.
        :param normalized: already-normalized string
        :return: True if it reads the same forward and backward
        '''
        return len(normalized) >= self.min_length and normalized == normalized[::-1]
    def _extract_tokens(self, text):
        '''
        Split raw text into (word, start_position) tokens.
        :param text: raw text to tokenize
        :return: list of (word, position) tuples in reading order
        '''
        return [(m.group(0), m.start()) for m in self.WORD_PATTERN.finditer(text)]
    def detect(self, text):
        '''
        Detect palindromic words and phrases in the given text.
        :param text: the text to analyze
        :return: dict with keys 'words', 'phrases', 'statistics'
        '''
        tokens = self._extract_tokens(text)
        normalized_tokens = [self._normalize(word) for word, _ in tokens]
        # --- Single-word palindromes ---
        word_hits = []
        for (word, position), normalized in zip(tokens, normalized_tokens):
            if self._is_palindrome(normalized):
                word_hits.append({
                    'text': word,
                    'length': len(normalized),
                    'position': position,
                })
        # --- Multi-word phrase palindromes (sliding windows of 2..max words) ---
        phrase_hits = []
        n = len(tokens)
        for i in range(n):
            for size in range(2, min(self.max_phrase_words, n - i) + 1):
                j = i + size  # exclusive end of the window
                joined = ''.join(normalized_tokens[i:j])
                if self._is_palindrome(joined):
                    phrase_hits.append({
                        'text': ' '.join(w for w, _ in tokens[i:j]),
                        'word_count': size,
                        'position': tokens[i][1],
                    })
        # --- Aggregate duplicates (case-insensitive), preserving first-seen order ---
        words = self._aggregate(word_hits)
        phrases = self._aggregate(phrase_hits)
        statistics = {
            'total_words': n,
            'palindrome_words': len(words),
            'palindrome_phrases': len(phrases),
            'word_occurrences': len(word_hits),
            'phrase_occurrences': len(phrase_hits),
        }
        return {'words': words, 'phrases': phrases, 'statistics': statistics}
    @staticmethod
    def _aggregate(items):
        '''
        Aggregate duplicate entries by text, counting occurrences, preserving order.
        '''
        counts = {}
        order = []
        for item in items:
            key = item['text'].lower()
            if key in counts:
                counts[key]['count'] += 1
            else:
                entry = dict(item)
                entry['count'] = 1
                counts[key] = entry
                order.append(key)
        return [counts[key] for key in order]