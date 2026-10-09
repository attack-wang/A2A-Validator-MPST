'''
file_handler.py
File input utilities for the palindrome detector.
Contains:
- FileHandler: validates and reads text files with encoding fallback.
'''
import os
class FileHandler:
    """Reads text files, trying several encodings before giving up."""
    DEFAULT_ENCODINGS = ("utf-8", "utf-8-sig", "latin-1")
    def read_file(self, path):
        """Return the full text content of `path` as a single string."""
        self.validate_file(path)
        last_error = None
        for encoding in self.DEFAULT_ENCODINGS:
            try:
                with open(path, "r", encoding=encoding, newline=None) as handle:
                    return handle.read()
            except UnicodeDecodeError as exc:
                last_error = exc
        raise ValueError(
            f"Could not decode '{path}' using any of the encodings: "
            f"{', '.join(self.DEFAULT_ENCODINGS)} (last error: {last_error})"
        )
    def validate_file(self, path):
        """Ensure `path` exists, is a regular file, and is readable."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Input file not found: '{path}'")
        if not os.path.isfile(path):
            raise IsADirectoryError(f"Input path is not a regular file: '{path}'")
        if not os.access(path, os.R_OK):
            raise PermissionError(f"Input file is not readable: '{path}'")