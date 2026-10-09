class BoardSpace:
    def __init__(self, index, name, short=None, type="property", price=0, rent=0, group=None, amount=0):
        self.index = index
        self.name = name
        self.short_name = short or name[:8]
        self.type = type
        self.price = price
        self.rent = rent
        self.group = group
        self.amount = amount