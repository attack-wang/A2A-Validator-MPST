'''
Input parsing and validation utilities.
Provides the InputValidator class, responsible for:
- Detecting quit commands.
- Converting raw user input into an integer.
- Ensuring the resulting value is a non-negative integer.
All failures raise ValueError with user-friendly messages that the
main loop forwards to the Display module.
'''
class InputValidator:
    """Parses and validates user input for the Fibonacci application."""
    QUIT_COMMANDS = ("q", "quit", "exit")
    @staticmethod
    def is_quit_command(raw_input):
        """Return True if the raw input is a quit command."""
        return raw_input.strip().lower() in InputValidator.QUIT_COMMANDS
    @staticmethod
    def parse(raw_input):
        """Convert raw string input into an integer.
        Args:
            raw_input (str): The raw text entered by the user.
        Returns:
            int: The parsed integer value.
        Raises:
            ValueError: If the input is empty or not a valid integer.
        """
        text = raw_input.strip()
        if not text:
            raise ValueError(
                "Input cannot be empty. Please enter a non-negative integer."
            )
        try:
            return int(text)
        except ValueError:
            raise ValueError(
                f"'{text}' is not a valid integer. "
                "Please enter a non-negative integer."
            )
    @staticmethod
    def validate(value):
        """Ensure the parsed value is a non-negative integer.
        Args:
            value (int): The parsed integer to validate.
        Returns:
            int: The validated value (unchanged).
        Raises:
            ValueError: If the value is negative.
        """
        if value < 0:
            raise ValueError(
                "The limit must be a non-negative integer (0 or greater)."
            )
        return value