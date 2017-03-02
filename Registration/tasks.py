from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from .emails import *
import vobject
from .models import *
from datetime import datetime, timedelta
from celery.task import periodic_task
from django.conf import settings
logger = get_task_logger(__name__)
from celery.schedules import crontab
from notifications.signals import notify

@task(name="send_member_mail")
def send_member_task(email, password,shop,website):
    logger.info("in member mail task")
    return send_member_email(email, password,shop,website)


@task(name="ws_member_send_businesscard__mail")
def ws_member_send_businesscard__mail(email,member_email,name):
    
    print("from task",email,member_email)
    logger.info("in sending business card  task")
    return send_vcf_mail1(email,member_email,name)

@task(name="send_vcf_mail")
def send_vcf_email_task(mail,member_mail,name,mem_detail):
    print("in send mail",mail)
    logger.info("in send vcf mail task")
    return send_vcf_mail(mail,member_mail,name,mem_detail)

@task(name="send_vcf_mail1")
def send_vcf_email_task1(mail,member_mail,name):
    print("in send mail1",mail)
    print("in sebd email memeber",member_mail)
    logger.info("in send vcf mail task")
    return send_vcf_mail1(mail,member_mail,name)

@periodic_task(
    #run_every=(timedelta(minute=30)),
    run_every=(timedelta(seconds=30)),
    name="make_existing_member_businesscard",
    ignore_result=False
)


def make_existing_member_businesscard():
    
    member=UserProfile.objects.all()
    for memberemail in member:
        
         user1=User.objects.get(pk=memberemail.user.id)
         email=user1.email
         f=open("static/vcards/"+email+".vcf",'w+')
         j = vobject.vCard()
         o = j.add('fn')
         o.value = user1.first_name+" "+user1.last_name
         o = j.add('n')
         o.value = vobject.vcard.Name( family=user1.last_name,given=user1.first_name )
         j.add('email')
         j.email.value = email
         j.email.type_param = 'INTERNET'
         j.email.type_param = 'HOME'
         j.add('tel')
         j.tel.type_param="cell"

         j.tel.value=str(memberemail.phone_no)
         str1=memberemail.shop_address+","+memberemail.city

         o = j.add('note')
         o.value =str1+",Australia"
         j.add('url')
         j.url.value=memberemail.website
         #j.add('adr')
         #j.adr.value=str1+",Australia"
         #j.adr.type_param='ADR-component-locality'
         f.write(j.serialize())
         f.close()

@periodic_task(
    #run_every=(timedelta(seconds=20)),
    run_every=(crontab(minute='0',hour="5")),
    name="check_expiration_mechanic_license_date",
    ignore_result=False
)


def check_expiration_mechanic_license_date():
    logger.info("in check exp date mechanic license task")
   # print("in license task")
    license_list=UserProfile.objects.all()
     
    today=datetime.today()
    for license in license_list:
        if license.member_mech_license_expiry_date:
            #logger.info("vehicle is "+str(vehicle.pk)+" and reg expiry date is"+str(vehicle.reg_expiry_date)+" lead--"+str(vehicle.lead.phone))
            date_diff=license.member_mech_license_expiry_date-today.date()
           # print("date difference",date_diff)
            member_user=User.objects.get(pk=license.user.pk)
            if date_diff.days==0:
                 logger.info("date is equal to 0")
                 notify.send(member_user,recipient=member_user,verb="Your mechanic license is expiring today.Please renew your license",app_name="remainder_mech_license_expiry_date",activity="mec_license_due_1months",object_id=license.pk)
            elif date_diff.days==30:
                 logger.info("date is equal to 30")
                 notify.send(member_user,recipient=member_user,verb="Your mechanic license  is going to expire after 30 days on " +str(license.member_mech_license_expiry_date)+" ",app_name="remainder_mech_license_expiry_date",activity="mec_license_due_1months",object_id=license.pk)
            elif date_diff.days==15:
                 logger.info("date is equal to 15")
                 notify.send(member_user,recipient=member_user,verb="Your mechanic license is going to expire after 15 days on " +str(license.member_mech_license_expiry_date)+" ",app_name="remainder_mech_license_expiry_date",activity="mec_license_due_1months",object_id=license.pk)
   
            else:
                 logger.info("date is not equal to 30")
        else:
             logger.info("no date available")         
             
             
@periodic_task(
    run_every=(timedelta(seconds=30)),
    #run_every=(crontab(minute='12',hour="5")),
    name="check_expiration_arc_license_date",
    ignore_result=False
)


def check_expiration_arc_license_date():
    logger.info("in check exp date mechanic license task")
   # print("in license task")
    license_list=UserProfile.objects.all()
     
    today=datetime.today()
    for license in license_list:
        if license.member_ARC_license_expiry_date:
            #logger.info("vehicle is "+str(vehicle.pk)+" and reg expiry date is"+str(vehicle.reg_expiry_date)+" lead--"+str(vehicle.lead.phone))
            date_diff=license.member_ARC_license_expiry_date-today.date()
           # print("date difference",date_diff)
            member_user=User.objects.get(pk=license.user.pk)
            if date_diff.days==0:
                 logger.info("date is equal to 0")
                 notify.send(member_user,recipient=member_user,verb="Your ARC license is expiring today.Please renew your license",app_name="remainder_mech_license_expiry_date",activity="arc_license_due_1months",object_id=license.pk)
            elif date_diff.days==30:
                 logger.info("date is equal to 30")
                 notify.send(member_user,recipient=member_user,verb="Your ARC license  is going to expire after 30 days on " +str(license.member_ARC_license_expiry_date)+" ",app_name="remainder_arc_license_expiry_date",activity="arc_license_due_1months",object_id=license.pk)
            elif date_diff.days==15:
                 logger.info("date is equal to 15")
                 notify.send(member_user,recipient=member_user,verb="Your ARC license is going to expire after 15 days on " +str(license.member_ARC_license_expiry_date)+" ",app_name="remainder_arc_license_expiry_date",activity="arc_license_due_1months",object_id=license.pk)
   
            else:
                 logger.info("date is not equal to 30")
        else:
             logger.info("no date available")  