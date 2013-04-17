$(document).ready(function(){
	$('.on-button, .off-button').on('click', function(){
		var plug = $(this).data('plug').toString();
		$.ajax({
			type: "POST",
			contentType: "text/plain",
			data: plug,
			success: function(data){
				console.log("Ajax Success");
			}
		
		});
	});
});
