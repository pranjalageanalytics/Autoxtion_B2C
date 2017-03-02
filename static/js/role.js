 $(document).ready(function(){
	//alert(" out side Hello");

  var group=$("#group").val();
  //alert("group="+group);
  if(group=="Customer")
  {
//alert("Hello");

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
   $("#footer_faq").hide();
   $("#promotion_mem").hide();
      $("#add_appointment").hide();
$("#appointment_history").hide();
$("#vcard_button").hide();
$("#id_video").hide();
  }
  
  else if(group=="Lead") {
$("#id_video").hide();
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
	   $("#footer_faq").hide();
	   $("#promotion_mem").hide();
	      $("#add_appointment").hide();
$("#appointment_history").hide();
$("#vcard_button").hide();
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
   //$(".req_edit_link").removeAttr("href");
   $(".leadlist_id").hide();
   $("#promotion_cust").hide();
   $("#history").hide();
   $(".acc_upsell").hide();
   
  }
  
  else if(group=="E_Customer"){
	  $("#id_video").hide();
	  $("#menubar").hide();
	  $("#ebc").hide();
	  $("#footer_1").hide();
	  $("#footer_2").hide();
	  $("#address_member").hide();
	 $("#tab2").hide();
	 $("#tab2default").hide();
	 $("#enroll").hide();
	 $("#footer_faq").hide();
	$("#sidenav01").hide();
           $("#add_appointment").hide();
$("#appointment_history").hide();
$("#vcard_button").hide();
  }
 else if(group=="Company"){
	  //alert("company");
	  $("#add_request").hide();
	  $("#req").hide();
	  $("#act").hide();
      $("#save_req").hide();
      $(".req_del").hide();
	  $("#crm").hide();
	  $("#id_video").hide();
	  $("#appointment_history").hide();
	  $("#add_appointment").hide();
	  $('.act_del').hide();
	  $("#dashboard_cust").hide();
	  $("#promotion_mem").hide();
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

   $("#promo_hide").hide();
   $("#address_member").hide();
   $("#footer_faq").hide();
   $("#promotion_mem").hide();
      $("#add_appointment").hide();
$("#appointment_history").hide();
$("#vcard_button").hide();
$("#member_emer_req").hide();
$("#appointment_act").hide();
$("#appoint_action").hide();
$("#request_id").hide();
$("#request_id").hide();
$("#job_done").hide();
  }


  });