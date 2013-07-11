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
				id_tag = ".at_" + data.id;
				$(id_tag).remove();
				return;
			}
			
			if(data.method == "2"){
				id_tag = ".cron_" + data.name.replace(" ","_");
				console.log(id_tag);
				$(id_tag).remove();
				return;
			}
				
			plugs = data.plugs;
			if (plugs.charAt(0) == "0"){
				var plugs1 = "Off";
			} else if (plugs.charAt(0) == "2") {
				var plugs1 = "Ignore";
			} else {
				var plugs1 = "On";
			}
			if (plugs.charAt(1) == "0"){
				var plugs2 = "Off";
			} else if (plugs.charAt(1) == "2") {
				var plugs2 = "Ignore";
			} else {
				var plugs2 = "On";
			}
			if (plugs.charAt(2) == "0"){
				var plugs3 = "Off";
			} else if (plugs.charAt(2) == "2") {
				var plugs3 = "Ignore";
			} else {
				var plugs3 = "On";
			}
			if (plugs.charAt(3) == "0"){
				var plugs4 = "Off";
			} else if (plugs.charAt(3) == "2") {
				var plugs4 = "Ignore";
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
				var node = '<tr class="at_' + id + '">' +
								'<td class="task-info">' +
									'<h4>' + name + '</h4>' +
										'<p>Id: ' + id + '</p>' +
										'<p><small>' +
											'Plug 1: ' + plugs1 + '&nbsp&nbsp&nbsp&nbsp&nbsp' +
											'Plug 2: ' + plugs2 +
									'</small></p>' +
									'<p><small>' +
										'Plug 3: ' + plugs3 + '&nbsp&nbsp&nbsp&nbsp&nbsp' +
										'Plug 4: ' + plugs4 +
									'</p></small>' +
									'<p>Scheduled for ' + hours + ':' + minutes + '</p>' +
								'</td>' +
								'<td width="40px" height="159px">' +
									'<button data-id=' + id + ' class="btn-danger btn-delete at_delete">' +
										'<span class="icon-remove"></span>' +
									'</button>' +
								'</td>' +
							'</tr>';
							
				$('#at_list').prepend(node);
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
				var node = '<tr class="cron_' + data.name + '">' +
								'<td class="task-info">' +
									'<h4>' + name + '</h4>' +
										'<p><small>' +
											'Plug 1: ' + plugs1 + '&nbsp&nbsp&nbsp&nbsp&nbsp' +
											'Plug 2: ' + plugs2 +
									'</small></p>' +
									'<p><small>' +
										'Plug 3: ' + plugs3 + '&nbsp&nbsp&nbsp&nbsp&nbsp' +
										'Plug 4: ' + plugs4 +
									'</small></p>' +
									'<p>Scheduled for ' + hours + ':' + minutes + '</p>' +
									'<p>Repeat on:'+ dow +'</p>' +
								'</td>' +
								'<td width="40px" height="159px">' +
									'<button data-id=' + data.name + ' class="btn-danger btn-delete cron_delete">' +
										'<span class="icon-remove"></span>' +
									'</button>' +
								'</td>' +
							'</tr>';
							
				$('#cron_list').prepend(node);
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
		if(!name){
			$("#name-error").show();
			$("#name-error").alert();
			return;
		}
		name = name.replace(/[^\w\s.-:]/gi,"");
		plugs = new String();
		if ($('#plug1').hasClass('on-state')){
			plugs = plugs + "1";
		} else if ($('#plug1').hasClass('ignore-state')){
			plugs = plugs + "2";
		} else {
			plugs = plugs + "0";
		}
		if ($('#plug2').hasClass('on-state')){
			plugs = plugs + "1";
		} else if ($('#plug2').hasClass('ignore-state')){
			plugs = plugs + "2";
		} else {
			plugs = plugs + "0";
		}
		if ($('#plug3').hasClass('on-state')){
			plugs = plugs + "1";
		} else if ($('#plug3').hasClass('ignore-state')){
			plugs = plugs + "2";
		} else {
			plugs = plugs + "0";
		}
		if ($('#plug4').hasClass('on-state')){
			plugs = plugs + "1";
		} else if ($('#plug4').hasClass('ignore-state')){
			plugs = plugs + "2";
		} else {
			plugs = plugs + "0";
		}
		var hours = $("#hours").val();
		var minutes = $("#minutes").val();
		hours = ("0" + hours).slice(-2);
		minutes = ("0" + minutes).slice(-2);
		if ($('#repeat').is(':checked')){
			dow = "0000000";
			if(!$("#dow").val()){
				$("#dow-error").show();
				$("#dow-error").alert();
				return;
			}
			$.each($("#dow").val(), function(){
				dow = dow.substring(0,this)+'1'+dow.substring(parseInt(this) + 1);
			});
			
			
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
		$("#task-creator").collapse('hide');
		$("#task-success").show();
		$("#task-success").alert();
	});

	$("#debug").on('click', function(){
		SocketHandler.socket.send("debug1")
	});
	
	$("#plug1,#plug2,#plug3,#plug4").on('click', function(){
		if ($(this).hasClass("on-state")){
			$(this).removeClass("on-state btn-success");
			$(this).addClass("ignore-state btn-warning");
		} else if ($(this).hasClass("ignore-state")){
			$(this).removeClass("ignore-state btn-warning");
			$(this).addClass("btn-danger");
		} else {
			$(this).removeClass("btn-danger");
			$(this).addClass("on-state btn-success");
		}
	});
});

