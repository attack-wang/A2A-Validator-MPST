'''
file_handler.py
File input/output utilities for the Palindrome Finder application.
'''
import os
class FileHandler:
    '''
    Handles reading text files and writing report files with robust error handling.
    '''
    # Encodings tried strictly, in order, before falling back to a permissive read.
    STRICT_ENCODINGS = ("utf-8-sig", "utf-8")
    # latin-1 maps every byte, so it can be used as a guaranteed last resort.
    FALLBACK_ENCODING = "latin-1"
    @classmethod
    def read_text_file(cls, filepath):
        '''
        Read the entire contents of a text file, trying multiple encodings.
        Raises FileNotFoundError / IsADirectoryError / PermissionError with
        friendly messages when the path itself is unusable.
        '''
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file '{filepath}' does not exist.")
        if os.path.isdir(filepath):
            raise IsADirectoryError(f"'{filepath}' is a directory, not a text file.")
        for encoding in cls.STRICT_ENCODINGS:
            try:
                with open(filepath, "r", encoding=encoding, errors="strict") as handle:
                    return handle.read()
            except UnicodeDecodeError:
                continue
        # Guaranteed last resort: latin-1 can decode any byte sequence.
        with open(filepath, "r", encoding=cls.FALLBACK_ENCODING, errors="replace") as handle:
            return handle.read()
    @staticmethod
    def write_text_file(filepath, content):
        '''
        Write text content to a file, creating parent directories if needed.
        Returns the absolute path of the written file.
        '''
        directory = os.path.dirname(os.path.abspath(filepath))
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as handle:
            handle.write(content)
        return os.path.abspath(filepath)