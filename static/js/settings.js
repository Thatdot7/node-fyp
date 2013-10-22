var SocketHandler = {
	socket: null,
	
	start: function() {
		var url = "ws://" + location.host + "/ws_settings";
		if ("WebSocket" in window) {
			SocketHandler.socket = new WebSocket(url);
		} else {
			SocketHandler.socket = new MozWebSocket(url);
		}
		SocketHandler.socket.onmessage = function(event) {
			var data = JSON.parse(event.data);
			if(data.method == "0"){
				id_tag = "#" + data.id + "_name";
				$(id_tag).text(data.value);
			}else if(data.method == "1"){
				id_tag = "#" + data.id + "_name";
				$(id_tag).text(data.value);
			};;
		}
	}
}

$(document).ready( function(){	
	SocketHandler.start();
	console.log("Javascript reloaded");
	$(".update").on('click', function() {
		id_tag = $(this).parent().find("input").attr("id");
		
		if(id_tag == "zone" | id_tag == "device"){
			method = "1";
		} else {
			method = "0";
		}
		var message = { "method" : method,
				"id" : id_tag,
				"value" : $("#" + id_tag).val() }
		SocketHandler.socket.send(JSON.stringify(message));
	});
	$("#wifi-wizard").on('click', function(){
		$(this).button('loading');
	});
});
