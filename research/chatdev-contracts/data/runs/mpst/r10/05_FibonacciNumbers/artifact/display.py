'''
Console output formatting and display utilities.
Provides the Display class, which centralizes every piece of text the
application prints: the welcome banner, the input prompt, formatted
result listings, error messages, and the goodbye message.
'''
class Display:
    """Formats and prints all application output to the console."""
    BANNER = "=" * 50
    @staticmethod
    def show_welcome():
        """Print the application welcome banner."""
        print(Display.BANNER)
        print("        Fibonacci Number Generator")
        print(Display.BANNER)
        print("Generate all Fibonacci numbers up to a given number.\n")
    @staticmethod
    def prompt():
        """Show the input prompt and return the user's raw input."""
        return input("Enter a number (or 'q' to quit): ")
    @staticmethod
    def show_results(numbers, limit):
        """Print the generated Fibonacci numbers in a numbered list.
        Args:
            numbers (list[int]): The Fibonacci numbers to display.
            limit (int): The upper limit used for generation.
        """
        print(f"\nFibonacci numbers up to {limit}:")
        if not numbers:
            print("  (no Fibonacci numbers found)")
        else:
            for position, number in enumerate(numbers, start=1):
                print(f"  {position:>3}. {number}")
        print(f"\nTotal Fibonacci numbers generated: {len(numbers)}\n")
    @staticmethod
    def show_error(message):
        """Print a formatted error message."""
        print(f"Error: {message}\n")
    @staticmethod
    def show_goodbye():
        """Print the goodbye message."""
        print("Goodbye! Thank you for using the Fibonacci Generator.")