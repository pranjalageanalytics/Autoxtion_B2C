$(document).ready(function(){	
	
	
	
	$("#submit_frm").click(function() {
		  
		  var a=$("#id_reg_expiry_date").val();
		 // alert(a);
		  var b=$("#id_vin_no").val();
		  var today = new Date();
		  var dd = today.getDate();
		  var mm = today.getMonth()+1; //January is 0!
		  var yyyy = today.getFullYear();

		  if(dd<10) {
		      dd='0'+dd
		  } 
		 
		  if(mm<10) {
		      mm='0'+mm
		  } 

		  today1 = mm+'/'+dd+'/'+yyyy;
		 // var date=$("#id_form-0-reg_expiry_date").val();
		  var arr = a.split("/");
		  //alert(arr[0])
		  var dd1=arr[0];
		  //alert(arr[1])
		  var mm1= arr[1]
		  //alert(arr[2])
		  var yyyy1= arr[2]
		  date2= mm1+'/'+dd1+'/'+yyyy1;
		  //alert(date2);
		  //alert(today1);
		  
		  
		  
		$("#id_name").attr("class","form-control");
		$("#id_address").attr("class","form-control");
		$("#id_licenseid").attr("class","form-control");
		$("#id_email").attr("class","form-control");
		$("#id_phone").attr("class","form-control");
		$("#id_form-0-reg_expiry_date").attr("class","form-control");
		//$("#id_form-0-vehicle_no").attr("class","form-control");
		
		
		flag=true;
		
		
		
		if(id_name.value==""){
			//alert("name");
			document.getElementById('error1').innerHTML=" This field is required!";
		     document.getElementById("id_name").style.borderColor = "#E34234";

			flag=false;
			
			
		}
		
		re = /^[A-Za-z\s]+$/;
		 if(id_name.value!=""){
	      if(!re.test(id_name.value)) {

	     document.getElementById('error1').innerHTML=" Firstname only conatin alphabets";
	     document.getElementById("id_name").style.borderColor = "#E34234";
	    flag=false;

	     }
	      else{
	    	  $('#error1').hide();
	            document.getElementById("id_name").style.borderColor = "#ccc";
	      }
	      }
		
		if(id_address.value==""){
			//alert("adress");
			document.getElementById('error2').innerHTML=" This field is required!";
		     document.getElementById("id_address").style.borderColor = "#E34234";

			flag=false;
		}
		else{
			flag=true;
		
		
		    $('#error2').hide();
            document.getElementById("id_address").style.borderColor = "#ccc";
		}
		
		 if(id_email.value==""){
			 //alert("email");
			 document.getElementById('error4').innerHTML="This field is required";
	            document.getElementById("id_email").style.borderColor = "#E34234";
	            flag=false;
		 }
			
			var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
	        if(id_email.value!=""){
	        if (reg.test(id_email.value) == false)
	        {
	            document.getElementById('error4').innerHTML="Invalid Email ID";
	            document.getElementById("id_email").style.borderColor = "#E34234";
	            flag=false;
	        }
	        else{
	            $('#error4').hide();
	            document.getElementById("id_email").style.borderColor = "#ccc";
	        }}
	        var phone_val=$("#id_phone").val();
	        if  ( phone_val =='')
	        {
	                $("#error5").text("This field is required");
	                $("#id_phone").css('border-color','#E34234');
	                flag=false;
	        }
	        re = /^[0-9]+$/;
	         if( phone_val!=''){
	        	 //alert("phone number is not null");
	        	if(!re.test(phone_val)){
	        		$("#error5").text(" Phone no contains only digits!");
                  $("#id_phone").css('border-color','#E34234');
                 flag=false;	
	        	}
	        	else if((phone_val.charAt(0)!=0 && phone_val.length!=8)){
	        		//alert("if charAt!=0");
            	  $("#error5").show();
                 $("#error5").text("Phone no must contain 8 digits");
                 $("#id_phone").css('border-color','#E34234');
                 flag=false;	
	        	}
	        	else if(phone_val.charAt(0)==0 && phone_val.length!=10){
	        		
	        		//alert("if charAt==0");
                  
             	 $("#error5").show();
                  $("#error5").text("Phone no must 10 digit");
                  $("#id_phone").css('border-color','#E34234');
                  flag=false;
	        	}
	        	else{
	        		//alert("else");
	        		 $("#error5").text("");
                   $("#id_phone").css('border-color','#ccc');
	        	}
	        }
		/*if(id_phone.value==""){
			//alert("phone");
			document.getElementById('error5').innerHTML=" This field is required!";
		     document.getElementById("id_phone").style.borderColor = "#E34234";
			flag=false;
		}
			
		if( id_phone.value.length<10 || id_phone.value.length>10){
	    	  document.getElementById('error5').innerHTML="Phone Number must be 10 digits long";
	    	  document.getElementById("id_phone").style.borderColor = "#E34234";
	    	  flag=false;
	    }
		else{
			flag=true;
		
			  $("#error5").hide();
			  document.getElementById("id_phone").style.borderColor = "#ccc";
			  document.getElementById('id_phone').innerHTML="Phone Number must be 10 digits long";
			  }
		
		 */
		 
		 if($("#id_vehicle_no").val().length==""){
			 $("#errors").show();
			// alert("vehno");
	            document.getElementById('errors').innerHTML="This field is required!";
	   document.getElementById("id_vehicle_no").style.borderColor = "#E34234";
	    flag=false;
	    }
		 else{
			// flag=true;
	    $("#errors").hide();
	    document.getElementById("id_vehicle_no").style.borderColor = "#ccc";
	    }
	   		

		if(a!="" && date2<today1){
			//alert("date");
			document.getElementById('error6').innerHTML="Registration Expiry date can not be less than Today's Date!";
			$("#error6").show();
		    document.getElementById("id_form-0-reg_expiry_date").style.borderColor = "#E34234";
		    flag=false;
		}
		else{
			
			  $("#error6").hide();
			  document.getElementById("id_reg_expiry_date").style.borderColor = "#ccc";
		}
		  var re = new RegExp("^[A-HJ-NPR-Z\\d]{8}[\\dX][A-HJ-NPR-Z\\d]{2}\\d{6}$");
	 		 if (b!=""){
	 			 
	 			 if(!re.test(b)){
	 				//alert("vin no");
	 				 $("#err9").show();
	 				document.getElementById('err9').innerHTML=" Enter valid VIN NO !";
	 			     document.getElementById("id_vin_no").style.borderColor = "#E34234";

	 				flag=false;
	 			} 
	 			 else {
	 				 // flag=true;
	 			   $("#err9").hide();
	 		  	  document.getElementById("id_vin_no").style.borderColor = "#ccc";
	 		 }
	 			 
	 		 }
	 		
		 //alert("flag"+flag);
	        return flag;
});
});