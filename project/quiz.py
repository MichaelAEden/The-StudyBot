from questionBuilder import *
from notes import Notes
import string
import jinja2
from jinja2 import Environment, PackageLoader, select_autoescape

class QuizCreator:

	def __init__(self):
		# The number of each type of question created
		self.question_types = {
			TRUE_FALSE : 0,
			FILL_BLANK : 0,
			MULTIPLE_CHOICE : 0
		}

		self.notes = None
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
		return self.questions[self.question_index].check_answer(user_answer)

	def reset(self):
		self.notes = None
		self.questions = []
		self.question_index = -1

	def replace_notes(self, string):
		self.notes = Notes(string)
		self.regenerate_questions()

	def add_notes(self, string):
		self.notes.add(string)
		self.regenerate_questions()

	def get_next_question(self):
		"""
		Gets the next question, and increments the question pointer.

		:return: False if out of bounds, True otherwise.
		"""

		self.question_index += 1

		if self.question_index >= len(self.questions):
			self.question_index = 0
			return False
		else:
			question = self.questions[self.question_index]
			return question

	def regenerate_questions(self):
		self.questions = []
		self.question_index = -1
		self.create_questions()

	# Generates a filled quiz template
	def generate_template(self):
		quiz = ""

		self.questions = [
			QuestionTrueFalse("Studybot is kind of cool."),
			QuestionMultipleChoice([
				"Mitochondria is the powerhouse of the cell",
				"Birds are made of cells",
				"Inorganic material is not made out of cells",
				"Studybot is cool"
			])
		]

		env = Environment(
			loader=PackageLoader('quiz', 'templates'),
			autoescape=select_autoescape(['html', 'xml'])
		)

		if len(self.questions) == 0:
			raise Exception("No questions to create quiz!")

		for question_index in range(len(self.questions)):
			question = self.questions[question_index]

			if isinstance(question, QuestionChoice):
				template = env.get_template('question_mc.html')

				quiz += template.render(
					question_id=str(question_index + 1) + ".",
					question=question.get_question(),
					responses=question.get_responses()
				)

			else:
				template = env.get_template('question_text.html')

				quiz += template.render(
					question_id=question_index,
					question=question.get_question()
				)

		return quiz