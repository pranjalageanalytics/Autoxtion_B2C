$(document).ready(function(){
		//alert("Page is loaded");
	$("#id_city").prepend("<option selected>Select State</option>");
	           
	            //var service=$("#id_Service_id option:selected").val();
	$("#id_email").change(function(){
		
	
	
	if (id_email.value == '')
	{
		document.getElementById('error4').innerHTML=" This field is required!";
		 document.getElementById("id_email").style.borderColor = "#E34234";
		 
		 

		flag=false;
		}
	
	var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    if(id_email.value!=""){
    if (reg.test(id_email.value) == false)
    {
        document.getElementById('error4').innerHTML="Invalid Email ID";
        document.getElementById("id_email").style.borderColor = "#E34234";
    }
    else{
        $('#error4').hide();
        document.getElementById("id_email").style.borderColor = "#ccc";
    }}
    });
	$("#id_first_name").change(function(){
		//alert("on change");
		if(id_first_name.value==""){
			document.getElementById('error1').innerHTML="This field is require!";
			document.getElementById("id_first_name").style.borderColor="#E34234";
		}
		
		re = /^[A-Za-z\s]+$/;
		
        if(id_first_name.value!=""){
        	//alert(id_first_name.value);
            if(!re.test(id_first_name.value)) {
             $("#error1").show();
           document.getElementById('error1').innerHTML=" Firstname only conatin alphabets";
           document.getElementById("id_first_name").style.borderColor = "#E34234";
          flag=false;
          	//alert("in fname if "+flag);
           
                }
          else{
            flag=true;
             $("#error1").hide();
             document.getElementById("id_first_name").style.borderColor = "#ccc";
           }}
        
        });
	
	
	$("#id_last_name").change(function(){
		//alert("on change");
		if(id_last_name.value==""){
			document.getElementById('error2').innerHTML="This field is require!";
			document.getElementById("id_first_name").style.borderColor="#E34234";
		}
		
		re = /^[A-Za-z\s]+$/;
		
        if(id_last_name.value!=""){
        	//alert(id_first_name.value);
            if(!re.test(id_last_name.value)) {
             $("#error2").show();
           document.getElementById('error2').innerHTML=" Lastname only conatin alphabets";
           document.getElementById("id_last_name").style.borderColor = "#E34234";
          flag=false;
          	//alert("in fname if "+flag);
           
                }
          else{
            flag=true;
             $("#error2").hide();
             document.getElementById("id_last_name").style.borderColor = "#ccc";
           }}
        
        });
	$("#pass2").change(function(){
		  flag=true;
		  console.log('on key up event of pass2');
		   if(pass2.value==""){
		    document.getElementById('error6').innerHTML=" This field is required!";
		         document.getElementById("pass2").style.borderColor = "#E34234";

		    flag=false;
		    //alert(pass2.value);
		    }
		  if (pass2.value!=pass1.value) {
		         
		         document.getElementById('error6').innerHTML=" Password and confirm password must be same!";
		         //document.getElementById("pass1").style.borderColor = "#E34234";
		         document.getElementById("pass2").style.borderColor = "#E34234";
		         flag=false;
		          }
		  else
		     {
		   document.getElementById('error6').innerHTML=" ";
		   document.getElementById("pass2").style.borderColor = "#ccc";
		     }
		  return flag;
		});
		 $("#pass1").change(function(){
		  console.log('on key up event of pass1');
		  flag=true;
		  if(pass1.value==""){
		   document.getElementById('error5').innerHTML=" This field is required!";
		        document.getElementById("pass1").style.borderColor = "#E34234";

		   flag=false;
		   //alert(pass1.value);
		   }
		  
		/*  if(pass1.value != "") {
		   
		         if(pass1.value.length < 8) {
		          console.log("length is less");
		     document.getElementById('error5').innerHTML=" Password must contain at least Eight characters!";
		     document.getElementById("pass1").style.borderColor = "#E34234";
		       // document.getElementById("pass2").style.borderColor = "#E34234";
		           
		           flag=false;
		         }
		         
		         
		         else if(!(re = /[0-9]/).test(pass1.value)) {
		          console.log("Number");
		        document.getElementById('error5').innerHTML=" password must contain at least one number (0-9)!";
		     document.getElementById("pass1").style.borderColor = "#E34234";
		     //document.getElementById("pass2").style.borderColor = "#E34234";
		           
		           flag=false;
		         }
		         
		         else if(!(re = /[a-z]/).test(pass1.value)) {
		          console.log("lowercase");
		        document.getElementById('error5').innerHTML=" password must contain at least one lowercase letter (a-z)!";
		     document.getElementById("pass1").style.borderColor = "#E34234";
		           
		           flag=false;
		         }
		         
		         else if(!(re = /[A-Z]/).test(pass1.value)) {
		          console.log("uppercase");
		     document.getElementById('error5').innerHTML=" password must contain at least one uppercase letter (A-Z)!";
		     document.getElementById("pass1").style.borderColor = "#E34234";
		           
		           flag=false;
		         }
		         else if(!(re = /[_\-!\"@;,.:]/).test(pass1.value)) {
		          console.log("special char");
		     document.getElementById('error5').innerHTML=" password must contain at least one special character!";
		     document.getElementById("pass1").style.borderColor = "#E34234";
		           
		           flag=false;
		         }*/
		         else
		          {
		          document.getElementById('error5').innerHTML=" ";
		          document.getElementById("pass1").style.borderColor = "#ccc";
		          }
		       
		   
		     
		return flag;

		 });	
	
	$("#create_button").click(function(){
			//alert("button click");
		    
		    flag = true;		    
		    if(id_first_name.value==""){
		        document.getElementById('error1').innerHTML=" This field is required!";
		             document.getElementById("id_first_name").style.borderColor = "#E34234";

		        flag=false;
		        }
		       
		          
		          re = /^[A-Za-z\s]+$/;
		        if(id_first_name.value!=""){
		            if(!re.test(id_first_name.value)) {
		             $("#error1").show();
		           document.getElementById('error1').innerHTML=" Firstname only conatin alphabets";
		           document.getElementById("id_first_name").style.borderColor = "#E34234";
		          flag=false;
		          	//alert("in fname if "+flag);
		           
		                }
		          else{
		            flag=true;
		             $("#error1").hide();
		             document.getElementById("id_first_name").style.borderColor = "#ccc";
		           }}
		         if(id_last_name.value==""){
		         document.getElementById('error2').innerHTML=" This field is required!";
		              document.getElementById("id_last_name").style.borderColor = "#E34234";

		         flag=false;
		         }
		            
		            re = /^[A-Za-z\s]+$/;
		            if(id_last_name.value!=""){
		            if(!re.test(id_last_name.value)) {
		             $("#error2").show();
		           document.getElementById('error2').innerHTML=" Lastname only conatin alphabets";
		           document.getElementById("id_last_name").style.borderColor = "#E34234";
		           flag=false;
		          // alert("in lname if "+flag);
		            }
		           else{
		            
		             $("#error2").hide();
		             document.getElementById("id_last_name").style.borderColor = "#ccc";
		           }}
		   
		    
		   
		    
		    if (id_email.value == '')
			{
				document.getElementById('error4').innerHTML=" This field is required!";
				 document.getElementById("id_email").style.borderColor = "#E34234";
				 
				 

				flag=false;
				}
			
			var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
	        if(id_email.value!=""){
	        if (reg.test(id_email.value) == false)
	        {
	            document.getElementById('error4').innerHTML="Invalid Email ID";
	            document.getElementById("id_email").style.borderColor = "#E34234";
	        }
	        else{
	            $('#error4').hide();
	            document.getElementById("id_email").style.borderColor = "#ccc";
	        }}
		    
		    
		    
		    
		    if(pass1.value==""){
				document.getElementById('error5').innerHTML=" This field is required!";
		    	  document.getElementById("pass1").style.borderColor = "#E34234";

				flag=false;
				//alert(pass1.value);
				}
		    else
	          {
	          document.getElementById('error5').innerHTML=" ";
	          document.getElementById("pass1").style.borderColor = "#ccc";
	          }
	       
		    if(pass2.value==""){
		    	//alert("empty");
				document.getElementById('error6').innerHTML=" This field is required!";
		    	  document.getElementById("pass2").style.borderColor = "#E34234";

				flag=false;
				//alert(pass2.value);
				}		    
		 console.log('on key up event of pass2');
		 if(pass2.value!=""){
			  if (pass2.value!=pass1.value) {
			         
			         document.getElementById('error6').innerHTML=" Password and confirm password must be same!";
			         //document.getElementById("pass1").style.borderColor = "#E34234";
			         document.getElementById("pass2").style.borderColor = "#E34234";
			         flag=false;
			          }
			  else
			     {
			   document.getElementById('error6').innerHTML=" ";
			   document.getElementById("pass2").style.borderColor = "#ccc";
			     }
		 }
			  
			 /* if(pass1.value==""){
				   document.getElementById('error5').innerHTML=" This field is required!";
				        document.getElementById("pass1").style.borderColor = "#E34234";

				   flag=false;
				   //alert(pass1.value);
				   }
				  if(pass1.value != "") {
				   
				         if(pass1.value.length < 8) {
				          console.log("length is less");
				     document.getElementById('error5').innerHTML=" Password must contain at least Eight characters!";
				     document.getElementById("pass1").style.borderColor = "#E34234";
				       // document.getElementById("pass2").style.borderColor = "#E34234";
				           
				           flag=false;
				         }
				         
				         
				         else if(!(re = /[0-9]/).test(pass1.value)) {
				          console.log("Number");
				        document.getElementById('error5').innerHTML=" password must contain at least one number (0-9)!";
				     document.getElementById("pass1").style.borderColor = "#E34234";
				     //document.getElementById("pass2").style.borderColor = "#E34234";
				           
				           flag=false;
				         }
				         
				         else if(!(re = /[a-z]/).test(pass1.value)) {
				          console.log("lowercase");
				        document.getElementById('error5').innerHTML=" password must contain at least one lowercase letter (a-z)!";
				     document.getElementById("pass1").style.borderColor = "#E34234";
				           
				           flag=false;
				         }
				         
				         else if(!(re = /[A-Z]/).test(pass1.value)) {
				          console.log("uppercase");
				     document.getElementById('error5').innerHTML=" password must contain at least one uppercase letter (A-Z)!";
				     document.getElementById("pass1").style.borderColor = "#E34234";
				           
				           flag=false;
				         }
				         else if(!(re = /[_\-!\"@;,.:]/).test(pass1.value)) {
				          console.log("special char");
				     document.getElementById('error5').innerHTML=" password must contain at least one special character!";
				     document.getElementById("pass1").style.borderColor = "#E34234";
				           
				           flag=false;
				         }*/
				        
				  
				   
				 // alert(flag+"flag");				   
					   	return flag;   
		    
		});
	
	
	
	
$("#submit").click(function(){
	 flag = true;
	 var postcode=$("#id_post_code").val();
     if  ( postcode =='')
     {
             $("#error_post").text("This field is required");
             $("#id_post_code").css('border-color','#E34234');
             flag=false;
     }
     
     re = /^[0-9]+$/;
      if( postcode!=''){
     	// alert("phone number is not null");
     	if(!re.test(postcode)){
     		$("#error_post").text(" Post Code contains only digits!");
           $("#id_post_code").css('border-color','#E34234');
          flag=false;	
     	}
     	else{
     		//alert("else");
     		 $("#error_post").text("");
            $("#id_post_code").css('border-color','#ccc');
     	}
      }
	//alert("submit button click");
	var re = /^(www.)[a-zA-Z0-9\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;
    if (id_website.value!=""){
    	//alert("website not empty");
    	if (!re.test(id_website.value)== true) { 
    		//alert("website not valid");
    		document.getElementById('error12').innerHTML=" Please  enter valid website!";
    		document.getElementById("id_website").style.borderColor = "#E34234";
    		flag=false;
    	}
    	else{	  
    		$("#error12").hide();
    		document.getElementById("id_website").style.borderColor = "#ccc";
  	   	 }
    }
   
    if(id_phone_no.value==""){
    		//alert("blank phone number");
    		document.getElementById('error3').innerHTML=" This field is required!";
    		document.getElementById("id_phone_no").style.borderColor = "#E34234";
    		flag=false;
	}
    var value1=$("#id_city option:selected").val();
    //alert(value1)
    if(value1=="Select State"){
    	document.getElementById('error11').innerHTML=" This field is required!";
		document.getElementById("id_city").style.borderColor = "#E34234";
		flag=false;
    }
    else{
    	$("#error11").hide();
		document.getElementById("id_city").style.borderColor = "#ccc";
    }
    var value2=$("#id_country option:selected").val();
    //alert(value2)
    if(value2=="Select Country"){
    	document.getElementById('error13').innerHTML=" This field is required!";
		document.getElementById("id_country").style.borderColor = "#E34234";
		flag=false;
    }
    else{
    	$("#error13").hide();
		document.getElementById("id_country").style.borderColor = "#ccc";
    }
    if(id_shop_name.value==""){
    		//alert("blank shop name");
    		document.getElementById('error7').innerHTML=" This field is required!";
    		document.getElementById("id_shop_name").style.borderColor = "#E34234";
    		flag=false;
	}
    if(id_shop_name.value!=""){	
    		$("#error7").hide();
	  	  	document.getElementById("id_shop_name").style.borderColor = "#ccc";
    }
    if(id_abn.value==""){
    		//alert("blank abn");
    		document.getElementById('error9').innerHTML=" This field is required!";
            document.getElementById("id_abn").style.borderColor = "#E34234";
            flag=false;
    }
    if (id_abn.value!=""){
    		if(id_abn.value.length<11){
    			//alert("abn less")
			flag=false;
    			document.getElementById('error9').innerHTML=" Please enter valid ABN ";
    			document.getElementById("id_abn").style.borderColor = "#E34234";
    		}
    		else{
    			$("#error9").hide();
    			document.getElementById("id_abn").style.borderColor = "#ccc";
    		}
    }
    	  
    

    if(id_shop_address.value==""){
    	//	alert("blank shop address");
    		document.getElementById('error8').innerHTML=" This field is required!";
    		document.getElementById("id_shop_address").style.borderColor = "#E34234";
    		flag=false;
	}
    if(id_shop_address.value!=""){
    //alert(id_shop_address.value)
	  	  	$("#error8").hide();
	  	  	document.getElementById("id_shop_address").style.borderColor = "#ccc";
	  	      
	}
   
    var phone_val=$("#id_phone_no").val();
    if  ( phone_val ==''&& area_val!="")
    {
            $("#error3").text("This field is required");
            $("#id_phone_no").css('border-color','#E34234');
            flag=false;
    }
    re = /^[0-9]+$/;
     if( phone_val!=''){
    	 //alert("phone number is not null");
    	if(!re.test(phone_val)){
    		$("#error3").text(" Phone no contains only digits!");
          $("#id_phone_no").css('border-color','#E34234');
         flag=false;	
    	}
    	else if((phone_val.charAt(0)!=0 && phone_val.length!=8)){
    		//alert("if charAt!=0");
    	  $("#error3").show();
         $("#error3").text("Phone no must contain 8 digits");
         $("#id_phone_no").css('border-color','#E34234');
         flag=false;	
    	}
    	else if(phone_val.charAt(0)==0 && phone_val.length!=10){
    		
    		//alert("if charAt==0");
          
     	 $("#error3").show();
          $("#error3").text("Phone no must 10 digit");
          $("#id_phone_no").css('border-color','#E34234');
          flag=false;
    	}
    	else{
    		//alert("else");
    		 $("#error3").text("");
           $("#id_phone_no").css('border-color','#ccc');
    	}
    }
 
     var area_val=$("#id_area_code").val();
       // var land_val=$("#landline_number").val();
    	//alert ("area code");		      
     if( area_val==""){
    		//alert("ifelse ");
    		$("#error001").show();
           document.getElementById('error001').innerHTML=" The field is required!";
           document.getElementById("id_area_code").style.borderColor = "red";
          flag=false;
          //alert("in ifelse");
    	   
       }
    		//alert("if");
        if((phone_val!="" )&&( area_val=="")){
    		//alert("ifelse ");
    		$("#error001").show();
           document.getElementById('error001').innerHTML=" Area code can not be empty!";
           document.getElementById("id_area_code").style.borderColor = "red";
          flag=false;
          //alert("in ifelse");
    	   
       }
    				          re = /^[0-9]+$/;
    				           if(area_val!=""){
    				            if(!re.test(area_val)) {
    				             //$("#error001").show();
    				             $("#error001").text(" Area code contain only digits");
    				           document.getElementById("id_area_code").style.borderColor = "#E34234";
    				          flag=false;
    				          	//alert("in fname if "+flag);
    				           
    				                }
    				          else{
    				            //flag=true;
    				             $("#error001").hide();
    				             document.getElementById("id_area_code").style.borderColor = "#ccc";
    				           }
    				        if ((area_val.length!=2 )){
    	                    	
    		                     
    	                    	// alert("if charAt!=0");
    	                    	  $("#error001").show();
    	                    	  document.getElementById('error001').innerHTML=" Area code must contain 2 digit";
	    				           document.getElementById("id_area_code").style.borderColor = "#E34234";
	    				          flag=false;
    	                        
    	                     }
    				        }
    				        
 				        if(document.getElementById('field_terms').checked){
 				    					    }else{
 				    					    	
 				    					    	document.getElementById('errors_term').innerHTML=" Please accept terms and conditions!";
 				    					    	 flag=false;
 				    					    }
 				        
 				    				        

    //alert(flag+"flag");
    return flag;
});
	
		});
