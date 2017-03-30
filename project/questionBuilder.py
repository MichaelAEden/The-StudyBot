import textAnalytics
import random
import re

class Question(object):

    question = None
    answer = None

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def check_answer(self, user_answer):
        return user_answer == self.answer

    @classmethod
    def create_from_notes(cls, notes):
        """
        Generates a question from notes.
        :param notes: Notes object
        :return: None if unsuccessful, Question object otherwise.
        """
        return None

class QuestionChoice(Question):
    """
    Type of question in which the user selects from different choices, rather than a text response.
    """

    responses = []
    answer_index = -1

    def __init__(self, question, answer, responses, answer_index):
        Question.__init__(self, question, answer)
        self.responses = responses
        self.answer_index = answer_index

    def get_responses(self):
        return self.responses

    def get_answer_response(self):
        return self.responses[self.answer_index]

    def check_answer(self, user_answer):
        """
        Checks if the user's answer was correct.
        :param user_answer: The index of the selected answer.
        :return: True if this equals the index of the correct answer, False otherwise.
        """
        return user_answer == self.answer_index

class QuestionTrueFalse(QuestionChoice):

    TRUE_STRING = "True"
    FALSE_STRING = "False"

    TRUE = 0
    FALSE = 1

    @classmethod
    def create_from_notes(cls, notes):
        statement = notes.get_next_statement()

        question = statement
        answer = statement
        responses = [cls.TRUE_STRING, cls.FALSE_STRING]
        answer_index = cls.TRUE

        # Randomly chooses if answer to question is "True" or "False"
        is_true = random.randint(0, 1)

        if not is_true:
            false_statement = get_false_statement(statement)
            if false_statement != None:
                question = false_statement
                answer_index = cls.FALSE

        notes.set_statement_used(statement)
        return cls(question, answer, responses, answer_index)

class QuestionFillBlank(Question):

    def __init__(self, question, answer):
        Question.__init__(self, question, answer)

    def check_answer(self, user_answer):
        user_answer = user_answer.lower().strip()
        return user_answer == self.answer.lower().strip()

    @classmethod
    def create_from_notes(cls, notes):
        statement = notes.get_next_statement()
        key_words = textAnalytics.get_key_phrases(statement)

        if not key_words or all(key == "" for key in key_words):
            print "Couldn't grab any key words!"
            return None

        key_word_index = random.randint(0, len(key_words) - 1)
        key_word = key_words[key_word_index]

        answer = key_word
        question = statement.replace(key_word, "________")

        notes.set_statement_used(statement)
        return cls(question, answer)

class QuestionMultipleChoice(QuestionChoice):

    MINIMUM_RESPONSES = 2
    MAXIMUM_RESPONSES = 4

    @classmethod
    def create_from_notes(cls, notes):
        """Tries to make a multiple choice question of at least 2 choices from inputted notes"""
        QuestionChoice.create_from_notes(notes)

        used_statements = []
        false_statements = []

        true_statement = None
        number_of_responses = 0

        while notes.are_unused_statements() and number_of_responses < cls.MAXIMUM_RESPONSES:
            statement = notes.get_next_statement()
            false_statement = get_false_statement(statement)

            if false_statement is not None:
                false_statements.append(false_statement)
                used_statements.append(statement)

            if false_statement is None or len(false_statements) == cls.MAXIMUM_RESPONSES - 1:
                if true_statement is None:
                    true_statement = statement
                else:
                    break

            number_of_responses = len(false_statements) + 1

        if number_of_responses <= cls.MINIMUM_RESPONSES:
            print "Couldn't find enough choices!"
            return None

        notes.set_statements_used(used_statements)
        answer_index = random.randint(0, len(false_statements))

        j = 0
        responses = []
        for i in range(number_of_responses):
            if i == answer_index:
                responses.append(true_statement)
            else:
                responses.append(false_statements[j])
                j += 1

        question = "Which of the following is true?"
        answer = true_statement

        return cls(question, answer, responses, answer_index)

def get_false_statement(statement):
    """
    Makes a true notes false.
    :param notes: A string representing a true notes.
    :return: String representing a false notes, or None if failed.
    """
    negatives = {
        "will not": "will",
        "weren't": "were",
        "aren't": "are",
        "wasn't": "was",
        "shouldn't": "should",
        "doesn't": "does",
        "isn't": "is",
        "not ": " "
    }
    number_match = re.search(r'\d+(\.\d+)?', statement)
    question = None

    # Replaces a number with a another number within a certain range (e.g.: 1.5 -> 2.0)
    if number_match != None:
        number_str = number_match.group(0)
        if "." in number_str:
            precision = len(number_str.split(".")[1])

        else:
            precision = 0

        number_val = float(number_str)
        lower_variance_limit, upper_variance_limit = 0.15, 0.50
        variance = random.uniform(lower_variance_limit, upper_variance_limit)

        if number_val != 1:
            new_val = number_val * variance
            if new_val != number_val:
                new_str = ("%%.%if" % precision) % new_val
                question = statement.replace(number_str, new_str)

    # Replaces a negative with its counterpart (e.g.: "wasn't" -> "was")
    if question == None:
        for negative, action in negatives.iteritems():
            if negative in statement:
                question = statement.replace(negative, action)

    # Replaces an action with its negative counterpart (e.g.: "was" -> "wasn't")
    if question == None:
        for action in negatives.keys():
            if action in statement:
                question = statement.replace(action, action + " not")

    return question