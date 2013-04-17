$(document).ready(function(){
	$('.on-button, .off-button').on('click', function(){
		var plug = $(this).data('plug').toString();
		$.ajax({
			type: "POST",
			contentType: "text/plain",
			data: plug,
			success: function(data){
				if(data.charAt(0) == "1"){
					$("#plug1").data('theme','g');
				} else {
					$("#plug1").data('theme','f');
				}
				if(data.charAt(1) == "1"){
					$("#plug1").data('theme','g');
				} else {
					$("#plug1").data('theme','f');
				}
				if(data.charAt(2) == "1"){
					$("#plug1").data('theme','g');
				} else {
					$("#plug1").data('theme','f');
				}
				if(data.charAt(3) == "1"){
					$("#plug1").data('theme','g');
				} else {
					$("#plug1").data('theme','f');
				}
			}
		
		});
	});
});
