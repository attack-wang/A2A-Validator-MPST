def buy(self, prop):
    """Purchase a property: transfer cash and record ownership."""
    if not self.can_afford(prop.price):
        raise ValueError(f"{self.name} cannot afford {prop.name}")
    self.pay(prop.price)
    prop.owner = self
    self.properties.append(prop)