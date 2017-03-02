$(document).ready(function(){
	//alert("hiiiii");
	//alert("ubjwrvebivber");
	$("#submit_frm").click(function() {
		
		flag=true;
		
		if(name1.value=="")
		{
			//alert("control in if");
		  document.getElementById('error1').innerHTML=" This field is required!";
  	      document.getElementById("name1").style.borderColor = "#E34234";
  	      flag=false;
  	      
  	    //alert("name if  "+flag);
		}
	else{
		//alert("control in else");
		//flag=true;
		//alert("name else  "+flag);
		document.getElementById('error1').innerHTML=" ";
	      document.getElementById("name1").style.borderColor = "";
	}
		re = /^[A-Za-z\s]+$/;
		 if(name1.value!=""){
	      if(!re.test(name1.value)) {

	     document.getElementById('error1').innerHTML=" Firstname only contain alphabets";
	     document.getElementById("name1").style.borderColor = "#E34234";
	    flag=false;

	     }
	     
	      }
		if(name2.value=="")
		{
			//alert("last_name");
		  document.getElementById('error11').innerHTML=" This field is required!";
  	      document.getElementById("name2").style.borderColor = "#E34234";
  	      flag=false;
  	      
  	    //alert("name if  "+flag);
		}
	else{
		//alert("control in else");
		//flag=true;
		//alert("name else  "+flag);
		document.getElementById('error11').innerHTML=" ";
	      document.getElementById("name2").style.borderColor = "";
	}
		
		re = /^[A-Za-z\s]+$/;
		 if(name2.value!=""){
	      if(!re.test(name2.value)) {

	     document.getElementById('error11').innerHTML=" Firstname only contain alphabets";
	     document.getElementById("name2").style.borderColor = "#E34234";
	    flag=false;

	     }
	     
	      }
		
		
		var email=$("#email").val();
		//var phone_val=$("#phone").val();
		// alert("email"+email);
		 //alert("phone"+phone_val);
		// alert("in other");
		
			//alert("in email");
			var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
			if(email!="")
			{
	        if (reg.test(email) == false)
				{
				//alert("control in if  email");
				 document.getElementById('error2').innerHTML=" Enter valid email!";
			      document.getElementById("email").style.borderColor = "#E34234";
			      flag=false;
			     //alert("email if  "+flag);
				}
			else{
				//flag=true;
				//alert("email else  "+flag);
				document.getElementById('error2').innerHTML=" ";
			      document.getElementById("email").style.borderColor = "";
			}
			//alert(flag);
			
		}
		  var phone_val=$("#phone").val();
	       
	        re = /^[0-9]+$/;
	        if((phone_val=="") && (email==""))
        	{
        	//alert("both are null");
        	 $("#error4").text("Please enter Email or Phone number");
             $("#phone").css('border-color','#E34234');
             $("#email").css('border-color','#E34234');
             flag=false;
        	}
	        else{
        		//alert("else");
        		 $("#error4").text("");
             $("#email").css('border-color','#ccc');
        	}
	        	
	         if( phone_val!=''){
	        	 //alert("phone number is not null");
	        	if(!re.test(phone_val)){
	        		$("#error3").text(" Phone no contains only digits!");
                $("#phone").css('border-color','#E34234');
               flag=false;	
	        	}
	        	else if((phone_val.charAt(0)!=0 && phone_val.length!=8)){
	        		//alert("if charAt!=0");
          	  $("#error3").show();
               $("#error3").text("Phone no must contain 8 digits");
               $("#phone").css('border-color','#E34234');
               flag=false;	
	        	}
	        	else if(phone_val.charAt(0)==0 && phone_val.length!=10){
	        		
	        		//alert("if charAt==0");
                
           	 $("#error3").show();
                $("#error3").text("Phone no must 10 digit");
                $("#phone").css('border-color','#E34234');
                flag=false;
	        	}
	        	else{
	        		//alert("else");
	        		 $("#error3").text("");
                 $("#phone").css('border-color','#ccc');
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
	         
	         
		return flag;
	});
});
