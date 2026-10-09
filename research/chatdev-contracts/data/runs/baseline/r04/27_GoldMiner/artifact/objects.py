def make_object(kind, x, y):
    from gold import Gold, Rock, Diamond, Bone, TNT, MysteryBag
    if kind.startswith('gold_'):
        return Gold(kind.split('_', 1)[1], x, y)
    if kind.startswith('rock_'):
        return Rock(kind.split('_', 1)[1], x, y)
    if kind == 'diamond':
        return Diamond(x, y)
    if kind == 'bone':
        return Bone(x, y)
    if kind == 'tnt':
        return TNT(x, y)
    if kind == 'mystery':
        return MysteryBag(x, y)
    raise ValueError(f'Unknown object kind: {kind}')