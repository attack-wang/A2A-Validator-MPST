'''
test_palindrome_detector.py
Unit tests for the PalindromeDetector class.
Run with: python -m unittest test_palindrome_detector.py
'''
import unittest
from palindrome_detector import PalindromeDetector
class TestPalindromeDetector(unittest.TestCase):
    '''
    Test suite covering palindrome detection at word, line, and phrase
    granularity, as well as normalization, case sensitivity, minimum
    length filtering, and edge cases.
    '''
    def setUp(self):
        '''
        Create a default detector instance for reuse across tests.
        '''
        self.detector = PalindromeDetector()
    def test_is_palindrome_basic(self):
        '''
        Verify basic palindrome and non-palindrome detection.
        '''
        self.assertTrue(self.detector.is_palindrome("racecar"))
        self.assertFalse(self.detector.is_palindrome("hello"))
    def test_is_palindrome_ignores_punctuation_and_case(self):
        '''
        Verify that punctuation, spaces, and casing are ignored by default.
        '''
        self.assertTrue(self.detector.is_palindrome("A man, a plan, a canal: Panama!"))
        self.assertTrue(self.detector.is_palindrome("Was it a car or a cat I saw?"))
    def test_is_palindrome_case_sensitive(self):
        '''
        Verify that case-sensitive mode rejects mixed-case palindromes.
        '''
        strict = PalindromeDetector(case_sensitive=True)
        self.assertFalse(strict.is_palindrome("Madam"))  # "Madam" != "madaM"
        self.assertTrue(strict.is_palindrome("racecar"))
    def test_min_length_filters_short_candidates(self):
        '''
        Verify that candidates shorter than min_length are rejected.
        '''
        strict = PalindromeDetector(min_length=3)
        self.assertFalse(strict.is_palindrome("a"))
        self.assertTrue(strict.is_palindrome("noon"))
    def test_find_palindrome_words(self):
        '''
        Verify detection and counting of palindromic words in text.
        '''
        result = self.detector.find_palindrome_words("Madam and racecar saw a noon")
        self.assertIn("Madam", result)
        self.assertIn("racecar", result)
        self.assertEqual(result["a"], 1)
    def test_find_palindrome_lines(self):
        '''
        Verify detection of whole lines that are palindromes, with
        correct line numbering.
        '''
        text = "hello world\nNever odd or even\nplain line"
        result = self.detector.find_palindrome_lines(text)
        self.assertEqual(result, [(2, "Never odd or even")])
    def test_find_palindrome_phrases(self):
        '''
        Verify detection of palindromic sentences split on punctuation.
        '''
        text = "Was it a car or a cat I saw? This is not. Never odd or even."
        result = self.detector.find_palindrome_phrases(text)
        self.assertEqual(len(result), 2)
        self.assertIn("Was it a car or a cat I saw", result[0])
    def test_empty_and_non_palindrome_input(self):
        '''
        Verify graceful handling of empty strings and non-palindromic text.
        '''
        self.assertFalse(self.detector.is_palindrome(""))
        self.assertEqual(self.detector.find_palindrome_words("abc def"), {})
if __name__ == '__main__':
    unittest.main()