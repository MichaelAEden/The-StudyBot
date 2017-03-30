import re
import textAnalytics

class Notes(object):

    UNUSED, USED = range(2)

    def __init__(self, string):
        self.amounts = []
        self.people = []
        self.places = []
        self.concepts = []

        self.statements = {}

        self.notes = self.process_string(string)

        self.statement_index = -1

    def add_notes(self, string):
        """Adds notes to the existing set of notes"""
        self.process_string(string)

    def process_string(self, string):
        # Used to split the string into sentences
        number_match = r'\d+(\.\d+)?'
        bullet_point_match = r'(?:(?=\n*)(\n\s*?[\-\*\>]\s*.*?)(?=\n))+'
        acronym_match = r'((?<!Dr|Mr|Ms|rs|St)\.)'

        statements = []

        # TODO: determine if the sentence leading up to the bullet points is a complete sentence
        for bullet_points in re.finditer(bullet_point_match, string):
            bullet_points = str(bullet_points.group(0))
            string = string.replace(bullet_points, "")  # Removes bullet points so they will not be duplicated

            bullet_points = bullet_points.replace("\n", "")
            statements += bullet_points.split("-")

        for number_match in re.finditer(number_match, string):
            self.amounts.append(float(number_match.group(0)))

        # Remove unnecessary whitespace
        string = string.replace("\n", "").replace("\t", "")
        statements += string.split(".")

        self.add_statements(statements)

    def get_statements(self):
        return self.statements.keys()

    def get_number_of_statements(self):
        return len(self.get_statements())

    def get_next_statement(self):
        """Gets a statement which has not yet been used in a question"""
        for statement, usage in self.statements.iteritems():
            if usage == self.UNUSED:
                return statement

        return None

    def set_statement_used(self, statement):
        """After a statement has been used for a question, indicate this question should not be used again"""
        self.statements[statement] = self.USED

    def set_statements_used(self, statements):
        """After a statement has been used for a question, indicate this question should not be used again"""
        for statement in statements:
            self.set_statement_used(statement)

    def are_unused_statements(self):
        """After a statement has been used for a question, indicate this question should not be used again"""
        return self.UNUSED in self.statements.values()

    def format_statements(self, statements):
        """Makes the sentences appear grammatically correct"""
        formatted_sentences = []
        for sentence in statements:
            sentence = sentence.strip()
            if sentence:
                sentence = list(sentence)
                sentence.append(".")
                sentence[0] = sentence[0].upper()
                formatted_sentences.append("".join(sentence))

        return formatted_sentences

    def add_statements(self, statements):
        statements = self.format_statements(statements)
        for statement in statements:
            self.statements[statement] = self.UNUSED