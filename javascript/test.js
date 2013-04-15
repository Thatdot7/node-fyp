$(document).ready(function(){
	$('.on-button').on('click', function(){
		var plug = $(this).data('plug');
		$.ajax({
			type: "POST",
			contentType: "text/plain",
			data: "11",
			success: function(data){
				console.log("Ajax Success");
			}
		
		});
	});
});