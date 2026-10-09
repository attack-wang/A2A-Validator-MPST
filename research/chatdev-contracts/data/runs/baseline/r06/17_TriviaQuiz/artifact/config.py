'''
config.py
Holds the runtime configuration of a quiz session. Values can come from
command-line arguments or interactive prompts. This is the single source
of truth for quiz settings (the former duplicate quizconfig.py was merged
into this module).
'''
from dataclasses import dataclass, field
from typing import List, Optional
@dataclass
class QuizConfig:
    """Settings that control how a QuizSession behaves."""
    show_answers_after: bool = True      # requirement: option to show correct answers after quiz
    shuffle_questions: bool = True
    shuffle_choices: bool = False
    num_questions: Optional[int] = None  # None means "use every matching question"
    topics: Optional[List[str]] = None   # None/empty means "all topics"
    immediate_feedback: bool = False     # reveal correctness right after each answer
    def __post_init__(self):
        if self.topics is None:
            self.topics = []