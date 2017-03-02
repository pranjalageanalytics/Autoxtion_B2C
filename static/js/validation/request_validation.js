$(document).ready(function(){
	
	$("#button_submit").click(function() {
		
		
		
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
		  
		  var date=$("#id_date").val();
		  var arr = date.split("/");
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
		
		
		 var fileUpload = $("#id_image");
		 var str = fileUpload.val();
		// alert("upload data"+fileUpload.val());
		 var n = str.endsWith(".png");
		 var m = str.endsWith(".jpeg");
		 var p = str.endsWith(".jpg");
		 
		 if (str != "")
			 {
			
		
		 
			 if (n||m||p)
				 {
				 var fuData = document.getElementById('id_image');
				 var FileUploadPath = fuData.value;
				// alert(FileUploadPath);
				 var size = (fuData.files[0].size/1024)/1024;
				 //alert(size);
				 if(size>1)
					 {
					 document.getElementById('lblError').innerHTML="Size should be less than 1MB";
						// alert("file format is not correct");
						 flag=false;
					 }
				 else{
				 $("#lblError").hide();
				// document.getElementById('lblError').innerHTML="File format correct";
				// alert("file format correct");
				 flag=true;
				 }
				 }
			 else{
				 document.getElementById('lblError').innerHTML="Please upload file in '.png' or '.jpeg'or 'jpg' format only";
				// alert("file format is not correct");
				 flag=false;
			 }
			 }
		
		
		
		if(id_date.value==""){
			   document.getElementById('error7').innerHTML=" This field is required!";
				document.getElementById("id_date").style.borderColor = "#E34234";

			   flag=false;
			   
			   
			  }
			  else{
				  $("#error7").hide();
				  document.getElementById("id_date").style.borderColor = "#ccc";  
			  }
		if(id_service_type.value==""){
			
			document.getElementById('error1').innerHTML=" This field is required!";
			document.getElementById("id_service_type").style.borderColor = "#E34234";

			flag=false;
			
			
		}
		else{
					
		
		    $('#error1').hide();
            document.getElementById("id_service_type").style.borderColor = "#ccc";
		}
		
		if(id_description.value==""){
			//alert("desc empty");
			document.getElementById('error2').innerHTML=" This field is required!";
			document.getElementById("id_description").style.borderColor = "#E34234";

			flag=false;
		}
		else{
			
			
		    $('#error2').hide();
            document.getElementById("id_description").style.borderColor = "#ccc";
		}
		if(id_description.value!=""){
		if(id_description.value.length>100){
		
			document.getElementById('error2').innerHTML=" Max-length of request is 100!";
			document.getElementById("id_description").style.borderColor = "#E34234";

			flag=false;
		}
		}
		 if(d101<d100){
			 document.getElementById('error7').innerHTML="Request date can not be less than Today's date!";
				$("#error7").show();
			    document.getElementById("id_date").style.borderColor = "#E34234";
			    flag=false;
		 }
		 		
	/*	 if( id_date.value!="" && date2<today1){
			   $("#error7").show();
			   document.getElementById('error7').innerHTML=" Request date can not be less than Today's date!";
				document.getElementById("id_date").style.borderColor = "#E34234";

			   flag=false;
			   
			  }*/
		 
		 if(id_from_time.value==""){
			   document.getElementById('error8').innerHTML=" This field is required!";
				document.getElementById("id_from_time").style.borderColor = "#E34234";

			   flag=false;
			   
			   
			  }
		  else{
			  $("#error8").hide();
			  document.getElementById("id_from_time").style.borderColor = "#ccc";
		  }
		  if(id_to_time.value==""){
			   document.getElementById('error9').innerHTML=" This field is required!";
				document.getElementById("id_to_time").style.borderColor = "#E34234";

			   flag=false;
			   
			   
			  }
		  else{
			  $("#error9").hide();
			  document.getElementById("id_to_time").style.borderColor = "#ccc";
		  }
		//alert("fhvbwvbi"+flag);
		if (flag)
			{
			request_form.submit();
			}
        return flag;		
		
	});
});