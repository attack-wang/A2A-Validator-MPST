class ReportGenerator:
    """Builds human-readable reports from palindrome scan results."""
    _WIDTH = 72
    @classmethod
    def _header(cls, title):
        lines = [
            '=' * cls._WIDTH,
            title.center(cls._WIDTH),
            '=' * cls._WIDTH,
        ]
        return '\n'.join(lines)
    @classmethod
    def _stats_block(cls, stats):
        lines = [
            'Scan summary',
            cls._SEPARATOR,
            f"  Source file        : {stats['source']}",
            f"  Detection mode     : {stats['mode']}",
            f"  Lines scanned      : {stats['total_lines']}",
            f"  Characters scanned : {stats['total_characters']}",
            f"  Palindromes found  : {stats['total_matches']}",
            f"  Unique (normalized): {stats['unique_normalized']}",
            f"  Longest (chars)    : {stats['longest']}",
        ]
        return '\n'.join(lines)
    @classmethod
    def _match_block(cls, matches):
        if not matches:
            return ['No palindromes were found in the provided text.']
        lines = ['Detected palindromes', cls._SEPARATOR]
        for index, match in enumerate(matches, start=1):
            lines.append(f'  {index:>3}. {match}')
        return lines
    @classmethod
    def generate_console_report(cls, matches, stats):
        """Pretty report for terminal output."""
        parts = [
            cls._header('PALINDROME DETECTION REPORT'),
            cls._stats_block(stats),
            '',
            *cls._match_block(matches),
            cls._SEPARATOR,
            'End of report',
        ]
        return '\n'.join(parts)
    @classmethod
    def generate_text_report(cls, matches, stats):
        """Plain report suitable for saving to a .txt file."""
        return cls.generate_console_report(matches, stats)