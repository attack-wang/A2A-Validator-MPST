class Board:
    def __init__(self, spaces_def=BOARD_SPACES):
        self.spaces = [BoardSpace(i, **d) for i, d in enumerate(spaces_def)]
        self.owners = {}
        self.pot = 0
    @property
    def size(self):
        return len(self.spaces)
    def get_space(self, index):
        return self.spaces[index]
    def set_owner(self, index, player):
        self.owners[index] = player
    def get_owner(self, index):
        return self.owners.get(index)
    def reset_ownership(self, index):
        self.owners.pop(index, None)
    def properties_in_group(self, group):
        return [s.index for s in self.spaces if s.group == group]
    def move_player(self, player, steps):
        old = player.position
        new = (old + steps) % self.size
        player.position = new
        passed_go = steps > 0 and (old + steps) >= self.size
        return passed_go
    def teleport(self, player, index, collect_go=False):
        old = player.position
        player.position = index
        # GO salary only if moving forward past GO (target wrapped behind old position)
        passed = collect_go and index < old
        return passed