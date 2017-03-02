 $(document).ready(function(){
	//alert("Hello");

  var group=$("#group").val();
  //alert("group="+group);
  if(group=="Customer")
  {
   $("#crm").hide();
   $("#footer_crm").hide();
   $("#ebc").hide();
   $("#enroll").hide();
   $("#footer_dashboard").hide();
   $("#dashboard_cust").hide();
   $("#add_promotion").hide();
   $('#act').hide();
   $('.act_del').hide();
   $('.link_n').removeAttr("href");
   $("#mem_dash").hide();
   $("#col_cust").hide();
   $(".cust_name").hide();
   $("#promo_hide").hide();
   $("#address_member").hide();
   $("#promotion_mem").hide();
$("#appointment_history").hide();
 
  }
  else if(group=="Member") {
   $("#add_request").hide();
   $("#add_feedback").hide();
   $("#cust_dash").hide();
   $("#desc").hide();
   $(".desc").hide();
   $("#footer_vehicle").hide();
   $("#vehicle").hide();
   $("#req").hide();
   $(".req_del").hide();
   $(".from_time").hide();
   $(".to_time").hide();
   $("#address_customer").hide();
   $("#ebc_cust").hide();
   $("#promotion_cust").hide();
  }
  else if(group=="E_Customer"){
	  
	  $("#menubar").hide();
	  $("#ebc").hide();
	  $("#footer_1").hide();
	  $("#footer_2").hide();
	  $("#address_member").hide();
	 $("#tab2").hide();
	 $("#tab2default").hide();
$("#appointment_history").hide();

  }
  });