$(document).ready(function(){
	$("#Submit_btn").click(function() {
		flag=true;
		if(id_company_name.value==""){
			document.getElementById('error1').innerHTML=" This field is required!";
			document.getElementById("id_company_name").style.borderColor = "#E34234";
			flag=false;
			}
		 else{
	            //flag=true;
	             $("#error1").hide();
	             document.getElementById("id_company_name").style.borderColor = "#ccc";
	           }
		if(id_address.value==""){
			document.getElementById('error2').innerHTML=" This field is required!";
			document.getElementById("id_address").style.borderColor = "#E34234";
			flag=false;
			}
		 else{
	            //flag=true;
	             $("#error2").hide();
	             document.getElementById("id_address").style.borderColor = "#ccc";
	           }
		if(id_email.value==""){
			document.getElementById('error3').innerHTML=" This field is required!";
			document.getElementById("id_email").style.borderColor = "#E34234";
			flag=false;
			}
		 else{
	            //flag=true;
	             $("#error3").hide();
	             document.getElementById("id_email").style.borderColor = "#ccc";
	           }
		if(id_person.value==""){
			document.getElementById('error5').innerHTML=" This field is required!";
			document.getElementById("id_person").style.borderColor = "#E34234";
			flag=false;
			}
		 else{
	            //flag=true;
	             $("#error5").hide();
	             document.getElementById("id_person").style.borderColor = "#ccc";
	           }
		re = /^[A-Za-z\s]+$/;
		 if(id_person.value!=""){
	      if(!re.test(id_person.value)) {
	    	  $("#error5").show();
	     document.getElementById('error5').innerHTML=" Firstname only conatin alphabets";
	     document.getElementById("id_person").style.borderColor = "#E34234";
	    flag=false;

	     }
	      }
		
		 
		 
		  var phone_val=$("#id_phone").val();
	        if  ( phone_val =='')
	        {
	                $("#error4").text("This field is required");
	                $("#id_phone").css('border-color','#E34234');
	                flag=false;
	        }
	        
	        re = /^[0-9]+$/;
	         if( phone_val!=''){
	        	// alert("phone number is not null");
	        	if(!re.test(phone_val)){
	        		$("#error4").text(" Phone no contains only digits!");
                    $("#id_phone").css('border-color','#E34234');
                   flag=false;	
	        	}
	        	else if((phone_val.charAt(0)!=0 && phone_val.length!=8)){
	        		//alert("if charAt!=0");
              	  $("#error4").show();
                   $("#error4").text("Phone no must contain 8 digits");
                   $("#id_phone").css('border-color','#E34234');
                   flag=false;	
	        	}
	        	else if(phone_val.charAt(0)==0 && phone_val.length!=10){
	        		
	        		//alert("if charAt==0");
                    
               	 $("#error4").show();
                    $("#error4").text("Phone no must 10 digit");
                    $("#id_phone").css('border-color','#E34234');
                    flag=false;
	        	}
	        	else{
	        		//alert("else");
	        		 $("#error4").text("");
                     $("#id_phone").css('border-color','#ccc');
	        	}
	        }
	       
	      
	      
	      //  alert(flag);
		return flag;		
	});
});