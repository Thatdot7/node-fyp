$(document).ready(function(){
	$('.on-button, .off-button').on('click', function(){
		var plug = $(this).data('plug').toString();
		$.ajax({
			type: "POST",
			contentType: "text/plain",
			data: plug,
			success: function(data){
				console.log(data);
				console.log($("#plug1").data("theme"));
				if(data.charAt(0) == "1"){
					$("#light1").attr("src","/images/images.png");
				} else {
					$("#light1").attr("src","/images/images2.png");
				}
				if(data.charAt(1) == "1"){
					$("#light2").attr("src","/images/images.png");
				} else {
					$("#light2").attr("src","/images/images2.png");
				}
				if(data.charAt(2) == "1"){
					$("#light3").attr("src","/images/images.png");
				} else {
					$("#light3").attr("src","/images/images2.png");
				}
				if(data.charAt(3) == "1"){
					$("#light4").attr("src","/images/images.png");
				} else {
					$("#light4").attr("src","/images/images2.png");
				}
				
			}
		
		});
	});
});
