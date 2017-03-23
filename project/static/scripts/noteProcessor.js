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

// Checks whether the quiz answers were correct and notifies the user accordingly
$('#process-notes__text').on('click', function () {
	for (var i = 0; i < $(".quiz-question").length; i++) {
		$("#question_" + i)
	}
});

function sendNotes(notes, is_file) {
	var url;

	if (is_file) {
		url = "/upload";
	}
	else {
		url = "/submit";
	}

	$.ajax({
		type: 'POST',
		url: url,
		data: notes,
		contentType: false,
		processData: false,
		async: true,
		success: function (data) {
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

