$(document).ready(function(){
   //alert('hello');
	$('#lead_table').DataTable({
		responsive: {
	        details: false
	    }
	});
	
	$("#email").on('change',function(){
		//alert("on change email");
		$("#phone").attr("readonly","readonly");
	});
	
	$("#phone").on('change',function(){
		//alert("on change email");
		$("#email").attr("readonly","readonly");
	});
	
	$(".qualify").on("click",function(){
		lead_id = $(this).closest('tr').find('td:eq(0)').text();
    	$("#lead_id").val(lead_id);
    	//alert(lead_id);
		});
	$('#cls').on('click', function () {
		  // do something…
		$("#email").removeAttr("readonly");
		$("#phone").removeAttr("readonly");
		$("#name1").val("");
		$("#email").val("");
		$("#phone").val("");
		})
		
		
		
	
	  $('#countcustomer').hide();
    $("input[name='leadname2[]']").click(function(){
        if($('.checkclass').is(":checked")) {
            $('#countcustomer').show() ;
             } else {
             $('#countcustomer').hide() ;
        }
    });      
		

		
});
