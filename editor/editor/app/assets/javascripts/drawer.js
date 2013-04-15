// For the Drawer
jQuery(document).ready(function($){
	$(document).ready(function() {
		$('#panelHandle').hover(function() {
			$('#sidePanel').stop(true, false).animate({
				'left': '0px'
			}, 900);
		}, function() {
			jQuery.noConflict();
		});

		jQuery('#sidePanel').hover(function() {
            // Do nothing
        }, function() {

        	jQuery.noConflict();
        	jQuery('#sidePanel').animate({
        		left: '-447px'
        	}, 800);

        });
	});
});