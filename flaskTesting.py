import os

from notes import Notes

from flask import url_for, request
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		string = "No upload :("

		if 'notes-file' not in request.files:
			return "No file found :("

		file = request.files['notes-file']
		if file.filename == '':
			return "No selected file :("

		if file:
			string = file.read()
			print "READ! :)"

		print string

	return render_template('index.html')

@app.route('/upload', )
def upload_notes():
	pass

# @app.route('/', methods=["GET", "POST"])
# def index():
# 	if request.method == "POST":
# 		string = "No upload :("
#
# 		if 'notes-file' not in request.files:
# 			print "No file found :("
# 		else:
# 			file = request.files['notes-file']
# 			if file.filename == '':
# 				print "No selected file :("
#
# 			if file:
# 				string = file.read()
# 				print "READ! :)"
#
# 		print "Done!"
# 		print string
#
# 	return render_template('index.html')

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
