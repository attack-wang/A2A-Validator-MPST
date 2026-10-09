import datetime
from file_handler import FileHandler
class ReportGenerator:
    LINE_WIDTH = 70
    def __init__(self, source, words, sentences=None, substrings=None, total_words=0, total_characters=0):
        self.source = source
        self.words = words or []
        self.sentences = sentences or []
        self.substrings = substrings or []
        self.total_words = total_words
        self.total_characters = total_characters
    def _rule(self, char="="):
        return char * self.LINE_WIDTH
    def _center(self, text):
        return text.center(self.LINE_WIDTH)
    def _total_occurrences(self):
        return sum(word["count"] for word in self.words)
    def build_report(self, include_timestamp=True):
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
            header = f"{'#':>4}  {'Word':<20} {'Length':>6} {'Count':>6}  Positions"
            lines.append(header)
            lines.append("-" * self.LINE_WIDTH)
            for index, entry in enumerate(self.words, start=1):
                positions = ", ".join(str(p) for p in entry["positions"][:8])
                if len(entry["positions"]) > 8:
                    positions += ", ..."
                lines.append(f"{index:>4}  {entry['word'][:20]:<20} {len(entry['normalized']):>6} {entry['count']:>6}  {positions}")
        lines.append("")
        # Sentences
        if self.sentences:
            lines.append(self._rule("-"))
            lines.append(f"PALINDROMIC SENTENCES ({len(self.sentences)} found)")
            lines.append(self._rule("-"))
            for entry in self.sentences:
                lines.append(f"[Sentence {entry['index']}] {entry['sentence']}")
            lines.append("")
        # Substrings
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
        print(self.build_report(include_timestamp=False))
    def save_report(self, filepath):
        return FileHandler.write_text_file(filepath, self.build_report(include_timestamp=True) + "\n")