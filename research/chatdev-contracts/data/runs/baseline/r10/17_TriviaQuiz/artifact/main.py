bank = QuestionBank.load(bank_path)
filtered = bank.filter_by_topic(args.topic)
if args.topic and not filtered.questions:
    available = ", ".join(bank.topics()) or "none"
    raise QuestionBankError(f"No questions found for topic '{args.topic}'. Available topics: {available}")
questions = filtered.select(count=args.count, shuffle=args.shuffle)