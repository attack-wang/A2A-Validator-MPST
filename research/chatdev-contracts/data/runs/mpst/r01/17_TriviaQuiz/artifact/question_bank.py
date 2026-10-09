'''
question_bank.py
Loading, validation, and management of trivia question collections.
Classes:
    QuestionBank      - In-memory collection of questions with filtering.
    QuestionBankError - Raised when a question bank file or entry is invalid.
Functions:
    build_default_bank() - Returns a QuestionBank with built-in sample questions.
The expected JSON schema for a bank file is:
    {
      "questions": [
        {
          "type": "multiple_choice",
          "topic": "Geography",
          "question": "What is the capital of France?",
          "choices": ["London", "Paris", "Berlin", "Madrid"],
          "answer": "Paris",
          "explanation": "Paris has been France's capital since..."
        },
        {
          "type": "short_answer",
          "topic": "Science",
          "question": "Which planet is known as the Red Planet?",
          "answer": "Mars",
          "accepted_answers": ["Mars", "the red planet"],
          "explanation": "Iron oxide dust gives Mars its red colour."
        }
      ]
    }
'''