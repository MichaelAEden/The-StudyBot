import questionBuilder
import notes

class QuizCreator:

	def __init__(self):
		# The number of each type of question created
		self.question_types = {
			TRUE_FALSE : 0,
			FILL_BLANK : 0,
			MULTIPLE_CHOICE : 0
		}

		self.sorted_notes = None

		self.questions = []
		self.question_index = -1

	# TODO: introduce randomness here
	def create_questions(self):
		question = None

		for statement in self.notes["Sentences"]:
			# To make an equal balance of questions, find the least asked type of question
			least_asked_question = min(self.question_types.items(), key=lambda x: x[1])[0]

			'''if least_asked_question == FILL_BLANK:
				question = QuestionFillBlank(statement)
				self.question_types[FILL_BLANK] += 1

			if least_asked_question == TRUE_FALSE or question == None:
				question = QuestionTrueFalse(statement)
				self.question_types[TRUE_FALSE] += 1'''

			if least_asked_question == MULTIPLE_CHOICE or question == None:
				current_index = self.sorted_notes["Sentences"].index(statement)
				question = QuestionMultipleChoice(self.sorted_notes["Sentences"][current_index:current_index+4])
				self.question_types[MULTIPLE_CHOICE] += 1

			if question == None:
				continue

			self.questions.append(question)
			question = None

	def check_answer(self, user_answer):
		return question.check_answer(user_answer)

	def reset(self):
		self.notes = None
		self.questions = []
		self.question_index = -1

	def add_notes(self, string):
		notes = Notes(string)
		self.regenerate_questions()

	def replace_notes(self, string):
		notes.add(string)
		self.regenerate_questions()

	def get_next_question(self):
		"""
		Gets the next question, and incremenets the question pointer.

		:return: False if out of bounds, True otherwise.
		"""

		self.question_index += 1

		if self.question_index >= len(self.questions):
			self.question_index = 0
			return False
		else:
			question = self.questions[self.question_index]
			question.ask_question(bot)
			return True

	def regenerate_questions(self):
		self.questions = []
		self.question_index = -1
		self.create_questions()
