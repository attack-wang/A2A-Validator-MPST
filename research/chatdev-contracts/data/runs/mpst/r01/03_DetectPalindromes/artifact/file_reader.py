'''
file_reader.py
File input handling for the Palindrome Detector application.
Provides the FileReader class, which safely reads the contents of a text
file (with encoding fallback) and tokenizes raw text into individual words.
A custom FileReadError exception is raised for any I/O problem so the
command-line interface can report a clean error message.
'''
import os
import re
class FileReadError(Exception):
    """Raised when a text file cannot be located or read."""
class FileReader:
    """Reads text files and turns their content into word tokens."""
    _FALLBACK_ENCODINGS = ('utf-8', 'utf-16', 'latin-1')
    def __init__(self, encoding='utf-8'):
        self.encoding = encoding
    def read_text(self, filepath):
        """
        Read and return the full text content of `filepath`.
        Tries the configured encoding first, then a small set of common
        fallback encodings. Raises FileReadError on any failure.
        """
        if not os.path.exists(filepath):
            raise FileReadError(f"File not found: '{filepath}'")
        if not os.path.isfile(filepath):
            raise FileReadError(f"Path is not a regular file: '{filepath}'")
        encodings = [self.encoding] + [e for e in self._FALLBACK_ENCODINGS if e != self.encoding]
        last_error = None
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as handle:
                    return handle.read()
            except (UnicodeDecodeError, UnicodeError) as error:
                last_error = error
                continue
            except OSError as error:
                raise FileReadError(f"Could not read '{filepath}': {error}")
        raise FileReadError(
            f"Could not decode '{filepath}' with any known encoding "
            f"({', '.join(encodings)}): {last_error}"
        )
    @staticmethod
    def tokenize(text):
        """
        Split raw text into word tokens.
        A token is a maximal run of letters, digits, or apostrophes, so
        punctuation attached to words ("madam,") is stripped automatically.
        """
        return re.findall(r"[A-Za-z0-9']+", text)