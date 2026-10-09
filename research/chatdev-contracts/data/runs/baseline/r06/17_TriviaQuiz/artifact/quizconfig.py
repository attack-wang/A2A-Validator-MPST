@dataclass
class QuizConfig:
    show_answers_after: bool = True
    shuffle_questions: bool = True
    num_questions: Optional[int] = None
    topics: Optional[List[str]] = None
    allow_skips: bool = True  # pressing Enter skips? Hmm.