var notify_badge_id;
var notify_menu_id;
var notify_api_url;
var notify_fetch_count;
var notify_unread_url;
var notify_mark_all_unread_url;
var notify_refresh_period = 15000;
var consecutive_misfires = 0;
var registered_functions = [];

function fill_notification_badge(data) {
    var badge = document.getElementById(notify_badge_id);
    if (badge) {
        badge.innerHTML = data.unread_count;
    }
}

function fill_notification_list(data) {
	emergency_count=0;
    normal_count=0;
    var menu = document.getElementById(notify_menu_id);
    //if (menu) {
       // menu.innerHTML = "";
        for (var i=0; i < data.unread_list.length; i++) {
        	
            var item = data.unread_list[i];
            

            if(item.emergency_status==1 && item.unread==1){
            	emergency_count=emergency_count+1;
            	
            }
            else if(!item.emergency_status && item.unread==1){
            	normal_count=normal_count+1;
            	
            }
   var d = new Date(item.timestamp);
   //alert(d);
   var d1 = new Date()
   //alert(d1);
   var seconds = (d1-d)/1000
   var mins= parseInt(seconds/60)
   var hrs1 =(mins/60)
   var hrs = parseInt(mins/60)
   var diff = hrs1-hrs
   var convrt_min = parseInt(diff*60);
   
            var message = ""
            if(typeof item.actor !== 'undefined'){
                message = item.actor;
            }
            if(typeof item.verb !== 'undefined'){
                message = message + " " + item.verb;
            }
            if(typeof item.target !== 'undefined'){
                message = message + " " + item.target;
            }
            if(typeof item.timestamp !== 'undefined'){
                message = message + "<br>" + hrs +" hours "+ " " + convrt_min + " minutes ago <hr style='margin-top:7px;margin-bottom:13px;border: 0;border-top: 1px solid #eee;'>";
            }

            //menu.innerHTML = menu.innerHTML + "<li>"+"<a>"+ message + "</a>" + "</li>";
        }
    //}
       
        document.getElementById("normal_count").textContent=normal_count;
        document.getElementById("emergency_count").textContent=emergency_count;
       // normal_count.innerHTML=normal_count;
       // emergency_count.innerHTML=emergency_count;
}

function register_notifier(func) {
    registered_functions.push(func);
}

function fetch_api_data() {
    if (registered_functions.length > 0) {
        //only fetch data if a function is setup
        var r = new XMLHttpRequest();
        r.open("GET", notify_api_url+'?max='+notify_fetch_count, true);
        r.onreadystatechange = function () {
            if (r.readyState != 4 || r.status != 200) {
                consecutive_misfires++;
            }
            else {
                consecutive_misfires = 0;
                for (var i=0; i < registered_functions.length; i++) {
                    var func = registered_functions[i];
                    func(JSON.parse(r.responseText));
                }
            }
        }
        r.send();
    }
    if (consecutive_misfires < 10) {
        setTimeout(fetch_api_data,notify_refresh_period);
    } else {
        var badge = document.getElementById(notify_badge_id);
        if (badge) {
            badge.innerHTML = "!";
            badge.title = "Connection lost!"
        }
    }
}

setTimeout(fetch_api_data,1000);