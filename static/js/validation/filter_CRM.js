$(document).ready(function(){	
	//alert("LLLL");
	$("#id_filter").click(function() {
	  flag=true;
	  if(from_dt.value==""){
	   document.getElementById('error7').innerHTML=" This field is required!";
		document.getElementById("from_dt").style.borderColor = "#E34234";
	   flag=false; 
	  }
	  if(to_dt.value==""){
		   document.getElementById('error8').innerHTML=" This field is required!";
			document.getElementById("to_dt").style.borderColor = "#E34234";
		   flag=false; 
		  }
     return flag;
	});
	
});

