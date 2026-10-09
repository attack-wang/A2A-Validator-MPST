RANK_ORDER = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
RANK_VALUE = {r: i+3 for i, r in enumerate(RANK_ORDER)}  # 3..15
SMALL_JOKER_VALUE = 16
BIG_JOKER_VALUE = 17