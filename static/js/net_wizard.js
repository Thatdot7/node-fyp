$(document).ready(function() {
	$(".connect").on('click', function(){
		$(this).button('loading');
		var id_tag = $(this).parents(".accordion-body").attr("id");
		id_tag = id_tag.split("-");
		
		if(id_tag[0] == "saved"){
			$.post('wifiwizard', {net_cat: id_tag[0], id: id_tag[1]}
			).done(function(data){
				location.reload();
				//console.log(data);
			});
		}
	});
});