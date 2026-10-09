'''
test_fibonacci.py
Unit tests for the Fibonacci generation logic.
Run with: python test_fibonacci.py
'''
import unittest
from fibonacci import fibonacci_generator, generate_fibonacci_up_to
class TestFibonacci(unittest.TestCase):
    '''Test suite covering generator and list-builder behaviour.'''
    def test_zero_limit(self):
        '''A limit of 0 yields only the first Fibonacci number.'''
        self.assertEqual(generate_fibonacci_up_to(0), [0])
    def test_small_limit(self):
        '''A limit of 10 yields the classic small sequence.'''
        self.assertEqual(generate_fibonacci_up_to(10), [0, 1, 1, 2, 3, 5, 8])
    def test_exact_boundary(self):
        '''A limit equal to a Fibonacci number includes that number.'''
        self.assertEqual(generate_fibonacci_up_to(13), [0, 1, 1, 2, 3, 5, 8, 13])
    def test_large_limit(self):
        '''A large limit produces the expected long sequence.'''
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        self.assertEqual(generate_fibonacci_up_to(144), expected)
    def test_negative_limit_raises(self):
        '''Negative limits are rejected with ValueError.'''
        with self.assertRaises(ValueError):
            generate_fibonacci_up_to(-1)
    def test_non_integer_raises(self):
        '''Non-integer limits are rejected with TypeError.'''
        with self.assertRaises(TypeError):
            generate_fibonacci_up_to(3.5)
    def test_generator_lazy(self):
        '''The generator yields values lazily and matches the list builder.'''
        gen_values = [n for n in fibonacci_generator(100)]
        self.assertEqual(gen_values, generate_fibonacci_up_to(100))
if __name__ == "__main__":
    unittest.main()