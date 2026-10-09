'''
file_handler.py
File input/output utilities for the palindrome detection application.
The FileHandler class reads the source text file and writes result
reports to disk, with basic error handling and directory creation.
'''
import os
class FileHandler:
    '''
    Utility class for reading text files and writing text output files.
    '''
    @staticmethod
    def read_text(filepath):
        '''
        Read the entire content of a text file.
        Args:
            filepath (str): Path to the input text file.
        Returns:
            str: The full text content of the file.
        Raises:
            FileNotFoundError: If the file does not exist.
            OSError: If the file cannot be opened or read.
        '''
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Input file not found: '{filepath}'")
        with open(filepath, 'r', encoding='utf-8') as handle:
            return handle.read()
    @staticmethod
    def write_text(filepath, content):
        '''
        Write text content to a file, creating parent directories if needed.
        Args:
            filepath (str): Path to the output file.
            content (str): The text content to write.
        Returns:
            str: The filepath that was written, for confirmation.
        '''
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as handle:
            handle.write(content)
        return filepath