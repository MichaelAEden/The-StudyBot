import random
import string

TRUE_FALSE = 0
FILL_BLANK = 1
MULTIPLE_CHOICE = 2



class Question:

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
			self.question = make_statement_false(statement)
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

		false_statements = []
		true_statement = None

		for i in range(len(statements)):
			if i == len(statements) - 1:
				true_statement = statements[i]
			else:
				false_statement = make_statement_false(statements[i])
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



def make_statement_false(statement):
	"""
	Makes a true statement alse.

	:param statement: A string representing a true statement.
	:return: A false version of the same statement, or None if this failed.
	"""
	action_verbs = ["is", "was", "are", "were", "will", "can", "should"]
	answer = True

	if "not" in statement:
		question = statement.replace("not ", "")
		answer = False
	else:
		for action_verb in action_verbs:
			if action_verb in statement:
				question = statement.replace(action_verb, action_verb + " not")
				answer = False

				break

	return question if (answer == False) else None




