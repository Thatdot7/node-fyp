$(document).ready(function(){
	$("#extend-enable").change(function(){
		if(this.checked){
			$("#dhcp-group").show();
			$("input[type=text], #pass-proc, input[type=password], select").prop('disabled', false);
		} else {
			$("#dhcp-group").hide();
			$("input[type=text], #pass-proc, input[type=password], select").attr('disabled', true);
		}
	});
	$("#pass-proc").change(function(){
		if(this.checked){
			$("input[type=password], #pass-type").prop('disabled', false);
		} else {
			$("input[type=password], #pass-type").prop('disabled', true);
		}
	});
	$("#save").on('click', function(){
		var message_json = {"enable" : $("#extend-enable").prop('checked'),
				"ssid" : $("#ssid").val(),
				"channel" : $("#channel").val(),
				"pass-proc" : $("#pass-proc").prop('checked'),
				"WPA" : $("#pass-type").val(),
				"psk" : $("#pass").val(),
				"router" : $("#address-1").val() + "." + $("#address-2").val() + "." + $("#address-3").val() + "." + $("#address-4").val(),
				"start" : $("#start-1").val() + "." + $("#start-2").val() + "." + $("#start-3").val() + "." + $("#start-4").val(),
				"end" : $("#end-1").val() + "." + $("#end-2").val() + "." + $("#end-3").val() + "." + $("#end-4").val(),
				"netmask" : $("#mask-1").val() + "." + $("#mask-2").val() + "." + $("#mask-3").val() + "." + $("#mask-4").val()}

		console.log(message_json);
		$.post('extend', message_json
		).done(function(data){
			//location.reload();
			console.log(data);
		});
	});
});