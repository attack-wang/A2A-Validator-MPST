### combination.py
The Combination class with classify. Need to handle:
- SINGLE: 1 card
- PAIR: 2 same rank
- TRIPLE: 3 same rank
- TRIPLE_SINGLE: 3+1
- TRIPLE_PAIR: 3+2
- STRAIGHT: ≥5 consecutive, 3-A only
- PAIR_STRAIGHT: ≥3 consecutive pairs, 3-A only
- AIRPLANE: ≥2 consecutive triples
- AIRPLANE_SINGLE: airplane + equal number of singles (wings can't be jokers... actually standard rules: wings cannot include jokers, and for airplane with wings, wings shouldn't form triples that extend the airplane... keep it simpler but reasonable)
- AIRPLANE_PAIR: airplane + equal number of pairs
- FOUR_TWO_SINGLES: 4 + 2 singles (attachments can't be jokers in standard rules; also can't be a pair? Actually 4+2 singles where the two singles can be the same rank? Standard: 四带二 - two singles, they can be a pair or two different; jokers usually not allowed as attachments in strict rules. I'll disallow jokers as attachments.)
- FOUR_TWO_PAIRS: 4 + 2 pairs
- BOMB: 4 same rank
- ROCKET: both jokers
For airplane with wings, there's a subtlety: e.g., 333444 + 5 6 is airplane with singles. But 333444555 + 6 7 8 could be interpreted as airplane of 3 with singles 678, or... Also 333444 + 4 4 — the wings shouldn't be part of the triples. Let me implement a reasonable classifier:
For AIRPLANE_SINGLE: find consecutive triple ranks (length ≥ 2), the remaining cards count must equal triple count, and remaining cards must be singles (no pairs among them? Actually wings can be any singles including forming... standard rule: the wings must be single cards, they can be same rank? No — if two wings are the same rank it's effectively a pair, which some rules allow as "two singles". Hmm. Common implementations allow wings as any cards that aren't jokers, as long as count matches. But to be safe: wings must not contain jokers, and wings must not contain cards that would extend the airplane (i.e., a wing card of rank adjacent to the triple run that has 3 copies... that's complex). Let me implement:
For airplane detection: count ranks with ≥3 copies among ranks 3-14 (2 and jokers can't be in the triple run? Actually 2 can't be part of airplane run since straights/sequences exclude 2; triples themselves can be of rank 2 though — e.g., 222333 is not a valid airplane because 2 can't be in sequence. Standard: airplane requires consecutive triples from 3 to A only (2 cannot be in a sequence). So triple run ranks must be within 3..14.
For AIRPLANE_SINGLE with n triples, wings = 2n singles. The wings must not be jokers (each wing card must not be a joker). Also, wings must not be cards whose rank is part of the triple run (that would be ambiguous — e.g., 33344455 + 5? no that's 3 triples + ... hmm). A common approach: try all possible triple runs and check the remainder forms valid wings.
Let me write classify to try candidate interpretations: