'''Configuration constants for the trivia quiz program.'''
# Default path to the question bank JSON file.
DEFAULT_QUESTION_BANK = "sample_questions.json"
# Default maximum number of questions (0 means "use all questions").
DEFAULT_MAX_QUESTIONS = 0
# Shuffle questions by default before presenting them.
DEFAULT_SHUFFLE = True
# Show the answer review after the quiz by default.
DEFAULT_SHOW_ANSWERS = True
# Give instant correct/incorrect feedback after each answer.
INSTANT_FEEDBACK = True
# Strip leading articles ("the", "a", "an") when normalizing answers.
STRIP_ARTICLES = True
# Letter labels used for multiple-choice options.
CHOICE_LABELS = ["A", "B", "C", "D", "E", "F", "G", "H"]