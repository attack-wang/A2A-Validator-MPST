'''
file_handler.py
Utility module that encapsulates all file input/output operations for
the Palindrome Detector application: reading the input text file and
writing the generated report to disk.
'''
class FileHandler:
    '''
    Provides static helper methods for reading and writing text files.
    '''
    @staticmethod
    def read_file(filepath):
        '''
        Read and return the entire content of a UTF-8 text file.
        Args:
            filepath (str): Path to the text file to read.
        Returns:
            str: The full content of the file.
        Raises:
            FileNotFoundError: If the file does not exist.
            UnicodeDecodeError: If the file is not valid UTF-8 text.
            OSError: If the file cannot be opened or read.
        '''
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    @staticmethod
    def write_file(filepath, content):
        '''
        Write the given content to a UTF-8 text file.
        Args:
            filepath (str): Path of the file to write.
            content (str): The content to write to the file.
        Raises:
            OSError: If the file cannot be opened or written.
        '''
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)