import time
import os

from notes import Notes
from quiz import QuizCreator

from app import app
from flask import url_for, request
from flask import render_template

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload', methods=["GET", "POST"])
def upload_notes():
	if request.method == "POST":
		print "Uploading notes!"

		if 'notes-file' not in request.files:
			return "No file found."

		file = request.files['notes-file']
		if file.filename == '':
			return "No selected file."

		if file:
			string = file.read()

			notes = Notes(string)
			quiz = QuizCreator(notes)

			return quiz.generate_template()
		else:
			return "400"

	elif request.method == "GET":
		return render_template("index.html")

@app.route('/submit', methods=["GET", "POST"])
def submit_notes():
	if request.method == "POST":
		print "Submitting notes!"
		form = request.data
		if form == '':
			return "400"
		else:
			notes = Notes(form)
			quiz = QuizCreator(notes)
			return quiz.generate_template()

	elif request.method == "GET":
		return render_template("index.html")



# Used to update website content
@app.context_processor
def override_url_for():
	return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
	if endpoint == 'static':
		filename = values.get('filename', None)
		if filename:
			file_path = os.path.join(app.root_path,
									 endpoint, filename)
			values['q'] = int(os.stat(file_path).st_mtime)
	return url_for(endpoint, **values)



if __name__ == "__main__":
	app.run()