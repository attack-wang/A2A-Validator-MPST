import unittest
from main import fibonacci_up_to


class TestFibonacci(unittest.TestCase):
    def test_negative(self):
        self.assertEqual(fibonacci_up_to(-5), [])

    def test_zero(self):
        self.assertEqual(fibonacci_up_to(0), [0])

    def test_small(self):
        self.assertEqual(fibonacci_up_to(10), [0, 1, 1, 2, 3, 5, 8])

    def test_large(self):
        self.assertEqual(fibonacci_up_to(100)[-1], 89)


if __name__ == "__main__":
    unittest.main()