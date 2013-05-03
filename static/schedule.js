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
			
			if(data.charAt(0) == "0"){
				data = data.split("%&^");
				console.log(data);
				id = data[1];
				data = data[0];
				if (data.charAt(1) == "0"){
					var plugs1 = "Off";
				} else {
					var plugs1 = "On";
				}
				if (data.charAt(2) == "0"){
					var plugs2 = "Off";
				} else {
					var plugs2 = "On";
				}
				if (data.charAt(3) == "0"){
					var plugs3 = "Off";
				} else {
					var plugs3 = "On";
				}
				if (data.charAt(4) == "0"){
					var plugs4 = "Off";
				} else {
					var plugs4 = "On";
				}
				var hours = data.substr(5,2);
				var minutes = data.substr(7,2);
				var name = data.substr(9);
				var node = '<li id="at_' + id + '"><a href="#">'+
								'<h2>' + name + '</h2>'+
								'<p>Id: ' + id + '</p>' +
								'<p>Plug 1: '+ plugs1 +'&nbsp&nbsp&nbsp&nbsp&nbsp' +
								'Plug 2: '+ plugs2 +'</p>' +
								'<p>Plug 3: '+ plugs3 +'&nbsp&nbsp&nbsp&nbsp&nbsp'+
								'Plug 4: '+ plugs4 +'</p>'+
								'<p>Scheduled for '+ hours +':'+ minutes +'</p></a>'+
								'<a href="#" data-id='+id+' class="at_delete"></a>'+
							'</li>';
				$('#at_list').prepend(node).listview('refresh');
			}
			
		}
	}
}

$(document).ready(function() {
	SocketHandler.start();
	console.log("Javascript reloaded");
	$("#repeat").on('click', function() {
		$("#days_repeat").show();
		console.log("Repeat Clicked");
	});
	$("#once-off").on('click', function() {
		$("#days_repeat").hide();
		console.log("Once-off clicked");
	});
	$("#at_list").on('click', '.at_delete', function() {
		id = $(this).data("id");
		message_string = "1" + id;
		console.log(message_string);
		SocketHandler.socket.send(message_string);
	});
	$("#save").on('click', function() {
		var name = $("#text-1").val();
		plugs = new String();
		if ($('#plug1').is(':checked')){
			plugs = plugs + "1";
		} else {
			plugs = plugs + "0";
		}
		if ($('#plug2').is(':checked')){
			plugs = plugs + "1";
		} else {
			plugs = plugs + "0";
		}
		if ($('#plug3').is(':checked')){
			plugs = plugs + "1";
		} else {
			plugs = plugs + "0";
		}
		if ($('#plug4').is(':checked')){
			plugs = plugs + "1";
		} else {
			plugs = plugs + "0";
		}
		var hours = $("#hours").val();
		var minutes = $("#minutes").val();
		hours = ("0" + hours).slice(-2);
		minutes = ("0" + minutes).slice(-2);
		if ($('#repeat').is(':checked')){
				dow = new String();
				if ($('#sunday').is(':checked')){
					dow = dow + "1";
				} else {
					dow = dow + "0";
				}
				if ($('#monday').is(':checked')){
					dow = dow + "1";
				} else {
					dow = dow + "0";
				}
				if ($('#tuesday').is(':checked')){
					dow = dow + "1";
				} else {
					dow = dow + "0";
				}
				if ($('#wednesday').is(':checked')){
					dow = dow + "1";
				} else {
					dow = dow + "0";
				}
				if ($('#thursday').is(':checked')){
					dow = dow + "1";
				} else {
					dow = dow + "0";
				}
				if ($('#friday').is(':checked')){
					dow = dow + "1";
				} else {
					dow = dow + "0";
				}
				if ($('#saturday').is(':checked')){
					dow = dow + "1";
				} else {
					dow = dow + "0";
				}
			SocketHandler.socket.send("3"+plugs+hours+minutes+dow+name);
		} else {
			SocketHandler.socket.send("0"+plugs+hours+minutes+name)
		}
		$('#popupDialog').hide();
	});
	$("#show_dialog").on('click', function(){
		$('#popupDialog').show();
	});
	$("#nav-bar").on('click', function(){
		if (!($(this).hasClass("ui-state-persist"))){
			SocketHandler.socket.close();
			console.log("webpage closing");
			
		}
	});
	$("#debug").on('click', function(){
		SocketHandler.socket.send("debug1")
	});
});

