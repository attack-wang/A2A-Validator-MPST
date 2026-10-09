'''
file_reader.py
This module handles reading and validating text files.
It provides the FileReader class used by the main application
to safely load text content from disk.
'''
import os
class FileReader:
    '''
    A class that reads and validates text files.
    '''
    DEFAULT_ENCODING = 'utf-8'
    def __init__(self, encoding=DEFAULT_ENCODING):
        '''
        Initialize the reader with a specific file encoding.
        :param encoding: text encoding to use when reading files
        '''
        self.encoding = encoding
    def validate_file(self, filepath):
        '''
        Validate that the given path points to an existing, readable file.
        :param filepath: path to the file
        :raises FileNotFoundError: if the file does not exist
        :raises PermissionError: if the file is not readable
        :raises ValueError: if the path is a directory
        '''
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: '{filepath}'")
        if os.path.isdir(filepath):
            raise ValueError(f"Path is a directory, not a file: '{filepath}'")
        if not os.access(filepath, os.R_OK):
            raise PermissionError(f"File is not readable: '{filepath}'")
    def read_file(self, filepath):
        '''
        Read the entire content of a text file.
        :param filepath: path to the file
        :return: the file content as a string
        '''
        self.validate_file(filepath)
        with open(filepath, 'r', encoding=self.encoding, errors='replace') as f:
            return f.read()
    def read_lines(self, filepath):
        '''
        Read a text file and return its non-empty lines.
        :param filepath: path to the file
        :return: list of non-empty stripped lines
        '''
        content = self.read_file(filepath)
        return [line.strip() for line in content.splitlines() if line.strip()]