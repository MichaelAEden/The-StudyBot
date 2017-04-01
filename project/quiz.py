from questionBuilder import *
from notes import Notes
from task import Task
from jinja2 import Environment, PackageLoader, select_autoescape

import operator


class QuizCreator(Task):

    def __init__(self, string):
        """Generates a quiz from the inputted notes"""

        # The number of each type of question created
        Task.__init__(self)

        self.notes = None
        self.questions = []
        self.question_index = -1

        self.process_notes(string)

    def process_notes(self, string):
        self.set_progress_text("Reading notes...")
        self.notes = Notes(string)
        self.add_progress(self.TASK_LENGTH_NOTES)

    def get_least_to_most_asked_questions(self):
        """Gets the type of question which appears the least in the list of questions"""
        questions = {}
        for Question in [QuestionFillBlank, QuestionMultipleChoice, QuestionTrueFalse]:
            questions[Question] = 0

        for question in self.questions:
            questions[question.__class__] += 1

        return sorted(questions, key=questions.get)

    # TODO: introduce randomness here
    def create_questions(self):
        """Creates questions based on the set of notes"""
        self.set_progress_text("Creating questions...")
        increment_progress = self.TASK_LENGTH_QUESTIONS/self.notes.get_number_of_statements()

        while self.notes.are_unused_statements():
            self.add_progress(increment_progress)

            # To make an equal balance of questions, find the least asked type of question
            question_types = self.get_least_to_most_asked_questions()

            for question_type in question_types:
                question = question_type.create_from_notes(self.notes)
                if question is not None:
                    self.questions.append(question)
                    break

    def reset(self):
        self.__init__(None)

    def regenerate_questions(self):
        self.__init__(self.notes)

    def add_notes(self, string):
        # self.notes.add(string)
        self.regenerate_questions()

    def generate_template(self):
        """Generates a filled quiz HTML template"""
        self.set_progress_text("Generating quiz...")
        increment_progress = self.TASK_LENGTH_TEMPLATES/len(self.questions)

        if len(self.questions) == 0:
            raise Exception("No questions to create quiz!")

        quiz = ""

        env = Environment(
            loader=PackageLoader('quiz', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        question_index = 1

        for question in self.questions:
            self.add_progress(increment_progress)

            if isinstance(question, QuestionChoice):
                response_template = env.get_template('question_mc.html')
                response = response_template.render(
                    responses=question.get_responses(),
                    question_id=question_index,
                    question_str=question.get_question(),
                    answer_str=question.get_answer(),
                    answer_response=question.get_answer_response()
                )
            else:
                response_template = env.get_template('question_text.html')
                response = response_template.render(
                    question_id=question_index,
                    question_str=question.get_question(),
                    answer_str=question.get_answer()
                )

            quiz += response
            question_index += 1

        self.set_progress(1)
        self.set_progress_text("Success!")
        return quiz
