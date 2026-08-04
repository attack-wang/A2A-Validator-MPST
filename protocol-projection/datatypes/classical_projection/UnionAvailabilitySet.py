class UnionAvailabilitySet:

    def __init__(self, list_avail_sets):
        self.list_avail_sets = list_avail_sets

    def compute_avail_msgs(self):
        avail_msgs = set()
        for lazy_avail_set in self.list_avail_sets:
            avail_set = lazy_avail_set.compute_avail_msgs()
            avail_msgs.update(avail_set)
        return avail_msgs