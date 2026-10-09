def has_item(item): return {"type": "has_item", "item": item}
def not_has_item(item): return {"type": "has_item", "item": item, "negate": True}
def rel_at_least(who, value): return {"type": "relationship_at_least", "who": who, "value": value}
def rel_below(who, value): return {"type": "relationship_at_least", "who": who, "value": value, "negate": True}
def flag(flag_name): return {"type": "flag", "flag": flag_name}
def no_flag(flag_name): return {"type": "flag", "flag": flag_name, "negate": True}
def var_at_least(name, value): return {"type": "var_at_least", "name": name, "value": value}
def var_equals(name, value): return {"type": "var_equals", "name": name, "value": value}
def visited(node_id): return {"type": "visited", "node": node_id}
def not_visited(node_id): return {"type": "visited", "node": node_id, "negate": True}
def add_item(item): return {"type": "add_item", "item": item}
def remove_item(item): return {"type": "remove_item", "item": item}
def change_relationship(who, delta): return {"type": "change_relationship", "who": who, "delta": delta}
def set_flag(flag_name): return {"type": "set_flag", "flag": flag_name}
def add_coins(amount): return {"type": "add_coins", "amount": amount}
def evaluate_condition(cond, state): dispatch on type with negation
def check_conditions(conds, state): all()