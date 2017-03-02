from django.shortcuts import render, render_to_response, get_object_or_404,redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from Registration.models import *
from Registration.forms import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
import logging
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.models import User
logger = logging.getLogger('Registration')
logger.addHandler(logging.NullHandler())
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from Autoxtion_B2C import settings
from customer.models import customer_request
from CRM.models import *
from CRM.forms import *
from customer.models import *
from Appointment.models import *
from django.db import models, signals
from django.utils.timezone import now
from datetime import datetime,date
import stripe
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.core.mail import get_connection, EmailMultiAlternatives
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from promotion.models import *
#from xhtml2pdf import pisa 
from django.utils import timezone
import pytz
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET
import vobject
from .tasks import *
from Timeline.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import calendar
import operator
import requests
import base64
import itertools
from django.db.models import Count
from Feedback.models import *
from dateutil.relativedelta import relativedelta

# Create your views here.

def login(request):
    return render(request,'registration/landing_page.html')

     

def member_login(request):
    logger.info("start of member login view")
    logger.debug("start of member login view")
  
    if request.method == 'POST':
      email = request.POST.get('email')
      password = request.POST.get('password')
      #shop=request.POST.get("customer1")
      #print("----------",shop)
      user = authenticate(username =email, password=password)
      if user is not None:
        if user.is_active:
    
                today=datetime.today()
                date=today.date()    
                logger.debug("User is active")
                print("user is active")
                group=Group.objects.get(user=user)
                print("-------group--------------",group.name)
                print(user.pk)
                cust=user.groups.get(user = user.id)
                date_joined=user.date_joined.date()
                if group.name=="Member":
                    #if shop=="member":      
                        print("mem")
                        sta=UserProfile.objects.get(user=user)
                        payment_day=date_joined.strftime('%d')
                        print("mem",date.year, date.month, payment_day)
                        
                        print("$$$$$$$$",sta)
                        if sta.status:
                            current_unsub_date=datetime.strptime(str(sta.unsubscribe_date.strftime('%d'))+""+str(date.month)+""+str(date.year), "%d%m%Y").date()
                            if sta.status.status=="Unsubscribed":
                                print("if status") 
                                print(sta.unsubscribe_date.date())
                                if sta.unsubscribe_date.date().day>=1 and sta.unsubscribe_date.date().day<=payment_day:
                                    if today.date()<=current_unsub_date:
                                         print("greater than today's date 1")
                                         auth_login(request, user)
                                         print("payment has been done")
                                         if sta.flag is True :
                                             return redirect('/registration/success/')
                                         return render(request, 'registration/sample.html',{'context22': sta })
                                        
                                    else:
                                        print(" less than today's date 1")
                                        auth_login(request, user)
                                        print("payment has been done")

                                        return redirect('/registration/newpayment/')
                                elif sta.unsubscribe_date.date().days>=payment_day+1 and sta.unsubscribe_date.date().days<=31:
                                    if today.date()<=current_unsub_date:
                                         print("greater than today's date 2")
                                         auth_login(request, user)
                                         print("payment has been done")
                                         return redirect('/registration/success/')
                                    else:
                                        print(" less than today's date 2")
                                        auth_login(request, user)
                                        print("payment has been done")
                                        return redirect('/registration/newpayment/')    
                                   
                        else:
                          
                            try:    
                                print("in try")
                                user1=Payment.objects.get(user=user)
                                if user1.stripe_id=='0' and today.date() > user.date_joined.date()+relativedelta(months=2):
                                    print("stripe id is 0") 
                                    auth_login(request, user)
                                    if sta.flag is True :
                                        return redirect('/registration/newpayment/')
                                    return render(request, 'registration/sample2.html',{'context22': sta })
                                     
                                else:
                                    print("stripe id in not 0")
                                    auth_login(request, user)
                                    if sta.flag is True :
                                        return redirect('/registration/success/')
                                    return render(request, 'registration/sample.html',{'context22': sta })
                                   
                            except:
                                    print("in except")
                                    auth_login(request, user)
                                    return redirect('/registration/newpayment/')
                
                else:
                    return render(request,'registration/member_login.html', {'context1': "Please enter valid credential"}) 
        else:
            logger.debug("User is not active")
            return render(request,'registration/member_login.html', {'context1': "User is not active"})
      else:
          logger.debug("Unknown User")
          return render(request,'registration/member_login.html', {'context1': "Incorrect User Name or Password"})            
                    
    else:
        return render(request,'registration/member_login.html')
    

def customer_login(request):
    logger.info("start of login view")
    logger.debug("start of login view")
  
    if request.method == 'POST':
      email = request.POST.get('email')
      password = request.POST.get('password')
      #shop=request.POST.get("customer1")
      #print("----------",shop)
      user = authenticate(username =email, password=password)
      if user is not None:
        if user.is_active:
                
                today=datetime.today()
                date=today.date()    
                logger.debug("User is active")
                print("user is active")
                group=Group.objects.get(user=user)
                print("-------group--------------",group.name)
                print(user.pk)
                cust=user.groups.get(user = user.id)
                date_joined=user.date_joined.date()
                          
                if group.name=="Customer":
                       print("customerrrrr")
                    #if shop=="customer":
                       request.session['user']=user.username
                       auth_login(request, user)
                       return redirect('/registration/success/') 
                    #else:
                    #    print("select else")
                    #    auth_login(request, user)
                    #    return render(request,'registration/login.html', {'context1': "Please enter valid credential"})  
                elif group.name == "E_Customer":
                    auth_login(request, user)
                    return redirect('/registration/success/') 
                elif group.name=="Lead":
                    #if shop=="customer":
                       
                       auth_login(request, user)
                       return redirect('/registration/success/') 
		elif group.name=="Company":
                   auth_login(request, user)
                   print("Group name is company---------")
                   return redirect('/CRM/editVehicle/')
                else:
                    return render(request,'registration/customer_login.html', {'context1': "Please enter valid credential"})  
                            
        else:
            logger.debug("User is not active")
            return render(request,'registration/customer_login.html', {'context1': "User is not active"})
      else:
          logger.debug("Unknown User")
          return render(request,'registration/customer_login.html', {'context1': "Incorrect User Name or Password"})
    else:
      return render(request,'registration/customer_login.html')
     

def soon():
    soon = datetime.today()
    return {'month': soon.month, 'year': soon.year}
  
def register(request):
        logger.debug("Start of register Views")
   
        registered = False
        print("i am here")
        print(stripe.api_key)
        if request.method == 'POST':
           print("in post") 
           user_form = UserForm(data=request.POST)
           profile_form = UserProfileForm(data=request.POST)
           print("---------",user_form.errors)
           print(profile_form.errors)
#            form=CardForm(data=request.POST)
#            print("form error",form.errors)
           
           if user_form.is_valid() and profile_form.is_valid():
               logger.debug("User and profile forms are valid")
               
               #profile.save()
               user = User(
                first_name = user_form.cleaned_data['first_name'],
                last_name = user_form.cleaned_data['last_name'],
                email = user_form.cleaned_data['email'],
               )
               try:
                   user_exists = User.objects.get(username=request.POST['email'])
                   
                   user_form = UserForm()
                   profile_form = UserProfileForm()
    
                   context= RequestContext(request,{'user_form': user_form,
                                                    'profile_form': profile_form,
                                                    'exist': 'Email Already Exist',
                                                    'registered': registered})
                                                  #  'months': range(1, 13),
                                                   # 'publishable': settings.STRIPE_PUBLISHABLE,
                                                   # 'soon': soon(),
                                                   # 'years': range(2016, 2036)})
                      
        
                   return render_to_response(
                                             'registration/register2.html', context) 
               
               
               except:
                   user.set_password(user_form.cleaned_data['password'])
                   user.username= user.email
                   user.save()
                   print("userrrrrr=======payment", user.email)
                   print("member password is =====", user_form.cleaned_data['password'])
                   user.groups.add(Group.objects.get(name='Member'))
                   
#                    customer = stripe.Customer.create(
#                                                       description = user_form.cleaned_data['email'],
#                                                       card = form.cleaned_data['stripe_token'],
#                                                       plan = "daily-1"
#                                                       
#                                                       )  
#                charge = stripe.Charge.create(
#                                               amount=5000, # amount in cents, again
#                                               currency="aud",
#                                               customer=customer.id,
#                                               description="Charge for portal.autoxtion.com.au",
#                                               receipt_email=user.email,
#                                               )
               
                   print(user)
                   profile = profile_form.save(commit=False)
                   #digit=form.cleaned_data['last_4_digits']
#                    print(digit)
#                    profile.last_4_digits=digit
#                    profile.stripe_id= customer.id
                   profile.user = user
                   user.save()
                   profile.save()
                   f=open("static/vcards/"+user_form.cleaned_data['email']+".vcf",'w+')
                   j = vobject.vCard()
                   o = j.add('fn')
                   o.value = user_form.cleaned_data['first_name']+" "+user_form.cleaned_data['last_name']
                   o = j.add('n')
                   o.value = vobject.vcard.Name( family=user_form.cleaned_data['last_name'],given=user_form.cleaned_data['first_name'] )
                   j.add('email')
                   j.email.value = user_form.cleaned_data['email']
                   j.email.type_param = 'INTERNET'
                   j.email.type_param = 'HOME'
                   j.add('tel')
                   #print(profile_form.cleaned_data['phone_no'])
                   j.tel.value=str(profile_form.cleaned_data['phone_no'])
                   str1=profile_form.cleaned_data['shop_address']+","+profile_form.cleaned_data['city']
                   #print(str1)
                   o = j.add('note')
                   o.value =str1+",Australia"
                   j.add('url')
                   j.url.value=profile_form.cleaned_data['website']
                                     
                   f.write(j.serialize())
                   f.close()
                   registered = True
                   var1=Payment(last_4_digits=0,
                                stripe_id=0,
                                subscribed=True,user=user)
                   var1.save()
                   #print(var1)
                   ctx={'email': user.username, 'name':user.first_name}
                   data = {}
        
                   send_member_task.delay(user.username, user_form.cleaned_data['password'],profile_form.cleaned_data['shop_name'],profile_form.cleaned_data['website'])
                   return render_to_response('registration/registration_success.html/')
               
           else:
               logger.debug("User and profile forms are not valid")
               user_form = UserForm(data=request.POST)
               profile_form = UserProfileForm(data=request.POST) 
               context= RequestContext(request,{'user_form': user_form,
                 'profile_form': profile_form,
                 'registered': registered,
                 'months': range(1, 13),
                 'publishable': settings.STRIPE_PUBLISHABLE,
                 'soon': soon(),
                 'years': range(2016, 2036)})
               return render_to_response('registration/register2.html',context)
               logger.debug("End of register Views")
               
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()
            
            context= RequestContext(request,{'user_form': user_form,
                 'profile_form': profile_form,
                 'registered': registered,
                 'months': range(1, 13),
                 'publishable': settings.STRIPE_PUBLISHABLE,
                 'soon': soon(),
                 'p': "Amount Payable: AUD 250",
                 'years': range(2016, 2036)})
                      
        
            return render_to_response(
                'registration/register2.html', context
                ) 
            logger.debug("End of register Views") 

@login_required(login_url="/registration/login/")
def newpayment(request):
     print("in new payment")
     user = request.user
     print("new key",stripe.api_key)
     print("user",user)
     if request.method == 'POST':
         form = CardForm(data=request.POST)
         #user_form=UserProfileForm(request.POST)
         if form.is_valid(): #and user_form.is_valid():
           print("form valid")
           customer = stripe.Customer.create(
           description = user.username,
           card = form.cleaned_data['stripe_token'],
            plan = "daily-1",
		tax_percent=10
            )
           
#            charge = stripe.Charge.create(
#                amount=5000, # amount in cents, again
#                currency="AUD",
#                customer=customer.id,
#                description="Charge for portal.autoxtion.com.au",
#                #receipt_email=user.email,
#            )
           paym= Payment.objects.get(user=user)
           print(paym)
           digits=form.cleaned_data['last_4_digits']
           paym.last_4_digits=digits
           paym.stripe_id=customer.id
           paym.subscribed=True 
           paym.save()
           today=datetime.today()
           var=UserProfile.objects.get(user=user)
           var.payment_date=today
           var.unsubscribe_date=None
           var.status=None
           var.save()
          
           return redirect( '/registration/success/' ) 
               
         else:
           print("form invalid")
     else:
       print("else")
       form = CardForm()
       today=datetime.today()
       today_year=today.year
     
       return render_to_response(
         'registration/payment_modalnew.html',
         {
           'form': form,
           'months': range(1, 13),
           'publishable': settings.STRIPE_PUBLISHABLE,
           'soon': soon(),
           'user': user,
           'years': range(today_year, 2036),
         },
         context_instance=RequestContext(request)
       )  

@login_required(login_url="/registration/login/")
def payment(request):
   user=request.user 
   print("in payment")
   if request.method == 'POST':
     print("in request")
     form = CardForm(data=request.POST)
     print(form)
     if form.is_valid():
            var1= Payment.objects.get(user=user)
            if var1.stripe_id is not None:
               print(" hi old stripe id:",var1.stripe_id)
               customer = stripe.Customer.create(
               description = user.email,
               card = form.cleaned_data['stripe_token'],
               plan = "basic_monthly"
              )
                     
               customer.save()
               print("Customer----",customer,customer.id)
               var1.last_4_digits = form.cleaned_data['last_4_digits']
               var1.stripe_id = customer.id
               var1.save()
               today=datetime.today()
               var=UserProfile.objects.get(user=user)
               var.payment_date=today
               var.save()
               return redirect('/registration/success/')
     else:
         print("form invalid")
   else:
     form = CardForm()
     print("in get")
     return render_to_response(
         'registration/payment_modal.html',
         {
           'form': form,
           'publishable': settings.STRIPE_PUBLISHABLE,
           'soon': soon(),
           'months': range(1, 13),
           'years': range(2011, 2036)
         },
         context_instance=RequestContext(request)
       )

@login_required(login_url="/registration/login/")
def unsubscribe(request):
    print("in unsubscribe*****************")
    today=datetime.today()
    date=today.date()
    user=request.user  
    payment=None
    try:
        payment=Payment.objects.get(user=user)
    except ObjectDoesNotExist:  
        print("in exception")
        user_profile=UserProfile.objects.get(user=user)
        status=Status.objects.get(status="Unsubscribed")
        user_profile.status=status
        user_profile.unsubscribe_date=date
        user_profile.save()
        var1=Payment(last_4_digits=0000,stripe_id=0,subscribed=False,user=user)
        var1.save()


        return redirect('/registration/logout/') 
    if payment.stripe_id!='0':
        print("in unsubscribe222")
        cust = stripe.Customer.retrieve(payment.stripe_id)
        print(cust.id,"customer sub list--",cust.subscriptions.data)
        #list_items=cust.subscriptions.data
        #print(list_items[0].id)
        if cust.subscriptions.data:
            sub = stripe.Subscription.retrieve(cust.subscriptions.data[0].id)
            print("sub=============",sub)
            sub.delete()
            s_list=stripe.Subscription.all()
            for s in s_list:
                print(s.id,"----",s.customer) 
            user_profile=UserProfile.objects.get(user=user)
            status=Status.objects.get(status="Unsubscribed")
            user_profile.status=status
            user_profile.unsubscribe_date=date
            user_profile.save()
            return redirect('/registration/logout/')
        else:
            return redirect('/registration/logout/')

    else:
         user_profile=UserProfile.objects.get(user=user)
         status=Status.objects.get(status="Unsubscribed")
         user_profile.status=status
         user_profile.unsubscribe_date=date
         user_profile.save()
         return redirect('/registration/logout/')


#@login_required(login_url="/registration/login/")
# def updatedetails(request, user_id):
        # logger.debug("Start of updatedetails Views")
# #    try: 
        # server1 = get_object_or_404(User, pk=user_id)
        # group=Group.objects.get(user=server1)
        # if group.name=="Member":
            # print("this is member")
            # server2 = get_object_or_404(UserProfile, user=server1)
            # if request.method == 'POST':
                # update_profile = UpdateProfileForm(request.POST)
                # if update_profile.is_valid():
                    # logger.debug("update profile form is valid")
                    # server1.first_name=update_profile.cleaned_data['first_name']
                    # server1.last_name=update_profile.cleaned_data['last_name']
                    # server2.phone_no=update_profile.cleaned_data['phone_no']
		    # server2.Emg_no=update_profile.cleaned_data['Emg_no']
                    # server2.shop_name=update_profile.cleaned_data['shop_name']
                    # server2.shop_address=update_profile.cleaned_data['shop_address']
                    # server2.country=update_profile.cleaned_data['country']
                    # server2.website=update_profile.cleaned_data['website']
                    # print("website isss=========",server2.website)
                    # server2.city=update_profile.cleaned_data['city']
                    # server2.area_code=update_profile.cleaned_data['area_code']
                    # #server2.landline_number=update_profile.cleaned_data['landline_number']
                    # server1.save()
                    # server2.save()
                    # variables = RequestContext(request,
                                       # {'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context1': "Your details has been updated"})
                    # return render_to_response(
                                                # 'registration/updateDetails.html', variables)
                # else:
                    # update_profile = UpdateProfileForm(initial={'first_name':server1.first_name,'last_name':server1.last_name, 'phone_no':server2.phone_no,  'Emg_no':server2.Emg_no,'area_code':server2.area_code,'shop_name':server2.shop_name, 'shop_address':server2.shop_address, 'country':server2.country, 'city':server2.city, 'website':server2.website})
                    # variables = RequestContext(request,
                                       # {'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm,'errorpassword': "Cannot leave field empty, please fill the complete details"})
                    # return render(request, 'registration/updateDetails.html', variables)
                
            # else:
                # update_profile = UpdateProfileForm(initial={'first_name':server1.first_name,'last_name':server1.last_name, 'phone_no':server2.phone_no, 'Emg_no':server2.Emg_no, 'area_code':server2.area_code,'shop_name':server2.shop_name, 'shop_address':server2.shop_address, 'country':server2.country, 'city':server2.city, 'website':server2.website})
                # #print("----------",server2.area_code,server2.landline_number)
		# variables = RequestContext(request,
                                       # {'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm})
                # return render_to_response(
                                          # 'registration/updateDetails.html', variables,
                                          # )
        # elif group.name=="Customer":
            # print("this is customer")
            # print(server1.pk)
            # lead_u=lead_user.objects.get(user=server1)
            # print(lead_u.pk,lead_u.customer)
            # lead=Lead.objects.get(pk=lead_u.customer.pk)
            # address= UserProfile.objects.get(user=lead.member) 
            
            # mem=lead.member
            # print(mem)
            # print(lead)
            # update_profile = LeadForm(request.POST or None, instance=lead)
            # if request.method=='POST':
                # print("post request")
                # if update_profile.is_valid():
                    # update_profile.save()
                    # cust1= update_profile.cleaned_data['name']
                    # print("new cuts nameeeeee==", cust1)
                    # server1.first_name=update_profile.cleaned_data['name']
                    # server1.save()
                    # #server12 = get_object_or_404(User, pk=user_id)
                    # #print(server12.first_name)
                    # #us= server12(first_name= cust1)
                    # #user.save()
                    # variables = RequestContext(request,
                                       # {'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context1': "Your details has been updated"})
                    # return render_to_response('registration/updateDetailsCustomer.html', variables)
                # else:
                    # update_profile=LeadForm(request.POST)
                    # variables = RequestContext(request,
                                       # {'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context2': "Please enter all valid details"})
                    # return render_to_response('registration/updateDetailsCustomer.html', variables)
            # else:
                # update_profile=LeadForm(instance=lead)
                # variables = RequestContext(request,
                                       # {'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm})
                # return render_to_response('registration/updateDetailsCustomer.html', variables) 
        
        # elif group.name=="Lead":
            # print("this is Lead")
            # print(server1.pk)
            # lead_u=lead_user.objects.get(user=server1)
            # print(lead_u.pk,lead_u.customer)
            # lead=Lead.objects.get(pk=lead_u.customer.pk)
            # address= UserProfile.objects.get(user=lead.member) 
            
            # mem=lead.member
            # print(mem)
            # print(lead)
            # update_profile = LeadForm(request.POST or None, instance=lead)
            # if request.method=='POST':
                # print("post request")
                # if update_profile.is_valid():
                    # update_profile.save()
                    # cust1= update_profile.cleaned_data['name']
                    # print("new Lead nameeeeee==", cust1)
                    # server1.first_name=update_profile.cleaned_data['name']
                    # server1.save()
                    # #server12 = get_object_or_404(User, pk=user_id)
                    # #print(server12.first_name)
                    # #us= server12(first_name= cust1)
                    # #user.save()
                    # variables = RequestContext(request,
                                       # {'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context1': "Your details has been updated"})
                    # return render_to_response('registration/updateDetailsCustomer.html', variables)
                # else:
                    # update_profile=LeadForm(request.POST)
                    # variables = RequestContext(request,
                                       # {'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context2': "Please enter all valid details"})
                    # return render_to_response('registration/updateDetailsCustomer.html', variables)
            # else:
                # update_profile=LeadForm(instance=lead)
                # variables = RequestContext(request,
                                       # {'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm})
                # return render_to_response('registration/updateDetailsCustomer.html', variables) 
        
        # else:
            # print("this is existing customer")
            
            # lead_u=lead_user.objects.get(user=server1)
            
            # print(lead_u.pk,lead_u.customer)
            # lead=Lead.objects.get(pk=lead_u.customer.pk)
            # address= UserProfile.objects.get(user=lead.member)
            # mem=lead.member
            # print(mem)
            # print(lead)
            # update_profile = LeadForm(request.POST or None, instance=lead)
            # if request.method=='POST':
                # print("post request")
                # if update_profile.is_valid():
                    # cd=update_profile.cleaned_data
                    # update_profile.save()
                    
                    # server1_group = User.groups.through.objects.get(user=server1)
                    # server1_group.group=Group.objects.get(name='Customer')
                    # server1_group.save()
                    # name1 = cd.get('name')
                    # print("nammmmmmmmmmmm=", name1)
                    # server1.first_name = unicode(name1)
                    # server1.save()
                    # group=Group.objects.get(name="Customer")
                    # print(group)
                    # variables = RequestContext(request,
                                       # {'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm,"group":group, 'context1': "Your details has been updated"})
                    # return render_to_response('registration/updateDetailsCustomer.html', variables)
                # else:
                    # update_profile=LeadForm(request.POST)
                    # variables = RequestContext(request,
                                       # {'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context1': "Please enter all valid details"})
                    # return render_to_response('registration/updateDetailsCustomer.html', variables)
            # else:
                # update_profile=LeadForm(instance=lead)
                # variables = RequestContext(request,
                                       # {'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context1': "Kindly confirm your details and submit"})
                # return render_to_response('registration/updateDetailsCustomer.html', variables)
# #    except Exception as e:
# #        print(e)
# #        return render(request,'registration/404.html')
        
 

@login_required(login_url="/registration/login/")
def updatedetails(request, user_id):
	
        timeline_list = Timeline.objects.order_by('-id')[:5]
#     try: 
        server1 = get_object_or_404(User, pk=user_id)
        group=Group.objects.get(user=server1)
        if group.name=="Member":
            server2 = get_object_or_404(UserProfile, user=server1)
            val=getProfileCompletedCount(server2.pk,group.name)
            if request.method == 'POST':
                update_profile = UpdateProfileForm(request.POST)
                if update_profile.is_valid():
                    logger.debug("update profile form is valid")
                    server1.first_name=update_profile.cleaned_data['first_name']
                    server1.last_name=update_profile.cleaned_data['last_name']
                    server2.phone_no=update_profile.cleaned_data['phone_no']
                    server2.Emg_no=update_profile.cleaned_data['Emg_no']
                    server2.shop_name=update_profile.cleaned_data['shop_name']
                    server2.shop_address=update_profile.cleaned_data['shop_address']
                    server2.country=update_profile.cleaned_data['country']
                    server2.website=update_profile.cleaned_data['website']
                    server2.city=update_profile.cleaned_data['city']
                    server2.area_code=update_profile.cleaned_data['area_code']
                    server2.postal_code=update_profile.cleaned_data['postal_code']
                    server2.member_mech_license=update_profile.cleaned_data['member_mech_license']
                    server2.member_ARC_license=update_profile.cleaned_data['member_ARC_license']
                    server2.member_mech_license_expiry_date=update_profile.cleaned_data['member_mech_license_expiry_date']
                    server2.member_ARC_license_expiry_date=update_profile.cleaned_data['member_ARC_license_expiry_date']

                    server1.save()
                    server2.save()
                    now = timezone.now()
                    variable=Timeline(comment1=" have Updated " , comment2="profile",action_create=now,user=request.user)
                    variable.save()                    
                    context = RequestContext(request)
                    user1=request.user.id
                    timeline_li=Timeline.objects.filter(user=user1).order_by('id')[:5]
                    
                    countt=timeline_li.count()
                    userimage = User_imageForm()
                    context_dict = {'timeline_list': timeline_li}
                    image1=UserProfile.objects.get(user_id=request.user)
                    print("IMage##################3",image1)
                    variables = RequestContext(request,
                                       {'val':val,'userimage':userimage,'image1':image1,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context1': "Your details has been updated"})
                    return render_to_response(
                                                'registration/member_profile.html',context_dict, variables)
                else:
                    image1=UserProfile.objects.get(user_id=request.user)
                    print("IMage##################3",image1)
                    userimage = User_imageForm()
                    update_profile =UpdateProfileForm(initial={'first_name':server1.first_name,'last_name':server1.last_name, 'phone_no':server2.phone_no,'postal_code':server2.postal_code,  'Emg_no':server2.Emg_no,'area_code':server2.area_code,'shop_name':server2.shop_name, 'shop_address':server2.shop_address, 'country':server2.country, 'city':server2.city, 'website':server2.website,'member_mech_license':server2.member_mech_license,'member_ARC_license':server2.member_ARC_license,'member_mech_license_expiry_date':server2.member_mech_license_expiry_date,'member_ARC_license_expiry_date':server2.member_ARC_license_expiry_date})
                    variables = RequestContext(request,
                                       {'val':val,'userimage':userimage,'image1':image1,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm,'errorpassword': "Cannot leave field empty, please fill the complete details"})
                    return render(request, 'registration/member_profile.html', variables)
                
            else:
                timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                userimage = User_imageForm(request.POST)
                image1=UserProfile.objects.get(user_id=request.user)
                update_profile = UpdateProfileForm(initial={'first_name':server1.first_name,'last_name':server1.last_name,'postal_code':server2.postal_code, 'phone_no':server2.phone_no, 'Emg_no':server2.Emg_no, 'area_code':server2.area_code,'shop_name':server2.shop_name, 'shop_address':server2.shop_address, 'country':server2.country, 'city':server2.city, 'website':server2.website,'member_mech_license':server2.member_mech_license,'member_ARC_license':server2.member_ARC_license,'member_mech_license_expiry_date':server2.member_mech_license_expiry_date,'member_ARC_license_expiry_date':server2.member_ARC_license_expiry_date})
                #print("----------",server2.area_code,server2.landline_number)
                variables = RequestContext(request,
                                       {'val':val,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm,'timeline_list': timeline_li,'userimage':userimage,'image1':image1})
                return render_to_response(
                                          'registration/member_profile.html', variables,
                                          )
        elif group.name=="Customer":
            lead_u=lead_user.objects.get(user=server1)
            lead=Lead.objects.get(pk=lead_u.customer.pk)
            address= UserProfile.objects.get(user=lead.member) 
            val=getProfileCompletedCount(lead.pk,group.name)
            mem=lead.member
            update_profile = CustomerForm(request.POST or None, instance=lead)
            flag=None
            try:
                comp_dri=Company_Driver.objects.get(driver=lead)
                if comp_dri:
                    flag=True
                else:
                    flag=False
            except Exception as e:
                pass
            if request.method=='POST':
                if update_profile.is_valid():
                    update_profile.save()
                    cust1= update_profile.cleaned_data['name']
                    server1.first_name=update_profile.cleaned_data['name']
                    server1.last_name=update_profile.cleaned_data['last_name']
                    now = timezone.now()
                    variable=Timeline(comment1=" have Updated" , comment2=" profile",action_create=now,user=request.user)
                    variable.save()
		    new_username=User.objects.get(pk=server1.pk)
                    new_username.first_name=update_profile.cleaned_data['name']
                    new_username.last_name=update_profile.cleaned_data['last_name']
                    new_username.save()
                    context = RequestContext(request)
                    user1=request.user.id
                    timeline_li=Timeline.objects.filter(user=user1).order_by('-id')[:5]
                    context_dict = {'timeline_list': timeline_li}

                    lead_u=lead_user.objects.get(user=server1)
                    image2=Lead.objects.get(pk=lead_u.customer.pk)
                    variables = RequestContext(request,
                                       {'val':val,'flag':flag,'image2':image2,'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context1': "Your details has been updated"})
                    return render_to_response('registration/customer_profile.html', variables)
                else:
                    lead_u=lead_user.objects.get(user=server1)
                    image2=Lead.objects.get(pk=lead_u.customer.pk)
                    update_profile=CustomerForm(request.POST)
                    userimage1 = cust_imageForm(request.POST)
                    image1=UserProfile.objects.get(user_id=request.user)
                    timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                    variables = RequestContext(request,
                                       {'val':val,'flag':flag,'image2':image2,'timeline_list': timeline_li,'image1':image1,'userimage1':userimage1,'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context2': "Please enter all valid details"})
                    return render_to_response('registration/customer_profile.html', variables)
            else:
                update_profile=CustomerForm(instance=lead)
                userimage1 = cust_imageForm()
                lead_u=lead_user.objects.get(user=server1)
                image2=Lead.objects.get(pk=lead_u.customer.pk)
                timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                variables = RequestContext(request,
                                       {'val':val,'flag':flag,'image2':image2,'timeline_list': timeline_li,'userimage1':userimage1,'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm})
                return render_to_response('registration/customer_profile.html', variables) 
        
        elif group.name=="Lead":
            lead_u=lead_user.objects.get(user=server1)
            lead=Lead.objects.get(pk=lead_u.customer.pk)
            address= UserProfile.objects.get(user=lead.member) 
            val=getProfileCompletedCount(lead.pk,group.name)
            mem=lead.member
            update_profile = LeadForm(request.POST or None, instance=lead)
            flag=None
            try:
                comp_dri=Company_Driver.objects.get(driver=lead)
                if comp_dri:
                    flag=True
                else:
                    flag=False
            except Exception as e:
                pass
            if request.method=='POST':
                if update_profile.is_valid():
                    update_profile.save()
                    cust1= update_profile.cleaned_data['name']
                    server1.first_name=update_profile.cleaned_data['name']
                    server1.save()
                    now = timezone.now()
                    variable=Timeline(comment1=" have Updated" , comment2=" profile",action_create=now,user=request.user)
                    variable.save()
                    context = RequestContext(request)
                    user1=request.user.id
                    timeline_li=Timeline.objects.filter(user=user1).order_by('-id')[:5]
                    context_dict = {'timeline_list': timeline_li}
                    userimage1 = cust_imageForm()
                    image2=Lead.objects.get(pk=lead_u.customer.pk)
                    variables = RequestContext(request,
                                       {'val':val,'flag':flag,'image2':image2,'userimage1':userimage1,'timeline_list': timeline_li,'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context1': "Your details has been updated"})
                    return render_to_response('registration/customer_profile.html',context_dict, variables)
                else:
                    image2=Lead.objects.get(pk=lead_u.customer.pk)
                    update_profile=LeadForm(request.POST)
                    userimage1 = cust_imageForm()
#                     image1=UserProfile.objects.get(user_id=request.user)
                    timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                    context_dict = {'timeline_list': timeline_li}
                    variables = RequestContext(request,
                                       {'val':val,'flag':flag,'image2':image2,'userimage1':userimage1,'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context2': "Please enter all valid details"})
                    return render_to_response('registration/customer_profile.html', context_dict,variables)
            else:
                userimage1 = cust_imageForm()
                update_profile=LeadForm(instance=lead)
                image2=Lead.objects.get(pk=lead_u.customer.pk)
#                 image1=UserProfile.objects.get(user_id=request.user)
                timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                context_dict = {'timeline_list': timeline_li}
                variables = RequestContext(request,
                                       {'val':val,'flag':flag,'image2':image2,'timeline_li':timeline_li,'userimage1':userimage1,'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm})
                return render_to_response('registration/customer_profile.html',context_dict, variables)
        elif group.name=="Company":
            cust=CustCompany.objects.get(email=server1)
           # val=getProfileCompletedCount(lead.pk,group.name)
            val=getProfileCompletedCount(cust.pk,group.name)
            print("$$$$$$$$",cust.email)
            company=CustForm(request.POST ,instance=cust)
            userimage1 = company_imageForm()
            timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
            print("in company profile")
            if request.method=='POST':
              #  print("in post")
                if company.is_valid():
                    #print("###### for form valid in if")
                    company.save()
                    company_user=User.objects.get(email=cust.email)
                    company_user.first_name=company.cleaned_data['company_name']
                    company_user.save()
                   # messages.success="Your profile updatesd successfully"
                    now = timezone.now()
                    variable=Timeline(comment1=" have Updated " , comment2="profile",action_create=now,user=request.user)
                    variable.save()
                    context = RequestContext(request)
                    user1=request.user.id
                    timeline_li=Timeline.objects.filter(user=user1).order_by('-id')[:5]
                    print("timeline:",timeline_li)
                    context_dict = {'timeline_list': timeline_li}
                    variables = RequestContext(request,
                                       {'val':val,'timeline_li':timeline_li,'group':group,'company':company,'group':group,'image2':cust,'userimage1':userimage1,'updatepassword':ChangePasswordForm,'timeline_li':timeline_li,'context1': "Your details has been updated"})

                    return render(request,'registration/company_profile.html',variables)   
                else:   
                # auth_login(request, user)
                    cust=CustCompany.objects.get(email=server1)
                    company=CustForm(request.POST ,instance=cust)
                    userimage1 = company_imageForm()
                    timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
                    context_dict = {'timeline_list': timeline_li}
                    variables = RequestContext(request,
                                       {'val':val,'image2':image2,'userimage1':userimage1,'address':address,'group':group,'company':company, 'updatepassword':ChangePasswordForm, 'context2': "Please enter all valid details"})
                    return render_to_response('registration/customer_profile.html', context_dict,variables)

                     #print("###### for form invalid in else")
                     #return render(request,'registration/company_profile.html',{'company':company,'image2':cust,'group':group,'userimage1':userimage1,'updatepassword':ChangePasswordForm,'timeline_li':timeline_li,'context2': "Please enter all valid details"})  
        
            else:
               print("******************in else for image")
               userimage1 = company_imageForm()
               company=CustForm(instance=cust)
               timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
               context_dict = {'timeline_list': timeline_li}
               #return render(request,'registration/company_profile.html',context_dict,{'group':group,'company':company,'image2':cust,'userimage1':userimage1,'updatepassword':ChangePasswordForm,'timeline_li':timeline_li})  
               variables = RequestContext(request,
                                       {'val':val,'group':group,'company':company,'image2':cust,'userimage1':userimage1,'timeline_li':timeline_li,'userimage1':userimage1,'company':company, 'updatepassword':ChangePasswordForm})
               return render(request,'registration/company_profile.html',context_dict,variables)  
        
 
        
        else:
            timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
            lead_u=lead_user.objects.get(user=server1)
            context_dict = {'timeline_list': timeline_li}
            lead=Lead.objects.get(pk=lead_u.customer.pk)
            address= UserProfile.objects.get(user=lead.member)
	    val=getProfileCompletedCount(lead.pk,group.name)
            mem=lead.member
            update_profile = LeadForm(request.POST or None, instance=lead)
            flag=None
            try:
                comp_dri=Company_Driver.objects.get(driver=lead)
                if comp_dri:
                    flag=True
                else:
                    flag=False
            except Exception as e:
                pass
            if request.method=='POST':
                if update_profile.is_valid():
                    cd=update_profile.cleaned_data
                    update_profile.save()
                    lead_obj=Status.objects.get(status="Lead")
                    lead_obj.save()
                    server1_group = User.groups.through.objects.get(user=server1)
                    server1_group.group=Group.objects.get(name='Lead')
                    server1_group.save()
                    name1 = cd.get('name')
                    server1.first_name = unicode(name1)
                    server1.save()
                    now = timezone.now()
                    variable=Timeline(comment1=" have Updated" , comment2=" profile",action_create=now,user=request.user)
                    variable.save()
                    context = RequestContext(request)
                    user1=request.user.id
                    timeline_li=Timeline.objects.filter(user=user1).order_by('id')
                    context_dict = {'timeline_list': timeline_li}
                    group=Group.objects.get(name="Lead")
                    userimage1 = cust_imageForm()
                    
                    variables = RequestContext(request,
                                       {'val':val,'flag':flag,'userimage1':userimage1,'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm,"group":group, 'context1': "Your details has been updated"})
                    return render_to_response('registration/customer_profile.html', variables)
                else:
                    timeline_li=Timeline.objects.filter(user=user1).order_by('id')
                    context_dict = {'timeline_list': timeline_li}
                    userimage1 = cust_imageForm()
                    update_profile=LeadForm(request.POST)
                    
                    variables = RequestContext(request,
                                       {'val':val,'flag':flag,'timeline_li':timeline_li,'userimage1':userimage1,'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context1': "Please enter all valid details"})
                    return render_to_response('registration/customer_profile.html',context_dict, variables)
            else:
                context_dict = {'timeline_list': timeline_li}
                userimage1 = cust_imageForm()
                update_profile=LeadForm(instance=lead)
                user1=request.user.id
                timeline_li=Timeline.objects.filter(user=user1).order_by('id')
                variables = RequestContext(request,
                                       {'val':val,'flag':flag,'timeline_li':timeline_li,'userimage1':userimage1,'address':address,'group':group,'update_profile':update_profile, 'updatepassword':ChangePasswordForm, 'context1': "Kindly confirm your details and submit"})
                return render_to_response('registration/customer_profile.html', context_dict,variables)




       
@login_required(login_url="/registration/login/")
def success(request):
    
#     print("inside success")
#     try:   
        user=request.user
        status=Status.objects.get(status="Activate")
        s=Status.objects.get(status="Lead")
        group=Group.objects.get(user=user)
        d=date.today()
        count5= 0;
        count6=0;
        count7=0;
        count8=0;
        count9=0;
        count10=0;
        count11=0;
        count12=0;
        count13=0;
        count14=0;
        count15=0;
        count16=0;
        past_sche_apntmnt_count=0;
        past_cmplt_apntmnt_count=0;
        pre_sche_appint_count=0;
        pre_cmplt_appint_count=0;
        scheduled_count=0;
        appointment_cmplt_count=0;
        date5=0;
        date10=0
        date15=0;
        date20=0;
        date25=0;
        date30=0;
        below_25=0;
        upto_50=0;
        upto_75=0;
        Above=0;
        if group.name=="Member":
            user1=Payment.objects.get(user=user)
 	    today1=datetime.today()
            if user1.stripe_id=='0' and today1.date() > user.date_joined.date()+relativedelta(months=2):

                print("stripe id is 0") 
                return redirect('/registration/newpayment/') 
            else:
				query = Lead.objects.filter(member=user,status=s)
				count = query.count()
				s=Status.objects.get(status="Customer")
				queryset1=Status.objects.filter(status=s)
			
				queryset = Lead.objects.filter(status__in=queryset1,member=user)
				#print(queryset)
				count1 = queryset.count()
				var1 = Lead.objects.filter(member=user)
				context = RequestContext(request)
				user1=request.user.id
				timeline_lli=Timeline.objects.filter(user=user1).order_by('id')
	#             print("Existing customer count",customer.count())
				var5=timeline_lli.filter(Q(comment1="have created an ") |  Q(comment1="have created a "))
				customer_data=var5.filter(Q(comment2="Existing Customer") | Q(comment2="Lead"))
				print("customer dataaaaaaaaaa",customer_data)
				today=datetime.today()
				current_month=today.month
				current_month_days=calendar.monthrange(d.year,current_month)[1]
				for time in customer_data:
					var7=time.action_create.date();
					var8=var7.month
					var9=var7.day
					
	#                 print("toooooooooooooo---------------------------------")
					if (var7.year==today.year):
						if (var8==today.month):
							
		#                     print("today month....................................")
							if 1<=var9<=5:
		#                         print("in 1-5")
								start_date = date(d.year, d.month, 1)
								end_date = date(d.year, d.month, 6)
								var5=Timeline.objects.filter(Q(comment1="have created an ") |  Q(comment1="have created a "),user=request.user,action_create__range=(start_date, end_date))
								qureyset10=var5.filter(Q(comment2="Existing Customer") | Q(comment2="Lead"))
	#                             qureyset10=Timeline.objects.filter(user=request.user,action_create__range=(start_date, end_date))
								count5=qureyset10.count()
							elif 6 <=var9<=10:
								start_date = date(d.year, d.month, 6)
								end_date = date(d.year, d.month, 11)
								var5=Timeline.objects.filter(Q(comment1="have created an ") |  Q(comment1="have created a "),user=request.user,action_create__range=(start_date, end_date))
								qureyset11=var5.filter(Q(comment2="Existing Customer") | Q(comment2="Lead"))
								count6=qureyset11.count()
                                                               # print("count6666666666666666666666666666666666666",count6)
							elif 11 <=var9<=15:
								start_date = date(d.year, d.month, 11)
								end_date = date(d.year, d.month, 16)
								var5=Timeline.objects.filter(Q(comment1="have created an ") |  Q(comment1="have created a "),user=request.user,action_create__range=(start_date, end_date))
								qureyset12=var5.filter(Q(comment2="Existing Customer") | Q(comment2="Lead"))
								count7=qureyset12.count()
							elif 16 <=var9<=20:
								start_date = date(d.year, d.month, 16)
								end_date = date(d.year, d.month, 21)
								var5=Timeline.objects.filter(Q(comment1="have created an ") |  Q(comment1="have created a "),user=request.user,action_create__range=(start_date, end_date))
								qureyset13=var5.filter(Q(comment2="Existing Customer") | Q(comment2="Lead"))
								count8=qureyset13.count()
							elif 21 <=var9<=25:
								start_date = date(d.year, d.month, 21)
								end_date = date(d.year, d.month, 26)
								var5=Timeline.objects.filter(Q(comment1="have created an ") |  Q(comment1="have created a "),user=request.user,action_create__range=(start_date, end_date))
								qureyset14=var5.filter(Q(comment2="Existing Customer") | Q(comment2="Lead"))
								count9=qureyset14.count()
							else:
								start_date = date(d.year, d.month, 26)
								end_date = date(d.year, d.month, current_month_days)
								var5=Timeline.objects.filter(Q(comment1="have created an ") |  Q(comment1="have created a "),user=request.user,action_create__range=(start_date, end_date))
								qureyset15=var5.filter(Q(comment2="Existing Customer") | Q(comment2="Lead"))
								count10=qureyset15.count()
					else:
							
						counttt=timeline_lli.count()
	#end of line chart
	#  bar chart
				member_i=UserProfile.objects.filter(user=int(user.id))
				status_schedule=Status.objects.filter(status="Scheduled")
				status_job_complete=Status.objects.filter(status="Job Completed")
				member_idd=MemberAppointment.objects.filter(Q(member=member_i) & Q(status=status_job_complete))
				member_id=MemberAppointment.objects.filter(Q(member=member_i) & Q(status=status_schedule))
				today_month=today.strftime('%B')
	#             print("sdfghjklkjhgfdsdfghjkjhgfdfghjkgfdfkhgfdhjjgf",today_month)
				today=datetime.today()
				current_month=today.month
				pre_month=today.month-1
	#             print("pre-monthhhhhhhhhhhhhhhhhhhhhhhhhh",pre_month)
				pre_month_str=calendar.month_name[int(pre_month)]
	#             print("fsdaghsdfhagsfdghasfghfasghfas",pre_month_str)
				past_month=today.month-2
				past_month_str=calendar.month_name[int(past_month)]
				customer=timeline_lli.filter(comment2="Existing Customer")
				lead=timeline_lli.filter(comment2="Lead")
	#customer added on current month
				if (current_month==2):
					start_date = date(d.year, current_month, 1)
					end_date = date(d.year, current_month, 28)
					scheduled_date=customer.filter(action_create__range=(start_date, end_date))
					current_cmplt_date=lead.filter(action_create__range=(start_date, end_date))
					customer_added=scheduled_date.count()
					lead_added=current_cmplt_date.count()
				else:
					start_date = date(d.year, current_month, 1)
					end_date = date(d.year, current_month, current_month_days)
					scheduled_date=customer.filter(action_create__range=(start_date, end_date))
					current_cmplt_date=lead.filter(action_create__range=(start_date, end_date))
					customer_added=scheduled_date.count()
					lead_added=current_cmplt_date.count()
	#customer added on pre month
				if (pre_month==0):
					start_date = date(d.year, 12, 1)
					end_date = date(d.year, 12, 31)
					scheduled_date=customer.filter(action_create__range=(start_date, end_date))
					current_cmplt_date=lead.filter(action_create__range=(start_date, end_date))
					pre_customer_added=scheduled_date.count()
					pre_lead_added=current_cmplt_date.count()
				elif (pre_month==2):
					start_date = date(d.year, pre_month, 1)
					end_date = date(d.year, pre_month, 28)
					scheduled_date=customer.filter(action_create__range=(start_date, end_date))
					current_cmplt_date=lead.filter(action_create__range=(start_date, end_date))
					pre_customer_added=scheduled_date.count()
					pre_lead_added=current_cmplt_date.count()
				else:
					start_date = date(d.year, pre_month, 1)
					end_date = date(d.year, pre_month, 30)
					scheduled_date=customer.filter(action_create__range=(start_date, end_date))
					current_cmplt_date=lead.filter(action_create__range=(start_date, end_date))
					pre_customer_added=scheduled_date.count()
	#             print("customer_added",pre_customer_added)
					pre_lead_added=current_cmplt_date.count()
	#             print("lead_added",pre_lead_added)
				
	#customer added on past month
				if(past_month==-1):
					start_date = date(d.year, 11, 1)
					end_date = date(d.year, 11, 30)
					scheduled_date=customer.filter(action_create__range=(start_date, end_date))
					current_cmplt_date=lead.filter(action_create__range=(start_date, end_date))
					past_customer_added=scheduled_date.count()
					past_lead_added=current_cmplt_date.count()
					
				elif(past_month==0):
					start_date = date(d.year, 12, 1)
					end_date = date(d.year, 12, 31)
					scheduled_date=customer.filter(action_create__range=(start_date, end_date))
					current_cmplt_date=lead.filter(action_create__range=(start_date, end_date))
					past_customer_added=scheduled_date.count()
					past_lead_added=current_cmplt_date.count()
				elif(past_month==2):
					start_date = date(d.year, past_month, 1)
					end_date = date(d.year, past_month, 28)
					scheduled_date=customer.filter(action_create__range=(start_date, end_date))
					current_cmplt_date=lead.filter(action_create__range=(start_date, end_date))
					past_customer_added=scheduled_date.count()
					past_lead_added=current_cmplt_date.count()
				else:
					start_date = date(d.year, past_month, 1)
					end_date = date(d.year, past_month, 30)
					scheduled_date=customer.filter(action_create__range=(start_date, end_date))
					current_cmplt_date=lead.filter(action_create__range=(start_date, end_date))
					past_customer_added=scheduled_date.count()
					past_lead_added=current_cmplt_date.count()  
	# for current month
				if(current_month==2):
					start_date = date(d.year, current_month, 1)
					end_date = date(d.year, current_month, 28)
					scheduled_date=member_id.filter(date_appointment__range=(start_date, end_date))
					current_cmplt_date=member_idd.filter(date_appointment__range=(start_date, end_date))
					scheduled_count=scheduled_date.count()
					appointment_cmplt_count=current_cmplt_date.count()
				else:
					start_date = date(d.year, current_month, 1)
					end_date = date(d.year, current_month, current_month_days)
					scheduled_date=member_id.filter(date_appointment__range=(start_date, end_date))
					current_cmplt_date=member_idd.filter(date_appointment__range=(start_date, end_date))
					scheduled_count=scheduled_date.count()
					appointment_cmplt_count=current_cmplt_date.count()
	# for pre month
				if(pre_month==0):
					start_date = date(d.year, 12, 1)
					end_date = date(d.year, 12, 31)
					pre_scheduled_date=member_id.filter(date_appointment__range=(start_date, end_date))
					pre_cmplt_date=member_idd.filter(date_appointment__range=(start_date, end_date))
					pre_sche_appint_count=pre_scheduled_date.count()
					pre_cmplt_appint_count=pre_cmplt_date.count()
				elif(pre_month==2):
					start_date = date(d.year, pre_month, 1)
					end_date = date(d.year, pre_month, 28)
					pre_scheduled_date=member_id.filter(date_appointment__range=(start_date, end_date))
					pre_cmplt_date=member_idd.filter(date_appointment__range=(start_date, end_date))
					pre_sche_appint_count=pre_scheduled_date.count()
					pre_cmplt_appint_count=pre_cmplt_date.count()
	# for past month
				if(past_month==-1):
					start_date = date(d.year, 12, 1)
					end_date = date(d.year, 12, 31)
					past_scheduled_date=member_id.filter(date_appointment__range=(start_date, end_date))
					past_cmplt_date=member_idd.filter(date_appointment__range=(start_date, end_date))
					past_sche_apntmnt_count=past_scheduled_date.count()
					past_cmplt_apntmnt_count=past_cmplt_date.count()
				elif(past_month==0):
					start_date = date(d.year, 11, 1)
					end_date = date(d.year, 11, 30)
					past_scheduled_date=member_id.filter(date_appointment__range=(start_date, end_date))
					past_cmplt_date=member_idd.filter(date_appointment__range=(start_date, end_date))
					past_sche_apntmnt_count=past_scheduled_date.count()
					past_cmplt_apntmnt_count=past_cmplt_date.count()
				elif(past_month==2):
					start_date = date(d.year, past_month, 1)
					end_date = date(d.year, past_month, 28)
					past_scheduled_date=member_id.filter(date_appointment__range=(start_date, end_date))
					past_cmplt_date=member_idd.filter(date_appointment__range=(start_date, end_date))
					past_sche_apntmnt_count=past_scheduled_date.count()
					past_cmplt_apntmnt_count=past_cmplt_date.count()
				else:
					start_date = date(d.year, past_month, 1)
					end_date = date(d.year, past_month, 30)
					past_scheduled_date=member_id.filter(date_appointment__range=(start_date, end_date))
					past_cmplt_date=member_idd.filter(date_appointment__range=(start_date, end_date))
					past_sche_apntmnt_count=past_scheduled_date.count()
					past_cmplt_apntmnt_count=past_cmplt_date.count()
	#end bar chart 
	# number of request
				no_lead=Lead.objects.filter(member=request.user)
				for req in no_lead:
					re_count=customer_request.objects.filter(customer=req.id)
					for dd in re_count:
						reqq_date=dd.date_request
						if reqq_date:
							var8=reqq_date.month
							var9=reqq_date.day
							
							if (var8==today.month):
								if 1<=var9<=5:
									start_date = date(d.year, d.month, 1)
									end_date = date(d.year, d.month, 6)
									qureyset16=customer_request.objects.filter(date_request__range=(start_date, end_date))
									count11=qureyset16.count()+date5
								elif 6 <=var9<=10:
									start_date = date(d.year, d.month, 6)
									end_date = date(d.year, d.month, 11)
									qureyset17=customer_request.objects.filter(date_request__range=(start_date, end_date))
									count12=qureyset17.count()+date10
								elif 11 <=var9<=15:
									start_date = date(d.year, d.month, 11)
									end_date = date(d.year, d.month, 16)
									qureyset18=customer_request.objects.filter(date_request__range=(start_date, end_date))
									count13=qureyset18.count()+date15
								elif 16 <=var9<=20:
									start_date = date(d.year, d.month, 16)
									end_date = date(d.year, d.month, 21)
									qureyset19=customer_request.objects.filter(date_request__range=(start_date, end_date))
									count14=qureyset19.count()+date20
								elif 21 <=var9<=25:
									start_date = date(d.year, d.month, 21)
									end_date = date(d.year, d.month, 26)
									qureyset20=customer_request.objects.filter(date_request__range=(start_date, end_date))
									count15=qureyset20.count()+date25
								else:
									if (d.month==2):
										start_date = date(d.year, d.month, 26)
										end_date = date(d.year, d.month, 28)
										qureyset21=customer_request.objects.filter(date_request__range=(start_date, end_date))
										count16=qureyset21.count()
									else:
										start_date = date(d.year, d.month, 26)
										end_date = date(d.year, d.month, current_month_days)
										qureyset21=customer_request.objects.filter(date_request__range=(start_date, end_date))
										count16=qureyset21.count()
							else:
									print("none")
					
	#end of number of request 
	# appintment start
				appp=Promotions.objects.filter(member=user.id)
				pricee=appp.filter(~Q(price=0))
				price_count=pricee.count()
				discount_c=appp.filter(~Q(discount=0))
				discount_count=discount_c.count()
				discount1=0;
				discount2=0;
				discount3=0;
				discount4=0;
				discount2=0;
				status_pending=Status.objects.get(status="Pending")
				for discountt in appp:
					discount_=discountt.discount
					if 0 <=discount_<=25:
							below_25=Promotions.objects.filter(member=user.id,discount=discount_)
							discount1=below_25.count()
					elif 26<=discount_<=50:
							upto_50=Promotions.objects.filter(member=user.id,discount=discount_)
							discount2=upto_50.count()
					elif 51<=discount_<=75:
							upto_75=Promotions.objects.filter(member=user.id,discount=discount_)
							discount3=upto_75.count()
					else:
						Above=Promotions.objects.filter(member=user.id, discount=discount_)
						discount4=Above.count()
	# End of appointment  

				var3=customer_request.objects.filter(customer__in=var1,emergency_status=None,date__gte = today.date(),status=status_pending)
				count2 = var3.count()
				profile=UserProfile.objects.get(user=user)
				today=datetime.today()
				queryset3 = MemberAppointment.objects.filter(~Q(status=Status.objects.get(status="Job Completed")),member=profile, date=today)
				count3= queryset3.count()
				cust = Lead.objects.filter(member=user, status= s)
				cust_user= lead_user.objects.filter(customer__in=cust)
				id=[]
				for cust in cust_user:
					id.append(cust.user.pk)
				cust_arr=[]
				cust_login= User.objects.filter(id__in=id)
				for cust in cust_login:
					if cust.last_login==None:
						pass
					else:
						y= cust.last_login.date()
						if y == today.date():
							cust_arr.append(cust)
				count4=len(cust_arr)
	# start of top five customers
				
				customer = Lead.objects.filter(member=request.user)
				list2=[]
				for custt in customer:
					request1=customer_request.objects.filter(customer=custt)
	#                 print("customerrrrrrrrrrrrrrrrrrr",request1)
					list2.append(request1)
	#                 custt.save()
	#             print("most request customerrrrrrrrrrrrrrrrr",list2)
				cnt=0
				k=[]
				
				for r in list2:
	#                print("hsghjgajhgJHDGJHASGDJHGASDJHAGSDJHAGSDJHGASDASD",len(r))
				
				   if len(r)!=0:
					for s in r:
	#                     print (s)
						k.append(s)
	#                     print("KKKKKKKKKKKK", k)
				groupnames=customer_request.objects.filter(id__in=[r.id for r in k]).values("customer__name","customer__last_name").annotate(request_count=Count('customer')).order_by('-request_count')[:5]
	# end of top five customers
	# start of top five promotions
				all_promo=Promotions.objects.filter(member=user)
				result=[]
				for promo in all_promo:
					cust_request=customer_request.objects.filter(promotion=promo)
					result.append(list(itertools.chain(cust_request)))
				cnt=0
				k=[]
				for r in result:
				   if len(r)!=0:
					for s in r:
					   k.append(s)
				sorted_dictt=customer_request.objects.filter(id__in=[r.id for r in k]).values("promotion__coupon_code","promotion__Service_id_id__service_type").annotate(promotion_count=Count('promotion')).order_by('-promotion_count')[:5]     
	# end of top five promotions

	#emergency request start
				customer = Lead.objects.filter(member=request.user)
				jan=[]
				feb=[]
				march=[]
				april=[]
				may=[]
				june=[]
				july=[]
				aug=[]
				sept=[]
				oct=[]
				nov=[]
				dec=[]
				for abc in customer:
					#jan month
					start_date = date(today.year, 1, 1)
					end_date = date(today.year,1, 31)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					jan.append(emergency_req_count)
					#feb month
					start_date = date(today.year, 2, 1)
					end_date = date(today.year,2, 28)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					feb.append(emergency_req_count)
					#march month
					start_date = date(today.year, 3, 1)
					end_date = date(today.year,3, 31)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					march.append(emergency_req_count)
					#april month
					start_date = date(today.year, 4, 1)
					end_date = date(today.year,4, 30)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					april.append(emergency_req_count)
					#may month
					start_date = date(today.year, 5, 1)
					end_date = date(today.year,5, 31)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					may.append(emergency_req_count)
					#june month
					start_date = date(today.year, 6, 1)
					end_date = date(today.year,6, 30)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					june.append(emergency_req_count)
					#july month
					start_date = date(today.year, 7, 1)
					end_date = date(today.year,7, 31)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					july.append(emergency_req_count)
					#aug month
					start_date = date(today.year, 8, 1)
					end_date = date(today.year,8, 31)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					aug.append(emergency_req_count)
					#sept month
					start_date = date(today.year, 9, 1)
					end_date = date(today.year,9, 30)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					sept.append(emergency_req_count)
					#oct month
					start_date = date(today.year, 10, 1)
					end_date = date(today.year,10, 31)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					oct.append(emergency_req_count)
					#nov month
					start_date = date(today.year, 11, 1)
					end_date = date(today.year,11, 30)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					nov.append(emergency_req_count)
					#dec month
					
					start_date = date(today.year, 12, 1)
					end_date = date(today.year,12, 31)
					req=customer_request.objects.filter(Q(customer=int(abc.id)) & Q(emergency_status=1))
					this_month_service=req.filter(date_request__range=(start_date, end_date))
					emergency_req_count=this_month_service.count()
					dec.append(emergency_req_count)
				jan_e_req_count=0
				feb_e_req_count=0
				march_e_req_count=0
				april_e_req_count=0
				may_e_req_count=0
				june_e_req_count=0
				july_e_req_count=0
				aug_e_req_count=0
				sept_e_req_count=0
				oct_e_req_count=0
				nov_e_req_count=0
				dec_e_req_count=0
				for i in jan:
					jan_e_req_count=jan_e_req_count+i
				for i in feb:
					feb_e_req_count=feb_e_req_count+i
				for i in march:
					march_e_req_count=march_e_req_count+i
				for i in april:
					april_e_req_count=april_e_req_count+i
				for i in may:
					may_e_req_count=may_e_req_count+i
				for i in june:
					june_e_req_count=june_e_req_count+i
				for i in july:
					july_e_req_count=july_e_req_count+i
				for i in aug:
					aug_e_req_count=aug_e_req_count+i
				for i in sept:
					sept_e_req_count=sept_e_req_count+i
				for i in oct:
					oct_e_req_count=oct_e_req_count+i
				for i in nov:
					nov_e_req_count=nov_e_req_count+i
				for i in dec:
					dec_e_req_count=dec_e_req_count+i
				
	#emergency request end
				start_date = date(today.year,d.month, 1)
                                end_date = date(today.year,d.month, current_month_days)
                                reques_receved=customer_request.objects.filter(customer__in=var1).exclude(status_id__in=[0,1,2,3,4,7,5,6,8,11])
                                request_today_month=reques_receved.filter(date_request__range=(start_date, end_date))
                                request_count = request_today_month.count()
                                apt_sche=customer_request.objects.filter(customer__in=var1).exclude(status_id__in=[0,10])
                                atp_sche_today_month=apt_sche.filter(date_request__range=(start_date, end_date))
                                scheduled_apt= atp_sche_today_month.count()
				today_year=today.year
				promotion_add=Timeline.objects.filter(Q(user=request.user)  & Q(comment2="promotion")).order_by('-id')[:1]
				E_customer_add=Timeline.objects.filter(Q(user=request.user) & Q(comment2="Existing Customer")).order_by('-id')[:1]
                                Lead_add=Timeline.objects.filter(Q(user=request.user) & Q(comment2="Lead")).order_by('-id')[:1]
				Appointment_add=Timeline.objects.filter(Q(user=request.user)  & Q(comment2="Appointment")).order_by('-id')[:1]
				update_profile=Timeline.objects.filter(Q(user=request.user) & Q(comment2="profile")).order_by('-id')[:1]
				timeline_list = Timeline.objects.filter(user=request.user).order_by('-id')[:4]
				return render(request,'registration/success.html',{'scheduled_apt':scheduled_apt,'request_count':request_count,'Lead_add':Lead_add,'sorted_dictt':sorted_dictt,'today_year':today_year,'dec_e_req_count':dec_e_req_count,'nov_e_req_count':nov_e_req_count,'oct_e_req_count':oct_e_req_count,'sept_e_req_count':sept_e_req_count,'aug_e_req_count':aug_e_req_count,'july_e_req_count':july_e_req_count,'june_e_req_count':june_e_req_count,'may_e_req_count':may_e_req_count,'april_e_req_count':april_e_req_count,'march_e_req_count':march_e_req_count,'feb_e_req_count':feb_e_req_count,'jan_e_req_count':jan_e_req_count,'update_profile':update_profile,'Appointment_add':Appointment_add,'E_customer_add':E_customer_add,'promotion_add':promotion_add,'sorted_dictt':sorted_dictt,'groupnames':groupnames,'past_lead_added':past_lead_added,'past_customer_added':past_customer_added,'pre_lead_added':pre_lead_added,'pre_customer_added':pre_customer_added,'lead_added':lead_added,'customer_added':customer_added,'discount_count':discount_count,'price_count':price_count,'discount1':discount1,'discount2':discount2,'discount3':discount3,'discount4':discount4,'count11':count11,'count12':count12,'count13':count13,'count14':count14,'count15':count15,'count16':count16,'today_month':today_month,'pre_month_str':pre_month_str,'past_month_str':past_month_str,'count':count,'count1':count1,'count2':count2,'count3':count3,'count4':count4,'count5':count5,'count6':count6,'count7':count7,'count8':count8,'count9':count9,'count10':count10,'scheduled_count':scheduled_count,'appointment_cmplt_count':appointment_cmplt_count,'pre_sche_appint_count':pre_sche_appint_count,'pre_cmplt_appint_count':pre_cmplt_appint_count,'past_sche_apntmnt_count':past_sche_apntmnt_count,'past_cmplt_apntmnt_count':past_cmplt_apntmnt_count,'last_cust': cust_arr,"group":group})
        elif group.name =="Customer":
            return redirect("/promotion/")
        
        elif group.name =="Lead":
            return redirect("/promotion/")
            
        elif group.name == "E_Customer":
            return HttpResponseRedirect(reverse('Registration:updatedetails', args=(request.user.pk,)))  
#     except Exception as e:
#           print(e)
#           return render(request,'Registration/404.html')
  
        
@login_required(login_url="/registration/login/")
def businesscard(request, user_id):
    user=request.user
    print(user)
    user=request.user
    group=Group.objects.get(user=user)
    detail1 = get_object_or_404(User, pk=user_id)
    detail2 = get_object_or_404(UserProfile, user=detail1)
    list=EBC.objects.filter(send_user=user).order_by('-ebctime')
    ctx={'list':list,'email':detail1,'website':detail2.website, 'fname':detail1.first_name, 'lname':detail1.last_name, 'phone':detail2.phone_no, 'shopname':detail2.shop_name, 'shopaddress':detail2.shop_address, 'city': detail2.city, 'country':detail2.country, 'group':group,'area_code':detail2.area_code}
    return render(request, 'registration/EBC.html', ctx)


@login_required(login_url="/registration/login/")
def businesscard_cust(request, user_id):
    server1 = get_object_or_404(User, pk=user_id)
    print("cust is a user=========", server1.id)
    group=Group.objects.get(user=server1)
    print("group of user is ==", group)
    if group.name=="Company":
        print("in group company")
        company_obj=CustCompany.objects.get(email=server1.email)
        detail1 = get_object_or_404(User, pk=company_obj.member.pk)
        #print("!!!!!!!!!!!",detail1)
        detail2 = get_object_or_404(UserProfile, user=detail1)
       # print("!!!!!!!!!!! print",detail2)
      
        address=UserProfile.objects.get(user=company_obj.member)
        list=EBC.objects.filter(send_user=request.user).order_by('-ebctime')
        ctx={'list':list,'email':detail1,'website':detail2.website, 'fname':detail1.first_name, 'lname':detail1.last_name, 'phone':detail2.phone_no, 'shopname':detail2.shop_name, 'shopaddress':detail2.shop_address, 'city': detail2.city, 'country':detail2.country, 'group':group, 'address':address}
        return render(request, 'registration/EBC.html',ctx)
    elif group.name=='Customer':
        cust_detail=lead_user.objects.get(user=server1.id)
        print("this is cust detail===", cust_detail.customer.id)
        mem_detail=Lead.objects.get(id=cust_detail.customer.id)
        print("this is member user ID=====", mem_detail.member.id)
        customer=lead_user.objects.get(user=server1)
        cust = Lead.objects.get(pk=customer.customer.pk)
        address= UserProfile.objects.get(user=cust.member) 
    
        detail1 = get_object_or_404(User, pk=mem_detail.member.id)
        detail2 = get_object_or_404(UserProfile, user=detail1)
        list=EBC.objects.filter(send_user=request.user).order_by('-ebctime')
        ctx={'list':list,'email':detail1,'website':detail2.website, 'fname':detail1.first_name, 'lname':detail1.last_name, 'phone':detail2.phone_no, 'shopname':detail2.shop_name, 'shopaddress':detail2.shop_address, 'city': detail2.city, 'country':detail2.country, 'group':group, 'address':address,'area_code':detail2.area_code}
        return render(request, 'registration/EBC.html', ctx)


def faq(request):
    return render(request, 'registration/FAQ.html')

@login_required(login_url="/registration/login/")
def enroll(request):
    user = request.user
    print("userrrrrrrrr================", user.id)
    group=Group.objects.get(user=user)
    
    return render(request, 'registration/enrollment.html', {'group':group,})

def pdfopen(request):
    return render(request,'registration/pdfopen.html')

def custom_404(request):
    print("on 404")
    return render(request,'registration/404.html')

@login_required(login_url="/registration/login/")
def subscribe(request):
    user=request.user 
    payment=Payment.objects.get(user=user)
    print(payment.stripe_id)
    if payment.stripe_id=='0':
            if request.method == 'POST':
             form = CardForm(data=request.POST)
             #user_form=UserProfileForm(request.POST)
             if form.is_valid(): #and user_form.is_valid():
               print("form valid")
               customer = stripe.Customer.create(
               description = user.email,
               card = form.cleaned_data['stripe_token'],
                plan = "daily-1",
		tax_percent=10
                )
               
               charge = stripe.Charge.create(
                   amount=5000, # amount in cents, again
                   currency="AUD",
                   customer=customer.id,
                   description="Charge for portal.autoxtion.com.au",
                   #receipt_email=user.email,
               )
               paym= Payment.objects.get(user=user)
               print(paym)
               digits=form.cleaned_data['last_4_digits']
               paym.last_4_digits=digits
               paym.stripe_id=customer.id
               paym.subscribed=True 
               paym.save()
               today=datetime.today()
               var=UserProfile.objects.get(user=user)
               var.payment_date=today
               var.save()
              
               return redirect('/registration/success/') 
                   
             else:
               print("form invalid")
            else:
               print("else")
               form = CardForm()
             
               return render_to_response(
                 'registration/subscribed.html',
                 {
                   'form': form,
                   'months': range(1, 13),
                   'publishable': settings.STRIPE_PUBLISHABLE,
                   'soon': soon(),
                   'user': user,
                   'years': range(2011, 2036),
                 },
                 context_instance=RequestContext(request)
           )
    else:
        plan=stripe.Plan.retrieve('daily-1')
        print(plan)
        customer = stripe.Customer.retrieve(payment.stripe_id)
        print("subscription1---",customer)
        stripe.Subscription.create(
                                   customer=payment.stripe_id,
                                   plan=plan
                                   )
        profile=UserProfile.objects.get(user=user)
        profile.status=None
        profile.save()
        return redirect('/registration/success/')

@login_required(login_url="/registration/login/")
def resubscribe(request):
    return render(request, 'registration/resubscribed.html')


def demologin(request):
  logger.info("start of login view")
  logger.debug("start of login view")
    
      #email = request.POST.get('email')
      #password = request.POST.get('password')
  print("in demo login")
  user = authenticate(username ="demo@yopmail.com", password="Admin@1234")
  print(user)
  if user is not None:
    if user.is_active:
        print("User is active")
        request.session['user']=user.username
        auth_login(request, user)
        logger.debug("End of login Views")
        return redirect('/registration/success/')
    else:
        logger.debug("User is not active")
  else:
          logger.debug("Unknown User")
          return render(request,'registration/login.html', {'context1': "Incorrect User Name or Password"})

def getVcard(request):
    print("in simple view getVcard")
    user=request.user
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",str(user.id))
    group=Group.objects.get(user=user)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",group)
    mem_detail=user
    print("((((((((((((((((",mem_detail.id)
    mail_id=request.POST.get("email")
    name=request.POST.get("name")
    today=datetime.today()
    ebc=EBC(email=mail_id,name=name,ebctime=today.date(),send_user=user)
    ebc.save()
    
    print("currently loggedin user",user.email,mail_id)
    
    group=Group.objects.get(user=user)
    if group.name=="Member": 
        messages.success(request,'Email has been sent to Email Id')
        send_vcf_email_task.delay(mail_id,user.email,name,mem_detail.id)
        print(name)
        print(user.email)
        print(mail_id)
        return redirect('/registration/EBC/'+str(user.id))
    else:
        print("in other than member")
        lead_u=lead_user.objects.get(user=user)
        lead=Lead.objects.get(pk=lead_u.customer.pk)
        member=User.objects.get(pk=lead.member.pk)
        msg1="Email has been sent to "+str(mail_id)
        messages.success(request,msg1)
        send_vcf_email_task.delay(mail_id,member.email,name,member.id)
        return redirect('/registration/EBC_cust/'+str(user.id))

    
def getVcard1(request):
    
    print("in simple view getVcard1")   
    user=request.user
    mem_detail=user
    mail_id=request.POST.get("email")
    name=request.POST.get("name")
    today=datetime.today()
    ebc=EBC(email=mail_id,name=name,ebctime=today.date(),send_user=user)
    ebc.save()
    print("currently loggedin user",user.email,mail_id)
    
    group=Group.objects.get(user=user)
    if group.name=="Member": 
        messages.success(request,'Email has been sent to Email Id')
        send_vcf_email_task1.delay(mail_id,user.email,name)
        print(name)
        print(user.email)
        print(mail_id)
        return redirect('/registration/EBC/'+str(user.id))
    elif group.name=='Company':
        messages.success(request,'Email has been sent to Email Id')
        company_obj=CustCompany.objects.get(email=user.email)
        send_vcf_email_task1.delay(mail_id,company_obj.member.email,name)
        print(name)
        print(user.email)
        print(mail_id)
        return redirect('/registration/EBC_cust/'+str(user.id))
    else:
        print("in other than member")
        lead_u=lead_user.objects.get(user=user)
        lead=Lead.objects.get(pk=lead_u.customer.pk)
        member=User.objects.get(pk=lead.member.pk)
        msg1="Email has been sent to "+str(mail_id)
        messages.success(request,msg1)
        send_vcf_email_task1.delay(mail_id,member.email,name)
        return redirect('/registration/EBC_cust/'+str(user.id))

@login_required(login_url="/registration/login/") 
def user_image(request,user_id):
    print("start of user_image view")
    server1 = get_object_or_404(User, pk=user_id)
   
    group=Group.objects.get(user=server1)
    print(group)
    if group.name=="Member":
         server2 = get_object_or_404(UserProfile, user_id=request.user.id)
#          server3=get_object_or_404(Lead,id=request.user.id)
         if request.method == 'POST':
            print("post ")
            userimage = User_imageForm(request.POST,request.FILES)
            update_profile = UpdateProfileForm(request.POST)
            print userimage.errors
            if userimage.is_valid():
                print("form is valid")
                k=userimage.save(commit=False)
                print("image",request.FILES['user_image'])
                server2.user_image=request.FILES['user_image']
                server2.save()
                user=request.user
                print("5555555555555",user.id)
                return redirect('/registration/updatedetails/'+str(user.id))
            else:
                userimage = User_imageForm()
                update_profile = UpdateProfileForm(request.POST)
                
            variables = RequestContext(request, {'userimage': userimage, 'update_profile':update_profile})
            return render_to_response('registration/member_profile.html',variables,)
        
    elif group.name=="Customer":
            print("this is customer")
            print(server1.pk)
            lead_u=lead_user.objects.get(user=server1)
            print(lead_u.pk,lead_u.customer)
            lead=Lead.objects.get(pk=lead_u.customer.pk)
#             address= UserProfile.objects.get(user=lead.member) 
            mem=lead.member
            print(mem)
            print(lead.id)
            userimage1 = cust_imageForm(request.POST,request.FILES)
            if request.method=='POST':
                print("post request---------")
                if userimage1.is_valid():
                    print("form is valid")
                    k1=userimage1.save(commit=False)
                    print("image",request.FILES['image'])
                    lead.image=request.FILES['image']
                    lead.save()
                
                user=request.user
                print("5555555555555",user.id)
                return redirect('/registration/updatedetails/'+str(user.id))
                    
                   
                   
            else:
                userimage1 = cust_imageForm()
                user=request.id   
                variables = RequestContext(request, {'user':user})
        
                return render_to_response('registration/profile_cust.html',variables,)
    elif group.name=="Lead":
        print("this is leaddddddddddddd")
        lead_u=lead_user.objects.get(user=server1)
        print(lead_u.pk,lead_u.customer)
        lead=Lead.objects.get(pk=lead_u.customer.pk)
        userimage1 = cust_imageForm(request.POST,request.FILES)
        if request.method=='POST':
                print("post request---------")
                if userimage1.is_valid():
                    print("form is valid")
                    k1=userimage1.save(commit=False)
                    print("image",request.FILES['image'])
                    lead.image=request.FILES['image']
                    lead.save()
                
                user=request.user
                print("5555555555555",user.id)
                return redirect('/registration/updatedetails/'+str(user.id))
                    
                   
                   
        else:
                userimage1 = cust_imageForm()
                user=request.id   
                variables = RequestContext(request, {'user':user})
        
                return render_to_response('registration/profile_cust.html',variables,)

    elif group.name=="Company":
        cust=CustCompany.objects.get(email=server1.email)
        print("$$$$$$$$",cust)
        company=CustForm(instance=cust)
        userimage1 = company_imageForm()
        print("!!@@@@@@@@@@",userimage1)
        val=getProfileCompletedCount(cust.pk,group.name)
        #  timeline_li=Timeline.objects.filter(user=request.user).order_by('-id')[:5]
        if request.method=='POST':
                print("in post")
                userimage1 = company_imageForm(request.POST,request.FILES)
                if userimage1.is_valid():
                    print("form is valid")
                    k1=userimage1.save(commit=False)
                    print("image",request.FILES['image'])
                    cust.image=request.FILES['image']
                    cust.save()
                   # messages.success="Your profile updatesd successfully"
                    return render(request,'registration/company_profile.html',{'val':val,'group':group,'company':company,'userimage1':userimage1,'image2':cust,'updatepassword':ChangePasswordForm,'image2':cust,'context1': "Your details has been updated"})   
                else:
                    userimage1 = company_imageForm()
                    user=request.id   
                    variables = RequestContext(request, {'user':user})   
                # auth_login(request, user)
                    return render(request,'registration/company_profile.html',{'val':val,'group':group,'company':company,'userimage1':userimage1,'image2':cust,'updatepassword':ChangePasswordForm,'context2': "Please enter all valid details"})  
        
        else:
            company=CustForm(instance=cust)
            userimage1 = company_imageForm(instance=cust)
            return render(request,'registration/company_profile.html',{'val':val,'group':group,'image2':cust,'company':company,'userimage1':userimage1,'updatepassword':ChangePasswordForm})  
             

    else:
            lead_u=lead_user.objects.get(user=server1)
            print(lead_u.pk,lead_u.customer)
            lead=Lead.objects.get(pk=lead_u.customer.pk)
            userimage1 = cust_imageForm(request.POST,request.FILES)
            if request.method=='POST':
                    print("post request---------")
                    if userimage1.is_valid():
                        print("form is valid")
                        k1=userimage1.save(commit=False)
                        print("image",request.FILES['image'])
                        lead.image=request.FILES['image']
                        lead.save()
                    
                    user=request.user
                    print("5555555555555",user.id)
                    return redirect('/registration/updatedetails/'+str(user.id))
                        
                       
                       
            else:
                userimage1 = cust_imageForm()
                user=request.id   
                variables = RequestContext(request, {'user':user})
        
                return render_to_response('registration/profile_cust.html',variables,)


@login_required(login_url="/registration/login/") 
def user_header_image(request):
    print("image view")
    user=request.user
    print(user)
    group=Group.objects.get(user=user)
    print(group)
    if group.name=="Member":
        try:
            userprofile=UserProfile.objects.get(user=user)
            user_image=userprofile.user_image.name
            if user_image:
                print("@@@@@@@@@@@@",user_image)
                return JsonResponse(user_image,safe=False)
            else:
                 print("in else")
                 user_image="images/default_avatar.png"
                 return JsonResponse(user_image,safe=False)  
            
        except Exception as e:
            str_path="images/default_avatar.png"
            return JsonResponse(str_path, safe=False)
    elif group.name=="Company":
        try:
            custcompany_obj=CustCompany.objects.get(email=user.email)
            user_image=custcompany_obj.image.name
            if user_image:
                user_image=user_image[2:]
                print("s--------",user_image)
               # print("@@@@@@@@@@@@",user_image)
                return JsonResponse(user_image,safe=False)
            else:
                 print("in else")
                 user_image="images/default_avatar.png"
                 return JsonResponse(user_image,safe=False)  
            
        except Exception as e:
            str_path="images/default_avatar.png"
            return JsonResponse(str_path, safe=False)
    else:
        try:
            print("in customer")
            l_u=lead_user.objects.get(user=user)
            lead=Lead.objects.get(pk=l_u.customer.id)
            user_image=lead.image.name
            if user_image:
                print("@@@@@@@@@@@@",user_image)
                return JsonResponse(user_image,safe=False)
            else:
                 print("in else")
                 user_image="images/default_avatar.png"
                 return JsonResponse(user_image,safe=False)
        except Exception as e:
            print("in customer but image not assigned")
            user_image="images/default_avatar.png"
            print(user_image)
            return JsonResponse(user_image, safe=False)
def contact(request):
    return render(request, 'registration/contact.html')

def getProfileCompletedCount(pk,group):
    print("**************************************",pk, " ",group )
    val=0
    if group=="Member":
        userprofile_obj=UserProfile.objects.get(pk=pk)
        if userprofile_obj.user_image:
            val=val+10
        if userprofile_obj.phone_no:
            val=val+10
        if userprofile_obj.shop_address: 
            val=val+10
        if userprofile_obj.website:
            val=val+10
        if userprofile_obj.Emg_no:
            val=val+10
        if userprofile_obj.area_code:
            val=val+10
        if userprofile_obj.shop_name:
            val=val+10
        if userprofile_obj.postal_code:
            val=val+10
	if userprofile_obj.member_mech_license:
            val=val+5
        if userprofile_obj.member_mech_license_expiry_date:
            val=val+5
        if userprofile_obj.member_ARC_license:
            val=val+5
        if userprofile_obj.member_ARC_license_expiry_date:
            val=val+5
        
        return val
    if group=="Customer":
        lead=Lead.objects.get(pk=pk)
        lead_vehicle=Lead_Vehicle.objects.filter(lead=lead)
        if lead.address:
            val=val+10
        if lead.email:
            val=val+20
        if lead.phone or lead.email:
            val=val+20
        if lead.image:
            val=val+10
        if lead.road_side_assistant_num:
            val=val+5
        if lead.Emg_no:
            val=val+5
        if lead.policy_number:
            val=val+5
        if lead.name:
            val=val+5
        if lead.last_name:
            val=val+5
        if lead.licenseid:
            val=val+5
        if lead.license_expiry_date:
            val=val+5
        if lead.area_code:
            val=val+5

        return val
    if group=="Lead":
        lead=Lead.objects.get(pk=pk)
        lead_vehicle=Lead_Vehicle.objects.filter(lead=lead)
        if lead.address:
            val=val+10
        if lead.email:
            val=val+20
        if lead.phone or lead.email:
            val=val+20
        if lead.image:
            val=val+10
        if lead.road_side_assistant_num:
            val=val+5
        if lead.Emg_no:
            val=val+5
        if lead.policy_number:
            val=val+5
        if lead.name:
            val=val+5
        if lead.last_name:
            val=val+5
        if lead.licenseid:
            val=val+5
        if lead.license_expiry_date:
            val=val+5
        if lead.area_code:
            val=val+5

        return val
    if group=="E_Customer":
        lead=Lead.objects.get(pk=pk)
        lead_vehicle=Lead_Vehicle.objects.filter(lead=lead)
        if lead.address:
            val=val+10
        if lead.email:
            val=val+20
        if lead.phone or lead.email:
            val=val+20
        if lead.image:
            val=val+20
        if lead.Emg_no:
            val=val+10
        if lead.name:
            val=val+10
        if lead.licenseid:
            val=val+10
        return val
    if group=="Company":
        cust=CustCompany.objects.get(pk=pk)
        #lead_vehicle=Lead_Vehicle.objects.filter(lead=lead)
        if cust.company_name:
            val=val+20
        if cust.address:
            val=val+10
        if cust.email:
            val=val+20
        if cust.phone :
            val=val+20
        if cust.image:
            val=val+20
        if cust.person:
            val=val+10
        return val


def Video_tutorial(request):
    user=request.user
    print(user)
    group=Group.objects.get(user=user)
#     global token_id
#     client_id = 'b303b5ba86af219d286a06f8e23ef088ec13b086'
#     client_secret = 'Z6Dcif8WjYvw8HWX7lOuM/jW3ZZ9vN9uHlihajiZrs0vE93x7CxFCs6HGjgK51t2zPS3fjgxPZcIhqh2lsPQTnc4QqzK06KMRM+V5tCEUzByZBXVD/ztvaHD+FQ5KGRN'
#     encoded = base64.b64encode("%s:%s" % (client_id, client_secret))
#     headers =  {'content-type' : 'application/json',
#                 "Authorization": "basic %s" % encoded
#                 }
#    
#     r = requests.post('https://api.vimeo.com/oauth/authorize/client?grant_type=client_credentials',headers=headers)
#     print("RESPONSE OF1111111111 SERVICE", r)
#     #print("RESPONSE CONTENT", r.content)
#     response=r.json()
#     #print("access_token access_token",response)
#     i=0
#     for key, value in response.items():
#         i=i+1
#         if i==1:
#             #print("RESPONSE KEY VALUE",key, value)
#             token=value
#     
#     token_id=str(token)
#     print("token_idtoken_idtoken_id",token_id)
    headers =  {'content-type' : 'application/json',
                 'authorization': "bearer ca8197f54e0b59b2c92eae49cd10856f", 
                #'authorization': 'bearer '+str(token_id)
                }
   
    r = requests.get('https://api.vimeo.com/channels/1173724/videos',headers=headers)
    #print("RESPONSE OF 222222222222 SERVICE", r)
    response= r.json()
    #print("JSON RESPONSE",response)
    
    return render(request,"registration/vemo.html",{'response':response,'group':group})



def member_agree(request):
    member = request.POST.getlist('membername')
    for x in member:
        member1= UserProfile.objects.filter(pk=x)
        print('del pk',member1)
        if request.method == 'POST':
            for r in member1:
                print('rrrrrr',r)
                r.flag = 1
                r.save()
    return redirect('/registration/success/')


def member_agree2(request):
    member = request.POST.getlist('membername')
    for x in member:
        member1= UserProfile.objects.filter(pk=x)
        print('del pk',member1)
        if request.method == 'POST':
            for r in member1:
                print('rrrrrr',r)
                r.flag = 1
                r.save()
    return redirect('/registration/newpayment/')


def unlink_member(request):
    user=request.user
    lead_user1=lead_user.objects.get(user=user)
    lead=Lead.objects.get(pk=lead_user1.customer.pk)
    status=Status.objects.get(status="Deregister")
    lead.status=status
    lead.save()
    deactive_user=User.objects.get(username=user.username)
    deactive_user.is_active=False
    deactive_user.save()
    request_obj=customer_request.objects.filter(customer=lead).delete()
    print("deleted request:",request_obj)
    appointment_obj=MemberAppointment.objects.filter(customer=lead).delete()
    print("deleted appointments:",appointment_obj)
    feedback_obj=Feedback_Star.objects.filter(customer=lead).delete()
    print("deleted feedback:",feedback_obj)
    return redirect('/registration/logout/')