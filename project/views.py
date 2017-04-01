import time
import os

from quiz import QuizCreator

from app import app
from flask import request, jsonify
from flask import render_template

import traceback

running_tasks = []

OK = "200"
BAD_REQUEST = "400"
SERVER_ERROR = "500"



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=["GET", "POST"])
def upload_notes():
    if request.method == "POST":
        print "Uploading notes!"

        if 'notes-file' not in request.files:
            return BAD_REQUEST

        file = request.files['notes-file']
        if file.filename == '':
            return BAD_REQUEST

        if file:
            return process_notes(string = file.read())

        else:
            return BAD_REQUEST

    elif request.method == "GET":
        return render_template("index.html"), OK

@app.route('/submit', methods=["GET", "POST"])
def submit_notes():
    if request.method == "POST":
        print "Submitting notes!"
        form = request.data
        if not form:
            return BAD_REQUEST
        else:
            return process_notes(form)

    elif request.method == "GET":
        return render_template("index.html"), OK

def process_notes(string):
    # try:
    quiz = QuizCreator(string)
    running_tasks.append(quiz)
    quiz.create_questions()
    return quiz.generate_template(), OK
    # except:
    #     traceback.print_exc()
    #     return SERVER_ERROR

@app.route('/progress')
def progress():
    if running_tasks != []:
        return '{"percent_progress":"%s", "progress_text":"%s"}' % (running_tasks[0].get_percent_progress(), running_tasks[0].get_progress_text())
        #return jsonify(percent_progress=running_tasks[0].get_percent_progress(), progress_text=running_tasks[0].get_progress_text())
    else:
        return '{"percent_progress":"0", "progress_text":"Submitting..."}'
        #return jsonify(percent_progress="0", progress_text="Submitting...")

if __name__ == "__main__":
    app.run()