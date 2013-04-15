$(document).ready(function(){
	setInterval(function(){
		$.ajax({
			type: "POST",
			data: $("#test_text").val(),
			success: function(data){
				var message = "<p>" + data + "</p>";
				$("#test_result").after($(message));
			}
		
		});
		
		
	}, 1000);
});