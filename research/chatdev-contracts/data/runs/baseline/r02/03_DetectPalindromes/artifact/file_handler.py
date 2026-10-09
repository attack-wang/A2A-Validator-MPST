'''
file_handler.py
Input/output utility module for the Palindrome Detector application.
Contains the FileHandler class, which centralizes all file system
operations: validating paths, reading the input text file and
writing the optional report file.
'''
import os
class FileHandler:
    '''
    Handles file input/output operations for the application.
    '''
    @staticmethod
    def validate_file(filepath):
        '''
        Validate that the given path points to an existing, readable file.
        :param filepath: path to the file.
        :raises FileNotFoundError: if the file does not exist.
        :raises IOError: if the path is not a regular file.
        '''
        if not os.path.exists(filepath):
            raise FileNotFoundError("Input file not found: '{}'".format(filepath))
        if not os.path.isfile(filepath):
            raise IOError("Path is not a regular file: '{}'".format(filepath))
    @staticmethod
    def read_file(filepath, encoding='utf-8'):
        '''
        Read the entire content of a text file.
        Falls back to replacing undecodable characters if the file
        is not valid in the requested encoding.
        :param filepath: path to the text file.
        :param encoding: text encoding used while reading.
        :return: full text content of the file as a string.
        '''
        FileHandler.validate_file(filepath)
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding=encoding, errors='replace') as file:
                return file.read()
    @staticmethod
    def write_file(filepath, content, encoding='utf-8'):
        '''
        Write text content to a file, creating parent directories if needed.
        :param filepath: path to the output file.
        :param content: text content to write.
        :param encoding: text encoding used while writing.
        '''
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filepath, 'w', encoding=encoding) as file:
            file.write(content)