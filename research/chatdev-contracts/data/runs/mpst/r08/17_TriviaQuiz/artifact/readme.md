'''
readme.md
Trivia Quiz Program documentation: usage, question bank format and project structure.
'''
# Trivia Quiz Program
A command-line trivia quiz that presents multiple-choice and short-answer
questions, tracks the score and shows the total correct answers at the end.
Correct answers can be reviewed after the quiz.
## Requirements
- Python 3.6+ (standard library only, no third-party packages)
## How to Run
    python main.py
Optional command-line arguments:
    -d, --bank-dir DIR    Directory containing JSON question banks (default: question_banks)
    -b, --bank NAME       Name of the question bank to use (skips the bank menu)
    -s, --shuffle         Shuffle the question order
    -a, --show-answers    Always show correct answers after the quiz
## Question Bank Format
Question banks are JSON files placed in the `question_banks/` directory:
    {
      "name": "General Knowledge",
      "description": "Optional description shown in the bank menu.",
      "questions": [
        {
          "type": "multiple_choice",
          "question": "What is the capital of France?",
          "options": ["London", "Paris", "Berlin", "Madrid"],
          "answer": "Paris",
          "topic": "Geography"
        },
        {
          "type": "short_answer",
          "question": "What planet is known as the Red Planet?",
          "answer": "Mars",
          "alternatives": ["the mars"],
          "topic": "Astronomy"
        }
      ]
    }
Field notes:
- `type`: `multiple_choice` or `short_answer`
- `answer` (multiple choice): option text (recommended), option letter ("B") or 1-based option number
- `alternatives` (short answer): extra accepted spellings (optional)
- Invalid bank files are skipped with a warning at startup.
## Project Structure
- `main.py` — entry point, argument parsing, menus
- `quiz.py` — quiz engine (question loop, scoring, results, review)
- `question_bank.py` — loading/validation/discovery of JSON banks
- `questions.py` — question model (multiple-choice and short-answer)
- `question_banks/` — JSON question banks