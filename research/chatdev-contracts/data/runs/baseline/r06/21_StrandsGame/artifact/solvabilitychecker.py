def _can_form(target, strand_texts):
    """True if some ordered concatenation of distinct strands equals target."""
    n = len(strand_texts)
    def search(remaining, used):
        if not remaining:
            return True
        for i in range(n):
            if used & (1 << i):
                continue
            if remaining.startswith(strand_texts[i]):
                if search(remaining[len(strand_texts[i]):], used | (1 << i)):
                    return True
        return False
    return search(target, 0)