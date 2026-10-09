'''
file_handler.py - File input/output utilities for the Palindrome Detector.
Provides a small helper class that safely reads the input text file
(trying several common encodings) and writes report files.
'''
import os
class FileHandler:
    """Reads and writes plain-text files with friendly error handling."""
    DEFAULT_ENCODING = "utf-8"
    FALLBACK_ENCODINGS = ("utf-8-sig", "latin-1")
    @classmethod
    def read_text_file(cls, filepath):
        """
        Read and return the full content of a text file.
        Tries the default encoding first, then a list of fallback
        encodings, so files saved with or without a BOM and simple
        Western-encoded files can both be processed.
        Raises:
            FileNotFoundError: if the file does not exist.
            IsADirectoryError: if the path points to a directory.
            ValueError: if the file cannot be decoded with any supported
                encoding.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: '{filepath}'")
        if os.path.isdir(filepath):
            raise IsADirectoryError(
                f"Expected a file but found a directory: '{filepath}'"
            )
        encodings = (cls.DEFAULT_ENCODING,) + cls.FALLBACK_ENCODINGS
        last_error = None
        for encoding in encodings:
            try:
                with open(filepath, "r", encoding=encoding) as handle:
                    return handle.read()
            except UnicodeDecodeError as error:
                last_error = error
        raise ValueError(
            f"Could not decode '{filepath}' using any of the supported "
            f"encodings: {', '.join(encodings)}."
        ) from last_error
    @classmethod
    def write_text_file(cls, filepath, content):
        """
        Write the given content to a text file (UTF-8).
        Creates parent directories when they do not exist yet.
        """
        directory = os.path.dirname(os.path.abspath(filepath))
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filepath, "w", encoding=cls.DEFAULT_ENCODING) as handle:
            handle.write(content)