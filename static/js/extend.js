$(document).ready(function(){
	$("#extend-enable").change(function(){
		if(this.checked){
			$("#dhcp").show();
			$("input[type=text], input[type=password], select").prop('disabled', false);
		} else {
			$("#dhcp").hide();
			$("input[type=text], input[type=password], select").attr('disabled', true);
		}
	});
});