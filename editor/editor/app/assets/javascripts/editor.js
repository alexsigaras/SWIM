jQuery(document).ready(function($){
//editor setup
var editor = ace.edit("editor");
editor.setTheme("ace/theme/textmate");
editor.getSession().setMode("ace/mode/python");
editor.gotoLine(2);
editor.setShowInvisibles(true);

$("#results").click(function() {
	$('#token').val(editor.getValue());
	alert($('#token').val());
	$('#submitme').click();
});


$("#clear").click(function() {
	editor.setValue("#Swim language webscraping language\n");
	editor.gotoLine(2);
});


//editor styling and sizing
$("#editor").height($(window).height()*.95);
$("#editor").width($(window).width()*.88);
editor.resize()



$(window).resize(function(){
	$("#editor").height($(window).height()*.95);
	$("#editor").width($(window).width()*.88);
	editor.resize()
});



//Changes the theme

$("#theme").change(function () {
  var str = "";
  $("#theme option:selected").each(function () {
  		a= $(this).val();
        editor.setTheme(a);
      });
})


//changes font size
$("#fontsize").change(function () {
  var str = "";
  $("#fontsize option:selected").each(function () {
  		a= $(this).val();
        document.getElementById('editor').style.fontSize=a;
      });
})



//shows hidden characters
$("#show_hidden").change(function(){

        if(this.checked) 
        {
            editor.setShowInvisibles(true);
        }
        else
        {
            editor.setShowInvisibles(false);
        }
    });





//shows indent guides 
$("#display_indent_guides").change(function(){

        if(this.checked) 
        {
            editor.setDisplayIndentGuides(true);
        }
        else
        {
            editor.setDisplayIndentGuides(false);
        }
    });


//shows highlighted words guides 
$("#highlight_selected_word").change(function(){

        if(this.checked) 
        {
            editor.setHighlightSelectedWord(true);
        }
        else
        {
            editor.setHighlightSelectedWord(false);
        }
    });

});
