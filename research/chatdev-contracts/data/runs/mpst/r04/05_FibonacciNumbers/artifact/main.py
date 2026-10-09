'''
test_fibonacci.py
Unit tests for the Fibonacci generation logic and input utilities.
Run with: python -m unittest test_fibonacci.py
'''
import unittest
from fibonacci import FibonacciGenerator, generate_fibonacci_up_to
from utils import parse_input, format_output
class TestGenerateFibonacciUpTo(unittest.TestCase):
    '''Tests for the generate_fibonacci_up_to function.'''
    def test_zero_limit(self):
        '''A limit of 0 should yield only [0].'''
        self.assertEqual(generate_fibonacci_up_to(0), [0])
    def test_one_limit(self):
        '''A limit of 1 should yield [0, 1, 1].'''
        self.assertEqual(generate_fibonacci_up_to(1), [0, 1, 1])
    def test_small_limit(self):
        '''A limit of 10 should yield the sequence up to 8.'''
        self.assertEqual(generate_fibonacci_up_to(10), [0, 1, 1, 2, 3, 5, 8])
    def test_exact_limit_included(self):
        '''The limit itself should be included when it is a Fibonacci number.'''
        self.assertEqual(generate_fibonacci_up_to(13)[-1], 13)
    def test_negative_limit_raises(self):
        '''Negative limits should raise a ValueError.'''
        with self.assertRaises(ValueError):
            generate_fibonacci_up_to(-1)
class TestFibonacciGenerator(unittest.TestCase):
    '''Tests for the FibonacciGenerator class.'''
    def test_generate_matches_function(self):
        '''The class-based generator should match the functional interface.'''
        self.assertEqual(FibonacciGenerator(100).generate(),
                         generate_fibonacci_up_to(100))
    def test_iteration(self):
        '''Iterating the generator should yield Fibonacci numbers one by one.'''
        self.assertEqual(list(FibonacciGenerator(20)),
                         [0, 1, 1, 2, 3, 5, 8, 13])
    def test_str(self):
        '''The string representation should join numbers with commas.'''
        self.assertEqual(str(FibonacciGenerator(5)), "0, 1, 1, 2, 3, 5")
    def test_negative_limit_raises(self):
        '''Constructing with a negative limit should raise a ValueError.'''
        with self.assertRaises(ValueError):
            FibonacciGenerator(-5)
class TestUtils(unittest.TestCase):
    '''Tests for input parsing and output formatting utilities.'''
    def test_parse_valid_integer(self):
        '''A plain integer string should parse correctly.'''
        self.assertEqual(parse_input("100"), 100)
    def test_parse_with_whitespace(self):
        '''Surrounding whitespace should be ignored.'''
        self.assertEqual(parse_input("  42  "), 42)
    def test_parse_empty_raises(self):
        '''Empty input should raise a ValueError.'''
        with self.assertRaises(ValueError):
            parse_input("")
    def test_parse_non_integer_raises(self):
        '''Non-integer text should raise a ValueError.'''
        with self.assertRaises(ValueError):
            parse_input("abc")
    def test_parse_negative_raises(self):
        '''Negative numbers should raise a ValueError.'''
        with self.assertRaises(ValueError):
            parse_input("-3")
    def test_format_output_empty(self):
        '''An empty list should produce a friendly message.'''
        self.assertIn("No Fibonacci", format_output([]))
    def test_format_output_numbers(self):
        '''A non-empty list should list all numbers.'''
        result = format_output([0, 1, 1, 2])
        self.assertIn("0, 1, 1, 2", result)
if __name__ == "__main__":
    unittest.main()