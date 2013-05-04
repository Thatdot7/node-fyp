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
			var data = JSON.parse(event.data);
			if(data.method == "1"){
				id_tag = "#at_" + data.id;
				$(id_tag).remove();
				return;
			}
			
			if(data.method == "2"){
				id_tag = ".cron_" + data.name;
				console.log(id_tag);
				$(id_tag).remove();
				return;
			}
				
			plugs = data.plugs;
			if (plugs.charAt(0) == "0"){
				var plugs1 = "Off";
			} else {
				var plugs1 = "On";
			}
			if (plugs.charAt(1) == "0"){
				var plugs2 = "Off";
			} else {
				var plugs2 = "On";
			}
			if (plugs.charAt(2) == "0"){
				var plugs3 = "Off";
			} else {
				var plugs3 = "On";
			}
			if (plugs.charAt(3) == "0"){
				var plugs4 = "Off";
			} else {
				var plugs4 = "On";
			}
			var hours = data.hours;
			var minutes = data.minutes;
			var name = data.name;
			while (name.indexOf("_") > -1) {
				name = name.replace("_", " ");
			}
				
			if(data.method == "0"){
				id = data.id;
				var node = '<li class="at_' + id + '"><a href="#">'+
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
			
			if(data.method == "3"){
				dow = new String();
				if (data.dow.charAt(0) == "1"){
					dow = dow + ' Sun';
				}
				if (data.dow.charAt(1) == "1"){
					dow = dow + ' Mon';
				}
				if (data.dow.charAt(2) == "1"){
					dow = dow + ' Tue';
				}
				if (data.dow.charAt(3) == "1"){
					dow = dow + ' Wed';
				}
				if (data.dow.charAt(4) == "1"){
					dow = dow + ' Thu';
				}
				if (data.dow.charAt(5) == "1"){
					dow = dow + ' Fri';
				}
				if (data.dow.charAt(6) == "1"){
					dow = dow + ' Sat';
				}
				var node = '<li class="cron_' + data.name +'"><a href="#">' +
						'<h2>'+ name +'</h2>' +
						'<p>Plug 1: '+ plugs1 +'&nbsp&nbsp&nbsp&nbsp&nbsp' +
						'Plug 2: '+ plugs2 +'</p>' +
						'<p>Plug 3: '+ plugs3 +'&nbsp&nbsp&nbsp&nbsp&nbsp' +
						'Plug 4: '+ plugs4 +'</p>' +
						'<p>Scheduled for '+ hours +':'+ minutes +'</p>' +
						'<p>Repeat on:'+ dow +'</p></a>' +
						'<a href="#" data-id=' + data.name + ' class="cron_delete"></a>';
				$('#cron_list').prepend(node).listview('refresh');
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
		var message_json = {"method" : "1",
				"id":id};
		SocketHandler.socket.send(JSON.stringify(message_json));
	});
	$("#cron_list").on('click', '.cron_delete', function() {
		id = $(this).data("id");
		var message_json = {"method" : "2",
				"name":id};
		SocketHandler.socket.send(JSON.stringify(message_json));
	});
	$("#save").on('click', function() {
		var name = $("#text-1").val();
		name = name.replace(/[^\w\s.-:]/gi,"");
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
				
			var message_json = {"method" : "3",
					"plugs" : plugs,
					"hours" : hours, 
					"minutes" : minutes,
					"dow" : dow,
					"name" : name};
			SocketHandler.socket.send(JSON.stringify(message_json));
			//SocketHandler.socket.send("3"+plugs+hours+minutes+dow+name);
		} else {
			var message_json = {"method" : "0",
					"plugs" : plugs,
					"hours" : hours, 
					"minutes" : minutes,
					"name" : name};
			SocketHandler.socket.send(JSON.stringify(message_json))
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

