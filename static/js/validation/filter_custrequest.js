$(document).ready(function(){	
	
	//alert("hiiiiii");
	
	$("#id_date_request_0").click(function() {	
		$("#id_month").prop('disabled', true);
	});
	$("#id_date_request_1").click(function() {	
		$("#id_month").prop('disabled', true);
	});
	$("#id_month").click(function() {	
		$("#id_date_request_0").prop('disabled', true);
		$("#id_date_request_1").prop('disabled', true);
	});
	
	
	/*$("#cust_filter").click(function() {	
		alert("close button clicked");
		$("#id_date_request_0").prop('disabled', false);
		$("#id_date_request_1").prop('disabled', false);
		$("#id_month").prop('disabled', false);
	});*/
	 $('#cust_filter').on('click', function () {
		// alert("close button clicked");
			$("#id_date_request_0").prop('disabled', false);
			$("#id_date_request_1").prop('disabled', false);
			$("#id_month").prop('disabled', false);
		  })
		
});
