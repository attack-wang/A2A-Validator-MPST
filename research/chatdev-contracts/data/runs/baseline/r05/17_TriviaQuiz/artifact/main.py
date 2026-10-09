def choose_count(chosen, available):
    '''Resolve the question count: use the CLI value, or prompt the user.'''
    if chosen is not None:
        return max(0, chosen)
    value = ask_int(
        "How many questions? (Enter = all {}): ".format(available),
        default=0, low=0)
    return min(value, available) if value else 0