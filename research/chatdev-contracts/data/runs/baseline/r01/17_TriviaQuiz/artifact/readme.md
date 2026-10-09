<!--
DOCSTRING: ChatDev Trivia Quiz -- user and developer documentation.
Documents how to run the program, its command-line options, scoring rules,
and the configurable question-bank file formats (JSON and CSV).
-->
# ChatDev Trivia Quiz
An interactive command-line trivia quiz written in pure Python (standard
library only, no third-party dependencies). It presents multiple-choice and
short-answer questions, tracks the score while you play, reports the total
number of correct answers at the end, and can optionally review every correct
answer afterwards. Question content is fully configurable through JSON or CSV
question-bank files.
## Features
- Multiple-choice questions: answer with a choice letter (e.g. `B`) or the full choice text.
- Short-answer questions: case-insensitive, whitespace-tolerant matching, with optional alternative answers.
- Real-time score tracking with instant per-question feedback.
- Final summary showing total correct answers, points earned, and percentage.
- Optional answer review after the quiz (interactive prompt or `--show-answers`).
- Configurable question banks in JSON or CSV format.
- Topic filtering, question-count limits, and shuffling with an optional reproducible seed.
## Requirements
- Python 3.6 or newer. No external packages are required.
## Project Structure
    main.py                  Entry point; command-line interface.
    quiz.py                  QuizEngine: quiz loop, scoring, answer review.
    question_bank.py         QuestionBank: loads JSON/CSV question banks.
    questions.py             Question class hierarchy (MC and short answer).
    sample_questions.json    Sample question bank (JSON format).
    sample_questions.csv     Sample question bank (CSV format).
    readme.md                This documentation file.
## How to Run
Run with the default sample bank (sample_questions.json):
    python main.py
Run with a custom question bank:
    python main.py --bank my_questions.json
List the topics available in a bank:
    python main.py --bank my_questions.csv --list-topics
## Command-Line Options
| Option | Short | Description |
|--------|-------|-------------|
| `--bank PATH` | `-b` | Path to a question-bank file (`.json` or `.csv`). Default: `sample_questions.json`. |
| `--topic NAME` | `-t` | Only ask questions from this topic (case-insensitive). |
| `--num-questions N` | `-n` | Maximum number of questions to ask (must be a positive integer). |
| `--show-answers` | `-s` | Always display the correct answers after the quiz, without prompting. |
| `--no-shuffle` | | Keep the bank's original question order (default is shuffled). |
| `--list-topics` | | List the topics available in the bank, then exit. |
| `--seed N` | | Random seed for reproducible question shuffling. |
## Question Bank Formats
### JSON format
A JSON object with a top-level `questions` list (a plain top-level list is also
accepted). Each question object supports the following keys:
| Key | Required | Description |
|-----|----------|-------------|
| `type` | no | `multiple_choice` (aliases: `multiple-choice`, `mc`) or `short_answer` (aliases: `short-answer`, `sa`). Default: `short_answer`. |
| `question` | yes | The question text (alias: `text`). |
| `answer` | yes | The correct answer. For multiple choice this may be the full choice text or a choice letter (e.g. `"B"`). |
| `choices` | for MC | List of choice strings (multiple choice only). |
| `alternatives` | no | Extra accepted answers for short-answer questions (list or `;`-separated string). |
| `topic` | no | Topic label used for filtering. Default: `General`. |
| `points` | no | Positive integer score value. Default: `1`. |
Example:
    {
      "questions": [
        {
          "type": "multiple_choice",
          "question": "What is the capital of France?",
          "choices": ["London", "Paris", "Berlin", "Madrid"],
          "answer": "Paris",
          "topic": "Geography",
          "points": 1
        },
        {
          "type": "short_answer",
          "question": "What planet is known as the Red Planet?",
          "answer": "Mars",
          "alternatives": ["the red planet"],
          "topic": "Science",
          "points": 1
        }
      ]
    }
### CSV format
The first row must be a header containing at least the columns `type`,
`question`, and `answer`. Recognized columns: `type`, `question`, `choices`,
`answer`, `alternatives`, `topic`, `points`. Multiple `choices` and
`alternatives` values are separated by `;` (a `|` is also accepted).
Example:
    type,question,choices,answer,alternatives,topic,points
    multiple_choice,What is the capital of France?,"London;Paris;Berlin;Madrid",Paris,,Geography,1
    short_answer,What planet is known as the Red Planet?,,Mars,red planet,Science,1
## Scoring and Answer Review
- Each question is worth its `points` value (default 1). The quiz reports both
  the number of correct answers and the total points earned.
- After the final summary the program offers an interactive
  "Review the correct answers? (y/n)" prompt, unless `--show-answers` was
  given, in which case the review is shown automatically.
- The review lists every question with your answer, the correct answer, and a
  CORRECT/WRONG marker.
## Error Handling
- Missing or malformed bank files produce a friendly error message and exit
  code 1.
- An empty bank, an unknown topic, or a non-positive `--num-questions` value
  is rejected before the quiz starts.
- Pressing Ctrl+C (or Ctrl+D) at any point exits gracefully.