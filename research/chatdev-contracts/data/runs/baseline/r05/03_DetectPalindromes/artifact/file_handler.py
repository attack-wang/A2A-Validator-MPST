'''
file_handler.py
File input/output and text tokenization utilities for the Palindrome
Detector application. Handles reading the target text file, writing
reports to disk, and splitting text into words and sentences.
'''
import os
import re
class FileHandler:
    '''
    Handles file operations and basic text tokenization.
    '''
    @staticmethod
    def read_text_file(filepath):
        '''
        Read the entire content of a text file.
        Args:
            filepath (str): Path to the text file.
        Returns:
            str: The full content of the file.
        Raises:
            FileNotFoundError: If the file does not exist.
            OSError: If the file cannot be read.
        '''
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    @staticmethod
    def write_text_file(filepath, content):
        '''
        Write content to a text file, overwriting it if it exists.
        Args:
            filepath (str): Destination path.
            content (str): Content to write.
        Raises:
            OSError: If the file cannot be written.
        '''
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
    @staticmethod
    def extract_words(text):
        '''
        Extract whitespace-separated word tokens from text.
        Args:
            text (str): The text to tokenize.
        Returns:
            list: Word tokens in order of appearance.
        '''
        return text.split()
    @staticmethod
    def extract_sentences(text):
        '''
        Split text into sentences on sentence-ending punctuation.
        Args:
            text (str): The text to split.
        Returns:
            list: Cleaned sentence strings.
        '''
        parts = re.split(r"(?<=[.!?])\s+", text)
        return [part.strip() for part in parts if part and part.strip()]