'''
report_generator.py
Module responsible for formatting palindrome detection results into
a human-readable report.
'''
class ReportGenerator:
    '''
    Formats detection results into a readable text report.
    '''
    @staticmethod
    def generate_report(results):
        '''
        Build a formatted report from detection results.
        Args:
            results (dict): Detection results with keys
                            'words', 'lines', 'phrases'.
        Returns:
            str: The formatted report.
        '''
        lines = []
        lines.append('=' * 60)
        lines.append('PALINDROME DETECTION REPORT')
        lines.append('=' * 60)
        words = results.get('words', {})
        lines.append('')
        lines.append('--- Palindromic Words ---')
        if words:
            for word, count in sorted(words.items()):
                lines.append(f'  "{word}" (found {count} time(s))')
            lines.append(f'  Total unique palindromic words: {len(words)}')
        else:
            lines.append('  No palindromic words found.')
        lines_found = results.get('lines', [])
        lines.append('')
        lines.append('--- Palindromic Lines ---')
        if lines_found:
            for line_number, line_content in lines_found:
                lines.append(f'  Line {line_number}: "{line_content}"')
            lines.append(f'  Total palindromic lines: {len(lines_found)}')
        else:
            lines.append('  No palindromic lines found.')
        phrases = results.get('phrases', [])
        lines.append('')
        lines.append('--- Palindromic Phrases ---')
        if phrases:
            for phrase in phrases:
                lines.append(f'  "{phrase}"')
            lines.append(f'  Total palindromic phrases: {len(phrases)}')
        else:
            lines.append('  No palindromic phrases found.')
        lines.append('')
        lines.append('=' * 60)
        lines.append('END OF REPORT')
        lines.append('=' * 60)
        return '\n'.join(lines)