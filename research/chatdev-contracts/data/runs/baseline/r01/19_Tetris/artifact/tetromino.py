    def __init__(self):
        self._bag = []
        self._next_key = None
        self._refill()
        self._advance()  # FIX: prime the first piece so next_shape() never returns None