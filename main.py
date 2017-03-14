# TODO: learn everything in this file
# - Flask module
# - @ operator
# - lambda keyword

import threading
import subprocess
import uuid			# Universally unique identifier
from flask import Flask
from flask import render_template, url_for, abort, jsonify, request
app = Flask(__name__)

background_scripts = {}

def run_script(id):
	subprocess.call(["quiz.py"])
	background_scripts[id] = True

# This decorator tells flask which URL triggers this function
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/generate')
def generate():
	id = str(uuid.uuid4())
	background_scripts[id] = False
	threading.Thread(target=lambda: run_script(id)).start()
	return render_template('processing.html', id=id)

@app.route('/is_done')
def is_done():
	id = request.args.get('id', None)

	# If the id of the completed script is not one of the background scripts running, abort
	if id not in background_scripts:
		abort(404)

	return jsonify(done=background_scripts[id])

def function(string):
	print string
	return "Fantastic!"