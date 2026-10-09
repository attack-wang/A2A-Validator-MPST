'''
palindrome_detector.py
Core palindrome detection logic for the Palindrome Finder application.
This module provides the PalindromeDetector class, which is responsible for
determining whether given text is a palindrome and for scanning larger
bodies of text for palindromic words, sentences, and substrings.
'''
import re
class PalindromeDetector:
    '''
    Detects palindromes within raw text using configurable rules.
    '''
    # Words may contain internal apostrophes/hyphens, e.g. "don't", "well-known".
    WORD_PATTERN = re.compile(r"[A-Za-z0-9]+(?:['\-][A-Za-z0-9]+)*")
    # A sentence is a run of characters ending at (or lacking) ., ! or ?.
    SENTENCE_PATTERN = re.compile(r"[^.!?]+[.!?]*")
    # Sentences shorter than this (after normalization) are ignored so that
    # trivial one-character "palindromes" such as "I." are not reported.
    MIN_SENTENCE_LENGTH = 3
    def __init__(self, min_word_length=1, case_insensitive=True, ignore_non_alphanumeric=True):
        '''
        Configure the detector's normalization and filtering rules.
        :param min_word_length: minimum normalized length for a word to count
        :param case_insensitive: if True, compare letters case-insensitively
        :param ignore_non_alphanumeric: if True, strip punctuation when comparing
        '''
        self.min_word_length = min_word_length
        self.case_insensitive = case_insensitive
        self.ignore_non_alphanumeric = ignore_non_alphanumeric
    def normalize(self, text):
        '''
        Normalize text according to detector settings: optionally lowercase
        it and strip characters that should be ignored when comparing.
        '''
        if self.case_insensitive:
            text = text.lower()
        if self.ignore_non_alphanumeric:
            # If the text was not lowercased above, IGNORECASE is required so
            # that uppercase letters are stripped as well.
            flags = 0 if self.case_insensitive else re.IGNORECASE
            text = re.sub(r"[^a-z0-9]", "", text, flags=flags)
        else:
            # Even when punctuation is kept, whitespace must be removed so
            # phrase palindromes ("never odd or even") are still detected.
            text = re.sub(r"\s+", "", text)
        return text
    def is_palindrome(self, text):
        '''
        Return True if the normalized text reads the same forwards and
        backwards and satisfies the minimum length requirement.
        '''
        normalized = self.normalize(text)
        if not normalized or len(normalized) < self.min_word_length:
            return False
        return normalized == normalized[::-1]
    def find_palindromic_words(self, text):
        '''
        Scan the text for palindromic words.
        Returns a list of dictionaries sorted by frequency (descending):
            {"word": original word, "normalized": cleaned form,
             "count": occurrences, "positions": [character offsets]}
        '''
        found = {}
        for match in self.WORD_PATTERN.finditer(text):
            word = match.group(0)
            normalized = self.normalize(word)
            if len(normalized) < self.min_word_length:
                continue
            if normalized != normalized[::-1]:
                continue
            entry = found.setdefault(
                normalized,
                {"word": word, "normalized": normalized, "count": 0, "positions": []},
            )
            entry["count"] += 1
            if match.start() not in entry["positions"]:
                entry["positions"].append(match.start())
        return sorted(found.values(), key=lambda e: (-e["count"], e["normalized"]))
    def find_palindromic_sentences(self, text):
        '''
        Scan the text for palindromic sentences (punctuation/spaces ignored).
        Returns a list of dictionaries:
            {"index": 1-based sentence number, "sentence": original sentence}
        '''
        results = []
        for index, match in enumerate(self.SENTENCE_PATTERN.finditer(text), start=1):
            sentence = match.group(0).strip()
            if not sentence:
                continue
            normalized = self.normalize(sentence)
            if len(normalized) < self.MIN_SENTENCE_LENGTH:
                continue
            if normalized == normalized[::-1]:
                results.append({"index": index, "sentence": sentence})
        return results
    def find_palindromic_substrings(self, text, min_length=3):
        '''
        Find unique palindromic substrings (length >= min_length) occurring
        inside the word tokens of the text, using center expansion so that
        every palindromic span is captured, not only the maximal ones.
        Returns a list of strings sorted by length (descending), then
        alphabetically.
        '''
        found = set()
        for match in self.WORD_PATTERN.finditer(text):
            token = self.normalize(match.group(0))
            n = len(token)
            if n < min_length:
                continue
            for center in range(n):
                # Odd-length palindromes centered on `center`.
                left = right = center
                while left >= 0 and right < n and token[left] == token[right]:
                    if right - left + 1 >= min_length:
                        found.add(token[left:right + 1])
                    left -= 1
                    right += 1
                # Even-length palindromes centered between center/center+1.
                left, right = center, center + 1
                while left >= 0 and right < n and token[left] == token[right]:
                    if right - left + 1 >= min_length:
                        found.add(token[left:right + 1])
                    left -= 1
                    right += 1
        return sorted(found, key=lambda s: (-len(s), s))
    def detect_all(self, text, include_sentences=False, include_substrings=False, min_substring_length=3):
        '''
        Convenience method that runs the enabled scans in one pass and
        returns a dictionary suitable for ReportGenerator.
        '''
        return {
            "words": self.find_palindromic_words(text),
            "sentences": self.find_palindromic_sentences(text) if include_sentences else [],
            "substrings": self.find_palindromic_substrings(text, min_substring_length) if include_substrings else [],
        }