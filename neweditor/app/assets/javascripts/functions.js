CodeMirror.commands.autocomplete = function(cm) {
	CodeMirror.showHint(cm, CodeMirror.pythonHint);
}

var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
	mode: {name: "swim",
	version: 2,
	singleLineStringErrors: false},
	keyMap: "emacs",
	lineNumbers: true,
	lineWrapping: true,
	autoCloseBrackets: true,
	enableSearchTools: true,
	enableCodeFolding: true,
	enableCodeFormatting: true,
	autoFormatOnStart: true,
	extraKeys: {"Ctrl-Space": "autocomplete"},
	indentWithTabs: true
});


editor.setOption("theme", "ambiance-light");
var input = document.getElementById("select");
function selectTheme() {
	var theme = input.options[input.selectedIndex].innerHTML;
	editor.setOption("theme", theme);
}


var choice = document.location.search &&
decodeURIComponent(document.location.search.slice(1));
if (choice) {
	input.value = choice;
	editor.setOption("theme", choice);
}


function sendCommand(){
	var command = editor.getValue();
	$("#stuff").fadeOut('1000');
	$.ajax({
		url: "code",
		type: "GET",
		async : false,
		data:{token: command},
		dataType:"text",
	}).done(function(html) {
		$('#stuff').empty();
		$('#stuff').html("<div class=\"container-fluid\"><div class=\"row-fluid\"><div class=\"span10 offset1\">"+html+"</div></div></div>")
	});
	$("#stuff").fadeIn();
}




$('#goButton').click(function(e) {
	e.preventDefault(); 
	var href = $(this).attr("href");

	// $.ajax({
	// 	url : href,
	// 	type : GET,
	// 	success : function(data){
	// 		wrapper.html(data);
	// 	}
	// });                


var command = editor.getValue();
$("#stuff").fadeOut('1000');
$.ajax({
	url: href,
	type: "GET",
	async : false,
	data:{token: command},
	dataType:"text",
}).done(function(html) {
	$('#stuff').empty();
	$('#stuff').html("<div class=\"container-fluid\"><div class=\"row-fluid\"><div class=\"span10 offset1\">"+html+"</div></div></div>")
});
$("#stuff").fadeIn();
history.pushState('', 'New URL: '+href, href);

});





window.onpopstate = function(event) {
	if(event.state === ''){
		var href = location.pathname,
		wrapper = $("#stuff");
		$.ajax({
			url : "index",
           type : GET,
           success : function(data){
                wrapper.html(data);
           }
		});
	}
};









window.addEventListener('load', initSlider, false);
/**
* Initializes sliders
*/
function initSlider(){
	    // get range input
	    var fontRange = document.getElementById("fontRange");
	    fontRange.addEventListener('change', function(){
	    	s = fontRange.value;
	    	$('.CodeMirror').css({"font-size":s+"px"});
			m = $('.CodeMirror').css("font-size"); //Without this the editor refresh won't work.  
			editor.refresh();
		});
	} 


	function wipeEditor(){
		editor.setValue("#include std;" + 
			"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"+
			"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"+
			"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
	}



	function loadProgram(progr){
		$.ajax({
			url : "samples/"+progr,
			dataType: "text",
			success : function (data) {
				editor.setValue(data);
			}
		});
	}




	$(document).ready(function() {
		loadProgram('fibonacci');
	});














