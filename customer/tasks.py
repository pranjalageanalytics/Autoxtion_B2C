from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from .models import *
from CRM.models import *
from django.conf import settings
from celery.task import periodic_task
from datetime import datetime, timedelta
logger = get_task_logger(__name__)
from celery.schedules import crontab
from notifications.signals import notify
from Appointment.models import *
from promotion.models import *
from push_notifications.models import  APNSDevice
from fcm_django.models import FCMDevice
from django.db.models import Q

@periodic_task(
    run_every=(crontab(minute='30',hour="0")),
    name="check_customer_request",
    ignore_result=False
)

def check_customer_request():
    #logger.info("in check customer request")
    request_list=customer_request.objects.all()
    today=datetime.today()
    for req in request_list:
        if req.date_request:
            status_obj=Status.objects.get(status="Lead")
            date_diff=today.date()-req.date_request
            #logger.info(str(date_diff.days))
            #logger.info(req.customer.status)
            if date_diff.days>548:
                #logger.info("date greater than 548")
                lead_obj=Lead.objects.get(pk=req.customer.pk)
                lead_obj.status=status_obj
                lead_obj.save()
                #logger.info("chnaged status to Lead of"+str(req.customer.pk))


@periodic_task(
    run_every=(crontab(minute='50',hour="0")),

    name="service_remainder",
    ignore_result=False
)                

def service_remainder():
  
   service_request=Service.objects.get(service_type="Log Book Service")
   
   cust_request=customer_request.objects.filter(service_type=service_request.id)
  
   for cust_request1 in cust_request:
       appointment_list=MemberAppointment.objects.filter(request=cust_request1)

       today=datetime.today()
       for appointment in appointment_list:
           print("in for",appointment)

           if appointment.date_update:
                date_diffrence=today.date()-appointment.date_update

                if date_diffrence.days>90:
                    lead=Lead.objects.get(pk=appointment.customer.pk) 
                    lead_u=lead_user.objects.get(customer=lead) 
                    message=" Your free three months tyre maintenance is due  "
                    #notifications for ios
                    try:        
                        deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                        print("ios devices:",deviceiOS)
                        message_sent=deviceiOS.send_message(message)
                        print("ios Msg sent")

                    except Exception as e:
                        print("exception in ios------------------------------------------",e.message)
                    #notifications for ios end
                    #notifications for android
                    try: 
                        device = FCMDevice.objects.filter(user=lead_u.user.pk)
                        device.send_message("Log book service",message)
                        #print("message sent")
                    except Exception as e:
                        print("exception in andriod------------------------------------------",e.message)
                     #notifications for android end 
                    notify.send(lead.member,recipient=lead_u.user,verb="Your free three months tyre maintenance is due",app_name="log_book_service_remainder",activity="maintenance_due_3months",object_id=appointment.pk)
                    print("notification sent 3 months")
                elif date_diffrence.days==75:
                    lead=Lead.objects.get(pk=appointment.customer.pk) 
                    lead_u=lead_user.objects.get(customer=lead) 
                    message="Remainder for free three months tyre maintenance is due on  "+str(appointment.date_update+timedelta(days=90))
                    #notifications for ios
                    try:        
                        deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                        print("ios devices:",deviceiOS)
                        message_sent=deviceiOS.send_message(message)
                        print("ios Msg sent")

                    except Exception as e:
                        print("exception in ios------------------------------------------",e.message)
                    #notifications for ios end
                    #notifications for android
                    try: 
                        device = FCMDevice.objects.filter(user=lead_u.user.pk)
                        print("devices to which notifications is sent: ",device)
                        device.send_message("Log book service",message)
                        print("message sent")
                    except Exception as e:
                        print("exception in andriod------------------------------------------",e.message)
                     #notifications for android end
                    notify.send(lead.member,recipient=lead_u.user,verb="Remainder for free three months tyre maintenance is due on"+str(appointment.date_update+timedelta(days=90)),app_name="log_book_service_remainder",activity="maintenance_due_15days",object_id=appointment.pk)
                    print("notification sent 15 days")
                elif date_diffrence.days==88:
                    lead=Lead.objects.get(pk=appointment.customer.pk) 
                    lead_u=lead_user.objects.get(customer=lead)
                    message="Remainder for free three months tyre maintenance is due on  "+str(appointment.date_update+timedelta(days=90))
                    #notifications for ios
                    try:        
                        deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                        print("ios devices:",deviceiOS)
                        message_sent=deviceiOS.send_message(message)
                        print("ios Msg sent")
                    except Exception as e:
                        print("exception in ios------------------------------------------",e.message)
                    #notifications for ios end
                    #notifications for android
                    try: 
                        device = FCMDevice.objects.filter(user=lead_u.user.pk)
                        device.send_message("Log book service",message)
                        print("message sent")
                    except Exception as e:
                        print("exception in andriod------------------------------------------",e.message)
                     #notifications for android end  
                    notify.send(lead.member,recipient=lead_u.user,verb="Remainder free three months tyre maintenance is due on"+str(appointment.date_update+timedelta(days=90)),app_name="log_book_service_remainder",activity="maintenance_due_2days",object_id=appointment.pk)
                    print("notification sent 2 days")
                else:
                    print("it is not due yet")  

@periodic_task(
    run_every=(crontab(minute='50',hour="2")),
    #run_every=timedelta(seconds=20),
    name="service_remainder_regochecks",
    ignore_result=False
)                

def service_remainder_regochecks():
  
   service_request=Service.objects.get(service_type="Rego checks - Pink Slip")
   service_request1=Service.objects.get(service_type="Rego checks - Blue Slip")
   service_request2=Service.objects.get(service_type="Rego checks - LPG")

   cust_request=customer_request.objects.filter(Q(service_type=service_request.id) | Q(service_type=service_request1.id) | Q(service_type=service_request2.id))
  
   for cust_request1 in cust_request:
        appointment_list=MemberAppointment.objects.filter(request=cust_request1)
        appointment_create=MemberAppointment.objects.filter(service_type=service_request.id)

        if appointment_list:
           today=datetime.today()
           for appointment in appointment_list:
                if appointment.date_update:
                    date_diffrence=today.date()-appointment.date_update
                    print("log book time diifrence:",(date_diffrence.days%90))
                    date_diff_90=date_diffrence.days%90
                    date_diff_75=date_diffrence.days%75
                    date_diff_88=date_diffrence.days%88
                    
                    if date_diff_90 is 30:
                        print("in if diffrence 90")
                        lead=Lead.objects.get(pk=appointment.customer.pk) 
                        lead_u=lead_user.objects.get(customer=lead) 
                        message=" Your "+str(cust_request1.service_type.service_type)+" maintenance is due "
                        #notifications for ios
                        try:        
                            deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                            print("ios devices:",deviceiOS)
                            message_sent=deviceiOS.send_message(message)
                            print("ios Msg sent")
    
                        except Exception as e:
                            print("exception in ios------------------------------------------",e.message)
                        #notifications for ios end
                        #notifications for android
                        try: 
                            device = FCMDevice.objects.filter(user=lead_u.user.pk)
                            device.send_message("Service Reminder",message)
                            #print("message sent")
                        except Exception as e:
                            print("exception in andriod------------------------------------------",e.message)
                         #notifications for android end 
                        #notify.send(lead.member,recipient=lead_u.user,verb="Your free three months tyre maintenance is due",app_name="log_book_service_remainder",activity="maintenance_due_3months",object_id=appointment.pk)
                        print("notification sent 3 months")
                    elif date_diff_75 is 15:
                        print("in if diffrence 75")

                        lead=Lead.objects.get(pk=appointment.customer.pk) 
                        lead_u=lead_user.objects.get(customer=lead) 
                        message="Remainder for "+str(cust_request1.service_type.service_type)+" maintenance is due "
                        #notifications for ios
                        try:        
                            deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                            print("ios devices:",deviceiOS)
                            message_sent=deviceiOS.send_message(message)
                            print("ios Msg sent")
    
                        except Exception as e:
                            print("exception in ios------------------------------------------",e.message)
                        #notifications for ios end
                        #notifications for android
                        try: 
                            device = FCMDevice.objects.filter(user=lead_u.user.pk)
                            print("devices to which notifications is sent: ",device)
                            device.send_message("Service Reminder",message)
                            print("message sent")
                        except Exception as e:
                            print("exception in andriod------------------------------------------",e.message)
                         #notifications for android end
                       # notify.send(lead.member,recipient=lead_u.user,verb="Remainder for free three months tyre maintenance is due on"+str(appointment.date_update+timedelta(days=90)),app_name="log_book_service_remainder",activity="maintenance_due_15days",object_id=appointment.pk)
                        print("notification sent 15 days")
                    elif date_diff_88 is 0:
                        print("in if diffrence 88")

                        lead=Lead.objects.get(pk=appointment.customer.pk) 
                        lead_u=lead_user.objects.get(customer=lead)
                        message="Remainder for "+str(cust_request1.service_type.service_type)+" maintenance is due "
                        #notifications for ios
                        try:        
                            deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                            print("ios devices:",deviceiOS)
                            message_sent=deviceiOS.send_message(message)
                            print("ios Msg sent")
                        except Exception as e:
                            print("exception in ios------------------------------------------",e.message)
                        #notifications for ios end
                        #notifications for android
                        try: 
                            device = FCMDevice.objects.filter(user=lead_u.user.pk)
                            device.send_message("Service Reminder",message)
                            print("message sent")
                        except Exception as e:
                            print("exception in andriod------------------------------------------",e.message)
                         #notifications for android end  
                        #notify.send(lead.member,recipient=lead_u.user,verb="Remainder free three months tyre maintenance is due on"+str(appointment.date_update+timedelta(days=90)),app_name="log_book_service_remainder",activity="maintenance_due_2days",object_id=appointment.pk)
                        print("notification sent 2 days")
                    else:
                        print("it is not due yet")    
        else:
            for appointment in appointment_create:


               if appointment.date_update:
                    
                    date_diffrence=today.date()-appointment.date_update
                    print("difference----------------------88",(date_diffrence.days%88),"---------",date_diffrence)
                    date_diff_90=date_diffrence.days%90
                    date_diff_75=date_diffrence.days%75
                    date_diff_88=date_diffrence.days%88
                    if date_diff_90 is 30:
                        lead=Lead.objects.get(pk=appointment.customer.pk) 
                        lead_u=lead_user.objects.get(customer=lead) 
                        message=" Your "+str(appointment.service_type.service_type)+" maintenance is due "
                        #notifications for ios
                        try:        
                            deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                            print("ios devices:",deviceiOS)
                            message_sent=deviceiOS.send_message(message)
                            print("ios Msg sent")
    
                        except Exception as e:
                            print("exception in ios------------------------------------------",e.message)
                        #notifications for ios end
                        #notifications for android
                        try: 
                            device = FCMDevice.objects.filter(user=lead_u.user.pk)
                            device.send_message("Service Reminder",message)
                            #print("message sent")
                        except Exception as e:
                            print("exception in andriod------------------------------------------",e.message)
                         #notifications for android end 
                        #notify.send(lead.member,recipient=lead_u.user,verb="Your free three months tyre maintenance is due",app_name="log_book_service_remainder",activity="maintenance_due_3months",object_id=appointment.pk)
                        print("notification sent 3 months")
                    elif date_diff_75 is 15:
                        lead=Lead.objects.get(pk=appointment.customer.pk) 
                        lead_u=lead_user.objects.get(customer=lead) 
                        message="Remainder for "+str(appointment.service_type.service_type)+" maintenance is due "
                        #notifications for ios
                        try:        
                            deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                            print("ios devices:",deviceiOS)
                            message_sent=deviceiOS.send_message(message)
                            print("ios Msg sent")
    
                        except Exception as e:
                            print("exception in ios------------------------------------------",e.message)
                        #notifications for ios end
                        #notifications for android
                        try: 
                            device = FCMDevice.objects.filter(user=lead_u.user.pk)
                            print("devices to which notifications is sent: ",device)
                            device.send_message("Service Reminder",message)
                            print("message sent")
                        except Exception as e:
                            print("exception in andriod------------------------------------------",e.message)
                         #notifications for android end
                       # notify.send(lead.member,recipient=lead_u.user,verb="Remainder for free three months tyre maintenance is due on"+str(appointment.date_update+timedelta(days=90)),app_name="log_book_service_remainder",activity="maintenance_due_15days",object_id=appointment.pk)
                        print("notification sent 15 days")
                    elif date_diff_88 is 2:
                        lead=Lead.objects.get(pk=appointment.customer.pk) 
                        lead_u=lead_user.objects.get(customer=lead)
                        message="Remainder for "+str(appointment.service_type.service_type)+" maintenance is due "
                        #notifications for ios
                        try:        
                            deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                            #print("ios devices:",deviceiOS)
                            message_sent=deviceiOS.send_message(message)
                            print("ios Msg sent")
                        except Exception as e:
                            print("exception in ios------------------------------------------",e.message)
                        #notifications for ios end
                        #notifications for android
                        try: 
                            device = FCMDevice.objects.filter(user=lead_u.user.pk)
                            device.send_message("Service Reminder",message)
                            print("message sent")
                        except Exception as e:
                            print("exception in andriod------------------------------------------",e.message)
                         #notifications for android end  
                        #notify.send(lead.member,recipient=lead_u.user,verb="Remainder free three months tyre maintenance is due on"+str(appointment.date_update+timedelta(days=90)),app_name="log_book_service_remainder",activity="maintenance_due_2days",object_id=appointment.pk)
                        print("notification sent 2 days")
                    else:
                        print("it is not due yet")        
        
                    
@periodic_task(
    #run_every=timedelta(seconds=10),
    run_every=(crontab(minute='30',hour="2")),
    name="service_remainder_logbook_fullcar",
    ignore_result=False
)
def service_remainder_logbook_fullcar():
    print("in demo")
    service_request=Service.objects.get(service_type="Log Book Service")
    service_req=Service.objects.get(service_type="Full Car Service")
    print("service request",service_request)
    print("service request",service_req)
    cust_request=customer_request.objects.filter(Q(service_type=service_request) | Q(service_type=service_req) )
    print("customer request@@@@@@@@@@@@@@@",cust_request)
    for cust_request1 in cust_request:
        print("------------------",cust_request1.pk)
        
        appointment_create=MemberAppointment.objects.filter(service_type=service_request.id)
        appointment_list=MemberAppointment.objects.filter(request=cust_request1)
        print("appointment list",appointment_list)
        today=datetime.today()
        if appointment_list:
            for appointment in appointment_list:
                print("in for if appointment list in logbook_fullcar:",appointment)
      
                if appointment.date_update:
                    date_diffrence=today.date()-appointment.date_update
                    print("@Log_full..diff..:",date_diffrence.days)
                    if date_diffrence.days>180:
                        print("date difference >180",date_diffrence.days>180)
                        lead=Lead.objects.get(pk=appointment.customer.pk) 
                        lead_u=lead_user.objects.get(customer=lead) 
                        notify.send(lead.member,recipient=lead_u.user,verb="Your your periodic maintainence is due",app_name="log_book_service_remainder",activity="maintenance_due_6months",object_id=appointment.pk)
    
                        message="Your your periodic maintainence is due"
                        #notifications for ios
                        try:        
                            deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                            message_sent=deviceiOS.send_message(message)
                        except Exception as e:
                            print("exception------------------------------------------",e.message)
                        #notifications for ios end
                        #notifications for android
                        try: 
                            device = FCMDevice.objects.filter(user=lead_u.user.pk)
                            device.send_message("Service Reminder",message)
                            #print("message sent")
                        except Exception as e:
                            print("exception------------------------------------------",e.message)
                         #notifications for android end 
                        print("notification sent 6 months for ")
                     
                    else:
                        print("it is not due yet")
        else:
            for appointment in appointment_create:
              
               if appointment.date_update:
                    
                    date_diffrence=today.date()-appointment.date_update
                    print("@@@@diff:",date_diffrence.days)
                    if date_diffrence.days>180:
                        lead=Lead.objects.get(pk=appointment.customer.pk) 
                        lead_u=lead_user.objects.get(customer=lead) 
                        message="Your "+appointment.service_type.service_type+" is  due"
                        #notifications for ios
                        try:        
                            deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                            message_sent=deviceiOS.send_message(message)
                        except Exception as e:
                            print("exception------------------------------------------",e.message)
                        #notifications for ios end
                        #notifications for android
                        try: 
                            device = FCMDevice.objects.filter(user=lead_u.user.pk)
                            device.send_message("Service Reminder",message)
                            #print("message sent")
                        except Exception as e:
                            print("exception------------------------------------------",e.message)
                         #notifications for android end 
                       # notify.send(lead.member,recipient=lead_u.user,verb="Your free three months tyre maintenance is due",app_name="log_book_service_remainder",activity="maintenance_due_3months",object_id=appointment.pk)
                        print("notification sent 6 months for ")
  