class Feedback:
    @staticmethod
    def valid_merge(word, strands, count, total, is_spangram):
        if is_spangram:
            return f"🌐 {word} — SPANGRAM! ({count}/{total})"
        return f"✨ {word} — valid! ({count}/{total} words found)"