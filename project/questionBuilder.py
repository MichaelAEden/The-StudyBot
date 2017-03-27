import textAnalytics
import random
import re

class Question(object):

    def __init__(self, statement):
        self.question = None
        self.answer = None

        self.create_question_from_statements(statement)

    def create_question_from_statements(self, statement):
        """
        Generates a question from a statement.
        :param statement: Some true statement.
        :return: False if unsuccessful, True otherwise.
        """
        return False

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def check_answer(self, user_answer):
        return user_answer == self.answer

class QuestionChoice(Question):
    """
    Type of question in which the user selects from different choices, rather than a text response.
    """

    def __init_(self, statement):
        Question.__init__(self, statement)

    def create_question_from_statements(self, statement):
        self.responses = []
        self.answer_index = -1

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

    def __init__(self, statement):
        QuestionChoice.__init__(self, statement)

    def create_question_from_statements(self, statement):
        QuestionChoice.create_question_from_statements(self, statement)
        self.answer = statement
        self.answer_index = self.TRUE
        self.responses = [self.TRUE_STRING, self.FALSE_STRING]

        # Randomly chooses if answer to question is "True" or "False"
        is_true = random.randint(0, 1)

        if not is_true:
            self.question = get_false_statement(statement)
            if self.question != None:
                self.answer_index = self.FALSE

        # If creating a statement with a false answer was unsuccessful, also create a true one
        if is_true or self.answer_index is self.TRUE:
            self.question = statement
            self.answer_index = self.TRUE

        return True

    def get_question(self):
        return self.question

class QuestionFillBlank(Question):

    def __init__(self, statement):
        Question.__init__(self, statement)

    def create_question_from_statements(self, statement):
        key_words = textAnalytics.get_key_phrases(statement)

        if key_words == []:
            return False

        key_word_index = random.randint(0, len(key_words) - 1)
        key_word = key_words[key_word_index]

        self.question = statement.replace(key_word, "________")
        self.answer = key_word

        return True

    def check_answer(self, user_answer):
        user_answer = user_answer.lower().strip()
        return user_answer == self.answer.lower().strip()

class QuestionMultipleChoice(QuestionChoice):

    def __init__(self, statement):
        QuestionChoice.__init__(self, statement)

    def create_question_from_statements(self, statements):
        """Tries to make a multiple choice question of at least 2 choices from inputted statements"""
        QuestionChoice.create_question_from_statements(self, statements)

        minimum_responses = 2
        if len(statements) < minimum_responses:
            return False

        false_statements = []
        true_statement = None

        for i in range(len(statements)):
            if i == len(statements) - 1:
                true_statement = statements[i]
            else:
                false_statement = get_false_statement(statements[i])
                if false_statement != None:
                    false_statements.append(false_statement)
                else:
                    if true_statement == None:
                        true_statement = statements[i]
                    else:
                        if i < minimum_responses:
                            return False
                        else:
                            break

        number_of_responses = len(false_statements) + 1
        answer_index = random.randint(0, len(false_statements))

        j = 0
        for i in range(number_of_responses):
            if i == answer_index:
                self.responses.append(true_statement)
            else:
                self.responses.append(false_statements[j])
                j += 1

        self.question = "Which of the following is true?"
        self.answer = true_statement
        self.answer_index = answer_index

        return True

def get_false_statement(statement):
    """
    Makes a true statement false.
    :param statement: A string representing a true statement.
    :return: String representing a false statement, or None if failed.
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