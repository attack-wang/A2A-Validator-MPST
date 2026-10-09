'''
file_reader.py
Input handling module for the Palindrome Detector application.
Provides the FileReader class, which safely loads plain-text content
from disk, trying several common encodings and raising clear, explicit
errors when a file cannot be read.
'''
import os
from typing import Iterable, List
class FileReader:
    """Reads the full text content of a file with robust error handling."""
    DEFAULT_ENCODINGS = ("utf-8", "utf-8-sig", "latin-1")
    def __init__(self, encodings: Iterable[str] = None) -> None:
        self.encodings: List[str] = list(encodings) if encodings else list(self.DEFAULT_ENCODINGS)
    def read(self, file_path: str) -> str:
        """
        Read and return the entire content of `file_path`.
        Raises:
            FileNotFoundError: if the path does not exist.
            IsADirectoryError: if the path points at a directory.
            ValueError: if the file cannot be decoded with any known encoding.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found: {0}".format(file_path))
        if os.path.isdir(file_path):
            raise IsADirectoryError("Expected a file but found a directory: {0}".format(file_path))
        last_error = None
        for encoding in self.encodings:
            try:
                with open(file_path, "r", encoding=encoding, errors="strict") as handle:
                    return handle.read()
            except UnicodeDecodeError as error:
                last_error = error
                continue
        raise ValueError(
            "Unable to decode '{0}' using encodings: {1}".format(file_path, ", ".join(self.encodings))
        )
    def read_lines(self, file_path: str) -> List[str]:
        """Read the file and return its content as a list of lines."""
        return self.read(file_path).splitlines()