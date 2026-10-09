<!--
README.md
Documentation for the Fibonacci Generator application.
Covers: overview, requirements, usage (one-shot and interactive modes),
examples, and project structure.
Updated: documents graceful EOF/Ctrl-C handling in interactive mode and
the sample_output.txt artifact (renamed from the invalid stray `.py` file).
-->
# Fibonacci Generator
A simple Python application that generates all Fibonacci numbers up to a
given number.
## Requirements
- Python 3.6+ (no external dependencies)
## Usage
### One-shot mode (command-line argument)
    python main.py 50
Output:
    Fibonacci numbers up to 50:
    0, 1, 1, 2, 3, 5, 8, 13, 21, 34
### Interactive mode
    python main.py
Then follow the prompts:
    Fibonacci Generator (interactive mode)
    Enter a non-negative integer limit, or 'q' to quit.
    Enter a limit: 20
    Fibonacci numbers up to 20:
    0, 1, 1, 2, 3, 5, 8, 13
    Enter a limit: q
    Goodbye!
### Non-interactive / automated environments
When stdin is closed or exhausted (e.g., `python main.py < /dev/null`,
empty piped input, or automated test harnesses), interactive mode exits
gracefully instead of crashing:
    Input stream closed. Goodbye!
## Project Structure
| File                | Purpose                                              |
|---------------------|------------------------------------------------------|
| `main.py`           | Entry point; CLI parsing and user interaction        |
| `fibonacci.py`      | Core Fibonacci generation and input validation logic |
| `utils.py`          | Output formatting and argument parser helpers        |
| `sample_output.txt` | Sample program output (reference only, not code)     |
## Error Handling
- Non-integer input (e.g., `abc`, `3.5`) → error message, exit code 1 in one-shot mode.
- Negative numbers → error message explaining the limit must be non-negative.
- Empty input in interactive mode → re-prompt.
- Closed/empty stdin in interactive mode → graceful exit ("Input stream closed. Goodbye!"), exit code 0.
- Ctrl-C in interactive mode → graceful exit ("Interrupted. Goodbye!").