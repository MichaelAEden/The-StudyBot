// Checks whether the quiz answers were correct and notifies the user accordingly
$('button#submit-quiz').on('click', function () {
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
		source = $RES_DIR + "correct.png";
	}
	else {
		source = $RES_DIR + "incorrect.png";
	}
	$("#question_" + id + " .answer-correct").attr("src", source);
	$("#question_" + id + " .answer-correct").attr("style", "display:block;");
}