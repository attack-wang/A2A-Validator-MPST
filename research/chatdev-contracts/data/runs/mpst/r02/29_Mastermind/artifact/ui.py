def calculate_feedback(secret, guess):
    exact = sum(1 for s, g in zip(secret, guess) if s == g)
    # Count remaining colors
    from collections import Counter
    secret_remaining = Counter(s for s, g in zip(secret, guess) if s != g)
    guess_remaining = Counter(g for s, g in zip(secret, guess) if s != g)
    partial = sum(min(secret_remaining[c], guess_remaining[c]) for c in secret_remaining)
    return exact, partial