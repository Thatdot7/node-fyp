var SocketHandler = {
	socket: null,
	
	start: function() {
		var url = "ws://" + location.host + "/ws";
		if ("WebSocket" in window) {
			SocketHandler.socket = new WebSocket(url);
		} else {
			SocketHandler.socket = new MozWebSocket(url);
		}
		SocketHandler.socket.onmessage = function(event) {
			var data = event.data;
			console.log(data);
			if(data.charAt(0) == "1"){
				$("#light1").removeClass("grayscale");
				console.log("Plug 1 to on");
			} else {
				$("#light1").addClass("grayscale");
				console.log("Plug 1 to off");
			}
			if(data.charAt(1) == "1"){
				$("#light2").removeClass("grayscale");
			} else {
				$("#light2").addClass("grayscale");
			}
			if(data.charAt(2) == "1"){
				$("#light3").removeClass("grayscale");
			} else {
				$("#light3").addClass("grayscale");
			}
			if(data.charAt(3) == "1"){
				$("#light4").removeClass("grayscale");
			} else {
				$("#light4").addClass("grayscale");
			};
		}
	}
}

$(document).ready( function(){	
	SocketHandler.start();
	console.log("Javascript reloaded");
	$(".on-button, .off-button").on('click', function(){
		var message = $(this).data("plug");
		SocketHandler.socket.send(message);
	});
	$("#nav-bar").on('click', function(){
		if (!($(this).hasClass("ui-state-persist"))){
			SocketHandler.socket.close();
			console.log("webpage closing");
		}
	});
});	

