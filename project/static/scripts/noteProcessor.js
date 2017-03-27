// Opens the file selection dialog when the button is clicked
$('#process-notes__file').on('click', function () {
	$('#notes-form__file input[type=file]').click();
});

// Sends the uploaded file to Flask framework, triggered when a file is uploaded
$('#notes-form__file').change( function () {
	$('#processing').collapse({
		toggle: true
	});
	var form_data = new FormData($('#notes-form__file')[0]);
	sendNotes(form_data, true);
});

// Sends the inputted text to the Flask framework
$('#process-notes__text').on('click', function () {
	$('#processing').collapse({
		toggle: true
	});

	var text = $('#notes-input').val();
	sendNotes(text, false);
});

function getQuestion(id) {
	return $("#question_" + id);
}

function checkMCAnswer(id) {
	return $("#question_" + id + " [data-correct=True] input").is(":checked");
}

function checkTextAnswer(id) {
	var userAnswer = $("#question_" + id + " input").val();
	var correctAnswer = $("#question_" + id).attr("data-answer");
	return userAnswer == correctAnswer;
}

function updateAnswer(id, isCorrect) {
	var source;
	if (isCorrect) {
		source = $RES_DIR + "/correct.png";
	}
	else {
		source = $RES_DIR + "/incorrect.png";
	}
	$("#question_" + id + " .answer-correct").attr("src", source);
	$("#question_" + id + " .answer-correct").attr("style", "display:block;");
}

// Checks whether the quiz answers were correct and notifies the user accordingly
$('#submit-quiz-button').on('click', function () {
	var questions = $(".quiz-question")

	for (var id = 1; id <= questions.length; id++) {
		var question_type = getQuestion(id).attr("data-type");

		if (question_type == "MultipleChoice") {
			updateAnswer(id, checkMCAnswer(id))
		}
		else if (question_type == "TextInput") {
			updateAnswer(id, checkTextAnswer(id))
		}
	}
});

function updateProgress() {
	$.get('/progress').done(function(percentComplete) {
		$('#progress-bar').animate({"width": percentComplete + "%"}).attr("aria-valuenow", percentComplete);
		console.log("Doing something??")
	})
}

function sendNotes(notes, is_file) {
	var url;

	if (is_file) {
		url = "/upload";
	}
	else {
		url = "/submit";
	}

	var interval;

	$.ajax({
		type: 'POST',
		url: url,
		data: notes,
		contentType: false,
		processData: false,
		async: true,
		beforeSend: function() {
			interval = setInterval(updateProgress, 1000);
		},
		success: function (data) {
			clearInterval(interval)
			if (data == "400") {
				$("#progress-text").css("color", "red");
				$("#progress-text").html("Failed");
			}
			else {
				$('#processing').collapse({
					toggle: false
				});
				$('#quiz').html(data);
				$('#quiz-section').collapse({
					toggle: true
				})
			}
		}
	});
}

