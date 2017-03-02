$(document).ready(function(){
	
	
	
	$("#old_password").change(function(){
		flag=true;
		console.log('on key up event of pass2');
		 if(old_password.value==""){
				document.getElementById('errs').innerHTML=" This field is required!";
		    	  document.getElementById("old_password").style.borderColor = "#E34234";

				flag=false;
				//alert(pass2.value);
				}
		if (old_password.value != "" && old_password.value == new_password.value) {
	        
	    	   document.getElementById('errs').innerHTML="Old password & new passsword are same!";
	    	   //document.getElementById("pass1").style.borderColor = "#E34234";
	    	   document.getElementById("old_password").style.borderColor = "#E34234";
	    	   flag=false;
	    	    }
		else
    	{
			document.getElementById('errs').innerHTML=" ";
			document.getElementById("old_password").style.borderColor = "#ccc";
    	}
		return flag;
});
	
	
	$("#confirm_password").change(function(){
		flag=true;
		console.log('on key up event of pass2');
		 if(confirm_password.value==""){
				document.getElementById('qwerty').innerHTML=" This field is required!";
		    	  document.getElementById("confirm_password").style.borderColor = "#E34234";

				flag=false;
				//alert(pass2.value);
				}
		if (confirm_password.value!=new_password.value) {
	        
	    	   document.getElementById('qwerty').innerHTML=" Password and confirm password must be same!";
	    	   //document.getElementById("pass1").style.borderColor = "#E34234";
	    	   document.getElementById("confirm_password").style.borderColor = "#E34234";
	    	   flag=false;
	    	    }
		else
    	{
			document.getElementById('qwerty').innerHTML=" ";
			document.getElementById("confirm_password").style.borderColor = "#ccc";
    	}
		return flag;
});
	$("#new_password").change(function(){
		console.log('on key up event of pass1');
		flag=true;
		if(new_password.value==""){
			document.getElementById('err1').innerHTML=" This field is required!";
	    	  document.getElementById("new_password").style.borderColor = "#E34234";

			flag=false;
			//alert(pass1.value);
			}
		/*if(new_password.value != "") {
			
	        if(new_password.value.length < 8) {
	        	console.log("length is less");
	    document.getElementById('err1').innerHTML=" Password must contain at least Eight characters!";
	    document.getElementById("new_password").style.borderColor = "#E34234";
	      // document.getElementById("pass2").style.borderColor = "#E34234";
	          
	          flag=false;
	        }
	        
	        
	        else if(!(re = /[0-9]/).test(new_password.value)) {
	        	console.log("Number");
	       document.getElementById('err1').innerHTML=" password must contain at least one number (0-9)!";
	    document.getElementById("new_password").style.borderColor = "#E34234";
	    //document.getElementById("pass2").style.borderColor = "#E34234";
	          
	          flag=false;
	        }
	        
	        else if(!(re = /[a-z]/).test(new_password.value)) {
	        	console.log("lowercase");
	       document.getElementById('err1').innerHTML=" password must contain at least one lowercase letter (a-z)!";
	    document.getElementById("new_password").style.borderColor = "#E34234";
	          
	          flag=false;
	        }
	        
	        else if(!(re = /[A-Z]/).test(new_password.value)) {
	        	console.log("uppercase");
	    document.getElementById('error5').innerHTML=" password must contain at least one uppercase letter (A-Z)!";
	    document.getElementById("new_password").style.borderColor = "#E34234";
	          
	          flag=false;
	        }
	        else if(!(re = /[_\-!\"@;,.:]/).test(new_password.value)) {
	        	console.log("special char");
	    document.getElementById('err1').innerHTML=" password must contain at least one special character!";
	    document.getElementById("new_password").style.borderColor = "#E34234";
	          
	          flag=false;
	        }*/
	        else
	        	{
	        	document.getElementById('err1').innerHTML=" ";
	    	    document.getElementById("new_password").style.borderColor = "#ccc";
	        	}
	      
	  
	    
return flag;

	});
	
	

$("#submit_frm").click(function() {
	
	 if(old_password.value==""){
			document.getElementById('errs').innerHTML=" This field is required!";
	    	  document.getElementById("old_password").style.borderColor = "#E34234";

			flag=false;
			//alert(pass2.value);
			}
	 
		if(new_password.value==""){
			document.getElementById('err1').innerHTML=" This field is required!";
	    	  document.getElementById("new_password").style.borderColor = "#E34234";

			flag=false;
			//alert(pass1.value);
			}
		 if(confirm_password.value==""){
				document.getElementById('qwerty').innerHTML=" This field is required!";
		    	  document.getElementById("confirm_password").style.borderColor = "#E34234";

				flag=false;
				//alert(pass2.value);
				}
		 return flag;
});
});