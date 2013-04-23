$(document).ready(function() {
	$("#repeat").on('click', function() {
		$("#days_repeat").show();
		console.log("Repeat CLicked");
	});
	$("#once-off").on('click', function() {
		$("#days_repeat").hide();
		console.log("Once-off clicked");
	});
});