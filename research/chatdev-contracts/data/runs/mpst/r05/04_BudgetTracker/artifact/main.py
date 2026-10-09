if args.demo and not tracker.transactions:
    tracker.seed_demo_data()
    tracker.save()