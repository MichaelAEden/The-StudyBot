from questionBuilder import *
from notes import Notes
from jinja2 import Environment, PackageLoader, select_autoescape

class QuizCreator(object):

	def __init__(self, notes):
		"""Generates a quiz from the inputted notes"""

		# The number of each type of question created
		self.questions = []

		self.notes = {
			"Sentences": ["Pie is great",
						  "mitochondria is the powerhouse of the cell",
						  "How much wood would a woodchuck fuck",
						  "Studybot is cool",
						  "There are 7000 horses in my basement"]
		}
		self.question_index = -1
		self.create_questions()

	def get_least_asked_question(self):
		"""Gets the type of question which appears the least in the list of questions"""
		questions = {}
		for Question in [QuestionFillBlank, QuestionMultipleChoice, QuestionTrueFalse]:
			questions[Question.__name__] = 0

		for question in self.questions:
			questions[question.__class__.__name__] += 1

		print questions
		return min(questions, key=questions.get)

	# TODO: introduce randomness here
	def create_questions(self):
		for statement in self.notes["Sentences"]:
			# To make an equal balance of questions, find the least asked type of question
			question = None
			least_asked_question = self.get_least_asked_question()
			print least_asked_question

			if least_asked_question == QuestionMultipleChoice.__name__:
				current_index = self.notes["Sentences"].index(statement)
				question = QuestionMultipleChoice(self.notes["Sentences"][current_index:current_index + 4])

			if least_asked_question == QuestionFillBlank.__name__:
				if question is None or question.get_question() is None:
					question = QuestionFillBlank(statement)

			if least_asked_question == QuestionTrueFalse.__name__:
				if question is None or question.get_question() is None:
					question = QuestionTrueFalse(statement)

			if question is not None and question.get_question() is not None:
				self.questions.append(question)

	def reset(self):
		self.__init__(None)

	def regenerate_questions(self):
		self.__init__(self.notes)

	def add_notes(self, string):
		# self.notes.add(string)
		self.regenerate_questions()

	def generate_template(self):
		"""Generates a filled quiz template"""

		if len(self.questions) == 0:
			raise Exception("No questions to create quiz!")

		quiz = ""

		env = Environment(
			loader=PackageLoader('quiz', 'templates'),
			autoescape=select_autoescape(['html', 'xml'])
		)

		question_index = 1
		for question in self.questions:
			if isinstance(question, QuestionChoice):
				response_template = env.get_template('question_mc.html')
				response = response_template.render(
					responses=question.get_responses(),
					question_id=question_index,
					question_str=question.get_question(),
					answer_str=question.get_answer(),
					answer_index=question.get_answer_index()
				)
				print response
			else:
				response_template = env.get_template('question_text.html')
				response = response_template.render(
					question_id=question_index,
					question_str=question.get_question(),
					answer_str=question.get_answer()
				)
				print response

			quiz += response

			question_index += 1

		return quiz