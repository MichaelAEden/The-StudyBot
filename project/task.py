class Task(object):

    TASK_LENGTH_NOTES = 0.15
    TASK_LENGTH_QUESTIONS = 0.75
    TASK_LENGTH_TEMPLATES = 0.10

    def __init__(self):
        self.progress = 0
        self.progress_text = "Processing..."

    def update_progress(self, progress):
        self.progress = progress

    def add_progress(self, progress):
        self.progress += progress

    def set_progress_text(self, text):
        self.progress_text = text

    def get_percent_progress(self):
        return str(int(self.progress * 100))

    def get_progress_text(self):
        return self.progress_text

