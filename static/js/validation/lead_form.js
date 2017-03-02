$(document).ready(function(){	
	
	//alert("hiiiiii");
	
	$("#promo").click(function() {
		  
		  var a=$("#id_form-0-reg_expiry_date").val();
		 //alert(a);
		  var today = new Date();
		 // alert("tredfghj"+today);
		  var dd = today.getDate();
		  var mm = today.getMonth(); //January is 0!
		  var yyyy = today.getFullYear();

		  if(dd<10) {
		      dd='0'+dd
		  } 
		 
		  if(mm<10) {
		      mm='0'+mm
		  } 
		  
      // new Date(dd/mm/yyyy)
		var today1 = dd+'/'+mm+'/'+yyyy;
		var d100=new Date(yyyy,mm,dd);
		 //alert("d100="+d100);
		  var dd6 = d100.getDate();
		  //alert(dd6);
		  var mm6 = d100.getMonth()+1; //January is 0!
		 // alert(mm6);
		  var yyyy6 = d100.getFullYear();
		 // alert(yyyy6);
		//alert("d100------"+d100);
		  
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
		  var d101=new Date(yyyy1,mm1,dd1);
		  //alert("d101----------------------"+d101);
		
		  
		$("#id_name").attr("class","form-control");
		$("#id_address").attr("class","form-control");
		$("#id_licenseid").attr("class","form-control");
		$("#id_email").attr("class","form-control");
		$("#id_phone").attr("class","form-control");
		$("#id_form-0-reg_expiry_date").attr("class","form-control");
		//$("#id_form-0-vehicle_no").attr("class","form-control");
		
		
		flag=true;
		 
		
		/* if (!$("input[name='customer1']:checked").val()) {
	         alert('Nothing is checked!');
	         document.getElementById('err3').innerHTML=" Please select valid option!";
	         document.getElementById("chasis_no").style.borderColor = "#E34234";
	          return false;
	      }
	      else {
	       $("#err3").hide();
	       document.getElementById("chasis_no").style.borderColor = "#ccc";
	        //alert('One of the radio buttons is checked!');
	       // document.getElementById('error3').innerHTML="One of the radio buttons is checked!";
	      }*/
	
		
		if(id_last_name.value==""){
			//alert("name");
			document.getElementById('error25').innerHTML=" This field is required";
		     document.getElementById("id_last_name").style.borderColor = "#E34234";

			flag=false;
			
			
		}
		re = /^[A-Za-z\s]+$/;
		 if(id_last_name.value!=""){
	      if(!re.test(id_last_name.value)) {

	     document.getElementById('error25').innerHTML=" Lastname only contain alphabets";
	     document.getElementById("id_last_name").style.borderColor = "#E34234";
	    flag=false;

	     }
	      else{
	    	  $('#error25').hide();
	            document.getElementById("id_last_name").style.borderColor = "#ccc";
	      }
	      }
		
		
		
		
		if(id_name.value==""){
			//alert("name");
			document.getElementById('error1').innerHTML=" This field is required!";
		     document.getElementById("id_name").style.borderColor = "#E34234";

			flag=false;
			
			
		}
		
		re = /^[A-Za-z\s]+$/;
		 if(id_name.value!=""){
	      if(!re.test(id_name.value)) {

	     document.getElementById('error1').innerHTML=" Firstname only contain alphabets";
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
	
		  var area_val=$("#id_area_code").val();
          
       
       
          if((phone_val.length==8)&&( area_val=="")){
        //alert("ifelse ");
        $("#er").show();
             document.getElementById('er').innerHTML=" Area code can not be empty!";
             document.getElementById("id_area_code").style.borderColor = "red";
            flag=false;
            //alert("in ifelse");
          
         }
          else{
              //flag=true;
               $("#er").hide();
               document.getElementById("id_area_code").style.borderColor = "#ccc";
             }
               
                    re = /^[0-9]+$/;
                     if(area_val!=""){
                      if(!re.test(area_val)) {
                       //$("#error001").show();
                       $("#er").text(" Area code contain only digits");
                     document.getElementById("id_area_code").style.borderColor = "#E34234";
                    flag=false;
                     //alert("in fname if "+flag);
                     
                          }
                    else{
                      //flag=true;
                       $("#er").hide();
                       document.getElementById("id_area_code").style.borderColor = "#ccc";
                     }
                  if ((area_val.length!=2 )){
                            
                             
                            // alert("if charAt!=0");
                              $("#er").show();
                              document.getElementById('er').innerHTML=" Area code must contain 2 digit";
                      document.getElementById("id_area_code").style.borderColor = "#E34234";
                     flag=false;
                               
                            }
                  if ((phone_val.length==10)){
                   
                   $("#er").show();
                      document.getElementById('error5').innerHTML="Phone no must contain 8 digits !";
                      document.getElementById("id_phone").style.borderColor = "red";
                     flag=false;
                     //alert("in ifelse");
                   
                  }
                  
                  }
		 if($("#id_form-0-vehicle_no").val().length==""){
			 $("#errors").show();
			// alert("vehno");
	            document.getElementById('errors').innerHTML="This field is required!";
	   document.getElementById("id_form-0-vehicle_no").style.borderColor = "#E34234";
	    flag=false;
	    }
		 else{
			// flag=true;
	    $("#errors").hide();
	    document.getElementById("id_form-0-vehicle_no").style.borderColor = "#ccc";
	    }
		 if(d101<d100){
			 document.getElementById('error6').innerHTML="Registration Expiry date can not be less than Today's Date!";
				$("#error6").show();
			    document.getElementById("id_form-0-reg_expiry_date").style.borderColor = "#E34234";
			    flag=false;
		 }
		  else{

			  $("#error6").hide();
			  document.getElementById("id_form-0-reg_expiry_date").style.borderColor = "#ccc";
		 }

		/*if(a!="" && a<today1){
			//alert("date");
			document.getElementById('error6').innerHTML="Registration Expiry date can not be less than Today's Date!";
			$("#error6").show();
		    document.getElementById("id_form-0-reg_expiry_date").style.borderColor = "#E34234";
		    flag=false;
		}
		else{
			
			  $("#error6").hide();
			  document.getElementById("id_form-0-reg_expiry_date").style.borderColor = "#ccc";
		}*/
		  var vin_no=$("#id_form-0-vin_no").val();
		 // alert(vin_no);
		
	 			if(vin_no!= "") {
				
		        if(vin_no.length < 17) {
		        	//console.log("length is less");
		    document.getElementById('err9').innerHTML=" Vin number must contain  seventeen characters and number!";
		    document.getElementById("id_form-0-vin_no").style.borderColor = "#E34234";
		      // document.getElementById("pass2").style.borderColor = "#E34234";
		          
		          flag=false;
		        }
		        
		        
		        else if(!(re = /[0-9]/).test(vin_no)) {
		        	//console.log("Number");
		        	 $("#err9").show();
		       document.getElementById('err9').innerHTML=" Vin number must contain at least one number (0-9)!";
		    document.getElementById("id_form-0-vin_no").style.borderColor = "#E34234";
		    //document.getElementById("pass2").style.borderColor = "#E34234";
		          
		          flag=false;
		        }
		        
		        else if(!(re = /[A-Za-z]/).test(vin_no)) {
		        	//console.log("lowercase");
		        	 $("#err9").show();
		       document.getElementById('err9').innerHTML=" Vin number must contain at least one character!";
		    document.getElementById("id_form-0-vin_no").style.borderColor = "#E34234";
		          
		          flag=false;
		        }
		          else if(re = /[({<_\-!\"@;,.:#$%*^&+=?'|?> })]/.test(vin_no)) {
		        	//console.log("special char");
		        	 $("#err9").show();
		    document.getElementById('err9').innerHTML=" Vin number will not allow special character!";
		    document.getElementById("id_form-0-vin_no").style.borderColor = "#E34234";
		          
		          flag=false;
		        }
		      /*  else if((re = /[a-z]/).test(vin_no)) {
		        	console.log("lowercase");
		       document.getElementById('err9').innerHTML=" Vin number will not allow  lowercase letter (a-z)!";
		    document.getElementById("id_form-0-vin_no").style.borderColor = "#E34234";
		          
		          flag=false;
		        }*/
	 			 else {
	 			//	 alert("in else");
	 				 // flag=true;
	 			   $("#err9").hide();
	 		  	  document.getElementById("id_form-0-vin_no").style.borderColor = "#ccc";
	 		 }
	 			 
	 		 }
				  var c=$("#id_form-0-chasis_no").val();
				  //alert(c);
	
		 		  re = /^[0-9]+$/;
		 		 if(c!=""){
		 			  //alert("in c");
		 			  if (!re.test(c)){
		 				  $("#err10").show();
		 					document.getElementById('err10').innerHTML=" Enter valid Chasis No !";
			 			     document.getElementById("id_form-0-chasis_no").style.borderColor = "#E34234";
	
			 				flag=false;
			 			}
		 			  else if($("#id_form-0-chasis_no").val().length!=6){
	 				 $("#err10").show();
	 				  //alert("in length");
	 				 document.getElementById('err10').innerHTML=" Chasis No must be 6 digit long!";
	 			     document.getElementById("id_form-0-chasis_no").style.borderColor = "#E34234";

	 				flag=false;
	 			  }
		 		 
		 		 else {
		 				// alert("in else");
		 				 // flag=true;
		 			   $("#err10").hide();
		 		  	  document.getElementById("id_form-0-chasis_no").style.borderColor = "#ccc";
		 		 }
		 			   
		 		 
		 		 }
	 		  
	 		
	 		 
	 		if (flag)
			{
	 			lead_form.submit();
			}
		// alert("flag"+flag);
	       return flag;
});
});