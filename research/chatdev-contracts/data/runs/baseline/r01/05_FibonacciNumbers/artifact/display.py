'''
display.py
Presentation helpers that format and print Fibonacci sequences in a
readable, user-friendly layout.
'''
def format_sequence(sequence, per_line=10):
    """
    Format a sequence of numbers into a readable multi-line string.
    Args:
        sequence (list[int]): The Fibonacci numbers to format.
        per_line (int): Maximum number of values shown per line.
    Returns:
        str: The formatted sequence.
    """
    if not sequence:
        return "(no Fibonacci numbers to display)"
    lines = []
    for start in range(0, len(sequence), per_line):
        chunk = sequence[start:start + per_line]
        lines.append(", ".join(str(num) for num in chunk))
    return "\n".join(lines)
def print_result(limit, sequence):
    """
    Print a summary of the generated Fibonacci sequence.
    Args:
        limit (int): The user-specified limit.
        sequence (list[int]): The generated Fibonacci numbers.
    """
    print(f"\nFibonacci numbers up to {limit}:")
    print(format_sequence(sequence))
    print(f"\nTotal numbers generated: {len(sequence)}")
    if sequence:
        print(f"Largest number generated: {sequence[-1]}")