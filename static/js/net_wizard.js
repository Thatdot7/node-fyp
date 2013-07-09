$(document).ready(function() {
	$(".connect, .delete").on('click', function(){
		var id_tag = $(this).parents(".accordion-body").attr("id");
		id_tag = id_tag.split("_-_");
		id_tag[1] = id_tag[1].replace("-_-", " ");
		var request_message;
		
		if(id_tag[0] == "scan"){
			$(this).button('loading');

			if($(this).hasClass("wps-pin")){
				request_message = {net_cat: id_tag[0], id: id_tag[1],
							method: "wps-pin", pin: $(this).parent().find("input").val()}
			} else if($(this).hasClass("wps-push")){
				request_message = {net_cat: id_tag[0], id: id_tag[1],
							method: "wps-push"}
			} else if($(this).hasClass("wpa")){
				request_message = {net_cat: id_tag[0], id: id_tag[1],
							method: "wpa", pass: $(this).parent().find("input").val()}
			} else if($(this).hasClass("eap")){
				console.log($(this).parent().find("input.pass").val());
				request_message = {net_cat: id_tag[0], id: id_tag[1],
							method: "eap", pass: $(this).parents(".control-group").find("input.pass").val(),
							identity: $(this).parents(".control-group").find("input.identity").val()}
			} else {
				request_message = {net_cat: id_tag[0], id: id_tag[1],
							method: "open"}
			}
		} else {
			if($(this).hasClass("connect")){
				$(this).button('loading');
				request_message = {net_cat: id_tag[0], id: id_tag[1],
							method: "connect"};
			} else {
				console.log("Delete Button");
				request_message = {net_cat: id_tag[0], id: id_tag[1],
							method: "delete"};
			}
		}		
		console.log(request_message);
		
		$.post('wifiwizard', request_message
		).done(function(data){
			location.reload();
			//console.log(data);
		});
	});
});
