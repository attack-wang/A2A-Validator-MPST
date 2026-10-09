'''
File input/output utilities for the Palindrome Detector.
This module handles reading the input text file and writing result
reports to disk, with consistent error handling via FileHandlerError.
'''
import os
class FileHandlerError(Exception):
    """Raised when a file operation fails (missing file, unreadable, unwritable, etc.)."""
    pass
def validate_file_exists(filepath):
    """
    Validate that the given path exists and is a file.
    :param filepath: Path to check.
    :raises FileHandlerError: If the path does not exist or is not a file.
    """
    if not os.path.exists(filepath):
        raise FileHandlerError(f"File not found: '{filepath}'")
    if not os.path.isfile(filepath):
        raise FileHandlerError(f"Path is not a file: '{filepath}'")
def read_text_file(filepath, encoding="utf-8"):
    """
    Read the entire content of a text file.
    :param filepath: Path to the text file.
    :param encoding: Text encoding to use when reading (default: utf-8).
    :return: The file content as a single string.
    :raises FileHandlerError: If the file cannot be read or the encoding is invalid.
    """
    validate_file_exists(filepath)
    try:
        with open(filepath, "r", encoding=encoding, errors="replace") as file:
            return file.read()
    except (OSError, LookupError) as error:
        # LookupError covers invalid/unknown encoding names.
        raise FileHandlerError(f"Could not read file '{filepath}': {error}")
def write_results_to_file(content, filepath, encoding="utf-8"):
    """
    Write text content to a file.
    :param content: The text to write.
    :param filepath: Destination path.
    :param encoding: Text encoding to use when writing (default: utf-8).
    :raises FileHandlerError: If the file cannot be written or the encoding is invalid.
    """
    try:
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filepath, "w", encoding=encoding) as file:
            file.write(content)
    except (OSError, LookupError, UnicodeError) as error:
        # LookupError: unknown encoding; UnicodeError: characters not encodable.
        raise FileHandlerError(f"Could not write to file '{filepath}': {error}")