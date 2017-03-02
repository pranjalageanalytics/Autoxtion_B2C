
$(document).ready(function()
{
$("#notificationLink").click(function()
{
$("#notificationContainer").fadeToggle(300);
$("#notification_count").fadeOut("slow");
return false;
});

//Document Click hiding the popup
$(document).click(function()
{
$("#notificationContainer").hide();
});

//Popup on click
$("#notificationContainer").click(function()
{
return false;
});

$("#see_all").click(function(){
	//alert("mark as read");
	$.ajax({
			url:'/inbox/notifications/mark-all-as-read/',
			type: "GET",

		}).done(function(data){
			   console.log(data);
		});
    window.location.href = "/inbox/notifications/";
});
$("#emergency_count_link").click(function(){
	//alert("mark as emg read");
	$.ajax({
			url:'/inbox/notifications/api/read_emg/',
			type: "GET",

		}).done(function(data){
			   console.log(data);
		});

});

$(".normal_count_link").click(function(){
	//alert("mark as normal read");
	$.ajax({
			url:'/inbox/notifications/api/read_normal/',
			type: "GET",

		}).done(function(data){
			   console.log(data);
		});

});
});
