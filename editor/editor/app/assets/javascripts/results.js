var x;
jQuery(document).ready(function($){
	$("#viewHtml").change(function(){

		if(this.checked) 
		{
			// alert("set");
			$('#resultContent').empty().append(x);
		}
		else
		{
			// alert("unset");
			x = $('#resultContent').html();
			$('#resultContent').html($('#resultContent').text());
		}
	});
});