$(document).ready(function(){
	//alert("page is loaded");
	//$("#id_city").prepend("<option selected>Select State</option>");	
	$("#Submit_btn").click(function() {
		
		flag=true;
		
		
		if(fname.value==""){
			//alert("shop name");
			  $("#error1").show();
			document.getElementById('error1').innerHTML=" This field is required!";
			document.getElementById("fname").style.borderColor = "#E34234";
			flag=false;
			}
		if(lname.value==""){	
		
			 $("#error2").show();
			document.getElementById('error2').innerHTML=" This field is required!";
			document.getElementById("lname").style.borderColor = "#E34234";
			flag=false;
			}
		

				
		re = /^[A-Za-z\s]+$/;
		 if(fname.value!=""){
	      if(!re.test(fname.value)) {
	    		//alert("fname");

	     document.getElementById('error1').innerHTML=" Firstname only conatin alphabets";
	     document.getElementById("fname").style.borderColor = "#E34234";
	    flag=false;

	     
	    	     }
	      else{
	            //flag=true;
	             $("#error1").hide();
	             document.getElementById("fname").style.borderColor = "#ccc";
	           }}
	      
	      re = /^[A-Za-z\s]+$/;
	      if(lname.value!=""){
	      if(!re.test(lname.value)) {
	    		//alert("lname");
 
	     document.getElementById('error2').innerHTML=" Lastname only conatin alphabets";
	     document.getElementById("lname").style.borderColor = "#E34234";
	     flag=false;
	     //$('#error1').hide();
	     //document.getElementById("fname").style.borderColor = "#ccc";
	     //return false;
	     //flag= false;
	     
	     }
	      else{
	            //flag=true;
	             $("#error2").hide();
	             document.getElementById("lname").style.borderColor = "#ccc";
	           } }
	        	     
	      
		     var area_val=$("#id_area_code").val();
		        
		    	//alert ("area code");		      
		    	
		    		//alert("if");
		      /*  if(( area_val=="")){
		    		//alert("ifelse ");
		    		$("#error001").show();
		           document.getElementById('error001').innerHTML=" The field is required!";
		           document.getElementById("id_area_code").style.borderColor = "red";
		          flag=false;
		          //alert("in ifelse");
		    	   
		       }
		    	
		        if((phone_val!="" )&&( area_val=="")){
		    		//alert("ifelse ");
		    		$("#error001").show();
		           document.getElementById('error001').innerHTML=" Area code can not be empty!";
		           document.getElementById("id_area_code").style.borderColor = "red";
		          flag=false;
		          //alert("in ifelse");
		    	   
		       }*/
		     var phone_val=$("#phone_num").val();  
		     if  ( phone_val =='')
		        {
		                $("#error3").text("This field is required");
		                $("#phone_num").css('border-color','#E34234');
		                flag=false;
		        }
		        
		        re = /^[0-9]+$/;
		         if( phone_val!=''){
		        	// alert("phone number is not null");
		        	if(!re.test(phone_val)){
		        		$("#error3").text(" Phone no contains only digits!");
	                  $("#phone_num").css('border-color','#E34234');
	                 flag=false;	
		        	}
		        	else if((phone_val.charAt(0)!=0 && phone_val.length!=8)){
		        		//alert("if charAt!=0");
	            	  $("#error3").show();
	                 $("#error3").text("Phone no must contain 8 digits");
	                 $("#phone_num").css('border-color','#E34234');
	                 flag=false;	
		        	}
		        	else if(phone_val.charAt(0)==0 && phone_val.length!=10){
		        		
		        		//alert("if charAt==0");
	                  
	             	 $("#error3").show();
	                  $("#error3").text("Phone no must 10 digit");
	                  $("#phone_num").css('border-color','#E34234');
	                  flag=false;
		        	}
		        	else{
		        		//alert("else");
		        		 $("#error3").text("");
	                   $("#phone_num").css('border-color','#ccc');
		        	}
		        }
		     if((phone_val.length==8)&&( area_val=="")){
		    		alert("ifelse ");
		    		$("#error001").show();
		           document.getElementById('error001').innerHTML=" Area code can not be empty!";
		           document.getElementById("id_area_code").style.borderColor = "red";
		          flag=false;
		          //alert("in ifelse");
		    	   
		       }
		        else{
		            //flag=true;
		             $("#error001").hide();
		             document.getElementById("id_area_code").style.borderColor = "#ccc";
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
                                   if ((phone_val.length==10)){
		    				        	
		    				        	$("#error001").show();
		    					           document.getElementById('error3').innerHTML="Phone no must contain 8 digits !";
		    					           document.getElementById("phone_num").style.borderColor = "red";
		    					          flag=false;
		    					          //alert("in ifelse");
		    					    	   
		    					       }
		    				        }
		    				        
		    	
	      
	       
	       
	         
	         
	         var value=$("#country option:selected").val();
	    //  alert(value);
			  var value1=$("#id_city option:selected").val();
			// alert(value1);
			  if(value=="Select Country"){
			    	//alert("country");
			        document.getElementById('error6').innerHTML=" This field is required!";
			             document.getElementById("country").style.borderColor = "#E34234";

			        flag=false;
			        }
			    else{	  
				  	  $("#error6").hide();
				  	  document.getElementById("country").style.borderColor = "#ccc";				  	   	   
				  	  }
			    if(value1=="Select State"){
			    	

			    	//alert("city");
			        document.getElementById('err15').innerHTML=" This field is required!";
			             document.getElementById("id_city").style.borderColor = "#E34234";

			        flag=false;
			        }
			    else{
					//alert("state not null");	  
				  	  $("#err15").hide();
			  	  document.getElementById("id_city").style.borderColor = "#ccc";
				  	   	   
				  	  }
			   
	      
	   
	       
   
	        if(shop_name.value==""){
				//alert("shop name");

				document.getElementById('error4').innerHTML=" This field is required!";
				document.getElementById("shop_name").style.borderColor = "#E34234";
				flag=false;
				}
			else{	//  flag=true;
			  	  $("#error4").hide();
			  	  document.getElementById("shop_name").style.borderColor = "#ccc";
			  	     
			  	  }
	        if(shop_name.value!=""){	
	        if(shop_name.value.length>255){
	    		
				document.getElementById('error4').innerHTML=" Max-length of shop is 255!";
				document.getElementById("shop_name").style.borderColor = "#E34234";

				flag=false;
			}}
	        var re = /^(www.)[a-zA-Z0-9\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;
		     if (id_website.value!=""){
		      
		     if (!re.test(id_website.value)) { 
		      $("#error12").show();
		        document.getElementById('error12').innerHTML=" Please  enter valid website!";
		        document.getElementById("id_website").style.borderColor = "#E34234";
		        flag=false;
		     }
		     else{ 
		      $("#error12").hide();
		      document.getElementById("id_website").style.borderColor = "#ccc";
		           
		      }}		        
	
		     if(id_shop_address.value==""){
					//alert("shop add");

					document.getElementById('error5').innerHTML=" This field is required!";
					document.getElementById("id_shop_address").style.borderColor = "#E34234";
					flag=false;
					}
				else{//	  flag=true;
				  	  $("#error5").hide();
				  	  document.getElementById("id_shop_address").style.borderColor = "#ccc";
				  	     
				  	  }
				  
			    if(id_shop_address.value!=""){	
			    if(id_shop_address.value.length>255){
			    	alert("shop add");
			    	 $("#error5").show();
					document.getElementById('error5').innerHTML=" Max-length of shop address is 255!";
					document.getElementById("id_shop_address").style.borderColor = "#E34234";
			
					flag=false;
				}}
				  	   var emg_val=$("#id_Emg_no").val();
				        re = /^[0-9]+$/;
				        if( emg_val!=''){
				        	// alert("phone number is not null");
				        	if(!re.test(emg_val)){
				        		$("#error7").text(" Emergency no contains only digits!");
			                    $("#id_Emg_no").css('border-color','#E34234');
			                   flag=false;	
				        	}
				        	/*else if((emg_val.charAt(0)!=0 && emg_val.length!=9)){
				        		//alert("if charAt!=0");
			              	  $("#error7").show();
			                   $("#error7").text("Emergency no must contain 9 digit");
			                   $("#id_Emg_no").css('border-color','#E34234');
			                   flag=false;	
				        	}
				        	else if(emg_val.charAt(0)==0 && emg_val.length!=10){
				        		
				        		//alert("if charAt==0");
			                    
			               	 $("#error7").show();
			                    $("#error7").text("Emergency number must 10 digit");
			                    $("#id_Emg_no").css('border-color','#E34234');
			                    flag=false;
				        	}*/
				        	else{
				        		//alert("else");
				        		 $("#error7").text("");
			                     $("#id_Emg_no").css('border-color','#ccc');
				        	}
				        }
						
	    
				        
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
				        	 if ((postcode.length!=4 )){
	    	                    	
    		                     
	    	                    	// alert("if charAt!=0");
	    	                    	  $("#error_post").show();
	    	                    	  document.getElementById('error_post').innerHTML=" Postal code must contain 4 digit";
		    				           document.getElementById("id_post_code").style.borderColor = "#E34234";
		    				          flag=false;
	    	                        
	    	                     }
				        	else{
				        		//alert("else");
				        		 $("#error_post").text("");
			                   $("#id_post_code").css('border-color','#ccc');
				        	}
				         }
	                                                 // alert("flag"+flag);
		                                               return flag;
				
	     });
	});
