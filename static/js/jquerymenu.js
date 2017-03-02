$(function(){

   

  var menu = $('#menu'),

    pos = menu.offset();

     

    $(window).scroll(function(){

      if($(this).scrollTop() > pos.top+menu.height() && menu.hasClass('navbar-static-top')){

        menu.fadeOut(1, function(){

          $(this).removeClass('navbar-static-top').addClass('fixed').fadeIn('slow');

        });

      } else if($(this).scrollTop() <= pos.top && menu.hasClass('fixed')){

        menu.fadeOut(1, function(){

          $(this).removeClass('fixed').addClass('navbar-static-top').fadeIn('slow');

        });

      }

   });

 

});