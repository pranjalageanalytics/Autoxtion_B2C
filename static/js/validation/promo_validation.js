$(document).ready(function(){
	//alert("hiiiiiii");
	
       
	
	$("#promo").click(function() {
		var total_amt=$("#id_total_amount").val();
		 var value=$("#id_Service_id option:selected").val();
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
    var date=$("#id_from_date").val();
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
  
 
   
   
   var date=$("#id_to_date").val();
   var arr1 = date.split("/");
 //  alert("to"+arr1[0])
   var dd2=arr1[0];
   //alert(arr1[1])
   var mm2= arr1[1]
  // alert(arr1[2])
   var yyyy2= arr1[2]
   date3= mm2+'/'+dd2+'/'+yyyy2;
   var d102=new Date(yyyy2,mm2,dd2);
  // alert("to"+d102);
   //alert(today1);  
  flag=true;
  

	  
	  if(id_to_date.value==""){
		  $("#error8").show();
	   document.getElementById('error8').innerHTML=" This field is required!!";
		document.getElementById("id_to_date").style.borderColor = "#E34234";

	   flag=false;
	  }

	  if(id_from_date.value==""){
		   document.getElementById('error7').innerHTML=" This field is required!";
			document.getElementById("id_from_date").style.borderColor = "#E34234";

		   flag=false;
		  }
	 
	
	  else{
		  $("#error7").hide();
		  document.getElementById("id_from_date").style.borderColor = "#ccc";
		  }
	  if(d102<d101  ){
		  $("#error8").show();
	   document.getElementById('error8').innerHTML=" To date can not be less than From date!";
		document.getElementById("id_to_date").style.borderColor = "#E34234";
	    flag=false;
	   }
	  if(id_to_date.value!="" && d102>d101){
		  //alert("in date3 blank");
		  $("#error8").hide();
		  document.getElementById("id_to_date").style.borderColor = "#ccc";
		  }
	  if( id_from_date.value!="" && d101<d100){
		  $("#error7").show();
		     document.getElementById('error7').innerHTML=" From date can not be less than Today's date!";
			document.getElementById("id_from_date").style.borderColor = "#E34234";

		   flag=false;
		   
		  }
	  if(id_from_date.value!="" && d101<d102 && d100<=d101){	 
		  $("#error7").hide();
		  document.getElementById("id_from_date").style.borderColor = "#ccc";
		  	   
		  }
  
  if (value==25) {
	 
  if(id_description.value==""){
	   document.getElementById('error6').innerHTML=" This field is required!";
		document.getElementById("id_description").style.borderColor = "#E34234";

	   flag=false;
	   
	  }
 if(id_price.value==""){
	 $("#error9").show();
	   document.getElementById('error9').innerHTML=" This field is required!";
		document.getElementById("id_price").style.borderColor = "#E34234";

	   flag=false;
	   
	  }else{	  
		  $("#error9").hide();
		  document.getElementById("id_price").style.borderColor = "#ccc";
		   	   
		  }
	  
 re = /^[0-9]+$/;
 if(id_price.value!=""){
     if(!re.test(id_price.value)) {
      $("#error9").show();
    document.getElementById('error9').innerHTML=" Price contain only digits";
    document.getElementById("id_price").style.borderColor = "#E34234";
   flag=false;
   	//alert("in fname if "+flag);
    
         }
 if(id_price.value.length>5){
	// alert("hiiiiii");
	  $("#error9").show();
	   document.getElementById('error9').innerHTML=" Price value can not greater than 5 digits!";
		document.getElementById("id_price").style.borderColor = "#E34234";

	   flag=false;
	   
	  }
 }
 
 
  if(id_description.value.length>100){
	   document.getElementById('error6').innerHTML=" Max length of description is 100!";
		document.getElementById("id_description").style.borderColor = "#E34234";

	   flag=false;
	  }
  if(id_description.value!="" && id_description.value.length<=100){	  
	  $("#error6").hide();
	  document.getElementById("id_description").style.borderColor = "#ccc";
	   	   
	  }
  }
 
  
  
  if(id_company.value==""){
   document.getElementById('error1').innerHTML=" This field is required!";
	document.getElementById("id_company").style.borderColor = "#E34234";

   flag=false;
   
   
  }
  if(id_company.value!=""){	  
	  $("#error1").hide();
	  document.getElementById("id_company").style.borderColor = "#ccc";
	   	   
	  }
  
  if(id_model_id.value==""){
   document.getElementById('error2').innerHTML=" This field is required!";
	document.getElementById("id_model_id").style.borderColor = "#E34234";

   flag=false;
  }
  if(id_model_id.value!=""){	  
	  $("#error2").hide();
	  document.getElementById("id_model_id").style.borderColor = "#ccc";
	     
	  }
  
  if(id_make_year.value==""){
		
	  document.getElementById('error3').innerHTML=" This field is required!";
	  document.getElementById("id_make_year").style.borderColor = "#E34234";
   flag=false;
  }
  if(id_make_year.value!=""){	  
	  $("#error3").hide();
	  document.getElementById("id_make_year").style.borderColor = "#ccc";
	    
	  }
  
  if(id_Service_id.value==""){
   document.getElementById('error4').innerHTML="This field is required!";
	document.getElementById("id_Service_id").style.borderColor = "#E34234";

   flag=false;
  }
  if(id_Service_id.value!=""){	  
	  $("#error4").hide();
	  document.getElementById("id_Service_id").style.borderColor = "#ccc";
	  	   
	  }	 
  
 
 
  
  if(value!=25){
	  //alert("value");
 /* if(id_discount.value==""){
   document.getElementById('error5').innerHTML=" This field is required!";
	document.getElementById("id_discount").style.borderColor = "#E34234";

   flag=false;
   
  }*/
	  if(id_discount.value=="")
		  {
		  //("discount is null");
		  $("#id_discount").val(0);
		  }
	  re = /^[0-9]+$/;
 if(id_discount.value!=""){
	
		//alert("in fname if "+flag);
	     if(!re.test(id_discount.value)) {
	      $("#error5").show();
	    document.getElementById('error5').innerHTML=" Discount contain only digits";
	    document.getElementById("id_discount").style.borderColor = "#E34234";
	   flag=false;
	   	//alert("in fname if "+flag);
	    
	         }
  if(id_discount.value<0){
   document.getElementById('error5').innerHTML=" Discount can not be negative!";
	document.getElementById("id_discount").style.borderColor = "#E34234";

   flag=false;
  }
  
  
  if(id_discount.value>100){
   document.getElementById('error5').innerHTML=" Discount can not be greater than 100!";
	document.getElementById("id_discount").style.borderColor = "#E34234";

   flag=false;
  }
  if(id_discount.value!="" && id_discount.value<100 && id_discount.value>0 ){	  
	  $("#error5").hide();
	  document.getElementById("id_discount").style.borderColor = "#ccc";
	  	   
	  }
  
  }}
if (total_amt==""){
   document.getElementById('total_error').innerHTML=" This field can not be null";
  document.getElementById("id_total_amount").style.borderColor = "#E34234";
  flag=false;

  }
  else{
   $("#total_error").hide();
   document.getElementById("id_total_amount").style.borderColor = "#ccc";
  }
  if (flag)
	{
		promo_form.submit();
	}
  //("flag"+flag);
return flag;
  });
});