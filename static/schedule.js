var SocketHandler = {
	socket: null,
	
	start: function() {
		var url = "ws://" + location.host + "/ws_schedule";
		if ("WebSocket" in window) {
			SocketHandler.socket = new WebSocket(url);
		} else {
			SocketHandler.socket = new MozWebSocket(url);
		}
		SocketHandler.socket.onmessage = function(event) {
			var data = event.data;
			if(data.charAt(0) == "1"){
				id_tag = "#at_" + data.substring(1);
				$(id_tag).remove();
			}
		}
	}
}

$(document).ready(function() {
	SocketHandler.start();
	$("#repeat").on('click', function() {
		$("#days_repeat").show();
		console.log("Repeat Clicked");
	});
	$("#once-off").on('click', function() {
		$("#days_repeat").hide();
		console.log("Once-off clicked");
	});
	$(".at_delete").on('click', function() {
		id = $(this).data("id");
		message_string = "1" + id;
		console.log(message_string);
		SocketHandler.socket.send(message_string);
	});
});

