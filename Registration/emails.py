from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.mail import get_connection, EmailMultiAlternatives

from django.template.loader import render_to_string, get_template
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from django.contrib.auth.models import User


def send_member_email(email, password,shop,website):
    logger.info("inside sending lead mail")
    connection = get_connection()
    connection.open()
    
    ctx={'user': email, 'password': password,'shop':shop,'website':website}
    data = {}

    template = get_template('registration/member_email.html')
    #html  = template.render(Context(data))
    subject='AutoXtion Successful registration'
    html_content = render_to_string('registration/member_email.html', ctx)
    text_content = "..."
    to=[email]
    from_email=settings.EMAIL_HOST_USER
    #send_mail(subject,"",from_email,to,fail_silently=True, html_message=html_content)
    msg= EmailMultiAlternatives(subject, " " ,from_email,to,bcc=['info@autoxtion.com.au'])
    msg.attach_alternative(html_content, "text/html")                                                                                                                                                                               
    msg.send()
    connection.close()

def send_vcf_mail(mail,member_mail,name,mem_detail):
   
    logger.info("inside send vcf mail")
    print("+++++++++++++in vcf mail")
    print(mail,member_mail)
    ctx={'mem_detail':mem_detail}
    
    user1=User.objects.get(username=member_mail)
    
    html_message="Hi  "+name+", \n Click For Registration \t http://192.168.1.129:8010/CRM/add/"+str(mem_detail)+""
    email = EmailMessage()
    email.subject = user1.first_name+" "+user1.last_name+" Business Card."
    email.body = html_message
    email.from_email = settings.EMAIL_HOST_USER
    email.to = [mail]
   
   # email.user1=[user1]
    #f=open("static/vcards/"+mail+".vcf",'r')
    email.attach_file("static/vcards/"+member_mail+".vcf")
    #f.close()
    return email.send()

def send_vcf_mail1(mail,member_mail,name):
   
    logger.info("inside send vcf mail")
    print("qqqqqqqqqqqqqqqqq+++++++++++++in vcf mail")
    print(mail,member_mail,name)
    
    
    user1=User.objects.get(username=member_mail)
    #user=User.objects.get(username=mail)
    html_message="Hi  "+name+", \n \n  \t"
    email = EmailMessage()
    email.subject = user1.first_name+" "+user1.last_name+" Business Card."
    email.body = html_message
    email.from_email = settings.EMAIL_HOST_USER
    email.to = [mail]
   
   # email.user1=[user1]
    #f=open("static/vcards/"+mail+".vcf",'r')
    email.attach_file("static/vcards/"+member_mail+".vcf")
    #f.close()
    return email.send()

