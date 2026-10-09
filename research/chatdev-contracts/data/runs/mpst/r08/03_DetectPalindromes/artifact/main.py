def main(argv=None):
    args = parse_arguments(argv)
    if args.textfile is None:
        return run_interactive(args)
    return 0 if analyze_file(args.textfile, options=args) else 1