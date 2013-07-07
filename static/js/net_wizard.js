$(document).ready(function() {
	$("#saved_net, #scan_net").on('click', function() {
		if($(this).attr("id") == "saved_net"){
			$("#saved-group").show();
			$("#scan-group").hide();
			$("#scan-start").hide();
		} else {
			$("#scan-group").show();
			$("#saved-group").hide();
			$("#scan-start").show();
		}
	});
});