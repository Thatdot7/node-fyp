$(document).ready(function(){	
	SocketHandler.start();
	$(".on-button, .off-button").on('click', function(){
		var message = $(this).data("plug");
		SocketHandler.socket.send(message);
	});
});

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
			if(data.charAt(0) == "1"){
				$("#light1").attr("src","static/images/images.png");
			} else {
				$("#light1").attr("src","static/images/images2.png");
			}
			if(data.charAt(1) == "1"){
				$("#light2").attr("src","static/images/images.png");
			} else {
				$("#light2").attr("src","static/images/images2.png");
			}
			if(data.charAt(2) == "1"){
				$("#light3").attr("src","static/images/images.png");
			} else {
				$("#light3").attr("src","static/images/images2.png");
			}
			if(data.charAt(3) == "1"){
				$("#light4").attr("src","static/images/images.png");
			} else {
				$("#light4").attr("src","static/images/images2.png");
			};
		}
	}
}