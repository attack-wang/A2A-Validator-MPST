def detect_phrases(self, text, max_phrase_length=6):
    sentences = re.split(r"[.!?;\n]+", text)
    results = []
    for index, sentence in enumerate(sentences, start=1):
        words = re.findall(r"[A-Za-z0-9']+", sentence)
        if len(words) < 2:
            continue
        seen = set()
        for size in range(min(max_phrase_length, len(words)), 1, -1):
            for start in range(0, len(words) - size + 1):
                window = words[start:start + size]
                normalized = self._normalize(" ".join(window))
                if len(normalized) < max(self.min_length, 3):
                    continue
                if normalized == normalized[::-1]:
                    phrase = " ".join(window)
                    key = normalized
                    if key not in seen:
                        seen.add(key)
                        results.append({...})
    results.sort(key=lambda item: (-item['length'], item['sentence']))
    return results