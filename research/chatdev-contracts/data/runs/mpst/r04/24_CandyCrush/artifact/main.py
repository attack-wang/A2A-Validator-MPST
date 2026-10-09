def drain_events(self):
    events = self.events
    self.events = []
    return events