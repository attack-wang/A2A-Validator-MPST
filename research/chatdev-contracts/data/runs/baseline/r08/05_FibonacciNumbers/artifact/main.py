'''
test_fibonacci.py
Unit tests for the Fibonacci application. Run with:
    python -m unittest test_fibonacci.py
'''
import unittest
from fibonacci import fibonacci_generator, generate_fibonacci, is_fibonacci_number
from utils import InputValidationError, parse_integer, validate_limit
class TestGenerateFibonacci(unittest.TestCase):
    '''Tests for generate_fibonacci.'''
    def test_zero_limit(self):
        self.assertEqual(generate_fibonacci(0), [0])
    def test_one_limit(self):
        self.assertEqual(generate_fibonacci(1), [0, 1, 1])
    def test_typical_limit(self):
        self.assertEqual(generate_fibonacci(10), [0, 1, 1, 2, 3, 5, 8])
    def test_exact_boundary(self):
        self.assertEqual(generate_fibonacci(13)[-1], 13)
    def test_negative_limit(self):
        self.assertEqual(generate_fibonacci(-5), [])
    def test_large_limit_length(self):
        # Fibonacci numbers below 10**100 number 481 in total.
        self.assertEqual(len(generate_fibonacci(10 ** 100)), 481)
class TestFibonacciGenerator(unittest.TestCase):
    '''Tests for the lazy generator.'''
    def test_matches_list_version(self):
        self.assertEqual(
            list(fibonacci_generator(1000)), generate_fibonacci(1000)
        )
    def test_lazy_first_values(self):
        generator = fibonacci_generator(100)
        self.assertEqual(next(generator), 0)
        self.assertEqual(next(generator), 1)
class TestIsFibonacciNumber(unittest.TestCase):
    '''Tests for the membership test.'''
    def test_known_members(self):
        for n in (0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144):
            self.assertTrue(is_fibonacci_number(n), msg=str(n))
    def test_known_non_members(self):
        for n in (4, 6, 7, 9, 10, 11, 12, 14, 100):
            self.assertFalse(is_fibonacci_number(n), msg=str(n))
    def test_negative(self):
        self.assertFalse(is_fibonacci_number(-1))
class TestUtils(unittest.TestCase):
    '''Tests for parsing and validation helpers.'''
    def test_parse_integer_ok(self):
        self.assertEqual(parse_integer(" 42 "), 42)
    def test_parse_integer_invalid(self):
        with self.assertRaises(InputValidationError):
            parse_integer("abc")
    def test_parse_integer_empty(self):
        with self.assertRaises(InputValidationError):
            parse_integer("   ")
    def test_validate_limit_ok(self):
        self.assertEqual(validate_limit(0), 0)
    def test_validate_limit_negative(self):
        with self.assertRaises(InputValidationError):
            validate_limit(-1)
if __name__ == "__main__":
    unittest.main()