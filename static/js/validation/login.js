$(document).ready(function(){
	//alert("Page loaded");
	$("#btn").click(function() {
		
		var value=$("input[name='customer1']:checked").val();
  //var valu=$("input[name='customer']:checked").val();
  //alert(value);
  //alert(valu);
  flag=true;
   if (!$("input[name='customer1']:checked").val()) {
         //alert('Nothing is checked!');
         document.getElementById('error3').innerHTML=" Please select valid option!";
         document.getElementById("member").style.borderColor = "#E34234";
          return false;
      }
      else {
       $("#error3").hide();
       document.getElementById("member").style.borderColor = "#ccc";
        //alert('One of the radio buttons is checked!');
       // document.getElementById('error3').innerHTML="One of the radio buttons is checked!";
      }
  if(value=="customer"){
   //alert("if");
    if(document.getElementById('field_terms').checked){
       }else{
        
        document.getElementById('errors_term').innerHTML=" Please accept terms and conditions!";
         flag=false;
       }
  }
  
  if (id_username.value == '')
  {
   document.getElementById('error1').innerHTML=" This field is required!";
    document.getElementById("id_username").style.borderColor = "#E34234";
   
    

   flag=false;
   }
  else {
   //flag=true;
   $("#error1").hide();
       document.getElementById("id_username").style.borderColor = "#ccc";
  }
  
  if(id_password.value==""){
   document.getElementById('error2').innerHTML=" This field is required!";
    document.getElementById("id_password").style.borderColor = "#E34234";
   flag=false;
   }
  else {
   //flag=true;
   $("#error2").hide();
       document.getElementById("id_password").style.borderColor = "#ccc";
  }
   //alert("flag"+flag);
  return flag;	
});
});