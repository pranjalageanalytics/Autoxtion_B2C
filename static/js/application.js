$(function() {
	$("#submit_frm ").click(function() {
		  
		   var c=$("#credit_card_number").val();
		   flag=true;
		      if(c==""){
		    document.getElementById('error6').innerHTML=" This Field Required!";
		       document.getElementById("credit_card_number").style.borderColor = "#E34234";

		   flag=false;
		    } 
		      else {
		       $("#error6").hide();
		        document.getElementById("credit_card_number").style.borderColor = "#ccc";
		    }
		     if(c!=""){
		      if(c.length!=16){
		       $("#error6").show();
		       document.getElementById('error6').innerHTML=" Card Number must be 16 digit long!";
		          document.getElementById("credit_card_number").style.borderColor = "#E34234";

		      flag=false;
		       }
		      
		     }
		     var d=$("#cvv").val();
		   if(d==""){
		      document.getElementById('error7').innerHTML=" This Field Required!";
		         document.getElementById("cvv").style.borderColor = "#E34234";

		     flag=false;
		      } 
		        else {
		       $("#error7").hide();
		          document.getElementById("cvv").style.borderColor = "#ccc";
		      }
		       if(d!=""){
		        if(d.length!=3 ){
		         $("#error7").show();
		          document.getElementById('error7').innerHTML=" CVV Number must be 3 digit long!";
		            document.getElementById("cvv").style.borderColor = "#E34234";

		        flag=false;
		         }
		        
		       }
		    
		  
		     return flag;
		 });
  $("#user_form").submit(function() {
	  
    if ( $("#credit-card").is(":visible")) {
      var form = this;
      var card = {
        number:   $("#credit_card_number").val(),
        expMonth: $("#expiry_month").val(),
        expYear:  $("#expiry_year").val(),
        cvc:      $("#cvv").val()
      };

      Stripe.createToken(card, function(status, response) {
        if (status === 200) {
          console.log(status, response);
          $("#credit-card-errors").hide();
          $("#last_4_digits").val(response.card.last4);
          $("#stripe_token").val(response.id);
          form.submit();
        } else {
          $("#stripe-error-message").text(response.error.message);
          $("#credit-card-errors").show();
          $("#user_submit").attr("disabled", false);
        }
      });
      
      return false;
      
    } 
    
    return true
    
  });

  $("#change-card a").click(function() {
    $("#change-card").hide();
    $("#credit-card").show();
    $("#credit_card_number").focus();
    return false;
  });

});
