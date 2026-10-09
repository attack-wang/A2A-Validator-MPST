    if args.save_bank:
        saved = bank.save_to_json(args.save_bank)
        print("Saved {} questions to {}".format(saved, args.save_bank))
        # Conversion-only run: exit without starting the quiz.
        return 0