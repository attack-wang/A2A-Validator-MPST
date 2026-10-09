'''
README.md
Usage documentation for the Fibonacci Number Generator application.
'''
# Fibonacci Number Generator
A Python application that generates all Fibonacci numbers up to a given
non-negative integer limit.
## Features
- Generates the complete Fibonacci sequence (0, 1, 1, 2, 3, 5, ...) up to
  and including the limit.
- Supports arbitrarily large limits thanks to Python's built-in big integers.
- Provides both an eager list generator (`generate_fibonacci_up_to`) and a
  memory-friendly lazy generator (`fibonacci_generator`).
- Includes a mathematical checker (`is_fibonacci_number`) that tests whether
  a number is a Fibonacci number via the perfect-square property.
## Usage
### One-shot mode
Pass the limit directly as a command-line argument: