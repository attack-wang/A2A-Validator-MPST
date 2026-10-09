'''
README.md
Documentation for the Fibonacci Number Generator application:
how to install, run, and use the tool, along with an overview of
the project structure and features.
'''
# Fibonacci Number Generator
A simple, interactive Python application that generates all
Fibonacci numbers up to a user-specified number (inclusive).
## Requirements
- Python 3.8 or later (uses `math.isqrt`)
- No third-party dependencies — standard library only
## How to Run
Open a terminal in the project folder and execute:
    python main.py
## Project Structure
| File           | Purpose                                                     |
|----------------|-------------------------------------------------------------|
| main.py        | Entry point; orchestrates the application loop              |
| fibonacci.py   | Core logic: sequence generation and Fibonacci tests         |
| interface.py   | User interaction: prompting, validation, result display     |
| utils.py       | Shared helpers: safe parsing/validation of raw user input   |
## Example Session
    ========================================================
         Welcome to the Fibonacci Number Generator!
    ========================================================
    Enter a number to generate Fibonacci numbers up to (or 'quit' to exit): 100
    ========================================================
      Fibonacci numbers up to 100:
    ========================================================
      0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
    --------------------------------------------------------
      Total count : 12
      Largest     : 89
    ========================================================
    Generate another sequence? (y/n): n
    Thank you for using the Fibonacci Generator. Goodbye!
## Features
- Iterative O(n) generation — fast even for very large limits
- Robust input validation with friendly, descriptive error messages
- Detects and highlights when the limit itself is a Fibonacci number
- Quit at any time by typing quit, q, or exit
- Clean multi-file architecture separating logic, interface, and utilities