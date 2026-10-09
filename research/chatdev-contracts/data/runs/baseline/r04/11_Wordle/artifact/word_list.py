import datetime
epoch = datetime.date(2021, 6, 19)  # original Wordle launch date
index = (date - epoch).days % len(ANSWER_WORDS)