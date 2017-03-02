$(document).ready(function(){
	//alert("hiiiii");
	//alert("ubjwrvebivber");
	$("#submit_frm").click(function() {
		$("#id_form-0-reg_expiry_date").attr("class","form-control");
		  var a=$("#id_form-0-reg_expiry_date").val();
		   // alert(a);
		  var vin_no=$("#id_form-0-vin_no").val();
		  var c=$("id_form-0-chasis_no").val();
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
          
          flag=true;
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
          
         /* if(a!="" && date2<today1){
  			//alert("date");
  			document.getElementById('error6').innerHTML="Registration Expiry date must be less than Today's Date!";
  			$("#error6").show();
  		    document.getElementById("id_form-0-reg_expiry_date").style.borderColor = "#E34234";
  		    flag=false;
  		}
  		else{
  			
  			  $("#error6").hide();
  			  document.getElementById("id_form-0-reg_expiry_date").style.borderColor = "#ccc";
  		}
  		*/
         /* var re = new RegExp("^[A-HJ-NPR-Z\\d]{8}[\\dX][A-HJ-NPR-Z\\d]{2}\\d{6}$");
 		 if (b!=""){
 			 
 			 if(!re.test(b)){
 				//alert("vin no");
 				 $("#err9").show();
 				document.getElementById('err9').innerHTML=" Enter valid VIN NO !";
 			     document.getElementById("id_form-0-vin_no").style.borderColor = "#E34234";

 				flag=false;
 			} else{// flag=true;
 			 $("#err9").hide();
 		  	  document.getElementById("id_form-0-vin_no").style.borderColor = "#ccc";
 		 }
 			 
 		 }
 		*/
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
	 				// alert("in else");
	 				 // flag=true;
	 			   $("#err9").hide();
	 		  	  document.getElementById("id_form-0-vin_no").style.borderColor = "#ccc";
	 		 }
	 			 
	 		 }
 		  var c=$("#id_form-0-chasis_no").val();
		 // alert(c);

 		  re = /^[0-9]+$/;
 		 if(c!=""){
 			//  alert("in c");
 			  if (!re.test(c)){
 				  $("#err10").show();
 					document.getElementById('err10').innerHTML=" Enter valid Chasis No !";
	 			     document.getElementById("id_form-0-chasis_no").style.borderColor = "#E34234";

	 				flag=false;
	 			}
 			  else if($("#id_form-0-chasis_no").val().length!=6){
				 $("#err10").show();
				//  alert("in length");
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
 			customer_vehicle_form.submit();
		}
 		// alert("flag"+flag);
		return flag;
	});
});