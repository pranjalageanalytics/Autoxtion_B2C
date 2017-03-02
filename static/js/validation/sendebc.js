$(document).ready(function(){
	//alert("hiiiii");
	$("#send").click(function() {
		flag=true;	
		if (name_id.value == '')
		{
			//alert("hello");
			document.getElementById('send_name').innerHTML=" This field is required!";
			 document.getElementById("name_id").style.borderColor = "#E34234";
			 flag=false;
			}
		   re = /^[A-Za-z\s]+$/;
	        if(name_id.value!=""){
	            if(!re.test(name_id.value)) {
	             $("#send_name").show();
	           document.getElementById('send_name').innerHTML=" Name only conatin alphabets";
	           document.getElementById("name_id").style.borderColor = "#E34234";
	          flag=false;
	  //        	alert("in fname if "+flag);
	           
	                }
		else {
			  	  $("#send_name").hide();
			  	  document.getElementById("name_id").style.borderColor = "#ccc";
		}
	        }
		if (email.value == '')
		{
		//	alert("in email");
			document.getElementById('send_error').innerHTML=" This field is required!";
			 document.getElementById("email").style.borderColor = "#E34234";
			 flag=false;
			}
		else {
			  	  $("#send_error").hide();
			  	  document.getElementById("email").style.borderColor = "#ccc";
		}
		if(email.value != ''){
			var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;	
			 if (reg.test(email.value) == false)
				 {
				  document.getElementById('send_error').innerHTML=" Invalid Email Id!";
				  document.getElementById("email").style.borderColor = "#E34234";
				  flag=false;
				 }
			 else{
				 $("#send_error").hide();
			  	  document.getElementById("email").style.borderColor = "#ccc";
			 }
		}
		//alert("flag"+flag);
		return flag;
	});
});