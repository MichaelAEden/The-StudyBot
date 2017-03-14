$('#process-file').on('click', function () {
	$('#notes-input input[type=file]').click();
});

$('#notes-input').change( function () {
	$('#notes-input input[type=submit]').click()
	$('#processing').collapse({
		toggle: true
	})
	$('#quiz').collapse({
		toggle: true
	})
});

