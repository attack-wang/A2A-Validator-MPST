'''
file_handler.py
File input/output utilities for the Palindrome Detector application.
'''
import os
class FileHandler:
    """Handles reading source text files and writing result files."""
    @staticmethod
    def validate_file(filepath):
        """Raise FileNotFoundError/ValueError if the path is unusable."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Input file not found: {filepath}")
        if not os.path.isfile(filepath):
            raise ValueError(f"Path is not a regular file: {filepath}")
        if not os.access(filepath, os.R_OK):
            raise PermissionError(f"Input file is not readable: {filepath}")
    @staticmethod
    def read_file(filepath, encoding='utf-8'):
        """Read the entire file and return its text content."""
        FileHandler.validate_file(filepath)
        with open(filepath, 'r', encoding=encoding, errors='replace') as fh:
            return fh.read()
    @staticmethod
    def write_file(filepath, content, encoding='utf-8'):
        """Write text content to a file, creating parent dirs if needed."""
        directory = os.path.dirname(os.path.abspath(filepath))
        os.makedirs(directory, exist_ok=True)
        with open(filepath, 'w', encoding=encoding) as fh:
            fh.write(content)