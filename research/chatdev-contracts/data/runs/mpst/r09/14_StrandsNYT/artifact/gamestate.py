class GameState:
    puzzle
    found_words: set of ThemeWord (or ids)
    found_non_theme: set of str
    hint_credit_progress: int (0..2)
    hint_credits: int
    hinted_words: set (words revealed via hint)