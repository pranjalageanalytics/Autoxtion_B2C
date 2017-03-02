$(document).ready(function(){
	
	 new_image=$(".image_get > a").attr("href");
	 //alert( $(".image_get > a").attr("href"));
	 var image_holder = $("#image-holder");
     image_holder.empty();
     $("<img />", {
         "src": new_image,
         "class": "thumb-image"
       }).appendTo(image_holder);
     image_holder.show();
     
});