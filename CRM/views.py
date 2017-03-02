from django.shortcuts import render,get_object_or_404, render_to_response,redirect
import logging
from django.http import JsonResponse, HttpResponse
from django.db.transaction import commit
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory, model_to_dict,modelformset_factory
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template.base import kwarg_re
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import first
logger = logging.getLogger('CRM')
logger.addHandler(logging.NullHandler())
from .forms import *
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import random
import string
from Registration.models import *
from django.template.loader import render_to_string, get_template
from django.template import Context
from .tasks import * 
import xlrd
from Appointment.models import *
from Timeline.models import *
from django.utils import timezone
from CRM.filters import *
from rest_framework.views import APIView
from rest_framework import generics
from CRM.serializers import *
import requests
from rest_framework.permissions import *
from django.contrib import messages
from wsgiref.util import FileWrapper
import mimetypes
# Create your views here.

@login_required(login_url="/registration/login/")
def index(request):
    logger.info("start of index lead")
    logger.debug("start of index lead")
    try:
        user=request.user
        group=Group.objects.get(user=request.user)
        
        status=Status.objects.get(status="Lead")
        list=Lead.objects.filter(status=status,member=user)
        qlist=Question.objects.all()
        question_list=Question.objects.all()
        inlineformset=formset_factory(QualifyForm, extra=0)
        qform=inlineformset()
        qform=inlineformset(initial=[{'question':v.question}for v in question_list])
        if request.method=='POST':
            from_dt=request.POST.get("from_date")
            to_dt = request.POST.get("to_date")
            r = requests.get('http://198.15.126.59:8010/CRM/get_leadlist/'+str(user.pk)+'/'+str(from_dt)+'/'+ str(to_dt))
            list = r.json()
            return render(request,'CRM/leadlist.html',{'leadl':list,"st":"Customer",'group':group}) 
        logger.debug("lead list returned to leadlist.html")
        logger.info("lead list returned to leadlist.html",list)
        msg=None
        group=Group.objects.get(user=user)
        print("group of leadddd=====", group)
        filter = LeadFilter(request.GET, queryset=list)
        return render(request,'CRM/leadlist.html',{'leadl':list,'qlist':qlist,'qform':qform,'user':user,'group':group,'filter':filter })
    except Exception as e:
        print(e)
        return render(request,'CRM/404.html')


@login_required(login_url="/registration/login/")
def addlead(request):
    try:
        user=request.user
        group=Group.objects.get(user=user)
        leadform=LeadForm()
        InlineFormSet = formset_factory(form=LeadVehicle_Form)
        vehicleform=InlineFormSet()
        if request.method=='POST':
            leadform = LeadForm(request.POST)
            vehicleform= InlineFormSet(request.POST )
            print("------------------------",leadform.errors)
            if leadform.is_valid() and vehicleform.is_valid():
                cd=leadform.cleaned_data
                print(cd.get('email'))
                lead_list=Lead.objects.filter(email=cd.get('email'))
                user=User.objects.filter(username=cd.get('email'))
                len1=len(lead_list)
            
                len2=len(user)
                if len1>0 or len2>0:
                     for lead_list1 in lead_list:
                        print("status of lead",)
                        deregis=Status.objects.get(status="Deregister")
                        if lead_list1.status==deregis:
                            
                                digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
                                chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
                                p=(digits + "@156"+chars)
                                print(p)
                                old_lead=Lead.objects.get(pk=lead_list1.pk,status=deregis)
                                old_user=User.objects.get(username=old_lead.email)    
                                print("old_user",old_user)                        

                                try:
                                    old_lead_user=lead_user.objects.get(customer=old_lead)
                                except old_lead_user.DoesNotExist as e:
                                    logger.debug("lead user matching query does not exist",e)
                                    lead_user_new=lead_user(customer=old_lead,user=old_user)
                                    lead_user_new.save()
                                #old_lead_user=lead_user.objects.get(customer=old_lead)
                                #old_user=User.objects.get(pk=old_lead_user.user.pk)
                                old_lead.status=Status.objects.get(status='Customer')
                                old_lead.name=leadform.cleaned_data['name']
                                old_lead.last_name=leadform.cleaned_data['last_name']
                                old_lead.licenseid=leadform.cleaned_data['licenseid']
                                old_lead.address=leadform.cleaned_data['address']
                                old_lead.area_code=leadform.cleaned_data['area_code']
                                old_lead.phone=leadform.cleaned_data['phone']
				old_lead.license_expiry_date=leadform.cleaned_data['license_expiry_date']
                                old_lead.postal_code=leadform.cleaned_data['postal_code']

                                old_lead.member=request.user
                                old_lead.cred=1
                                old_lead.save()
                                now = timezone.now()
                                variable=Timeline(comment1="have created a ", comment2="Customer",action_create=now,user=request.user)
                                variable.save()
                                print("old lead edited:",old_lead.pk)
                                old_user.is_active=True
                                old_user.first_name=leadform.cleaned_data['name']
                                old_user.last_name=leadform.cleaned_data['last_name']
				new_group = User.groups.through.objects.get(user=old_user)
                                new_group.group=Group.objects.get(name='Customer')
                                new_group.save()
                                old_user.set_password(p)
                                old_user.save()
                                print("old user edited:",old_user.pk)
                                for form in vehicleform.forms:
                                    cd=form.cleaned_data
                                    vehicle=form.save(commit=False)
                                    vehicle.lead=old_lead
                                    vehicle.reg_expiry_date=cd.get('reg_expiry_date')
                                    vehicle.save()
                                    print("vehicle new added:",vehicle)
                                messages.success(request,"Lead has been added successfully")
                                detail1 = get_object_or_404(User, pk=old_lead.member.id)
                                detail2 = get_object_or_404(UserProfile, user=detail1)
                                send_lead_task.delay(old_user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,old_lead.email,old_user.first_name,old_lead.member.username,detail2.website)

                                return redirect("/CRM/crmcust/")
                        else:
                             form = LeadForm(request.POST )
                             vehicleform= InlineFormSet(request.POST)
                             return render(request,"CRM/leadform.html",{"leadform":leadform,"vehicleform":vehicleform,"msg":"Email already exist. Try another.","st":" Add Lead",'group':group})
                else:
                    cd1=leadform.cleaned_data
                    lead=leadform.save(commit=False)
                    status=Status.objects.get(status="Customer")
                    lead.status=status
                    lead.member=request.user
                    lead.last_name= leadform.cleaned_data['last_name']
                    #lead.cred=0
                    #l=lead.save()
                   
                   
                    lead.cred=1
                    lead.save()
             
                    digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
                    chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
                    p=(digits + "@156"+chars)
                    print(p)
                    print("last name",leadform.cleaned_data['last_name'])
                    user = User.objects.create_user(username=lead.email,
                                                  email=lead.email,
                                                  password =p, first_name=lead.name,last_name=leadform.cleaned_data['last_name'])
                    
                    user.groups.add(Group.objects.get(name='Customer'))
                    var1=lead_user(customer=lead, user=user)
                    
                    var1.save()
                    now = timezone.now()
                    variable=Timeline(comment1="have created an ", comment2="Customer",action_create=now,user=request.user)
                    variable.save()
                    member_d=User.objects.get(pk=request.user.pk)
                    cust_detail=lead_user.objects.get(user=user.pk)
                    mem_detail=Lead.objects.get(id=cust_detail.customer.id)
                    detail1 = get_object_or_404(User, pk=mem_detail.member.id)
                    detail2 = get_object_or_404(UserProfile, user=detail1)
                    ctx={'email': user.username, 'name':lead.name, 'password': p, 'name':detail1.first_name, 'phone':detail2.phone_no, 'shop':detail2.shop_name, 'address':detail2.shop_address}
                    send_lead_task.delay(user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,user.first_name,mem_detail.member.username,detail2.website)
                    data = {}
                    
                    
                    for form in vehicleform.forms:
                        cd=form.cleaned_data
                        vehicle=form.save(commit=False)
                        vehicle.lead=lead
                        vehicle.reg_expiry_date=cd.get('reg_expiry_date')
                        vehicle.save()
                    return HttpResponseRedirect(reverse('CRM:cindex2', args=(1,)))
            else:
                form = LeadForm(request.POST )
                vehicleform= InlineFormSet(request.POST)
                return render(request,"CRM/leadform.html",{"leadform":leadform,"vehicleform":vehicleform,"msg":"Please enter valid details","st":" Add Lead",'group':group})
        return render(request,"CRM/leadform.html",{"leadform":leadform,"vehicleform":vehicleform,"st":" Add Lead",'group':group})
    except Exception as e:
        print(e)
        return render(request,'CRM/404.html')


@login_required(login_url="/registration/login/")
def deleteVehicle(request):
   value=request.POST.get("veh_del")
   lead=request.POST.get("leadveh_id")
   
   vehicle=Lead_Vehicle.objects.get(pk=value)
   vehicle.delete()
   str="/CRM/edit/"+lead
   return redirect(str)
   

@login_required(login_url="/registration/login/") 
def edit_lead(request,lead_id):
    try:
        leadform=LeadForm()
        InlineFormSet = modelformset_factory(model=Lead_Vehicle,form=LeadVehicle_Form,can_delete=True)
        lead= get_object_or_404(Lead, pk=lead_id)
        print("-----------------",lead.last_name) 
        st=lead.status.status
        leadform = LeadForm(request.POST or None, instance=lead)
        qset=Lead_Vehicle.objects.filter(lead=lead)
        vehicleform = InlineFormSet(request.POST or None,queryset=qset)
        user=request.user 
        group=Group.objects.get(user=user)
        if request.method=='POST':
            leadform = LeadForm(request.POST or None, instance=lead)
            qset=Lead_Vehicle.objects.filter(lead=lead)
            vehicleform = InlineFormSet(request.POST or None,queryset=qset)
            if leadform.is_valid() and vehicleform.is_valid():
                lead1 = leadform.save()
                now = timezone.now()
                variable=Timeline(comment1="have updated a ", comment2="Lead",action_create=now,user=request.user)
                variable.save()
            
                for form in vehicleform.forms:
                    cd=form.cleaned_data
                    
                    if  cd.get('vehicle_no') is None:
                        pass
                    else:
                        vehicle=form.save(commit=False)
                        vehicle.lead=lead1
                        vehicle.reg_expiry_date=cd.get('reg_expiry_date')
                        vehicle.save()
                        
                stt=int(lead.status.pk)
                if stt==1:    
                    return HttpResponseRedirect(reverse('CRM:index2', args=(4,)))
                else:
                    return HttpResponseRedirect(reverse('CRM:cindex2', args=(2,)))
            else:
                return render(request,"CRM/leadform.html",{"leadform":leadform,"vehicleform":vehicleform,"st":"Edit "+st,"msg":"Please enter Valid details",'group':group})
        else:   
            return render(request,"CRM/leadform.html",{"leadform":leadform,"vehicleform":vehicleform,"st":"Edit "+st,'group':group})
    except Exception as e:
        print(e)
        return render(request,'CRM/404.html')
    
@login_required(login_url="/registration/login/")
def change_status(request,lead_id):
    logger.debug("inside lead delete for ",lead_id)
    
    try:
        lead=Lead.objects.get(pk=lead_id)
                #status = get_object_or_404(Status, pk=10)
    except Lead.DoesNotExist as e:
            logger.debug("status does not exist",e)
            return render(request,'CRM/error.html')
    if request.method=='GET':
        if lead.status.status=="Deactivate":
            
            try:
                status = get_object_or_404(Status, status="Customer")
            except Lead.DoesNotExist as e:
                logger.debug("status does not exist",e)
                return render(request,'CRM/error.html')
            
            try:
                lead_u=lead_user.objects.get(customer=lead)
                lead.status=status
                if lead.cred:
                    pass  
                lead.save()
                
                user=User.objects.get(pk=lead_u.user.pk)
                user.is_active=True
                user.save()
                return HttpResponseRedirect(reverse('CRM:cindex2', args=(3,)))
            except ObjectDoesNotExist:
                return HttpResponseRedirect(reverse('CRM:cindex2', args=(5,)))
        elif lead.status.status=="Customer":
            
            try:
                status = get_object_or_404(Status, status="Deactivate")
                
            except Lead.DoesNotExist as e:
                logger.debug("status does not exist",e)
                return render(request,'CRM/error.html')
            
            try:
                lead_u=lead_user.objects.get(customer=lead)
                lead.status=status
                lead.cred=0
                lead.save()
                
                user=User.objects.get(pk=lead_u.user.pk)
                user.is_active=False
                user.save()
                return HttpResponseRedirect(reverse('CRM:cindex2', args=(3,))) 
            except:
                return HttpResponseRedirect(reverse('CRM:cindex2', args=(5,)))
    try:
           list=Lead.objects.all()
    except Lead_Vehicle.DoesNotExist as e:
            logger.debug("lead vehicle does not exist",e)
            return render(request,'CRM/error.html')    

@login_required(login_url="/registration/login/")
def get_models(request):
    c=request.GET.get('company',None)
    company=Company.objects.get(company_name=c)
    
    modelnames=Company_Model.objects.filter(company=company).values('model_name','id','company').distinct() 
    
    dict=[]
    for model in modelnames:
        dict.append(model)
        #print(model)
    
    return JsonResponse(dict,safe=False)

@login_required(login_url="/registration/login/")
def get_mod(request):
    c1=str(request.GET.get('company',None))
    c2=str(request.GET.get('model',None))
    c3=str(request.GET.get('year',None))
    
    company=Company.objects.get(company_name=c1)
    
    modeln=Company_Model.objects.get(company=company,model_name=c2,make_year=c3) 
    dict=[]
    shiftdata=model_to_dict(modeln)
    dict.append(shiftdata)
    
    return JsonResponse(dict,safe=False)

"""@login_required(login_url="/registration/login/")
@csrf_exempt  
def qualify_lead(request):
    try:
        lead_id = request.POST.get('lead_id');
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('CRM:index2', args=(3,)))
    
    try:
        lead=Lead.objects.get(pk=lead_id)
        question_list=Question.objects.all()
        inlineformset=formset_factory(QualifyForm,extra=0)
        qform=inlineformset()
        qform=inlineformset(request.POST)
        
        count=0
        if qform.is_valid():
            
            for form in qform.forms:
                questionfrm=form.cleaned_data['question']
                answerfrm=form.cleaned_data['answer']
                
                question=Question.objects.get(question=questionfrm)
                qualify_obj=Qualify(lead=lead,question=question,answer=answerfrm)
                qualify_obj.save()
                if answerfrm=="Yes":
                    count+=1
        
        """"if count==3:"""""
        status=Status.objects.get(status="Customer")
        lead.status=status
        lead.cred=1
        lead.save()
        digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
        chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
        p=(digits + "@156"+chars)
        
        user = User.objects.create_user(username=lead.email,
                  email=lead.email,
                 password =p, first_name=lead.name)
    
        user.groups.add(Group.objects.get(name='Customer'))
        var1=lead_user(customer=lead, user=user)
        var1.save()
        
        cust_detail=lead_user.objects.get(user=user.pk)
        mem_detail=Lead.objects.get(id=cust_detail.customer.id)
        detail1 = get_object_or_404(User, pk=mem_detail.member.id)
        detail2 = get_object_or_404(UserProfile, user=detail1)
        ctx={'email': user.username, 'name':lead.name, 'password': p, 'name':detail1.first_name, 'phone':detail2.phone_no, 'shop':detail2.shop_name, 'address':detail2.shop_address}
        data = {}
        template = get_template('CRM/customer_email.html')
        html  = template.render(Context(data))
    
        subject='Successfully Qualified as Customer for AutoXtion'
        html_content = render_to_string('CRM/customer_email.html', ctx)
                                             
        to=[lead.email]
        from_email=settings.EMAIL_HOST_USER
        send_mail(subject,"",from_email,to,fail_silently=True, html_message=html_content)
        return HttpResponseRedirect(reverse('CRM:cindex2', args=(1,)))
                
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('CRM:index2', args=(3,)))"""

@login_required(login_url="/registration/login/")
def customer_index(request):
    logger.info("start of index lead")
    logger.debug("start of index lead")
    try:
        user=request.user
        status1=Status.objects.filter(status="Customer" )
        status2=Status.objects.filter(status="Deactivate" )
    
        list1=Lead.objects.filter(Q(status=status1) | Q(status=status2),member=user)
        list=list1.filter(Q(status=status1) | Q(status=status2))   
        group=Group.objects.get(user=user)
        companylist=CustCompany.objects.filter(member=request.user)
        if request.method=='POST':
        	from_dt=request.POST.get("from_date")
        	to_dt = request.POST.get("to_date")
        	r = requests.get('http://198.15.126.59:8010/CRM/get_customerlist/'+str(user.pk)+'/'+str(from_dt)+'/'+ str(to_dt))
       		list = r.json()
        	return render(request,'CRM/customer.html',{'leadl':list,"st":"Customer",'group':group,'companylist':companylist})
        logger.debug("lead list returned to leadlist.html")
        logger.info("lead list returned to leadlist.html",list)
        filter = LeadFilter(request.GET, queryset=list)
        return render(request,'CRM/customer.html',{'leadl':list,"st":"Customer",'group':group,'filter':filter,'companylist':companylist})
    except Exception as e:
        print(e)
        return render(request,'CRM/404.html')
        logger.info("lead list does not exist",e)
        
@login_required(login_url="/registration/login/")
def customer_index2(request,d):
    logger.info("start of index lead")
    logger.debug("start of index lead")
    try:
        msg=None
        msg2=None
        user=request.user
        status1=Status.objects.get(status="Customer")
        status2=Status.objects.get(status="Deactivate")
        group=Group.objects.get(user=user)
        list=Lead.objects.filter(Q(status=status1) | Q(status=status2),member=user)  
        print("-------------------",list)
        if d==str(1):
            msg2="Customer successfully added and email sent to customer with login credentials "
        elif d==str(2):
            msg2="information saved successfully"
        elif d==str(3):
            msg2="Status changed successfully"
        elif d==str(4):
            msg="Customer already exist. Try another"
        elif d==str(5):
            msg="Failed to change status"
        elif d==str(6):
            msg="Can not add Customer"
        logger.debug("lead list returned to leadlist.html")
        logger.info("lead list returned to leadlist.html",list)
        
        return render(request,'CRM/customer.html',{'leadl':list,"st":"Customer","msg2":msg2,"msg":msg,'group':group})
    except Exception as e:
        print(e)
        return render(request,'CRM/404.html')
        logger.info("lead list does not exist",e)
        
        
@login_required(login_url="/registration/login/")
def get_make_year(request):
    model=request.GET.get('model',None)
    model_obj=Company_Model.objects.get(pk=model)
    make_year=MakeYear.objects.filter(model=model_obj)
    dict=[]
    for make_y in make_year:
        shiftdata=model_to_dict(make_y)
        dict.append(shiftdata)
    return JsonResponse(dict,safe=False)


@login_required(login_url="/registration/login/")
def index2(request,d):
    logger.info("start of index lead")
    logger.debug("start of index lead")
    try:
        msg=None
        msg2=None
        
        user=request.user
        group=Group.objects.get(user=user)
        status=Status.objects.get(status="Customer")
        list=Lead.objects.filter(~Q(status=status),member=user)
        qlist=Question.objects.all()
        question_list=Question.objects.all()
        inlineformset=formset_factory(QualifyForm, extra=0)
        qform=inlineformset()
        qform=inlineformset(initial=[{'question':v.question}for v in question_list]) 
        logger.debug("lead list returned to leadlist.html")
        logger.info("lead list returned to leadlist.html",list)
        msg=None
        msg2=None
        if d==str(2):
            msg="Lead successfully created and email has been sent to Lead with login credentials, kindly confirm the same with lead"
            print(msg2,"-------",d)
        if d==str(3):
            msg="Lead failed to qualify"
            print(msg2,"-------",d) 
        if d==str(1):
            msg="Status changed successfully" 
        if d==str(4):
            msg="Information saved successfully"
        
        return render(request,'CRM/leadlist.html',{'leadl':list,'qlist':qlist,'qform':qform,'msg':msg,'msg2':msg2,'group':group})
    except Exception as e:
        print(e)
        return render(request,'CRM/404.html')
        logger.info("lead list does not exist",e)
        
        
        
def existing_cust(request):
    email=request.POST.get("email")
    name=request.POST.get("name")
    phone=request.POST.get("phone")
    last_name = request.POST.get("last_name")
    area_code=request.POST.get("area_code")
    print("phone number", phone)
    print("email isssss", email)
    member_obj=request.user
    print("maillllllllllllllllllllllllll",member_obj.email)
    try:
        if email:
            lead_list=Lead.objects.filter(email=email)
            user=User.objects.filter(username=email)
            len1=len(lead_list)
            
            len2=len(user)
            if len1>0 or len2>0:
                print("yes already exists")
                for lead_list1 in lead_list:
                    deregis=Status.objects.get(status="Deregister")
                    if lead_list1.status==deregis:
                                digits = "".join( [random.choice(string.digits) for i in xrange(2)] )
                        	chars = "".join( [random.choice(string.letters) for i in xrange(2)] )
                        	p=(digits + "@156"+chars)
                        	old_lead=Lead.objects.get(pk=lead_list1.pk,status=deregis)
                        	try:
                            		old_lead_user=lead_user.objects.get(customer=old_lead)
                            		old_user=User.objects.get(username=old_lead.email)                            
                        	except old_lead_user.DoesNotExist as e:
                            		logger.debug("lead user matching query does not exist",e)
                            		lead_user_new=lead_user(customer=old_lead,user=old_user)
                            		lead_user_new.save()
                                   
                        	old_lead.status=Status.objects.get(status='Lead')
                        	old_lead.member=request.user
                        	old_lead.name=name
                        	old_lead.last_name=last_name
                        	old_lead.save()
                        	print("old lead edited:",old_lead.pk)
                        	old_user.is_active=True
                                new_group = User.groups.through.objects.get(user=old_user)
                        	new_group.group=Group.objects.get(name='Lead')
                        	new_group.save()
                        	old_user.first_name=name
                        	old_user.last_name=last_name
                        	old_user.set_password(p)
                        	old_user.save()
                        	print("old user edited:",old_user.pk)
                        	messages.success(request,"Lead has been added successfully")
                        	detail1 = get_object_or_404(User, pk=old_lead.member.id)
                        	detail2 = get_object_or_404(UserProfile, user=detail1)
                        	send_ext_customer_task.delay(old_user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,old_lead.email,request.user.email,detail2.website)

                        	return redirect("/CRM/")
                    else:
                        return HttpResponseRedirect(reverse('CRM:cindex2', args=(4,))) 
            
        if phone:
            lead_list=Lead.objects.filter(phone=phone)
            user=User.objects.filter(username=phone)
            len1=len(lead_list)
            
            len2=len(user)
            if len1>0 or len2>0:
                print("yes already exists")
                for lead_list1 in lead_list:
                    if lead_list1.status=="Deregister":
                        digits = "".join( [random.choice(string.digits) for i in xrange(2)] )
                        chars = "".join( [random.choice(string.letters) for i in xrange(2)] )
                        p=(digits + "@156"+chars)
                        print(p)
                        old_lead=Lead.objects.get(pk=lead_list1.pk,status=Status.objects.get(status="Deregister"))
                        try:
                            old_lead_user=lead_user.objects.get(customer=old_lead)
                            old_user=User.objects.get(username=old_lead.email)                            
                        except old_lead_user.DoesNotExist as e:
                            logger.debug("lead user matching query does not exist",e)
                            lead_user_new=lead_user(customer=old_lead,user=old_user)
                            lead_user_new.save()
                        
                        old_lead_user=lead_user.objects.get(customer=old_lead)
                        old_user=User.objects.get(pk=old_lead_user.user.pk)
                        old_lead.status=Status.objects.get(status='Lead')
                        old_lead.member=user
                        old_lead.name=name
                        old_lead.last_name=last_name
                        old_lead.save()
                        print("old lead edited:",old_lead.pk)
                        old_user.is_active=True
                        new_group = User.groups.through.objects.get(user=old_user)
                        new_group.group=Group.objects.get(name='Lead')
                        new_group.save()
                        old_user.first_name=name
                        old_user.last_name=last_name
                        old_user.set_password(p)
                        old_user.save()
                        print("old user edited:",old_user.pk)
                        detail1 = get_object_or_404(User, pk=old_lead.member.id)
                        detail2 = get_object_or_404(UserProfile, user=detail1)
                        messages.success(request,"Lead has been added successfully")
                        message="Welcome to AutoXtion Communication Platform. \n" \
                        "We are revolutionising the we interact with each other.\n " \
                        "Kindly Login to http://portal.autoxtion.com.au/registration/login/ " \
                        "to access the portal.\n" \
                        " Your credentials are - \n Username :  "+user.username+ \
                        "\n Password :  "+p+ \
                        "\n Thank You \n "+detail1.first_name+"\n "+detail2.shop_name+" \n "+detail2.shop_address+"\n "+str(detail2.phone_no)

                        print("$$$$$$############@@@@@@@@@@@@@@!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                        print('+61'+old_user.username)
                        send_lead_sms_task.delay('+61'+old_user.username,message)

                        return redirect("/CRM/")
                    else:
                        return HttpResponseRedirect(reverse('CRM:cindex2', args=(4,)))        
        digits = "".join( [random.choice(string.digits) for i in xrange(2)] )
        chars = "".join( [random.choice(string.letters) for i in xrange(2)] )
        p=(digits + "@156"+chars)
        lead= None
        user= None
        if phone:
            print("1st else")
            print(phone)
            lead=Lead(name=name,last_name=last_name,phone=phone,member=request.user,status=Status.objects.get(status='Lead'),email=str(phone))
            lead.save()
            now = timezone.now()
            variable=Timeline(comment1="have created a ", comment2="Lead",action_create=now,user=request.user)
            variable.save()
            user = User.objects.create_user(username=phone,
                      password =p,
                      first_name=name,
                      last_name=last_name
                     )
        
        else:
            print("1 if")
            print(email)
            lead=Lead(name=name,last_name=last_name,email=email,member=request.user,status=Status.objects.get(status='Lead'))
            lead.save()
            now = timezone.now()
            variable=Timeline(comment1="have created a ", comment2="Lead",action_create=now,user=request.user)
            variable.save()
            user = User.objects.create_user(username=email,
                      email=email,
                     password =p,
                     first_name=name,
                      last_name=last_name
                     )
            
        user.groups.add(Group.objects.get(name='E_Customer'))
        member_d=User.objects.get(pk=request.user.pk)
        var1=lead_user(customer=lead, user=user)
        var1.save()
        if phone:
             print("2nd else")
             cust_detail=lead_user.objects.get(user=user.pk)
             mem_detail=Lead.objects.get(id=cust_detail.customer.id)
             detail1 = get_object_or_404(User, pk=mem_detail.member.id)
             detail2 = get_object_or_404(UserProfile, user=detail1)
             
             message="Welcome to AutoXtion Communication Platform. \n" \
                        "We are revolutionising the we interact with each other.\n " \
                        "Kindly Login to http://portal.autoxtion.com.au/registration/login/ " \
                        "to access the portal.\n" \
                        " Your credentials are - \n Username :  "+user.username+ \
                        "\n Password :  "+p+ \
                        "\n Thank You \n "+member_d.first_name+"\n "+detail2.shop_name+" \n "+detail2.shop_address+"\n "+str(detail2.phone_no)

             #print("$$$$$$############@@@@@@@@@@@@@@!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
             print('+61'+user.username)
             send_lead_sms_task.delay('+61'+user.username,message)
             try:
                      member_sms=Member_SMS.objects.get(member=request.user)
             except Member_SMS.DoesNotExist as e:
                      print("object does not exist",e)
                      member_sms=Member_SMS()
                      member_sms.member=request.user
                      member_sms.count=0
                      member_sms.save()
             member_sms.count=member_sms.count+1
             member_sms.save()
            
        else:
            print("2nd  if")
            cust_detail=lead_user.objects.get(user=user.pk)
            mem_detail=Lead.objects.get(id=cust_detail.customer.id)
            detail1 = get_object_or_404(User, pk=mem_detail.member.id)
            detail2 = get_object_or_404(UserProfile, user=detail1)
            
            ctx={'email': user.username, 'name':lead.name, 'password': p, 'name':detail1.first_name, 'phone':detail2.phone_no, 'shop':detail2.shop_name, 'address':detail2.shop_address}
            data = {}
            send_ext_customer_task.delay(user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,request.user.email,detail2.website)
            
        
        return HttpResponseRedirect(reverse('CRM:index2', args=(2,))) 
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('CRM:index2', args=(6,)))
    
def addVehicle(request):
    try:
        user=request.user
        group=Group.objects.get(user=user)
        var3=lead_user.objects.get(user=user)
        var1 = Lead.objects.get(pk=var3.customer.pk)
        address= UserProfile.objects.get(user=var1.member)
        
        InlineFormSet = formset_factory(form=LeadVehicle_Form)
        vehicleform=InlineFormSet()
        lead_u=lead_user.objects.get(user=request.user)
        lead=Lead.objects.get(pk=lead_u.customer.pk)
        if request.method=='POST':
        
            vehicleform= InlineFormSet(request.POST )
        
            
            if  vehicleform.is_valid():
                for form in vehicleform.forms:
                    vehicle=form.save(commit=False)
                    vehicle.lead=lead
                    vehicle.save()
            
            else:
            
                vehicleform= InlineFormSet(request.POST)
                return render(request,"CRM/CustomerVehicle.html",{"vehicleform":vehicleform,"msg2":"Please enter valid details","st":" Add Lead",'group':group})
        return render(request,"CRM/CustomerVehicle.html",{"vehicleform":vehicleform,"st":" Add Vehicle",'group':group})
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('CRM:index2', args=(3,)))
    
def editVehicle(request):
    address=None
    vehicleform=None
    try:
	
        user=request.user
        group=Group.objects.get(user=user)
        if group.name=="Company":
            user=request.user
            company_obj=CustCompany.objects.get(email=user.email)
            return redirect('CRM:edit_drivers')
            #return redirect('CRM/edit_drivers/'+(str(user.pk)))
        else:
            InlineFormSet = None
            lead_u=lead_user.objects.get(user=request.user)
            lead=Lead.objects.get(pk=lead_u.customer.pk)
	    flag=0
	    
            try:
                company_driver=Company_Driver.objects.get(driver=lead)
		flag=1
            except Exception as e:
                pass
            if flag is 1:
		print("-------------------------flag",flag)
                InlineFormSet = modelformset_factory(model=Lead_Vehicle,form=LeadVehicle_Form,can_delete=True,extra=0)
                #InlineFormSet = modelformset_factory(model=Lead_Vehicle,form=LeadVehicle_Form,can_delete=True,extra=0)
            else:
		print("**************************flag",flag)
                InlineFormSet = modelformset_factory(model=Lead_Vehicle,form=LeadVehicle_Form,can_delete=True)
            address= UserProfile.objects.get(user=lead.member)
            qset=Lead_Vehicle.objects.filter(lead=lead)
            vehicleform = InlineFormSet(request.POST or None,queryset=qset)
            if request.method=='POST':
                qset=Lead_Vehicle.objects.filter(lead=lead)
                vehicleform = InlineFormSet(request.POST or None,queryset=qset)
                if vehicleform.is_valid():
                    for form in vehicleform.forms:
                        cd=form.cleaned_data
                        if  cd.get('vehicle_no') is None:
                            pass
                        else:
                            vehicle=form.save(commit=False)
                            vehicle.lead=lead
                            vehicle.save()
                    return redirect('CRM:editVehicle')
                else:
                    return render(request,"CRM/CustomerVehicle.html",{"vehicleform":vehicleform,"st":"Vehicle","msg":"Please enter Valid details",'group':group,'flag':flag})
            else:
                return render(request,"CRM/CustomerVehicle.html",{ "vehicleform":vehicleform,"st":" Vehicle" ,'group':group,'flag':flag})
    except Exception as e:
        print(e)
        return render(request,"CRM/CustomerVehicle.html",{ "vehicleform":vehicleform,"st":"Vehicle","msg":"Error occured while updating vehicle details",'group':group})
    
def deleteVehicleCust(request):
    try:
        value=request.POST.get("veh_del")
        
        vehicle=Lead_Vehicle.objects.get(pk=value)
        lead=vehicle.lead.pk
        vehicle.delete()
        
        return redirect('CRM:editVehicle')
    except ObjectDoesNotExist:
        return redirect('CRM:editVehicle')

def new(request):
    return render(request,"CRM/new.html",)

def validate_mail(request):
    value=request.GET.get("lead_mail")
    lead_list=Lead.objects.filter(email=value)
    user=User.objects.filter(username=value)
    len1=len(lead_list)
    len2=len(user)
    msg=None
    if len1>0 and len2>0:
        msg={"msg":"Available"}
    else:
        msg={"msg":"not Available"}
    return HttpResponse(json.dumps(msg), content_type='application/json')

def excelsheet(request):
    result_id = None
    user=request.user
    form=ExcelForm()
    group=Group.objects.get(user=user)
    if request.method=='POST':
        print("post method")
        form=ExcelForm(request.POST,request.FILES)
        if form.is_valid():
             print("excel uploaded")
             obj=form.save()
             
             print(obj.pk,user.pk)
             import_lead_vehicle_data.delay(obj.pk,request.user.id)
            # result=import_lead_vehicle_data.delay(obj.pk,request.user.id)
#              print("result status",result.status)
#              print("result status",result.ready())
#              print("result status",result.successful())
#              print("result status",result.state)
#              
             #print("result get",result.get())
             #get_task_status(result.id)
#              print("taks",task)
#              print("taks",task)
#              print("taks",task)
             #task.AsyncResult(task.request.id).state
             #print(result.id)              
             return render(request,'CRM/excelupload.html',{'form':form,'group':group,'msg':"Your data has been sent and you will be informed regarding status."})   
    else:
        form=ExcelForm()
        return render(request,'CRM/excelupload.html',{'form':form,'group':group})


@login_required(login_url="/registration/login/")    
def view_history(request,lead_id):
    lead=Lead.objects.get(pk=lead_id)
    user=request.user
    group=Group.objects.get(user=user)
    print("@@Lead:",lead)
    status = Status.objects.get(status="Job Completed")
    var3=MemberAppointment.objects.filter(customer=lead,status=status).order_by('-date_update')
    detail=UpcellAppointment.objects.filter(appointment__in=[app_details.pk for app_details in var3])
    sub_detail=UpcellAppointmentSubService.objects.filter(upcellappointment__in=[sub_details.pk for sub_details in detail])
    
    
    
    ctx={'var3':var3,'detail':detail,'sub_detail':sub_detail,'group':group}
    return render(request,"CRM/Customerhistory.html",ctx)




def customer_registration(request):
    leadform=CustomerForm()
    vehicleform=LeadVehicle_Form()
    if request.method=="POST":
        print("in post")
        leadform=CustomerForm(request.POST)
        vehicleform=LeadVehicle_Form(request.POST)
        if leadform.is_valid() and vehicleform.is_valid():
            print("form valid")
            cd1=leadform.cleaned_data
            #print(cd.get('email'))
            lead_list=Lead.objects.filter(email=cd1.get('email'))
            user=User.objects.filter(username=cd1.get('email'))
            len1=len(lead_list)
            len2=len(user)
            if len1>0 or len2>0:
                print("email exist")
                leadform = CustomerForm(request.POST )
                vehicleform= LeadVehicle_Form(request.POST)
                return render(request,"CRM/customer_register.html",{"leadform":leadform,"vehicleform":vehicleform,"msg":"Email already exist.","st":" Add Lead",})
            else:
                lead=leadform.save(commit=False)
                status=Status.objects.get(status="Customer")
                lead.status=status
                lead.member=User.objects.get(username="chandan@yopmail.com")
                lead.add_by="barter"
                lead.cred=1
                lead.save()
                print("@@@@@@@@@@@@@:",lead.email)
                digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
                chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
                p=(digits + "@156"+chars)

                user = User.objects.create_user(username=lead.email,
                                              email=lead.email,
                                              password =p, first_name=lead.name)

                user.groups.add(Group.objects.get(name='Lead'))
                var1=lead_user(customer=lead, user=user)
                var1.save()
                member_d=User.objects.get(pk=request.user.pk)
                cust_detail=lead_user.objects.get(user=user.pk)
                mem_detail=Lead.objects.get(id=cust_detail.customer.id)
                detail1 = get_object_or_404(User, pk=mem_detail.member.id)
                detail2 = get_object_or_404(UserProfile, user=detail1)

                ctx={'email': user.username, 'name':lead.name, 'password': p, 'name':detail1.first_name, 'phone':detail2.phone_no, 'shop':detail2.shop_name, 'address':detail2.shop_address}
                send_lead_task.delay(user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,user.first_name,mem_detail.member.username,detail2.website)
                data = {}


                cd=vehicleform.cleaned_data
                vehicle=vehicleform.save(commit=False)
                vehicle.lead=lead
                vehicle.reg_expiry_date=cd.get('reg_expiry_date')
                vehicle.save()
                return render(request,"CRM/customer_register_success.html")
            return render(request,'CRM/customer_register.html',{'leadform':leadform,'vehicleform':vehicleform})
        else:
            print("in form invalid")
            return render(request,'CRM/customer_register.html',{'leadform':leadform,'vehicleform':vehicleform})
    else:
        print("in get")
        return render(request,'CRM/customer_register.html',{'leadform':leadform,'vehicleform':vehicleform})


def customer_delete(request):    
    customer = request.POST.getlist('leadname2[]')
    print('customer box', customer)
    for x in customer:
        customer1= Lead.objects.filter(pk=x)
        print('del pk',customer1)
        if request.method == 'POST':
            for r in customer1:
                lead_user_obj=lead_user.objects.get(customer=r)
                user_obj=User.objects.get(pk=lead_user_obj.user.pk)
                print('rrrrrr',r)
                user_obj.is_active=False
                user_obj.save()
                r.status_id = 11
                r.save()
    value= request.POST.get('leadname3[]')
    print('value box', value)
    if value == "1":  
        messages.success(request,'Lead deleted successfully')            
        return redirect("CRM:index")
    else:
        messages.success(request,'Customer deleted successfully')
        return redirect("CRM:customer_index")

class get_customer(generics.ListAPIView):
     permission_classes = (AllowAny,)
     serializer_class = GetCustomerSerializer
     def get_queryset(self):
        #user=self.request.user
        from_date=self.kwargs['from_dt']
        to_date=self.kwargs['to_dt']
        print("from_dt get cust",from_date)
        print("to_date get cust",to_date)
        user=self.kwargs['user_id']
        print("user",user)
        status=Status.objects.get(status="Customer")
        list=Lead.objects.filter(member=user,status=status)
        lead_u=lead_user.objects.filter(customer__in=list)
        print("lead_u lead_u",lead_u)
        us= User.objects.filter(pk__in=[r.user.pk for r in lead_u],date_joined__range=[from_date, to_date])
        
        new_lead_u=lead_user.objects.filter(user__in=us)
        print("new_lead_u new_lead_u",new_lead_u)
        new_list=Lead.objects.filter(pk__in=[j.customer.pk for j in new_lead_u])
        group=Group.objects.get(user=user)
#         data = {'html': render_to_string('CRM/customer.html', {'leadl':new_list,'user':user})}
#         return HttpResponse(json.dumps(data), content_type='application/json')
        return new_list
    
class get_leadlist(generics.ListAPIView):
     permission_classes = (AllowAny,)
     serializer_class = GetCustomerSerializer
     def get_queryset(self):
        #user=self.request.user
        from_date=self.kwargs['from_dt']
        to_date=self.kwargs['to_dt']
        print("from_dt get cust",from_date)
        print("to_date get cust",to_date)
        user=self.kwargs['user_id']
        print("user",user)
        status=Status.objects.get(status="Customer")
        list=Lead.objects.filter(member=user,status=status)
        lead_u=lead_user.objects.filter(customer__in=list)
        print("lead_u lead_u",lead_u)
        us= User.objects.filter(pk__in=[r.user.pk for r in lead_u],date_joined__range=[from_date, to_date])
        
        new_lead_u=lead_user.objects.filter(user__in=us)
        print("new_lead_u new_lead_u",new_lead_u)
        new_list=Lead.objects.filter(pk__in=[j.customer.pk for j in new_lead_u])
        group=Group.objects.get(user=user)
#         data = {'html': render_to_string('CRM/customer.html', {'leadl':new_list,'user':user})}
#         return HttpResponse(json.dumps(data), content_type='application/json')
        return new_list


def add(request,mem_detail):
    ab=User.objects.get(id=mem_detail)
    print("XXXXXXXXXXXXXXXXXXXXXX",ab)
    leadform=LeadForm()
    InlineFormSet = formset_factory(form=LeadVehicle_Form)
    vehicleform=InlineFormSet()
    if request.POST:
        print("****************")
        print("****************")
        leadform = LeadForm(request.POST)
        InlineFormSet = formset_factory(form=LeadVehicle_Form)
        vehicleform= InlineFormSet(request.POST )
              
        if leadform.is_valid()  and vehicleform.is_valid():
            print ("In form valid")
            cd=leadform.cleaned_data
            print(cd.get('email'))
            lead_list=Lead.objects.filter(email=cd.get('email'))
            user=User.objects.filter(username=cd.get('email'))
            len1=len(lead_list)
            len2=len(user)
            if len1>0 or len2>0:
                form = LeadForm(request.POST )
                vehicleform= InlineFormSet(request.POST)
                return render(request,"CRM/Customer_Reg.html",{"leadform":leadform,"vehicleform":vehicleform,"msg":"Email already exist. Try another.","st":" Add Lead",})
            else:
                cd1=leadform.cleaned_data
                lead=leadform.save(commit=False)
                status=Status.objects.get(status="Lead")
                lead.status=status
                lead.member=ab
                lead.cred=1
                lead.save()
                now = timezone.now()
                digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
                chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
                p=(digits + "@156"+chars)
                print(p)
                user = User.objects.create_user(username=lead.email,
                                              email=lead.email,
                                              password =p, first_name=lead.name,last_name=leadform.cleaned_data['last_name'])
                
                user.groups.add(Group.objects.get(name='Lead'))
                var1=lead_user(customer=lead, user=user)
                var1.save()
                member_d=User.objects.get(id=mem_detail)
                cust_detail=lead_user.objects.get(user=user.pk)
                mem_detail=Lead.objects.get(id=cust_detail.customer.id)
                detail1 = get_object_or_404(User, pk=mem_detail.member.id)
                detail2 = get_object_or_404(UserProfile, user=detail1)
                ctx={'email': user.username, 'name':lead.name, 'password': p, 'name':detail1.first_name, 'phone':detail2.phone_no, 'shop':detail2.shop_name, 'address':detail2.shop_address}
                send_lead_task.delay(user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,user.first_name,mem_detail.member.username,detail2.website)
                data = {}
                for form in vehicleform.forms:
                    cd=form.cleaned_data
                    vehicle=form.save(commit=False)
                    vehicle.lead=lead
                    vehicle.reg_expiry_date=cd.get('reg_expiry_date')
                    vehicle.save()
#                     
                return render_to_response("CRM/newcustomer_done.html",)
        else:
            form = LeadForm(request.POST )
            vehicleform= InlineFormSet(request.POST)
            return render(request,"CRM/Customer_Reg.html",{"leadform":leadform,"vehicleform":vehicleform,"msg":"Please enter valid details","st":" Add Lead",})
    return render(request,"CRM/Customer_Reg.html",{"leadform":leadform,"vehicleform":vehicleform,"st":" Add Lead",})


def downloadDemoTemplate(request):
    wrapper=FileWrapper(open("static/excel/demo_excel.xlsx","rb"))
    response=HttpResponse(wrapper,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet ')
    response['Content-Disposition'] = 'attachment;filename=Demo Excel Template.xlsx'

    return response

@login_required(login_url="/registration/login/")
def generateCredentials(request):
    new_email= request.POST.get('new_email')
    lead_id= request.POST.get('lead_id')   
    try:
        if request.POST:
            lead_email=Lead.objects.get(pk=lead_id)
            
            if lead_email.email==new_email:
                print("if lead email",lead_email)
                digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
                chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
                p=(digits + "@156"+chars)
                try:
                        l_u=lead_user.objects.get(customer=lead_email)
                        a_user= User.objects.get(username=lead_email.email)
                except lead_user.DoesNotExist as e:
                        a_user= User.objects.get(username=lead_email.email)
                        logger.debug("lead user matching query does not exist",e)
                        lead_user_new=lead_user(customer=lead_email,user=a_user)
                        lead_user_new.save()
                a_user.set_password(p)
                a_user.save()
                detail1 = get_object_or_404(User, pk=lead_email.member.id)
                detail2 = get_object_or_404(UserProfile, user=detail1)
		print("before task call")
                send_new_credentials.delay(a_user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead_email.email,a_user.first_name,lead_email.member.username,detail2.website)
		print("after task call")
                status=Status.objects.get(status=lead_email.status)
                messages.success(request,"New Credentials has been generated successfully")
                if status.status=="Lead":
                        return redirect("/CRM/")
                else:
                        return redirect("/CRM/crmcust/")
            else:
                user_list=User.objects.filter(email=new_email)
                #lead_list=Lead.objects.get(email=new_email)
                print("print user_list ",user_list)
                len1=len(user_list)
                #len2=len(lead_list)
                if len1>0 :
                    lead_obj=Lead.objects.get(pk=lead_id)
                    status_obj=Status.objects.get(status=lead_obj.status)
                    messages.success(request,"Email already exist. Try another.")
                    if status_obj.status=="Lead" :
                        return redirect("/CRM/")
                    else:
                         return redirect("/CRM/crmcust/")
                else:
                    lead=Lead.objects.get(pk=lead_id)
                    try:
                        l_u=lead_user.objects.get(customer=lead)
                        a_user= User.objects.get(username=lead.email)
                    except lead_user.DoesNotExist as e:
                        logger.debug("lead user matching query does not exist",e)
                        lead_user_new=lead_user(customer=lead,user=a_user)
                        lead_user_new.save()
                        
                    lead.email=new_email
                    lead.save()
                    digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
                    chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
                    p=(digits + "@156"+chars)
                    a_user.username=lead.email
                    a_user.email=lead.email
                    #user.password = p
                    a_user.set_password(p)
                    a_user.save()
                    detail1 = get_object_or_404(User, pk=lead.member.id)
                    detail2 = get_object_or_404(UserProfile, user=detail1)
                    send_new_credentials.delay(a_user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,a_user.first_name,lead.member.username,detail2.website)
                    status=Status.objects.get(status=lead.status)
                    messages.success(request,"New Credentials has been generated successfully")
                    if status.status=="Lead":
                        return redirect("/CRM/")
                    else:
                         return redirect("/CRM/crmcust/")
            
    except Lead.DoesNotExist as e:
            logger.debug("status does not exist",e)
            return render(request,'CRM/error.html')


def addCompany(request):
    companyform=CompanyForm()
    vehicleformset=formset_factory(form=CompanyVehicleForm)
    detail2=UserProfile.objects.get(user=request.user)
    if request.method=="POST":
        print("------------------------------------------------in post")
        companyform=CompanyForm(request.POST)

        vehicleformdata=vehicleformset(request.POST)
        print("@@@@@@@@",companyform.errors)
        print("########",vehicleformdata.errors)
        if companyform.is_valid() & vehicleformdata.is_valid():
            company_mail=companyform.cleaned_data['email']
            list1=User.objects.filter(email=company_mail)
            if len(list1)>0:
                messages.success(request,'Company Email already exist.Try another.')
                return render(request,'CRM/Company.html',{'companyform':companyform,'vehicleformset':vehicleformset,})
            else:
                i=0
                for f in vehicleformdata:
                    i=i+1
                    print(i)
                    flag=0
                    if f.cleaned_data['email']:
                        list2=User.objects.filter(email=f.cleaned_data['email'])
                        if len(list2)>0:
                            flag=1
                        if flag==1:
                            messages.success(request,'Driver email already exist')
                            return render(request,'CRM/Company.html',{'companyform':companyform,'vehicleformset':vehicleformset,})

            company_obj=CustCompany(
                        company_name=companyform.cleaned_data['company_name'],
                        address=companyform.cleaned_data['address'],
                        email=companyform.cleaned_data['email'],
                        phone=companyform.cleaned_data['phone'],
                        member=request.user,
                        person=companyform.cleaned_data['person'],
            )
            company_obj.save()
            request.session['company_added']= company_obj.pk
# generate auth user credentials for driver
            digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
            chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
            password=(digits + "@156"+chars)
            print("Password company-------------------",password)
            user_company_obj = User.objects.create_user(username=companyform.cleaned_data['email'],
                                          email=companyform.cleaned_data['email'],
                                          password =password,
                                          first_name=companyform.cleaned_data['company_name'],
                                          )

            user_company_obj.groups.add(Group.objects.get(name='Company'))
            print("pk1 ",company_obj.pk," pk2 ",request.user.pk)
            send_company_mail_task(company_obj.pk,request.user.pk,password)
            i=0
            for f in vehicleformdata:
                i=i+1
                print(i)
                if f.cleaned_data['email']:
                    list2=User.objects.filter(email=f.cleaned_data['email'])
                    if len(list2)>0:
                        flag=1
                        if flag==1:
                            messages.success(request,'Driver email already exist')
                            return HttpResponseRedirect(reverse('CRM:UpdateCompany', args=(request.session['company_added'],)))
                    else:
			p=None
                        lead_obj=Lead(
                            email=f.cleaned_data['email'],
                            name=f.cleaned_data['name'],
                            last_name=f.cleaned_data['last_name'],
                            licenseid=f.cleaned_data['licenseid'],
                            phone=f.cleaned_data['phone'],
                            address=f.cleaned_data['address'],
                            member=request.user,
                            status=Status.objects.get(status="Customer")
                        )
                        lead_obj.save()
                        vehicle_obj=Lead_Vehicle(
                            lead=lead_obj,
                            vehicle_no=f.cleaned_data['vehicle_no'],
                            company=f.cleaned_data['company'],
                            model=f.cleaned_data['model'],
                            makeyear=f.cleaned_data['makeyear'],
                            reg_expiry_date=f.cleaned_data['reg_expiry_date'],
                            vin_no=f.cleaned_data['vin_no'],
                            chasis_no=f.cleaned_data['chasis_no'],
                        )
                        vehicle_obj.save()
                        companydriver_obj=Company_Driver(company=company_obj,driver=lead_obj)
                        companydriver_obj.save()
    # generate auth user credentials for driver
                        digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
                        chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
                        p=(digits + "@156"+chars)
                        print("Password driver-------------------",p)
                        user_obj = User.objects.create_user(username=lead_obj.email,
                                                      email=lead_obj.email,
                                                      password =p, first_name=lead_obj.name,last_name=lead_obj.last_name)
    
                        user_obj.groups.add(Group.objects.get(name='Customer'))
                        var1=lead_user(customer=lead_obj, user=user_obj)
                        var1.save()
                        print("---------------------------",p)
                        send_driver_mail_task.delay(lead_obj.pk,company_obj.pk,request.user.pk,p)
                        print("----------------------------after task call")
#send driver mail as added lead
            messages.success(request,'Company details with driver added successfully')
            return redirect('/CRM/company_list')
        else:
            print("------------------------------------form invalid")
            return render(request,'CRM/Company.html',{'companyform':companyform,'vehicleformset':vehicleformset,})
    else:
        return render(request,'CRM/Company.html',{'companyform':companyform,'vehicleformset':vehicleformset,})

def UpdateCompany(request, company_id):
    
    user=request.user
    group=Group.objects.get(user=user)
    company_driver_detail= Company_Driver.objects.filter(company=company_id)
    #print("-----company_driver_detail-----------", company_driver_detail)
    lead_queryset = Lead.objects.filter(pk__in=[lead.driver.pk for lead in company_driver_detail])
    #print("-----------", lead_queryset)
    #for x in lead_queryset:
    #    print(x.pk)
    vehicle_queryset = Lead_Vehicle.objects.filter(lead__in=[lead.driver.pk for lead in company_driver_detail])
    #print("-----vehicle_queryset------", vehicle_queryset)
    leadform = modelformset_factory(Lead, form=DriverForm, extra=0)
    vehicleform = modelformset_factory(Lead_Vehicle, form=LeadVehicle_Form, extra=0)
    company_obj=CustCompany.objects.get(pk=company_id)
    #print("---------company_obj---------", company_obj)
    
    companyform=CompanyUpdateForm(instance=company_obj)
    leadformset = leadform(queryset =lead_queryset, prefix='form1')
    vehicleformset = vehicleform(queryset =vehicle_queryset, prefix='form2')
    
    if request.method == 'POST':
        companyform1 = CompanyUpdateForm(request.POST or None, instance=company_obj)
        leadformset1 = leadform(request.POST, prefix='form1')
        vehicleformset1 = vehicleform(request.POST, prefix='form2')
        print("-------companyform errors------", companyform.errors)
        if companyform1.is_valid():
            company_obj=companyform1.save()
        for Lform,Vform in zip(leadformset1.forms,vehicleformset1.forms):
        #for Lform in leadformset1.forms:
            print("-------Lform errors-------", Lform.errors)
            if Lform.is_valid():
                list2=User.objects.filter(email=Lform.cleaned_data['email'])
                
                print("lform instance",Lform.instance.pk)
                lead_obj= Lform.save(commit=False)
                lead_obj.member=user 
                lead_obj.status= Status.objects.get(status="customer")  
                lead_obj.save()
                #print("lead pk",s.object.pk)
                print("lead_obj", lead_obj.pk)
                p=None
                try:
                    #lead_user_obj=lead_user.objects.get(pk=lead_obj.pk)
                    lead_user_obj=lead_user.objects.get(customer=lead_obj.pk)
                    
                except:
                    print("no Lead user object")
                    digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
                    chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
                    p=(digits + "@156"+chars)
                    print("Password driver-------------------",p)
                    user_obj = User.objects.create_user(username=lead_obj.email,
                                                  email=lead_obj.email,
                                                  password =p, first_name=lead_obj.name,last_name=lead_obj.last_name)
  
                    user_obj.groups.add(Group.objects.get(name='Customer'))
                    var1=lead_user(customer=lead_obj, user=user_obj)
                    var1.save()
                    send_driver_mail_task.delay(lead_obj.pk,company_obj.pk,request.user.pk,p)
                try:
                    company_driver_obj=Company_Driver.objects.get(driver=lead_obj.pk)
                except:
                    company=CustCompany.objects.get(pk=company_obj.pk)
                    lead_object=Lead.objects.get(pk=lead_obj.pk)
                    new_company_driver_obj= Company_Driver(company=company, driver=lead_object)
                    new_company_driver_obj.save()
            send_driver_mail_task.delay(lead_obj.pk,company_obj.pk,request.user.pk,p)
            if Vform.is_valid():                 
                veh_obj=Vform.save(commit=False)
                veh_obj.lead=lead_obj
                veh_obj.save()


        print("SAVE SUCCESSFULLY")
        return redirect("/CRM/company_list/")
    return render(request,"CRM/company_update.html",{'companyform':companyform, "leadformset":leadformset,'vehicleformset':vehicleformset, 'group':group,})

def driver_delete_ajax(request,vehicle_id):
   # upcell_id = request.GET.get('upcellid', None)
    tag_to_delete = get_object_or_404(Lead_Vehicle, pk=vehicle_id)
    #print("---------tag_to_delete-----------", tag_to_delete)
    driver_lead = get_object_or_404(Lead, pk=tag_to_delete.lead.pk)
    #print("----driver_lead----------",driver_lead)
    company=Company_Driver.objects.get(driver=driver_lead.pk)
    request.session['company'] = company.company.pk
    driver_lead.delete()
    tag_to_delete.delete()
    #return HttpResponseRedirect(reverse(upcell_app_update, args=(appointment.pk,)))
    #return HttpResponseRedirect(reverse('CRM:UpdateCompany', args=(request.session['company'],)))
    log_user=request.user
    group=Group.objects.get(user=log_user)
    if group.name=='Member':
	print("memebr logged in user")
        #return redirect('CRM:UpdateCompany',)
        return HttpResponseRedirect(reverse('CRM:UpdateCompany', args=(request.session['company'],)))

    else:		 
	print("log in user is company")
    	return redirect('CRM:edit_drivers')


def edit_drivers(request):
    user_id=request.user.pk
    user_obj=User.objects.get(pk=user_id)
    #user=request.user
    group=Group.objects.get(user=user_obj.pk)
    company_obj=CustCompany.objects.get(email=user_obj.username)
    company_driver_detail= Company_Driver.objects.filter(company=company_obj.pk)
    #print("-----company_driver_detail-----------", company_driver_detail)
    lead_queryset = Lead.objects.filter(~Q(status=Status.objects.get(status="Inacitve")),pk__in=[lead.driver.pk for lead in company_driver_detail])
    #print("-----------", lead_queryset)
    #for x in lead_queryset:
    #    print(x.pk)
    vehicle_queryset = Lead_Vehicle.objects.filter(lead__in=[lead.driver.pk for lead in company_driver_detail])
    #print("-----vehicle_queryset------", vehicle_queryset)
    leadform = modelformset_factory(Lead, form=DriverForm, extra=0)
    vehicleform = modelformset_factory(Lead_Vehicle, form=LeadVehicle_Form, extra=0)
    #company_obj=CustCompany.objects.get(pk=company_id)
    #print("---------company_obj---------", company_obj)

    #companyform=CompanyUpdateForm(instance=company_obj)
    leadformset = leadform(queryset =lead_queryset, prefix='form1')
    vehicleformset = vehicleform(queryset =vehicle_queryset, prefix='form2')

    if request.method == 'POST':
        #companyform1 = CompanyUpdateForm(request.POST or None, instance=company_obj)
        leadformset1 = leadform(request.POST, prefix='form1')
        vehicleformset1 = vehicleform(request.POST, prefix='form2')
        #print("-------companyform errors------", companyform.errors)
        #if companyform1.is_valid():
        #    company_obj=companyform1.save()
        for Lform,Vform in zip(leadformset1.forms,vehicleformset1.forms):
        #for Lform in leadformset1.forms:
            print("-------Lform errors-------", Lform.errors)
            if Lform.is_valid():
                print("lform instance",Lform.instance.pk)
                lead_obj= Lform.save(commit=False)
                lead_obj.member=company_obj.member
                lead_obj.status= Status.objects.get(status="customer")
                lead_obj.save()
                #print("lead pk",s.object.pk)
                print("lead_obj", lead_obj.pk)
                p=None
                try:
                    lead_user_obj=lead_user.objects.get(customer=lead_obj.pk)
                    print("----lead_user_obj----", lead_user_obj)
                except:
                    print("no Lead user object")
                    digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
                    chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
                    p=(digits + "@156"+chars)
                    print("Password driver-------------------",p)
                    user_obj = User.objects.create_user(username=lead_obj.email,
                                                  email=lead_obj.email,
                                                  password =p, first_name=lead_obj.name,last_name=lead_obj.last_name)

                    user_obj.groups.add(Group.objects.get(name='Customer'))
                    var1=lead_user(customer=lead_obj, user=user_obj)
                    var1.save()
                    send_driver_mail_task.delay(lead_obj.pk,company_obj.pk,company_obj.member.pk,p)
                try:
                    company_driver_obj=Company_Driver.objects.get(driver=lead_obj.pk)
                except:
                    company=CustCompany.objects.get(pk=company_obj.pk)
                    lead_object=Lead.objects.get(pk=lead_obj.pk)
                    new_company_driver_obj= Company_Driver(company=company, driver=lead_object)
                    new_company_driver_obj.save()

            if Vform.is_valid():
                veh_obj=Vform.save(commit=False)
                veh_obj.lead=lead_obj
                veh_obj.save()

        print("SAVE SUCCESSFULLY")
        return redirect('CRM:edit_drivers')
        #return redirect('/CRM/')
    return render(request,"CRM/driver_update.html",{"leadformset":leadformset,'vehicleformset':vehicleformset, 'group':group,})

@login_required(login_url="/registration/login/")
def company_index(request):
    logger.info("start of index lead")
    logger.debug("start of index lead")
    print("in company list")
    user=request.user
    group=Group.objects.get(user=user)
    companylist=CustCompany.objects.filter(member=request.user)
    print(companylist)
    return render(request,'CRM/CompanyList.html',{'list':companylist,})