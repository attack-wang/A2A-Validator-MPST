'''
file_handler.py
File input/output helpers for the Palindrome Detector application.
Classes:
    FileHandler -- reads text files, formats analysis reports and
                   writes reports back to disk.
'''
class FileHandler:
    """Handles reading text files and writing formatted reports."""
    @staticmethod
    def read_file(path):
        """
        Read and return the full content of the text file at *path*.
        Raises:
            FileNotFoundError: If *path* does not point to an existing file.
            UnicodeDecodeError: If the file is not valid UTF-8 text.
            OSError: If the file cannot be opened or read.
        """
        with open(path, 'r', encoding='utf-8') as handle:
            return handle.read()
    @staticmethod
    def format_report(filename, result):
        """
        Build a human-readable report from an analysis result dictionary.
        Args:
            filename (str): Name of the analysed file (shown in the header).
            result (dict): Output of PalindromeDetector.analyze().
        Returns:
            str: The formatted, multi-line report.
        """
        line = '=' * 62
        lines = [
            line,
            f"Palindrome Detection Report - {filename}",
            line,
            f"Total words analysed : {result['total_words']}",
            f"Palindromic words    : {result['word_count']}",
            f"Palindromic phrases  : {result['phrase_count']}",
            "",
            "--- Palindromic Words ---",
        ]
        if result['palindromic_words']:
            for word in result['palindromic_words']:
                lines.append(f"  * {word}")
        else:
            lines.append("  (none found)")
        lines += ["", "--- Palindromic Phrases / Sentences ---"]
        if result['palindromic_phrases']:
            for phrase in result['palindromic_phrases']:
                lines.append(f"  * {phrase}")
        else:
            lines.append("  (none found)")
        lines.append(line)
        return '\n'.join(lines)
    @staticmethod
    def write_report(path, report):
        """
        Write *report* to the file at *path*.
        Raises:
            OSError: If the file cannot be created or written.
        """
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(report + '\n')