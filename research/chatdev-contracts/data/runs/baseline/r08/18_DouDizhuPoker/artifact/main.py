def _analyze(self):
    counts = Counter(c.rank for c in self.cards)
    n = len(self.cards)
    values = sorted(set(RANK_VALUE[r] for r in counts))
    # Rocket
    if n == 2 and counts.get('SJ', 0) == 1 and counts.get('BJ', 0) == 1:
        return ComboType.ROCKET, RANK_VALUE['BJ'], 0
    # Bomb
    if n == 4 and len(counts) == 1:
        return ComboType.BOMB, values[0], 0
    # Single
    if n == 1:
        return ComboType.SINGLE, values[0], 0
    # Pair
    if n == 2 and len(counts) == 1:
        return ComboType.PAIR, values[0], 0
    # Triple
    if n == 3 and len(counts) == 1:
        return ComboType.TRIPLE, values[0], 0
    # Triple with single
    if n == 4 and len(counts) == 2 and 3 in counts.values():
        return ComboType.TRIPLE_SINGLE, RANK_VALUE[self._rank_with_count(counts, 3)], 0
    # Triple with pair
    if n == 5 and len(counts) == 2 and 3 in counts.values() and 2 in counts.values():
        return ComboType.TRIPLE_PAIR, RANK_VALUE[self._rank_with_count(counts, 3)], 0
    # Straight: >= 5 consecutive singles
    if n >= 5 and len(counts) == n and self._is_consecutive(values) and values[-1] <= RANK_VALUE['A']:
        return ComboType.STRAIGHT, values[-1], n
    # Pair straight: >= 3 consecutive pairs
    if n >= 6 and n % 2 == 0 and all(c == 2 for c in counts.values()):
        length = n // 2
        if length >= 3 and self._is_consecutive(values) and values[-1] <= RANK_VALUE['A']:
            return ComboType.PAIR_STRAIGHT, values[-1], length
    # Airplane pure: >= 2 consecutive triples
    if n >= 6 and n % 3 == 0 and all(c == 3 for c in counts.values()):
        length = n // 3
        if length >= 2 and self._is_consecutive(values) and values[-1] <= RANK_VALUE['A']:
            return ComboType.AIRPLANE, values[-1], length
    # Four with two singles: 4 + 1 + 1 (6 cards) - the two singles must be different? Actually standard rules: 4+2 singles can be like 4444 3 5 or 4444 33? Hmm. In standard Dou Dizhu, 四带二单: four cards + two single cards. The two singles can be a pair (e.g., 4444+55)? Actually there's ambiguity. Common rule: 四带两单 - the two kickers can be any two cards (including a pair). But some rules say 四带两对 requires pairs. Let me handle: n == 6, one rank with count 4, remaining two cards are singles (could be same rank = pair, which would be interpreted as four-with-two-singles where the two singles happen to be the same rank). Hmm, but 444455 could also be... no other interpretation. Actually wait, 444455: counts {4:4, 5:2}. Is this four-with-two-singles (4444 + 5 + 5)? Some rules allow it, some don't. The review comment says "44445555 is four-with-two-pairs". So 4444 5555: counts {4:4, 5:4}. Interpretations: four-with-two-pairs (4444 + 55 + 55)? Or bomb 4444 + bomb 5555? Standard: 四带两对 = 4444 + two pairs. So 44445555 = four-with-two-pairs. OK.
    # Four with two singles (n=6): one rank count 4, other two cards any (two singles or one pair)
    # Four with two pairs (n=8): one rank count 4, remaining 4 cards form two pairs
    # Airplane with singles: m triples consecutive + m singles (4m total)
    # Airplane with pairs: m triples consecutive + m pairs (5m total)