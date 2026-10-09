class Space:
    GO = "go"
    CHANCE = "chance"
    JAIL = "jail"
    FREE_PARKING = "free_parking"
    GO_TO_JAIL = "go_to_jail"
    PROPERTY = "property"
    def __init__(self, name, kind, property_ref=None)