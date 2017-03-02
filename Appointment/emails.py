from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.mail import get_connection, EmailMultiAlternatives

from django.template.loader import render_to_string, get_template
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

def send_appointment_create_email(date,from_time,to_time,description,first_name,phone_no,shop_name,shop_address,cust_email,mem_email,website):
    logger.info("inside sending lead mail")
    
    connection = get_connection()
    connection.open()
    ctx={'date': date, 'from_time': from_time, 'to_time': to_time, 'request': description, 'name':first_name, 'phone':phone_no, 'shop':shop_name, 'address':shop_address,'email':mem_email,'website':website}
    data = {}
    template = get_template('Appointment/appointment_email.html')
    #html  = template.render(Context(data))
    subject='AutoXtion Appointment Successfully Scheduled'
    html_content = render_to_string('Appointment/appointment_email.html', ctx)
    text_content = "..."
    to=[cust_email]
    from_email=settings.EMAIL_HOST_USER
    #send_mail(subject,"",from_email,to,fail_silently=True, html_message=html_content)
    msg= EmailMultiAlternatives(subject, " " ,from_email,to,bcc=['askate243@gmail.com'])
    msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
    msg.send()
    connection.close()

def send_appointment_update_email(date,from_time,to_time,coment, description,first_name,phone_no,shop_name,shop_address,cust_email,mem_mail,mem_name,website):
    logger.info("inside sending update appointment mail")
    
    connection = get_connection()
    connection.open()
    print("-----------",website)
    ctx={'date': date, 'from_time': from_time, 'to_time': to_time,'coment': coment, 'request': description, 'name':first_name, 'phone':phone_no, 'shop':shop_name, 'email':mem_mail,'address':shop_address,'mem_name':mem_name,'website':website}
    data = {}
    template = get_template('Appointment/appointment_update_email.html')
    #html  = template.render(Context(data))
    subject='AutoXtion Appointment Rescheduled'
    html_content = render_to_string('Appointment/appointment_update_email.html', ctx)
    text_content = "..."
    to=[cust_email]
    #bcc=['gera.sachin89@gmail.com']
    from_email=settings.EMAIL_HOST_USER
    #send_mail(subject,"",from_email,to,fail_silently=True, html_message=html_content)
    msg= EmailMultiAlternatives(subject, " " ,from_email,to,bcc=['askate243@gmail.com'])
    msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
    msg.send()
    connection.close()


def send_appointment_delete_email(shop,name,email,address,phone,cust_email,website):
    print("in delete appoint mail")
    connection = get_connection()
    connection.open()
    template = get_template('Appointment/appointment_delet_email.html')
    ctx={'shop': shop, 'name': name, 'email': email, 'address':address, 'phone': phone,'website':website}
    data = {}
    #html  = template.render(Context(data))
    subject='AutoXtion Appointment Cancelled'
    html_content = render_to_string('Appointment/appointment_delet_email.html', ctx)
    text_content = "..."
    to=[cust_email]
    from_email=settings.EMAIL_HOST_USER
    msg= EmailMultiAlternatives(subject, " " ,from_email,to,bcc=['askate243@gmail.com'])
    msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
    msg.send()
    connection.close()


def send_appointment_done_email(shop,name,email,address,phone,cust_email, coment,website):
    connection = get_connection()
    connection.open()
    template = get_template('Appointment/appointment_done_email.html')
    ctx={'shop': shop, 'name': name, 'email': email, 'address':address, 'phone': phone, 'coment': coment,'website':website}
    data = {}
    #html  = template.render(Context(data))
    subject='AutoXtion Service Successfully Done'
    html_content = render_to_string('Appointment/appointment_done_email.html', ctx)
    text_content = "..."
    to=[cust_email]
    from_email=settings.EMAIL_HOST_USER
    msg= EmailMultiAlternatives(subject, " " ,from_email,to,bcc=['askate243@gmail.com'])
    msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
    msg.send()
    connection.close()


def send_appointment_reminder_mail(date,from_time,to_time,first_name,phone_no,shop_name,shop_address,cust_email,cust_name,website):
    connection = get_connection()
    connection.open()

    logger.info("inside sending reminder of appointment mail"+str(cust_email))
    ctx={'cust_name':cust_name,'date': date, 'from_time': from_time, 'to_time': to_time,  'name':first_name, 'phone':phone_no, 'shop':shop_name, 'address':shop_address,"name1":cust_name,'website':website}
    data = {}
    template = get_template('Appointment/appointment_reminder_email.html')
    #html  = template.render(Context(data))
    subject='AutoXtion Appointment Successfully Scheduled'
    html_content = render_to_string('Appointment/appointment_reminder_email.html', ctx)
    text_content = "..."
    to=[cust_email]
    from_email=settings.EMAIL_HOST_USER
    msg= EmailMultiAlternatives(subject, " " ,from_email,to,bcc=['askate243@gmail.com'])
    msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
    msg.send()
    connection.close()
