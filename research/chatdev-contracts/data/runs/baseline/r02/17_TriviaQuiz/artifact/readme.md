# Trivia Quiz Program
An interactive command-line trivia quiz written in Python.
## Features
- Multiple-choice and short-answer questions on various topics
- Real-time score tracking after every question
- Configurable JSON question banks (load any bank file)
- Topic filtering, question-count limiting and shuffling
- Optional answer review (correct answers + explanations) after the quiz
## Requirements
- Python 3.6+ (standard library only, no external dependencies)
## Files
- `main.py` — entry point; loads the bank, configures and runs the quiz
- `question.py` — `Question` model (validation, answer checking, display)
- `question_bank.py` — `QuestionBank` (load/save/filter JSON banks)
- `quiz_game.py` — `QuizGame` (game loop, scoring, final report)
- `questions.json` — default sample question bank
## Usage
Run with the default bank:
    python main.py
Command-line options:
    python main.py [-f bank.json] [-t topic] [-n count] [--shuffle] [--shuffle-choices] [--show-answers]
- `-f, --file`          : path to a JSON question bank (default: `questions.json`)
- `-t, --topic`         : only ask questions of this topic
- `-n, --num`           : maximum number of questions to ask
- `--shuffle`           : shuffle question order
- `--shuffle-choices`   : shuffle multiple-choice option order at runtime
- `--show-answers`      : automatically show the answer review at the end
Options not supplied on the command line are requested interactively.
## Question bank format
Question banks are JSON files with a top-level `"questions"` list. Each
question supports the fields below (`answer` may be a string or a list of
acceptable strings, useful for short-answer questions):