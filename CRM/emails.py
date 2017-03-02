from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.mail import get_connection, EmailMultiAlternatives

from django.template.loader import render_to_string, get_template
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from .models import *
from Registration.models import *

def send_lead_email(email,name,password,phone,shop,address,lead_mail,fname,mem_mail,website):
    logger.info("inside sending lead mail")
    connection = get_connection()
    connection.open()
    logger.info(email+"---------"+lead_mail)
    data = {}
    template = get_template('CRM/customer_email.html')
    #html  = template.render(Context(data))
    subject='Successfully added as Customer for AutoXtion'
    ctx={'email':email , 'name':name, 'password': password, 'phone':phone, 'shop':shop, 'address':address,"email1":mem_mail,"name1":fname,'website':website}
    html_content = render_to_string('CRM/customer_email.html', ctx)
    to=[email]
    from_email=settings.EMAIL_HOST_USER
    #send_mail(subject,"",from_email,to,fail_silently=True, html_message=html_content)
    msg= EmailMultiAlternatives(subject, " " ,from_email,to,bcc=['info@autoxtion.com.au','askate243@gmil.com','nikijadhav0407@gmail.com'])
    msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
    msg.send()
    logger.info("send lead mail")
    connection.close()


def send_ext_customer_mail(email,name,password,phone,shop,address,lead_mail,mem_mail,website):
    connection = get_connection()
    connection.open()
    print("member site@@@@@@@@@ ",website)
    data={}
    template = get_template('CRM/existing_cust_email.html')
    #html  = template.render(Context(data))
    print("member mail in email.py",mem_mail)
    ctx={'email': email, 'name':name, 'password': password, 'phone':phone, 'shop':shop, 'address':address,'email1':mem_mail,'website':website}
    subject='Successfully Qualified as Lead for AutoXtion'
    html_content = render_to_string('CRM/existing_cust_email.html', ctx)

    to=[lead_mail]
    from_email=settings.EMAIL_HOST_USER
    
    msg= EmailMultiAlternatives(subject, " " ,from_email,to,bcc=['info@autoxtion.com.au','askate243@gmil.com'])
    msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
    msg.send()
    connection.close()

def send_lead_generate(email,name,password,phone,shop,address,lead_mail,fname,mem_mail,website):
    logger.info("inside sending lead mail")
    connection = get_connection()
    connection.open()
    logger.info(email+"---------"+lead_mail)
    data = {}
    template = get_template('CRM/customer_regenerate.html')
    #html  = template.render(Context(data))
    subject=shop+': New login credentials for AutoXtion'
    ctx={'email':email , 'name':name, 'password': password, 'phone':phone, 'shop':shop, 'address':address,"email1":mem_mail,"name1":fname,'website':website}
    html_content = render_to_string('CRM/customer_regenerate.html', ctx)
    to=[email]
    from_email=settings.EMAIL_HOST_USER
    #send_mail(subject,"",from_email,to,fail_silently=True, html_message=html_content)
    msg= EmailMultiAlternatives(subject, " " ,from_email,to,bcc=['info@autoxtion.com.au','askate243@gmail.com'])
    msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
    msg.send()
    logger.info("send lead mail")
    connection.close()


def send_driver_mail(lead_id,company_id,member_auth_id,password):
    connection = get_connection()
    connection.open()
    lead_obj=Lead.objects.get(pk=lead_id)
    company_obj=CustCompany.objects.get(pk=company_id)
    member_auth_obj=User.objects.get(pk=member_auth_id)
    userprofile_obj=UserProfile.objects.get(user=member_auth_obj)
    data={}
    template = get_template('CRM/existing_cust_email.html')
    #html  = template.render(Context(data))

    ctx={'comapny_person':company_obj.person,'email': lead_obj.email, 'name':lead_obj.name, 'password': password, 'phone':userprofile_obj.phone_no, 'shop':userprofile_obj.shop_name, 'address':userprofile_obj.shop_address,'email1':member_auth_obj.email,'website':userprofile_obj.website}
    subject='Successfully Qualified as Customer for AutoXtion'
    html_content = render_to_string('CRM/existing_cust_email.html', ctx)

    to=[lead_obj.email]
    from_email=settings.EMAIL_HOST_USER

    msg= EmailMultiAlternatives(subject, " " ,from_email,to,bcc=['askate243@gmil.com'])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    connection.close()


def send_company_mail(company_id,member_id,password):
    connection = get_connection()
    connection.open()
    data={}
    member_user_obj=User.objects.get(pk=member_id)
    company_obj=CustCompany.objects.get(pk=company_id)
    memberprofile_obj=UserProfile.objects.get(user=member_user_obj)
    template = get_template('CRM/existing_cust_email.html')
    print("member mail in email.py",company_obj)
    ctx={'email': company_obj.email, 'name':company_obj.person, 'password': password, 'phone':memberprofile_obj.phone_no, 'shop':memberprofile_obj.shop_name, 'address':memberprofile_obj.shop_address,'email1':member_user_obj.email,'website':memberprofile_obj.website}
    subject=memberprofile_obj.shop_name+': Successfully Qualified as Lead for AutoXtion'
    html_content = render_to_string('CRM/customer_email.html', ctx)
    to=[company_obj.email]
    from_email=settings.EMAIL_HOST_USER

    msg= EmailMultiAlternatives(subject, " " ,from_email,to,bcc=['askate243@gmil.com'])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    connection.close()