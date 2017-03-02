$(document).ready(function(){
	$("#Submit_btn").click(function() {
		flag=true;
		if(id_name.value==""){
			document.getElementById('error1').innerHTML=" This field is required!";
			document.getElementById("id_name").style.borderColor = "#E34234";
			flag=false;
			}
		if(id_last_name.value==""){
			document.getElementById('error7').innerHTML=" This field is required!";
			document.getElementById("id_last_name").style.borderColor = "#E34234";
			flag=false;
			}
		if(id_address.value==""){
			document.getElementById('error2').innerHTML=" This field is required!";
			document.getElementById("id_address").style.borderColor = "#E34234";
			flag=false;
			}
		/*if(id_licenseid.value==""){
			document.getElementById('error3').innerHTML=" This field is required!";
			document.getElementById("id_licenseid").style.borderColor = "#E34234";
			flag=false;
			}*/
		if(id_email.value==""){
			document.getElementById('error4').innerHTML=" This field is required!";
			document.getElementById("id_email").style.borderColor = "#E34234";
			flag=false;
			}
		
		re = /^[A-Za-z\s]+$/;
		 if(id_name.value!=""){
	      if(!re.test(id_name.value)) {
	        
	     document.getElementById('error1').innerHTML=" Firstname only conatin alphabets";
	     document.getElementById("id_name").style.borderColor = "#E34234";
	    flag=false;

	     }
	      }
		 if(id_last_name.value!=""){
		      if(!re.test(id_last_name.value)) {
		        
		     document.getElementById('error7').innerHTML=" Lastname only conatin alphabets";
		     document.getElementById("id_last_name").style.borderColor = "#E34234";
		    flag=false;

		     }
		      }
	   
		 
		 
		  var phone_val=$("#id_phone").val();
	        if  ( phone_val =='')
	        {
	                $("#error5").text("This field is required");
	                $("#id_phone").css('border-color','#E34234');
	                flag=false;
	        }
	        
	        re = /^[0-9]+$/;
	         if( phone_val!=''){
	        	// alert("phone number is not null");
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
		        
		    	//alert ("area code");		      
		    	
		    		//alert("if");
		       /* if(( area_val=="")){
		    		//alert("ifelse ");
		    		$("#error001").show();
		           document.getElementById('error001').innerHTML=" The field is required!";
		           document.getElementById("id_area_code").style.borderColor = "red";
		          flag=false;
		          //alert("in ifelse");
		    	   
		       }*/
		    	
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
	         
	         
	        var emg_val=$("#id_Emg_no").val();
	        re = /^[0-9]+$/;
	        if( emg_val!=''){
	        	//alert("phone number is not null");
	        	if(!re.test(emg_val)){
	        		$("#error6").text(" Emergency no contains only digits!");
                    $("#id_Emg_no").css('border-color','#E34234');
                   flag=false;	
	        	}
	        	/*else if((emg_val.charAt(0)!=0 && emg_val.length!=9)){
	        		//alert("if charAt!=0");
              	  $("#error6").show();
                   $("#error6").text("Emergency no must contain 9 digit");
                   $("#id_Emg_no").css('border-color','#E34234');
                   flag=false;	
	        	}
	        	else if(emg_val.charAt(0)==0 && emg_val.length!=10){
	        		
	        		//alert("if charAt==0");
                    
               	 $("#error6").show();
                    $("#error6").text("Emergency no must 10 digit");
                    $("#id_Emg_no").css('border-color','#E34234');
                    flag=false;
	        	}*/
	        	else{
	        		//alert("else");
	        		 $("#error6").text("");
                     $("#id_Emg_no").css('border-color','#ccc');
	        	}
	        }
	        var roadside_no=$("#id_roadsides_no").val();
	      //  alert(roadside_no);
	        re = /^[0-9]+$/;
	         if( roadside_no!=''){
	        // alert("phone number is not null");
	        	if(!re.test(roadside_no)){
	        		$("#error8").text(" Road side assistant number contains only digits!");
                   $("#id_roadsides_no").css('border-color','#E34234');
                  flag=false;	
	        	}
	        	else{
	        	//	alert("else");
	        		 $("#error8").text("");
                     $("#id_roadsides_no").css('border-color','#ccc');
	        	}
	         }
	       //  alert(flag);
		return flag;
		
		
		
		
	});
});