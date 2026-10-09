'''
Configuration module for the Palindrome Detector application.
Centralizes default settings and shared regular-expression patterns
used across the whole application, so behaviour can be tuned in one
single place.
'''
# Minimum number of alphanumeric characters a token must have to be
# reported as a palindrome (single characters are trivial palindromes
# and are skipped by default to keep reports useful).
DEFAULT_MIN_LENGTH = 2
# Whether palindrome checking distinguishes uppercase from lowercase
# letters by default (False means comparisons are case-insensitive).
DEFAULT_CASE_SENSITIVE = False
# Whether whole lines containing several words should also be checked
# as palindromic phrases by default.
DEFAULT_INCLUDE_PHRASES = False
# Default path of the report file; an empty string means that the
# report is only printed to the console and not saved to disk.
DEFAULT_OUTPUT_FILE = ""
# Regular expression that matches a single word (letters and digits).
WORD_PATTERN = r"[A-Za-z0-9]+"
# Regular expression that matches every character that must be ignored
# when a candidate string is normalized before the palindrome check.
IGNORED_CHARS_PATTERN = r"[^A-Za-z0-9]"