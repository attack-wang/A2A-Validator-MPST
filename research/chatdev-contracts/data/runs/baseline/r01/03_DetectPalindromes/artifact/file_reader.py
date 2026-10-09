'''
File reading utilities for the Palindrome Detector application.
Provides robust text file reading with error handling.
'''
import os
class FileReadError(Exception):
    '''Custom exception raised when a text file cannot be read.'''
    pass
def read_text_file(filepath):
    '''Read the entire content of a text file.
    Args:
        filepath: path to the text file
    Returns:
        The file content as a string
    Raises:
        FileReadError: if the file does not exist, is a directory, or cannot be read
    '''
    # Validate the path argument itself
    if filepath is None or not isinstance(filepath, str) or not filepath.strip():
        raise FileReadError("Invalid file path: path must be a non-empty string")
    # Check existence and type
    if not os.path.exists(filepath):
        raise FileReadError(f"File not found: '{filepath}'")
    if os.path.isdir(filepath):
        raise FileReadError(f"'{filepath}' is a directory, not a file")
    # Attempt to read with UTF-8 first, falling back to latin-1
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Retry with latin-1 fallback for files with non-UTF-8 encodings
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            raise FileReadError(f"Unable to decode file '{filepath}': {e}")
    except PermissionError:
        raise FileReadError(f"Permission denied when reading '{filepath}'")
    except OSError as e:
        raise FileReadError(f"Error reading file '{filepath}': {e}")
def read_text_file_lines(filepath):
    '''Read a text file and return its content as a list of lines.
    Each returned line has trailing newline characters removed, which is
    convenient for line-numbered analysis (e.g., palindrome detection).
    Args:
        filepath: path to the text file
    Returns:
        A list of strings, one per line of the file
    Raises:
        FileReadError: if the file cannot be read
    '''
    content = read_text_file(filepath)
    return content.splitlines()