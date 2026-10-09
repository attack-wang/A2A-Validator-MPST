'''
File input/output helpers.
This module centralizes all disk access for the application:
reading the source text file and writing the generated report,
using a consistent encoding and raising clear, standard exceptions
that the caller can translate into friendly error messages.
'''
def read_text_file(filepath, encoding="utf-8"):
    """
    Read and return the entire content of a text file.
    :param filepath: Path to the file to read.
    :param encoding: Text encoding to use (default: utf-8).
    :return: The file content as a single string.
    :raises FileNotFoundError: If the file does not exist.
    :raises UnicodeDecodeError: If the content cannot be decoded.
    :raises OSError: For other I/O problems (permissions, etc.).
    """
    with open(filepath, "r", encoding=encoding) as file_handle:
        return file_handle.read()
def write_text_file(filepath, content, encoding="utf-8"):
    """
    Write string content to a text file (overwriting if it exists).
    :param filepath: Path to the output file.
    :param content: The text to write.
    :param encoding: Text encoding to use (default: utf-8).
    :raises OSError: If the file cannot be written.
    """
    with open(filepath, "w", encoding=encoding) as file_handle:
        file_handle.write(content)