import re

class Notes(object):

	def __init__(self, string):
		self.notes = self.process_string(string)

	def add_notes(self, string):
		"""Adds notes to the existing set of notes"""
		self.process_string(string)

	def process_string(self, string):
		# Used to split the string into sentences
		re.match(r'\w\.\ ', string)

		sentences = string.split(".")

		return {
			"Pythagorean theory" : ["An example of a pythagorean triple is: 3, 4, 5",
									"Pythagorean Theorem applies to right angle triangles"
									"Pythagorean Theorem does not apply to any other shape."],
			"Sin, cos, tan" : ["sin, cos, and tan are the primary trig operations"]
		}
