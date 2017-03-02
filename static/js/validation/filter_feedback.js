$(document).ready(function(){	
	
	//alert("hiiiiii");
	
	$("#id_feedback_date_0").click(function() {	
		$("#id_month").prop('disabled', true);
	});
	$("#id_feedback_date_1").click(function() {	
		$("#id_month").prop('disabled', true);
	});
	$("#id_month").click(function() {	
		$("#id_feedback_date_0").prop('disabled', true);
		$("#id_feedback_date_1").prop('disabled', true);
	});
	
	
	 $('#feedback_filter').on('click', function () {
		//alert("close button clicked");
			$("#id_feedback_date_0").prop('disabled', false);
			$("#id_feedback_date_1").prop('disabled', false);
			$("#id_month").prop('disabled', false);
		  })
		
});
