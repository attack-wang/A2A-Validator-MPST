# Trivia Quiz
A configurable command-line trivia quiz written in Python (standard library only, no external packages).
## Features
- Multiple-choice and short-answer questions on various topics
- Interactive answer entry with immediate per-question feedback
- Automatic score tracking
- Final summary showing total correct answers, incorrect count, and percentage
- Configurable JSON question banks (add/edit questions without touching the code)
- Optional answer review after the quiz (automatic via flag, or on request)
## Requirements
- Python 3.6 or newer
## Files
- `main.py` — entry point; parses options, loads the bank, runs the quiz
- `config.py` — command-line configuration (`QuizConfig`, `parse_arguments`)
- `questionbank.py` — loads and validates a JSON question bank
- `question.py` — question data models (multiple-choice and short-answer)
- `quiz.py` — core quiz engine (`QuizGame`): game loop, scoring, results, review
- `question_bank.json` — sample question bank (10 questions)
## Usage
    python main.py [-b BANK] [-s] [-a]
Options:
- `-b, --bank PATH` — path to the JSON question bank file (default: `question_bank.json`)
- `-s, --shuffle` — shuffle the question order before starting
- `-a, --show-answers` — automatically display the correct answers after the quiz
Examples:
    python main.py
    python main.py -b my_questions.json -s -a
## Question Bank Format
Question banks are JSON files with a title and a list of questions:
    {
      "title": "General Knowledge Trivia",
      "questions": [
        {
          "type": "multiple_choice",
          "topic": "Geography",
          "question": "What is the capital of Australia?",
          "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
          "answer": "C"
        },
        {
          "type": "short_answer",
          "topic": "Science",
          "question": "What planet is known as the Red Planet?",
          "answer": ["mars"]
        }
      ]
    }
Notes:
- `type` is `multiple_choice` (or `mc`) or `short_answer` (or `short`/`text`).
- For multiple choice, `answer` may be the letter (`"C"`), the 1-based option
  number (`3` or `"3"`), or the exact option text (`"Canberra"`).
- For short answer, `answer` may be a single string or a list of accepted
  variants; matching is case-insensitive and ignores extra whitespace.
## Creating Your Own Question Bank
1. Copy `question_bank.json` to a new file, e.g. `my_questions.json`.
2. Edit the title and add, remove, or modify questions following the format above.
3. Run the quiz with your bank:
    python main.py -b my_questions.json