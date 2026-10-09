'''
conditions.py — Condition classes for gating story choices and text variants.
Each Condition subclass implements evaluate(state) -> bool. Conditions are
constructed from dictionaries via Condition.from_dict(data), which dispatches
on the "type" key. Supported types:
    has_item, not, and, or, flag, relationship, variable, visited
'''