$(document).ready(function(){
	 // alert("hiiiii");
	$("#promo_btn").click(function()
			
	{
		
		 flag=true;
		  if(id_coment.value==""){
		   document.getElementById('err7').innerHTML=" This field is required!";
			document.getElementById("id_coment").style.borderColor = "#E34234";

		   flag=false;
		   
		   
		  }
		  else{
			  $("#err7").hide();
			  document.getElementById("id_coment").style.borderColor = "#ccc";  
		  }
		  if (flag)
			{
				appointment_form.submit();
			}
		  return flag;
	});
});