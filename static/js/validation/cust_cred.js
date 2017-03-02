$(document).ready(function(){	
 
	$("#new_submit").click(function(){
		 flag=true;
		if (new_email.value == '')
		{
			document.getElementById('error_email').innerHTML=" This field is required!";
			 document.getElementById("new_email").style.borderColor = "#E34234";
	    	flag=false;
			}
		
		var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
	    if(new_email.value!=""){
	    if (reg.test(new_email.value) == false)
	    {
	        document.getElementById('error_email').innerHTML="Invalid Email ID";
	        document.getElementById("new_email").style.borderColor = "#E34234";
	        flag=false;
	    }
	    else{
	        $('#error_email').hide();
	        document.getElementById("new_email").style.borderColor = "#ccc";
	        flag=true;
	    }}
		return flag;
	});
});