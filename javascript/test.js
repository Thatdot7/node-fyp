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
					$("#plug1").closest(".ui-collapsible").attr("data-theme", "g").find("a").first().attr("data-theme","g").removeClass(".ui-btn-up-f .ui-btn-hover-f .ui-btn-up-b").addClass(".ui-btn-up-g .ui.btn-hover-g");
					console.log($("plug1").data("theme"));
				} else {
					$("#plug1").data('theme',"f");
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
