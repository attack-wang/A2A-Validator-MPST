'''
file_handler.py
File input/output utilities for the palindrome detector.
Provides the FileHandler class, which reads plain-text files with a
graceful encoding fallback chain and writes report files, plus a small
exception hierarchy (FileHandlerError, FileReadError, FileWriteError)
used to signal problems to callers.
'''
import os
class FileHandlerError(Exception):
    """Base exception for file handling problems."""
class FileReadError(FileHandlerError):
    """Raised when a text file cannot be read."""
class FileWriteError(FileHandlerError):
    """Raised when a report file cannot be written."""
class FileHandler:
    """Reads and writes plain-text files with graceful encoding fallback."""
    FALLBACK_ENCODINGS = ("utf-8-sig", "utf-8", "latin-1")
    def read_text(self, filepath, encoding=None):
        """Read an entire text file, trying the requested encoding or a fallback chain."""
        if not os.path.exists(filepath):
            raise FileReadError("File not found: {}".format(filepath))
        if os.path.isdir(filepath):
            raise FileReadError("Expected a file but found a directory: {}".format(filepath))
        encodings = (encoding,) if encoding else self.FALLBACK_ENCODINGS
        last_error = None
        for candidate in encodings:
            try:
                with open(filepath, "r", encoding=candidate, errors="strict") as handle:
                    return handle.read()
            except UnicodeDecodeError as exc:
                last_error = exc
                continue
            except OSError as exc:
                raise FileReadError("Could not read '{}': {}".format(filepath, exc))
        raise FileReadError(
            "Could not decode '{}' with any of the encodings: {}".format(
                filepath, ", ".join(encodings))
        )
    def write_text(self, filepath, content, encoding="utf-8"):
        """Write content to a file, creating parent directories when needed."""
        try:
            directory = os.path.dirname(os.path.abspath(filepath))
            if directory and not os.path.isdir(directory):
                os.makedirs(directory, exist_ok=True)
            with open(filepath, "w", encoding=encoding) as handle:
                handle.write(content)
        except OSError as exc:
            raise FileWriteError("Could not write '{}': {}".format(filepath, exc))
        return filepath