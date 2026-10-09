'''
test_file_reader.py
Unit tests for the FileReader class in file_reader.py.
Covers tokenization, missing-file errors, encoding fallback, and
round-trip reading of temporary files.
'''
import os
import tempfile
import unittest
from file_reader import FileReadError, FileReader
class FileReaderTests(unittest.TestCase):
    def test_tokenize_strips_punctuation(self):
        tokens = FileReader.tokenize('Hello, world! Madam, I am Adam.')
        self.assertEqual(tokens, ['Hello', 'world', 'Madam', 'I', 'am', 'Adam'])
    def test_tokenize_keeps_apostrophes_and_digits(self):
        tokens = FileReader.tokenize("I'm level 121, ok?")
        self.assertEqual(tokens, ["I'm", 'level', '121', 'ok'])
    def test_read_missing_file_raises(self):
        reader = FileReader()
        with self.assertRaises(FileReadError):
            reader.read_text('definitely_missing_file_xyz.txt')
    def test_read_directory_raises(self):
        reader = FileReader()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileReadError):
                reader.read_text(tmp)
    def test_read_text_roundtrip(self):
        reader = FileReader()
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'sample.txt')
            with open(path, 'w', encoding='utf-8') as handle:
                handle.write('level kayak noon')
            self.assertEqual(reader.read_text(path), 'level kayak noon')
    def test_encoding_fallback_latin1(self):
        reader = FileReader()
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'latin.txt')
            with open(path, 'w', encoding='latin-1') as handle:
                handle.write('caf\xe9 level')  # é is not valid UTF-8 as raw byte
            self.assertEqual(reader.read_text(path), 'café level')