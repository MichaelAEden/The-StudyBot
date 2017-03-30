// Intervals
hideProgressInterval = null
updateProgressInterval = null

// Opens the file selection dialog when the button is clicked
$('#process-notes__file').on('click', function () {
	$('#notes-form__file input[type=file]').click();
});

// Sends the uploaded file to Flask framework, triggered when a file is uploaded
$('#notes-form__file').change( function () {
	var form_data = new FormData($('#notes-form__file')[0]);
	sendNotes(form_data, true);
});

// Sends the inputted text to the Flask framework
$('#process-notes__text').on('click', function () {
	var text = $('#notes-input').val();
	sendNotes(text, false);
});

function updateProgress() {
	$.get('/progress').done( function(percentComplete) {
		animateProgressBar(percentComplete)
	});
}

function hideProgress() {
	$('#processing').collapse('hide');
	clearInterval(hideProgressInterval)
}

function animateProgressBar(percentComplete) {
	$('#progress-bar').animate({"width": percentComplete + "%"}).attr("aria-valuenow", percentComplete);
}

function reset() {
	// Resets the value of the progress bar
	$('#processing').collapse('show');
	$("#progress-text").css("color", "darkblue");
	$("#progress-text").html("Processing...");
	$('#progress-bar').attr("aria-valuenow", 0);
}

function sendNotes(notes, is_file) {
	var url;

	reset()

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
		beforeSend: function() {
			updateProgressInterval = setInterval(updateProgress, 500);
		},
		success: function (data) {
			clearInterval(updateProgressInterval);
			hideProgressInterval = setInterval(hideProgress, 3000);
			if (data == "400" || data == "500") {
				$("#progress-text").css("color", "red");
				$("#progress-text").html("Failed");
			}
			else {
				animateProgressBar("100")
				$("#progress-text").css("color", "green");
				$("#progress-text").html("Success!");
				$('#quiz').html(data);
				$('#quiz-section').collapse('show')
			}
		}
	});
}

