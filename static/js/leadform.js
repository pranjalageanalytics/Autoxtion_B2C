$(document).ready(function () {
		
	//alert("page loaded");
    // Code adapted from http://djangosnippets.org/snippets/1389/  
    function updateElementIndex(el, prefix, ndx) {
    	
        var id_regex = new RegExp('(' + prefix + '-\\d+-)');
        var replacement = prefix + '-' + ndx + '-';
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
        replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
       
        if (el.name) el.name = el.name.replace(id_regex, replacement);
        
    }

    function deleteForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (formCount > 1) {
            // Delete the item/form
            $(btn).parents('.item').remove();
            var forms = $('.item'); // Get all the forms  
            // Update the total number of forms (1 less than before)
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            var i = 0;
            // Go through the forms and set their indices, names and IDs
            for (formCount = forms.length; i < formCount; i++) {
                $(forms.get(i)).children().children().each(function () {
                    if ($(this).attr('type') == 'text') updateElementIndex(this, prefix, i);
                });
            }
        } // End if
        else {
            //alert("You have to enter at least one Vehicle item!");
        }
        return false;
    }

    function addForm(btn, prefix) {
    	
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        console.log('form is added');
        
        // You can only submit a maximum of 10 todo items 
        if (formCount < 10) {
        	
            // Clone a form (without event handlers) from the first form
            var row = $(".item:first").clone(false).get(0);
            // Insert it after the last form
            $(row).removeAttr('id').hide().insertAfter(".item:last").slideDown(300);

            // Remove the bits we don't want in the new row/form
            // e.g. error messages
            $(".errorlist", row).remove();
            $(row).children().removeClass("error");

            // Relabel or rename all the relevant bits
            $(row).find('input,select,textarea').each(function() {
             updateElementIndex(this, prefix, formCount);
             if ( $(this).attr('type') == 'text' )
               $(this).val('');
           });
            $('#id_form-'+formCount+'-company').change(function(){
        		console.log('done');
        		console.log(this);
        		append_data(formCount);
        	});
            // Add an event handler for the delete item/form link 
            $(row).find(".delete").click(function () {
                return deleteForm(this, prefix);
            });
            // Update the total form count
            $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);
        } // End if
        else {
            //alert("Sorry, you can only enter a maximum of ten items.");
        }
        return false;
    }
    // Register the click event handlers
    $("#add").click(function () {
    
        return addForm(this, "form");
    });

    $(".delete").click(function () {
        return deleteForm(this, "form");
    });
    
  
		
});
function append_data(formcount){
	console.log(formcount);
	dict1=null;
	arr=[];
	array1={};
	array2=[];
	id1=null;
	id2=null;
	id3=null;
	company=$('#id_form-'+formcount+'-company option:selected ').text();
	console.log(company);
	$.ajax({
		url:'/CRM/get_models/',
		type: "GET",
		data:{company:company},
	}).done(function(data)
			{
				
				 console.log(data);
				 dict1=data;
				 $("#id_form-"+formcount+"-companymodel").empty();
				 $("#id_form-"+formcount+"-companymodel").prepend("<option selected>Please Select</option>");
				 $.each(data,function(key,value)
				{
					 console.log("for data"+key);
					 $("#id_form-"+formcount+"-companymodel").append('<option value="'+data[key].id+'">'+data[key].model_name+'</option>');
					 
				}		 
				
				 
				 );
				 
	array2=[];
			});
}
	

