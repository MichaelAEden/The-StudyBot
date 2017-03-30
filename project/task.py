class Task(object):
    def __init__(self):
        self.progress = 0

    def update_progress(self, progress):
        self.progress = progress

    def add_progress(self, progress):
        self.progress += progress

    def get_percent_progress(self):
        return str(int(self.progress * 100))
