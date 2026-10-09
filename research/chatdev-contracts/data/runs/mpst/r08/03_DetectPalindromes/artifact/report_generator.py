'''
report_generator.py
Formats and presents palindrome detection results for the Palindrome Finder
application. Builds human-readable reports from PalindromeDetector results
and can print them to the console or save them to a file.
'''
import datetime
from file_handler import FileHandler
class ReportGenerator:
    '''
    Builds human-readable reports from PalindromeDetector results.
    '''
    LINE_WIDTH = 70
    def __init__(self, source, words, sentences=None, substrings=None, total_words=0, total_characters=0):
        '''
        Store the detection results and basic text statistics.
        :param words: list of dicts with keys "word", "normalized", "count", "positions"
        :param sentences: list of dicts with keys "index", "sentence"
        :param substrings: list of palindromic substring strings
        :param total_words: total number of words in the analyzed text
        :param total_characters: total number of characters in the analyzed text
        '''
        self.source = source
        self.words = words or []
        self.sentences = sentences or []
        self.substrings = substrings or []
        self.total_words = total_words
        self.total_characters = total_characters
    def _rule(self, char="="):
        '''Return a horizontal rule of the given character.'''
        return char * self.LINE_WIDTH
    def _center(self, text):
        '''Center text within the report width.'''
        return text.center(self.LINE_WIDTH)
    def _total_occurrences(self):
        '''Sum the occurrence counts of all palindromic words.'''
        return sum(word["count"] for word in self.words)
    def _longest_word_line(self):
        '''
        Describe the longest palindromic word found, or None when no words
        were detected.
        '''
        if not self.words:
            return None
        longest = max(self.words, key=lambda w: len(w["normalized"]))
        return (f"Longest palindromic word     : '{longest['word']}' "
                f"({len(longest['normalized'])} chars)")
    def build_report(self, include_timestamp=True):
        '''
        Assemble the full report as a single string.
        '''
        lines = []
        lines.append(self._rule())
        lines.append(self._center("PALINDROME FINDER REPORT"))
        lines.append(self._rule())
        if include_timestamp:
            lines.append(f"Generated : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Source    : {self.source}")
        lines.append(f"Characters: {self.total_characters}")
        lines.append(f"Words     : {self.total_words}")
        lines.append("")
        # Summary section
        lines.append(self._rule("-"))
        lines.append("SUMMARY")
        lines.append(self._rule("-"))
        lines.append(f"Unique palindromic words     : {len(self.words)}")
        lines.append(f"Total palindromic occurrences: {self._total_occurrences()}")
        longest_line = self._longest_word_line()
        if longest_line:
            lines.append(longest_line)
        if self.sentences:
            lines.append(f"Palindromic sentences        : {len(self.sentences)}")
        if self.substrings:
            lines.append(f"Palindromic substrings       : {len(self.substrings)}")
        lines.append("")
        # Words section
        lines.append(self._rule("-"))
        lines.append(f"PALINDROMIC WORDS ({len(self.words)} found)")
        lines.append(self._rule("-"))
        if not self.words:
            lines.append("No palindromic words were found.")
        else:
            header = f"{'#':>4}  {'Word':<24} {'Length':>6} {'Count':>6}  Positions"
            lines.append(header)
            lines.append("-" * self.LINE_WIDTH)
            for index, entry in enumerate(self.words, start=1):
                positions = ", ".join(str(p) for p in entry["positions"][:8])
                if len(entry["positions"]) > 8:
                    positions += ", ..."
                display_word = entry["word"] if len(entry["word"]) <= 24 else entry["word"][:21] + "..."
                lines.append(f"{index:>4}  {display_word:<24} {len(entry['normalized']):>6} {entry['count']:>6}  {positions}")
        lines.append("")
        # Sentences section
        if self.sentences:
            lines.append(self._rule("-"))
            lines.append(f"PALINDROMIC SENTENCES ({len(self.sentences)} found)")
            lines.append(self._rule("-"))
            for entry in self.sentences:
                lines.append(f"[Sentence {entry['index']}] {entry['sentence']}")
            lines.append("")
        # Substrings section
        if self.substrings:
            lines.append(self._rule("-"))
            lines.append(f"PALINDROMIC SUBSTRINGS ({len(self.substrings)} found)")
            lines.append(self._rule("-"))
            for index, substring in enumerate(self.substrings, start=1):
                lines.append(f"{index:>4}. {substring}")
            lines.append("")
        lines.append(self._rule())
        lines.append(self._center("END OF REPORT"))
        lines.append(self._rule())
        return "\n".join(lines)
    def print_report(self):
        '''Print the report to standard output.'''
        print(self.build_report(include_timestamp=False))
    def save_report(self, filepath):
        '''Save the report to a file and return its absolute path.'''
        return FileHandler.write_text_file(filepath, self.build_report(include_timestamp=True) + "\n")