$(document).ready(function(){
//alert("Page is loaded");
$("#submit_frm").click(function(){
	//alert("button  is clicked");
    var pass1 = document.getElementById("pass1").value;
    //alert("Page is loaded");
    var pass2 = document.getElementById("pass2").value;
    var ok = true;
    if (pass1 != pass2) {
        //alert("Passwords Do not match");
        document.getElementById("pass1").style.borderColor = "#E34234";
        document.getElementById("pass2").style.borderColor = "#E34234";
        //alert("Passwords does not Match!!!");
        ok = false;
    }
    else {
        ok=true;
    }
    return ok;
});
});