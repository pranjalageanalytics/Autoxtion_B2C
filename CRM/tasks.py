from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from .emails import *
from .sms import *
from Autoxtion_B2C.settings.base import BASE_DIR
from celery.schedules import crontab
logger = get_task_logger(__name__)
from celery.task import periodic_task
import xlrd
from .models import *
import random
import string
import os
from notifications.signals import notify
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from Registration.models import *
from datetime import datetime, timedelta
from push_notifications.models import  APNSDevice
from fcm_django.models import FCMDevice



@task(name="send_lead_mail")
def send_lead_task(email,name,password,phone,shop,address,lead_mail,fname,mem_mail,website):
    """sends an email when lead saved successfully"""

    logger.info("in send lead mail task")
    return send_lead_email(email,name,password,phone,shop,address,lead_mail,fname,mem_mail,website)

@task(name="send_existing_customer_mail")
def send_ext_customer_task(email,name,password,phone,shop,address,lead_mail,mem_mail,website):
    """sends an email when lead saved successfully"""
    print("member email",mem_mail)
    logger.info("in sending existing customer mail task")
    return send_ext_customer_mail(email,name,password,phone,shop,address,lead_mail,mem_mail,website)

@task(name="send_new_credentials")
def send_new_credentials(email,name,password,phone,shop,address,lead_mail,fname,mem_mail,website):
    """sends an email when lead saved successfully"""

    logger.info("in send lead mail task")
    return send_lead_generate(email,name,password,phone,shop,address,lead_mail,fname,mem_mail,website)

@task(name="send_lead_sms_task")
def send_lead_sms_task(number,message):
    logger.info("in sending lead sms task")
    return send_lead_sms(number,message)

@task(name="send_driver_mail_task")
def send_driver_mail_task(lead_id,company_id,member_auth_id,password):
    logger.info("in sending driver mail task")
    return send_driver_mail(lead_id,company_id,member_auth_id,password)

@task(name="send_company_mail_task")
def send_company_mail_task(company_id,member_auth_id,password):
    logger.info("in sending company mail task")
    return send_company_mail(company_id,member_auth_id,password)


@periodic_task(
    run_every=(crontab(minute='20',hour="0")),
    #run_every=(timedelta(seconds=40)),
    name="check_expiration_vehicle_date",
    ignore_result=False
)


def check_expiration_vehicle_date():
    logger.info("in check exp date vehicle task")
    vehicle_list=Lead_Vehicle.objects.all()
    today=datetime.today()
    for vehicle in vehicle_list:
        if vehicle.reg_expiry_date:
                #logger.info("vehicle is "+str(vehicle.pk)+" and reg expiry date is"+str(vehicle.reg_expiry_date)+" lead--"+str(vehicle.lead.phone))
         	l_u=None
		try:
                	l_u=lead_user.objects.get(customer=vehicle.lead)
		except Exception as e:
			auth_u=User.objects.get(email=vehicle.lead.member.email)
			l_u=lead_user(customer=vehicle.lead,user=auth_u)
			l_u.save()

                date_diff=vehicle.reg_expiry_date-today.date()
                if date_diff.days==30:
                    #logger.info("date is equal to 30:")
                    notify.send(l_u.user,recipient=l_u.user,verb="Your vehicle registration is going to expire after 30 days on "+str(vehicle.reg_expiry_date),app_name="CRM",activity="Vehicle_registration_expiry",object_id=vehicle.pk)
                    new_message="Your vehicle registration is going to expire after 30 days on "+str(vehicle.reg_expiry_date)
                    reg_expiry_push_notifications(l_u.pk,new_message)
                elif date_diff.days==15:          
                    #logger.info("date is equal to 15 : ")
                    notify.send(l_u.user,recipient=l_u.user,verb="Your vehicle registration is going to expire after 15 days on "+str(vehicle.reg_expiry_date),app_name="CRM",activity="Vehicle_registration_expiry",object_id=vehicle.pk)
                    new_message="Your vehicle registration is going to expire after 15 days on "+str(vehicle.reg_expiry_date)
                    reg_expiry_push_notifications(l_u.pk,new_message)
                elif date_diff.days==0:
                    #print("date is equal to 0")
                    notify.send(l_u.user,recipient=l_u.user,verb="Your vehicle registration is going to expire today.Please renew your license.",app_name="CRM",activity="Vehicle_registration_expiry",object_id=vehicle.pk)
                    new_message="Your vehicle registration is going to expire today.Please renew your license."
                    reg_expiry_push_notifications(l_u.pk,new_message)
                    print("push notifications sent")
                else:
                    logger.info("date is not equal to 30")
        else:
            logger.info("no date available")


def reg_expiry_push_notifications(l_uid,new_message):
        #print("in def reg_expiry_push_notifications")
        l_u=lead_user.objects.get(pk=l_uid)
        print("user id=",l_u.user.email)
        #notifications for ios
        try:        
            deviceiOS = APNSDevice.objects.filter(user=l_u.user)
            message_sent=deviceiOS.send_message(new_message)
        except Exception as e:
            print("exception------------------------------------------",e.message)
                        #notifications for ios end
                        #notifications for android
        try: 
            device = FCMDevice.objects.filter(user=l_u.user)
            device.send_message("Remainder Vehicle Expiry",new_message)
            print("message sent")
        except Exception as e:
            print("exception------------------------------------------",e.message)
                         #notifications for android end 

@task(name="import_excel_data")
def import_lead_vehicle_data(id,user_id):
         logger.info("inside import lead vehicle data")
         #print(id)
  
         user1=User.objects.get(pk=user_id)
         detail2 = get_object_or_404(UserProfile,user=user1)
         jj=0
         try:
             obj=UploadFile.objects.get(pk=id)
             path=os.path.join(BASE_DIR,"media")
             #print(path)
             #print(obj.file.name)
             book=xlrd.open_workbook(path+"/"+obj.file.name,"rb")
             sheet1=book.sheet_by_index(0)
             status=Status.objects.get(status="Customer")

               
             for r in range(1,sheet1.nrows):
                  jj=jj+1
                  #print(jj)
                  fname=sheet1.cell(r,0).value
                  lname=sheet1.cell(r,1).value
                  email=sheet1.cell(r,2).value
                  
                  lead_obj=Lead(name=fname+" "+lname,email=email,status=status,member=user1)
                  
                  lead_obj.save()
                  #print("------------------ob save")
                  digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
                  chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
                  p=(digits + "@156"+chars)
                  if email !="" and phone_no =="":
                      user = User.objects.create_user(username=email,
                                                   email=email,
                                                   password =p, 
                                                   first_name=fname)
                   
                      user.groups.add(Group.objects.get(name='Customer'))
                      Lead_user=lead_user(customer=lead_obj,user=user)
                      Lead_user.save()
                      vehicle_no1= sheet1.cell(r,4).value
                      vehicle_no=str(vehicle_no1)
                      company_id1= sheet1.cell(r,5).value
                      #print("CCCCCCCCCCCCCCCCCCCCCCCC",str(company_id1))
                      company_name=Company.objects.get(company_name=str(company_id1)) 
                      model_id1= sheet1.cell(r,6).value
                  
                      model_name=Company_Model.objects.get(model_name=str(model_id1),company=company_name)     
                      makeyear_id1= sheet1.cell(r,7).value
                  
                      mk=int(makeyear_id1)
                      make_year=Make_Year1.objects.get(make_year=str(mk)) 
                      obj=Lead_Vehicle.objects.create(vehicle_no=vehicle_no,company=company_name,
                                                     lead=lead_obj,
                                                     model=model_name,
                                                     makeyear=make_year,
                                                     ) 
                      obj.save()
                      i=i+1 
                      #email,name,password,phone,shop,address,lead_mail,fname,mem_mail,website
                      send_lead_task.delay(user.username,user1.first_name,p,detail2.phone_no ,detail2.shop_name,detail2.shop_address,user1.first_name,user1.email,detail2.website,user1.email)
              
                  if phone_no !="" and email =="": 
                      user = User.objects.create_user(username=phone_no,
                                                   password =p, 
                                                   first_name=fname)
                   
                      user.groups.add(Group.objects.get(name='Customer'))
                      Lead_user=lead_user(customer=lead_obj,user=user)
                      Lead_user.save()
                      vehicle_no=str(vehicle_no1)
                      company_id1= sheet1.cell(r,5).value
                      #print("CCCCCCCCCCCCCCCCCCCCCCCC",str(company_id1))
                      company_name=Company.objects.get(company_name=str(company_id1)) 
                      model_id1= sheet1.cell(r,6).value
                  
                      model_name=Company_Model.objects.get(model_name=str(model_id1),company=company_name)     
                      makeyear_id1= sheet1.cell(r,7).value
                  
                      mk=int(makeyear_id1)
                      make_year=Make_Year1.objects.get(make_year=str(mk)) 
                      obj=Lead_Vehicle.objects.create(vehicle_no=vehicle_no,company=company_name,
                                                     lead=lead_obj,
                                                     model=model_name,
                                                     makeyear=make_year,
                                                     ) 
                      obj.save()
                      i=i+1 
                      #email,name,password,phone,shop,address,lead_mail,fname,mem_mail,website
                      #send_lead_task.delay(user.username,user1.first_name,p,detail2.phone_no ,detail2.shop_name,detail2.shop_address,user1.first_name,user1.email,detail2.website,user1.email)
                      message="Welcome to AutoXtion Communication Platform. \n" \
                            "We are revolutionising the we interact with each other.\n " \
                            "Kindly Login to http://portal.autoxtion.com.au/registration/login/ " \
                            "to access the portal.\n" \
                            " Your credentials are - \n Username :  "+user.username+ \
                            "\n Password :  "+p+ \
                            "\n Thank You \n "+member_d.first_name+"\n "+detail2.shop_name+" \n "+detail2.shop_address+"\n "+str(detail2.phone_no)
                      #print("$$$$$$############@@@@@@@@@@@@@@!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                      #print('+61'+user.username)
                      send_lead_sms_task.delay('+61'+user.username,message)
                      try:
                          member_sms=Member_SMS.objects.get(member=user1)
                      except Member_SMS.DoesNotExist as e:
                      #print("object does not exist",e)
                          member_sms=Member_SMS()
                          member_sms.member=user1
                          member_sms.count=0
                          member_sms.save()
                      member_sms.count=member_sms.count+1
                      member_sms.save()
                  
                  
                  if email !="" and phone_no !="":
                      user = User.objects.create_user(username=email,
                                                   email=email,
                                                   password =p, 
                                                   first_name=fname)
                   
                      user.groups.add(Group.objects.get(name='Customer'))
                      Lead_user=lead_user(customer=lead_obj,user=user)
                      Lead_user.save()
              
                      vehicle_no1= sheet1.cell(r,4).value
                      vehicle_no=str(vehicle_no1)
                      company_id1= sheet1.cell(r,5).value
                      #print("CCCCCCCCCCCCCCCCCCCCCCCC",str(company_id1))
                      company_name=Company.objects.get(company_name=str(company_id1)) 
                      model_id1= sheet1.cell(r,6).value
                  
                      model_name=Company_Model.objects.get(model_name=str(model_id1),company=company_name)     
                      makeyear_id1= sheet1.cell(r,7).value
                  
                      mk=int(makeyear_id1)
                      make_year=Make_Year1.objects.get(make_year=str(mk)) 
                      obj=Lead_Vehicle.objects.create(vehicle_no=vehicle_no,company=company_name,
                                                     lead=lead_obj,
                                                     model=model_name,
                                                     makeyear=make_year,
                                                     ) 
                      obj.save()
                      i=i+1 
                      #email,name,password,phone,shop,address,lead_mail,fname,mem_mail,website
                      send_lead_task.delay(user.username,user1.first_name,p,detail2.phone_no ,detail2.shop_name,detail2.shop_address,user1.first_name,user1.email,detail2.website,user1.email)
                      
             notify.send(user1,recipient=user1,verb="Your data uploaded successfully")
         except Exception as e:
             #print("------------########",e)
             notify.send(user1,recipient=user1,verb=" data upload failed. Error at line "+str(jj))

@periodic_task(
    run_every=(timedelta(seconds=40)),
    #run_every=(crontab(minute='0',hour="4")),
    name="check_expiration_license_date",
    ignore_result=False
)


def check_expiration_license_date():
    logger.info("in check expiration date license task")
    try:
        lead_list=Lead.objects.all()
        today=datetime.today()
        for lead in lead_list:
            if lead.license_expiry_date:
                date_diff=lead.license_expiry_date-today.date()
                l_u=None
                try:
                    l_u=lead_user.objects.get(customer=lead)
                except Exception as e:
                    auth_u=User.objects.get(email=lead.email)
                    l_u=lead_user(customer=lead,user=auth_u)
                    l_u.save()

                if date_diff.days==30:
                    logger.info("date is equal to 30:")
                    notify.send(l_u.user,recipient=l_u.user,verb="Your License is going to expire after 30 days on "+str(lead.license_expiry_date),app_name="CRM",activity="License_expiry",object_id=lead.pk)
                    new_message="Your driving license is going to expire after 30 days on "+str(lead.license_expiry_date)
                    check_expiration_license_date_push_notifications(l_u.pk,new_message)

                elif date_diff.days==15:          
                    logger.info("date is equal to 15 : ")
                    notify.send(l_u.user,recipient=l_u.user,verb="Your License is going to expire after 15 days on "+str(lead.license_expiry_date),app_name="CRM",activity="License_expiry",object_id=lead.pk)
                    new_message="Your driving license is going to expire after 15 days on "+str(lead.license_expiry_date)
                    check_expiration_license_date_push_notifications(l_u.pk,new_message)
                elif date_diff.days==0:
                    logger.info("date is equal to 0")
                    notify.send(l_u.user,recipient=l_u.user,verb="Your License is going to expire today.Please renew your license.",app_name="CRM",activity="License_expiry",object_id=lead.pk)
                    new_message="Your driving license is going to expire today.Please renew your license."
                    check_expiration_license_date_push_notifications(l_u.pk,new_message)

                else:
                    logger.info("date is not equal to 30")
            else:
                logger.info("no date available")
    except Exception as e:
             print("Exception occurred: ",e)
             
def check_expiration_license_date_push_notifications(l_uid,new_message):
        print("in def reg_expiry_push_notifications")
        l_u=lead_user.objects.get(pk=l_uid)
        print("user id=",l_u.user.email)
        #notifications for ios
        try:        
            deviceiOS = APNSDevice.objects.filter(user=l_u.user)
            message_sent=deviceiOS.send_message(new_message)
        except Exception as e:
            print("exception------------------------------------------",e.message)
                        #notifications for ios end
                        #notifications for android
        try: 
            device = FCMDevice.objects.filter(user=l_u.user)
            device.send_message("Remainder Vehicle Expiry",new_message)
            print("message sent")
        except Exception as e:
            print("exception------------------------------------------",e.message)
                         #notifications for android end 
