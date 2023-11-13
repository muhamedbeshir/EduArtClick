$(function() {
	$("#datepicker").datepicker({    
	        dateFormat: 'yy-mm-dd',
	        beforeShowDay: function(date) {
	        var day = date.getDay();
	        return [(day == 0), ''];
	        
	        }
	        
	    });
	});
