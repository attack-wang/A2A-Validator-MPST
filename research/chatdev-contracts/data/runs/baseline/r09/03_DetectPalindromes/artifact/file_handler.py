'''
file_handler.py
File input/output utilities for the palindrome detector application.
All disk access is centralized here so the rest of the application never
touches the file system directly. Provides safe reading of the user's text
file and writing of the optional results report.
'''
class FileHandler:
    """Reads the input text file and writes result reports to disk."""
    @staticmethod
    def read_text_file(filepath, encoding='utf-8'):
        """
        Read and return the entire content of a text file.
        :param filepath: Path to the text file to read.
        :param encoding: Text encoding used when reading the file.
        :return: The file content as a single string.
        :raises FileNotFoundError: If the file does not exist.
        :raises UnicodeDecodeError: If the file cannot be decoded with the
                                    given encoding.
        :raises OSError: If the file cannot be read for any other reason.
        """
        with open(filepath, 'r', encoding=encoding) as handle:
            return handle.read()
    @staticmethod
    def write_text_file(filepath, content, encoding='utf-8'):
        """
        Write text content to a file, overwriting it if it already exists.
        :param filepath: Path of the file to write.
        :param content: The text content to write.
        :param encoding: Text encoding used when writing the file.
        :return: None
        :raises OSError: If the file cannot be written.
        """
        with open(filepath, 'w', encoding=encoding) as handle:
            handle.write(content)