def make_object(kind, x, y, rng):
    if kind.startswith("gold_"): return Gold(kind, x, y)
    if kind.startswith("stone_"): return Stone(kind, x, y)
    if kind == "diamond": return Diamond(kind, x, y)
    if kind == "bone": return Bone(kind, x, y)
    if kind == "tnt": return TNT(kind, x, y)
    if kind == "mystery": return Mystery(kind, x, y, value=rng.randint(50, 550))
    raise ValueError(f"Unknown kind: {kind}")