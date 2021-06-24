class RoadmapItem():
    def __init__(self, name, done, details):
        self.name = name
        self.done = done
        self.details = details
    
    @property
    def icon_class(self):
        if self.done:
            return 'fas fa-check-circle text-success'
        else:
            return 'fas fa-times-circle text-danger'
