// Opens the file selection dialog when the button is clicked
$('#process-file').on('click', function () {
	$('#notes-form input[type=file]').click();
});

// Sends the uploaded file to Flask framework, triggered when a file is uploaded
$('#notes-form').change( function () {
	$('#processing').collapse({
		toggle: true
	})

	var form_data = new FormData($('#notes-form')[0])
	$.ajax({
		type: 'POST',
		url: '/upload',
		data: form_data,
		contentType: false,
		processData: false,
		async: true,
		success: function (data) {
			console.log("File successfully uploaded!")
			console.log(data)
			$('#processing').collapse({
				toggle: false
			})
			$('#quiz').html(data);
			$('#quiz').collapse({
				toggle: true
			})
		}
	})
});

