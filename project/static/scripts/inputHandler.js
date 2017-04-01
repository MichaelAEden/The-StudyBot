// Intervals
hideProgressInterval = null
updateProgressInterval = null

// Opens the file selection dialog when the button is clicked
$('button#submit-notes-file').on('click', function () {
	$('form#notes-file input[type=file]').click();
});

// Sends the uploaded file to Flask framework, triggered when a file is uploaded
$('form#notes-file').change( function () {
	var form_data = new FormData($('form#notes-file')[0]);
	sendNotes(form_data, true);
});

// Sends the inputted text to the Flask framework
$('button#submit-notes-text').on('click', function () {
	var text = $('textarea#notes-input').val();
	sendNotes(text, false);
});

// Fills the notes textarea with sample notes
$('button#submit-notes-sample').on('click', function () {
    file_name = 'notes_sample.txt'
    $.get($RES_DIR + file_name, function(data) {
        var text = $('textarea#notes-input').val(data);
	    sendNotes(data, false);
    }, 'text');
});

function updateProgress() {
	$.get('/progress').done( function(data) {
		var progress = jQuery.parseJSON(data);
		updateProgressBar(progress.percent_progress, progress.progress_text)
	});
}

function hideProgress() {
	$('div#processing-progress').collapse('hide');
	clearInterval(hideProgressInterval)
}

function updateProgressBar(percentComplete, progressText) {
	$("#processing-progress-text").html(progressText);
	$('div#processing-progress-bar').css("width", percentComplete + "%").attr("aria-valuenow", percentComplete);
}

// Resets the value of the progress bar
function reset() {
	updateProgressBar("0", "Submitting...")
	$("#processing-progress-text").css("color", "darkblue");
	$('div#processing-progress').collapse('show');
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
			updateProgressInterval = setInterval(updateProgress, 50);
		},
		success: function (data) {
			clearInterval(updateProgressInterval);
			hideProgressInterval = setInterval(hideProgress, 2000);
			if (data == "400" || data == "500") {
				$("#processing-progress-text").css("color", "red");
				updateProgressBar("0", "Failed...")
			}
			else {
				updateProgressBar("100", "Success!")
				$("#processing-progress-text").css("color", "green");
				$('#quiz-questions').html(data);
				$('#quiz').collapse('show')
			}
		}
	});
}

