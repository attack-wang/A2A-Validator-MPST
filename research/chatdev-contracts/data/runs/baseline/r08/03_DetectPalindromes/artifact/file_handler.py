'''
File handling module for the Palindrome Detector application.
Provides the FileHandler class, which is responsible for reading the
input text file and writing the detection report to an output file,
with robust error handling for common I/O problems.
'''
import os
class FileHandler:
    '''Handles reading input text files and writing result files.'''
    @staticmethod
    def read_file(file_path):
        '''Read the whole content of a text file and return it as a string.
        Raises FileNotFoundError / OSError with a friendly message when
        the file cannot be read.
        '''
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: '{file_path}'")
        if not os.path.isfile(file_path):
            raise ValueError(f"Path is not a regular file: '{file_path}'")
        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                return handle.read()
        except UnicodeDecodeError:
            # Fall back to a more permissive encoding
            with open(file_path, "r", encoding="latin-1") as handle:
                return handle.read()
        except OSError as error:
            raise OSError(f"Could not read file '{file_path}': {error}")
    @staticmethod
    def write_file(file_path, content):
        '''Write the given content to a text file, creating parent dirs.'''
        directory = os.path.dirname(os.path.abspath(file_path))
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        try:
            with open(file_path, "w", encoding="utf-8") as handle:
                handle.write(content)
        except OSError as error:
            raise OSError(f"Could not write file '{file_path}': {error}")