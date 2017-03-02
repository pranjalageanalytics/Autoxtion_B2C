$(document).ready(function(){
	//alert("hiiiii");
	$("#send1").click(function() {
		flag=true;	
		if (name_id1.value == '')
		{
			//alert("hello");
			document.getElementById('send_name1').innerHTML=" This field is required!";
			 document.getElementById("name_id1").style.borderColor = "#E34234";
			 flag=false;
			}
		   re = /^[A-Za-z\s]+$/;
	        if(name_id1.value!=""){
	            if(!re.test(name_id1.value)) {
	             $("#send_name1").show();
	           document.getElementById('send_name1').innerHTML=" Name only conatin alphabets";
	           document.getElementById("name_id1").style.borderColor = "#E34234";
	          flag=false;
	  //        	alert("in fname if "+flag);
	           
	                }
		else {
			  	  $("#send_name1").hide();
			  	  document.getElementById("name_id1").style.borderColor = "#ccc";
		}
	        }
		if (email1.value == '')
		{
		//	alert("in email1");
			document.getElementById('send_error1').innerHTML=" This field is required!";
			 document.getElementById("email1").style.borderColor = "#E34234";
			 flag=false;
			}
		else {
			  	  $("#send_error1").hide();
			  	  document.getElementById("email1").style.borderColor = "#ccc";
		}
		if(email1.value != ''){
			var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;	
			 if (reg.test(email1.value) == false)
				 {
				  document.getElementById('send_error1').innerHTML=" Invalid Email Id!";
				  document.getElementById("email1").style.borderColor = "#E34234";
				  flag=false;
				 }
			 else{
				 $("#send_error1").hide();
			  	  document.getElementById("email1").style.borderColor = "#ccc";
			 }
		}
		//alert("flag"+flag);
		return flag;
	});
});