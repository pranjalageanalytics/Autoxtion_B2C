$(document).ready(function(){
	
	$("#promo").click(function() {
		

		flag=true;
		if(id_service_type.value==""){
			document.getElementById('error1').innerHTML=" This field is required!";
			flag=false;
			
			
		}
		if(id_feedback.value==""){
			document.getElementById('error2').innerHTML=" This field is required!";
			flag=false;
		}
		
		
        return flag;		
		
	});
});