try:
    from game import Game
    PYGAME_AVAILABLE = True
except ModuleNotFoundError as exc:
    if exc.name != "pygame":
        raise
    PYGAME_AVAILABLE = False