def spritecollideany(sprite, group, collided=None):
    """...
    """
    if collided is not None:
        for s in group.sprites():
            if collided(sprite, s):
                return s
    else:
        # Special case old behaviour if no collided function supplied.
        # This checks for any special collision methods that may be
        # defined on the group.
        ...
        for s in group.sprites():
            if sprite.rect.colliderect(s.rect):
                return s
    return None