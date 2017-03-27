import re

class Notes(object):
    def __init__(self, string):
        self.people = []
        self.places = []
        self.concepts = []

        self.sentences = []

        self.notes = self.process_string(string)

    def add_notes(self, string):
        """Adds notes to the existing set of notes"""
        self.process_string(string)

    def process_string(self, string):
        # Used to split the string into sentences
        number_match = re.findall(r'\d+(\.\d+)?', string)
        bullet_point_match = re.findall(r'(?=\n*)(\n\s*?[\-\*\>]\s*.*?)(?=\n)', string)

        sentences = string.split(".")
