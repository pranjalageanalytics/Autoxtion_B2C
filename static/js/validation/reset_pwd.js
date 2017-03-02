 $(document).ready(function(){
  
  $("#submit_frm").click(function()
  {
    
flag=true
    
    if(pwd1.value== "" ) {
      
       
  document.getElementById('error1').innerHTML=" This field is required!";
  document.getElementById("pwd1").style.borderColor = "#E34234";
    
        
      flag=false;
      }
    else
	{
		document.getElementById('error1').innerHTML=" ";
		document.getElementById("pwd1").style.borderColor = "#ccc";
	}

if(pwd2.value== "" ) {
    
    
	  document.getElementById('error2').innerHTML=" This field is required!";
	  document.getElementById("pwd2").style.borderColor = "#E34234";
	    
	        
	       flag=false;
	      }
	    else
		{
			document.getElementById('error2').innerHTML=" ";
			document.getElementById("pwd2").style.borderColor = "#ccc";
		}
if (pwd1.value!=pwd2.value) {
    
	   document.getElementById('error2').innerHTML="New password and confirm password must be same!";
	   //document.getElementById("pass1").style.borderColor = "#E34234";
	   document.getElementById("pwd2").style.borderColor = "#E34234";
	   flag=false;
	    }
      return flag;

    
  
 });
  });