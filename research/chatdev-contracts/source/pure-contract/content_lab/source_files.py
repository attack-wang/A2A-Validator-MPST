"""Extract explicitly declared final files, never guess from surrounding prose."""
from __future__ import annotations

import re


class SourceExtractionError(ValueError):
    def __init__(self, rule, message):
        self.rule = rule
        super().__init__(message)


def declared_filename(line):
    title = re.sub(r'^\s*#{1,6}\s+', '', line).strip().rstrip(':').strip()
    title = re.sub(r'^(?:file|filename)\s*:\s*', '', title, flags=re.I).strip()
    title = title.strip('`* ').strip()
    # A declaration is a standalone filename, not a sentence containing one.
    if not title.lower().endswith('.py') or re.search(r'\s', title):
        return None
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.-]*\.py', title) or '/' in title or '\\' in title:
        raise SourceExtractionError('source_filename', 'Declared source must be a flat Python filename: ' + title)
    return title


def parse_source_files(text):
    lines = text.splitlines()
    files = {}
    position = 0
    while position < len(lines):
        opening = re.fullmatch(r'\s*(`{3,})([^`]*)', lines[position])
        if not opening:
            position += 1
            continue
        previous = position - 1
        while previous >= 0 and not lines[previous].strip():
            previous -= 1
        name = declared_filename(lines[previous]) if previous >= 0 else None
        language = opening.group(2).strip().lower()
        fence_size = len(opening.group(1))
        end = position + 1
        while end < len(lines):
            closing = re.fullmatch(r'\s*(`{3,})\s*', lines[end])
            if closing and len(closing.group(1)) >= fence_size:
                break
            end += 1
        if end == len(lines):
            if name or not files:
                raise SourceExtractionError('output_truncated', 'Response ends inside a fenced block; no partial files can be delivered.')
            break
        if name:
            if language not in {'python', 'py', ''}:
                raise SourceExtractionError('source_block_language', 'A declared Python file needs a Python code fence.')
            if name in files:
                raise SourceExtractionError('duplicate_source_file', 'Return each final file once: ' + name)
            body = '\n'.join(lines[position + 1:end])
            if not body.strip():
                raise SourceExtractionError('empty_source_file', 'Declared file is empty: ' + name)
            files[name] = body
        position = end + 1
    return files
