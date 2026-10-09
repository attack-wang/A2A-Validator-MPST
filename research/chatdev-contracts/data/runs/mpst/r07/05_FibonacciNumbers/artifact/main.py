'''
test_fibonacci.py
Unit tests for the core Fibonacci module (fibonacci.py).
Run with:
    python -m unittest test_fibonacci.py -v
'''
import unittest
from fibonacci import (
    fibonacci_generator,
    generate_fibonacci_up_to,
    is_fibonacci,
    parse_limit,
)
class TestFibonacciGenerator(unittest.TestCase):
    """Tests for the lazy fibonacci_generator."""
    def test_basic_sequence(self):
        self.assertEqual(list(fibonacci_generator(10)), [0, 1, 1, 2, 3, 5, 8])
    def test_limit_zero(self):
        self.assertEqual(list(fibonacci_generator(0)), [0])
    def test_limit_one(self):
        self.assertEqual(list(fibonacci_generator(1)), [0, 1, 1])
    def test_limit_is_inclusive(self):
        # 13 is a Fibonacci number and must be included for limit 13.
        self.assertEqual(list(fibonacci_generator(13))[-1], 13)
    def test_negative_limit_raises(self):
        with self.assertRaises(ValueError):
            list(fibonacci_generator(-5))
    def test_large_limit_last_term(self):
        numbers = list(fibonacci_generator(10 ** 12))
        self.assertEqual(numbers[-1], 956722026041)
        self.assertLessEqual(numbers[-1], 10 ** 12)
class TestGenerateFibonacciUpTo(unittest.TestCase):
    """Tests for the list-returning wrapper."""
    def test_returns_full_list(self):
        self.assertEqual(
            generate_fibonacci_up_to(100),
            [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89],
        )
    def test_negative_limit_raises(self):
        with self.assertRaises(ValueError):
            generate_fibonacci_up_to(-1)
class TestIsFibonacci(unittest.TestCase):
    """Tests for the Fibonacci membership check."""
    def test_known_fibonacci_numbers(self):
        for n in (0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 956722026041):
            self.assertTrue(is_fibonacci(n), f"{n} should be a Fibonacci number")
    def test_non_fibonacci_numbers(self):
        for n in (4, 6, 7, 9, 10, 11, 12, 100):
            self.assertFalse(is_fibonacci(n), f"{n} should not be a Fibonacci number")
    def test_negative_numbers(self):
        self.assertFalse(is_fibonacci(-1))
class TestParseLimit(unittest.TestCase):
    """Tests for input validation."""
    def test_valid_input(self):
        self.assertEqual(parse_limit("42"), 42)
        self.assertEqual(parse_limit("  7  "), 7)
        self.assertEqual(parse_limit("0"), 0)
    def test_invalid_input(self):
        for bad in ("", "   ", "abc", "3.5", "-4"):
            with self.assertRaises(ValueError):
                parse_limit(bad)
if __name__ == "__main__":
    unittest.main()