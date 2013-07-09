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
});