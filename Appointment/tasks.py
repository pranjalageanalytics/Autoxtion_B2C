from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from .emails import *
from django.conf import settings
logger = get_task_logger(__name__)
from celery.schedules import crontab
from celery.task import periodic_task
from notifications.signals import notify
from datetime import datetime, timedelta
from CRM.models import *
from Appointment.models import *
from Registration.models import *
from django.contrib.auth.models import User, Group
from push_notifications.models import  APNSDevice
from fcm_django.models import FCMDevice
from django.db.models import Q

@task(name="send_appointment_create_task")
def send_appt_create_task(date,from_time,to_time,description,first_name,phone_no,shop_name,shop_address,cust_email,mem_email,website):
    logger.info("send appointment create task")
    
    return send_appointment_create_email(date,from_time,to_time,description,first_name,phone_no,shop_name,shop_address,cust_email,mem_email,website)

@task(name="send_appointment_delete_task")
def send_appt_delete_task(shop,name,email,address,phone,cust_email,website):
    logger.info("send appointment delete task")
    return send_appointment_delete_email(shop,name,email,address,phone,cust_email,website)

@task(name="send_appointment_done_task")
def send_appt_done_task(shop,name,email,address,phone,cust_email, coment,website):
    logger.info("send appointment done task")
    return send_appointment_done_email(shop,name,email,address,phone,cust_email, coment,website)

@task(name="send_appointment_update_task")
def send_appt_update_task(date,from_time,to_time,coment,description,first_name,phone_no,shop_name,shop_address,cust_email,mem_mail,mem_name,website):
    logger.info("send appointment update task")

    return send_appointment_update_email(date,from_time,to_time,coment, description,first_name,phone_no,shop_name,shop_address,cust_email,mem_mail,mem_name,website)

@periodic_task(
    run_every=(crontab(minute='40',hour="0")),
    #run_every=(timedelta(seconds=30)),
    name="check_appointment_date",
    ignore_result=False
)


def check_appointment_date():
    logger.info("in check appointment date")
    status=Status.objects.get(status="Scheduled")
    appointment_list=MemberAppointment.objects.filter(status=status)
    today=datetime.today()

    for appointment_obj in appointment_list:
        #logger.info(str(appointment_obj.pk)+"appointment time is"+str(appointment_obj.date)+" yesterdays date is "+str(today))
        date_diff=appointment_obj.date-today.date()
        logger.info("date difference="+str(date_diff))
        cust_detail=Lead.objects.get(pk=appointment_obj.customer.pk)
        mem_detail=UserProfile.objects.get(pk=appointment_obj.member.pk)
        if date_diff.days==1:
            #logger.info("date diff is one")
            lead_u=lead_user.objects.get(customer=appointment_obj.customer)
            #logger.info("lead user id="+str(lead_u.customer.pk))
            mem_detail=User.objects.get(pk=appointment_obj.member.user.pk)
            userprofile=UserProfile.objects.get(pk=appointment_obj.member.pk)
            notify.send(appointment_obj.customer.member,recipient=lead_u.user,verb="has sent you a reminder about tomorrows appointment")
            send_appointment_reminder_mail(appointment_obj.date,appointment_obj.from_time,appointment_obj.to_time,mem_detail.first_name,userprofile.phone_no,userprofile.shop_name,userprofile.shop_address,cust_detail.email,cust_detail.name,userprofile.website)        
        else:
            logger.info("date difference is="+str(date_diff.days))

@periodic_task(
    run_every=(crontab(minute='0',hour="2")),
    #run_every=(timedelta(seconds=10)),
    name="checkPendingEffort",
    ignore_result=False
)
           
def checkPendingEffort():
    logger.info("in check pending effort")
    try:
        status=Status.objects.get(status="Scheduled")
        appointment_obj=MemberAppointment.objects.filter(status=status)
        for appointment_obj1 in appointment_obj:
            upsell_list=UpcellAppointment.objects.filter(appointment=appointment_obj1.id)
            today=datetime.today()
            for upsell_obj1 in upsell_list:
                date_diff=today.date()-upsell_obj1.created_at
                if date_diff.days == 10:
                    if upsell_obj1.accept== False :
                        lead_u=lead_user.objects.get(customer=appointment_obj1.customer)
                        notify.send(appointment_obj1.customer.member,recipient=lead_u.user,verb="has sent you a remainder that extra effort for your appointment is still pending",app_name="Appointment",activity="Add_upsell",object_id=upsell_obj1.pk)
          
    except UpcellAppointment.DoesNotExist as e:
        logger.info("date difference in upsell is:"+str(date_diff.days))


@periodic_task(
    run_every=(crontab(minute='15',hour="2")),
    #run_every=timedelta(seconds=20),
    name="appointment_reminder_six_month",
    ignore_result=False
)

def appointment_reminder_six_month():
    logger.info("in appointment_reminder_three_month")
    status=Status.objects.get(status="Job Completed")
    service_type1=Service.objects.get(service_type="Log Book Service")
    service_type2=Service.objects.get(service_type="Full Car Service")
    appointment_list=MemberAppointment.objects.filter(status=status)
    today=datetime.today()
    print("for loop")
    for appointment in appointment_list:
        if appointment.request:
            print("appointment with request")
            if appointment.request.service_type==service_type1 or appointment.request.service_type==service_type2:
                print("within appointment with request with service type ",appointment.request.service_type," for ",appointment.pk)
                if appointment.date_update:
                    print("in update date")
                    date_diffrence=today.date()-appointment.date_update
                    print("difference--------------",date_diffrence,"--------",(date_diffrence.days%90))
                    diff=(date_diffrence.days%90)
                    if diff is 0:
                        print("in three month with request---------------------------------",appointment.pk)
                        send_notification(appointment.request.customer.pk,appointment.request.service_type.pk)

        else:
            if appointment.date_update:
                print("in update date")
                date_diffrence=today.date()-appointment.date_update
                print("difference--------------",date_diffrence,"--------",(date_diffrence.days%90))
                diff=(date_diffrence.days%90)

                if diff is 0:
                    print("in three month without request---------------------------------",appointment.pk)
                    send_notification(appointment.customer.pk,appointment.service_type.pk)

def send_notification(leadid,serviceid):
    try:
        print("in other functions-----------------------")
        service_type=Service.objects.get(pk=serviceid)
        lead_obj=Lead.objects.get(pk=leadid)
        lead_user_obj=lead_user.objects.get(customer=lead_obj)
        print("user id=",lead_user_obj.user.email)
        message="Your "+str(service_type)+" is pending"
        #notifications for ios
        try:        
            deviceiOS = APNSDevice.objects.filter(user=lead_user_obj.user.pk)
            message_sent=deviceiOS.send_message(message)
        except Exception as e:
            print("exception------------------------------------------",e.message)
                        #notifications for ios end
                        #notifications for android
        try: 
            device = FCMDevice.objects.filter(user=lead_user_obj.user.pk)
            device.send_message("Service Reminder",message)
                            #print("message sent")
        except Exception as e:
            print("exception------------------------------------------",e.message)
                         #notifications for android end 

    except Exception as e:
        print(e)
