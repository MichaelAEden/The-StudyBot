import os
import time

from notes import Notes
from quiz import QuizCreator

from flask import url_for, request
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload', methods=["GET", "POST"])
def upload_notes():
	if request.method == "POST":
		time.sleep(2)

		string = "No upload :("

		if 'notes-file' not in request.files:
			return "No file found :("

		file = request.files['notes-file']
		if file.filename == '':
			return "No selected file :("

		if file:
			string = file.read()
			print "READ! :)"

		return QuizCreator().generate_template()

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