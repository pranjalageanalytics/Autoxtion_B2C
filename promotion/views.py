from django.shortcuts import render, render_to_response
#from promotion.forms import PromotionForm, ModelForm, CompanyForm
from django.template import RequestContext
from django.views.generic.edit import CreateView
from promotion.models import *
from .forms import *
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from CRM.models import *
from django.http import JsonResponse
from django.forms.models import model_to_dict
import logging
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from django.db.models.query import QuerySet
from django.contrib.gis.serializers.geojson import Serializer
from django.contrib.auth.views import redirect_to_login
from django.views.generic.detail import DetailView
logger = logging.getLogger('promotion')
logger.addHandler(logging.NullHandler())
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group
from CRM.models import *
from datetime import datetime,time
from rest_framework import viewsets
from .serializers import *
from rest_framework import generics
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import AccessMixin
from django.template.response import TemplateResponse
from promotion.mixin import *
from notifications.signals import notify
from customer.models import *
from django.shortcuts import render,get_object_or_404, render_to_response,redirect
from Timeline.models import *
from django.utils import timezone
from promotion.filters import *
from fcm_django.models import FCMDevice
from push_notifications.models import  APNSDevice
from django.db.models import Q
# Create your views here.

class PromotionList(AuthRequiredMixin, ListView):
    model= Promotions
    template_name = 'promotion/promotions_list.html'
    success_url = reverse_lazy('promotion:server_list')
    
    def get_context_data(self, **kwargs):
        #print("in get context")
        context = super(PromotionList, self).get_context_data(**kwargs)
        response = TemplateResponse(self.request, self.template_name)
        user = self.request.user
        group=Group.objects.get(user=user)
	address=None
        if group.name=="Company":
            obj=[]
            #print("in company")
            company_obj=CustCompany.objects.get(email=user.email)
            #print("Company obj",company_obj)
            driver_list=Company_Driver.objects.filter(company=company_obj)
            for driver in driver_list:
                lead_obj=Lead.objects.get(pk=driver.driver.pk)
                #print(lead_obj)
                veh=Lead_Vehicle.objects.filter(lead=lead_obj)
                today=datetime.today()
                msg=None
                if veh:
                    #print("Vehicle object",veh)
                    for vehicle in veh:
                        print("vehicle details",vehicle.company.pk," ",vehicle.model.pk," ",vehicle.makeyear.pk," ",today.date())
                        var2=Promotions.objects.filter(member=company_obj.member,
                                                       company=vehicle.company,
                                                       model_id=vehicle.model,
                                                       make_year=vehicle.makeyear,
                                                       to_date__gte = today.date(),
                                                       display_to="Customer")
                        print("QQQQQQQ1",var2)
                        for v in var2:
                            obj.append(model_to_dict(v))
                        promo_list2=Promotions.objects.filter(member=company_obj.member,
                                                              company=vehicle.company,
                                                              model_id=vehicle.model,
                                                              make_year=vehicle.makeyear,
                                                              to_date__gte = today.date(),
                                                              display_to="Lead")
                        print("QQQQQQQ2",promo_list2)
                        for v in promo_list2:
                            obj.append(model_to_dict(v))
                        try:
                            allpromo=Promotions.objects.filter(member=company_obj.member,
                                                               company=vehicle.company,
                                                               model_id=vehicle.model,
                                                               make_year=vehicle.makeyear,
                                                               to_date__gte = today.date(),
                                                               display_to="All")
                            print("QQQQQQQ3",allpromo)
                            for f in allpromo:
                                obj.append(model_to_dict(f))
                        except Exception as e:
                            pass
                            print("no promotion for ALL")
            print("final obj list",obj)
            com=Company.objects.get(company_name='All')
            var3=Promotions.objects.filter(company=com,member=company_obj.member,to_date__gte = today.date())

            for pv in var3:
                obj.append(model_to_dict(pv))

            count=None
            if len(obj)>7:
                count=1
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",obj)
            context['object_list'] = obj
            context['group'] = group

            context['count'] = count
            return context

        else:
            lead_u=lead_user.objects.get(user=user)

            lead_obj=Lead.objects.get(pk=lead_u.customer.pk)

            group=Group.objects.get(user=user)
            groupname=group.name
            #var3=lead_user.objects.get(user=user)
            #var1 = Lead.objects.get(pk=var3.customer.pk)
            #address= UserProfile.objects.get(user=lead_obj.member)
            #print("-------------address",address.shop_name)
            obj=[]
            veh=Lead_Vehicle.objects.filter(lead=lead_obj)
            today=datetime.today()
            msg=None
            print(groupname)
            if groupname=="Customer":
                if veh:
                    for vehicle in veh:
                        if groupname != "All":
                            #var2=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date())
                            var2=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to="Customer")
                            print("QQQQQQQ1",var2)
                            for v in var2:
                                obj.append(model_to_dict(v))
                        #if groupname == "All":
                        try:
                            allpromo=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to="All")
                            print("QQQQQQQ2",allpromo)
                            for f in allpromo:
                                obj.append(model_to_dict(f))
                        except Exception as e:
                            pass
                            print("no promotion for ALL")
                com=Company.objects.get(company_name='All')

                #modd=Company_Model.objects.get(model_name='All')
                #mk=Make_Year1.objects.get(make_year='All')
                var3=Promotions.objects.filter(company=com,member=lead_obj.member,to_date__gte = today.date())

                for pv in var3:
                    obj.append(model_to_dict(pv))
                #print(len(obj))
                count=None
                if len(obj)>7:
                    count=1
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",obj)
                context['object_list'] = obj
                context['group'] = group
                #context['address'] = address
                context['count'] = count
                return context
            if groupname=="Lead":
                if veh:

                    for vehicle in veh:
                        if groupname != "All":
                            #var2=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date())
                            var2=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to="Lead")
                            print("QQQQQQQ1",var2)
                            for v in var2:
                                obj.append(model_to_dict(v))
                        #if groupname == "All":
                        try:
                            allpromo=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to="All")
                            print("QQQQQQQ2",allpromo)
                            for f in allpromo:
                                obj.append(model_to_dict(f))
                        except Exception as e:
                            pass
                            print("no promotion for ALL")
                com=Company.objects.get(company_name='All')

                #modd=Company_Model.objects.get(model_name='All')
                #mk=Make_Year1.objects.get(make_year='All')
                var3=Promotions.objects.filter(company=com,member=lead_obj.member,to_date__gte = today.date())

                for pv in var3:
                    obj.append(model_to_dict(pv))
                #print(len(obj))
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",obj)
                context['object_list'] = obj
                context['group'] = group
                context['address'] = address
                return context
            if groupname=="E_Customer":
                if veh:

                    for vehicle in veh:
                        if groupname != "All":
                            #var2=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date())
                            var2=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to="Customer")
                            print("QQQQQQQ1",var2)
                            for v in var2:
                                obj.append(model_to_dict(v))
                        #if groupname == "All":
                        try:
                            allpromo=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to="All")
                            print("QQQQQQQ2",allpromo)
                            for f in allpromo:
                                obj.append(model_to_dict(f))
                        except Exception as e:
                            pass
                            print("no promotion for ALL")
                com=Company.objects.get(company_name='All')

                #modd=Company_Model.objects.get(model_name='All')
                #mk=Make_Year1.objects.get(make_year='All')
                var3=Promotions.objects.filter(company=com,member=lead_obj.member,to_date__gte = today.date())

                for pv in var3:
                    obj.append(model_to_dict(pv))
                #print(len(obj))
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",obj)
                count=None
                if len(obj)>7:
                    count=1
                context['object_list'] = obj
                context['group'] = group
                context['address'] = None
                context['count'] = count
                return context
 
               
class PromotionListall(AuthRequiredMixin, ListView):
    model= Promotions
    template_name = 'promotion/promotion_all.html'
    success_url = reverse_lazy('promotion:server_list_all')
    
    def get_context_data(self, **kwargs):
        
        context = super(PromotionListall, self).get_context_data(**kwargs)
        response = TemplateResponse(self.request, self.template_name)
        user = self.request.user

        group=Group.objects.get(user=user)
        groupname=str(group.name)
	address=None
        if group.name=="Company":

            obj=[]
            #print("in company")
            company_obj=CustCompany.objects.get(email=user.email)
            #print("Company obj",company_obj)
            driver_list=Company_Driver.objects.filter(company=company_obj)
            for driver in driver_list:
                lead_obj=Lead.objects.get(pk=driver.driver.pk)
                #print(lead_obj)
                veh=Lead_Vehicle.objects.filter(lead=lead_obj)
                today=datetime.today()
                msg=None
                if veh:
                    #print("Vehicle object",veh)
                    for vehicle in veh:
                        print("vehicle details",vehicle.company.pk," ",vehicle.model.pk," ",vehicle.makeyear.pk," ",today.date())
                        var2=Promotions.objects.filter(member=company_obj.member,
                                                       company=vehicle.company,
                                                       model_id=vehicle.model,
                                                       make_year=vehicle.makeyear,
                                                       to_date__gte = today.date(),
                                                       display_to="Customer")
                        print("QQQQQQQ1",var2)
                        for v in var2:
                            obj.append(model_to_dict(v))
                        promo_list2=Promotions.objects.filter(member=company_obj.member,
                                                              company=vehicle.company,
                                                              model_id=vehicle.model,
                                                              make_year=vehicle.makeyear,
                                                              to_date__gte = today.date(),
                                                              display_to="Lead")
                        print("QQQQQQQ2",promo_list2)
                        for v in promo_list2:
                            obj.append(model_to_dict(v))
                        try:
                            allpromo=Promotions.objects.filter(member=company_obj.member,
                                                               company=vehicle.company,
                                                               model_id=vehicle.model,
                                                               make_year=vehicle.makeyear,
                                                               to_date__gte = today.date(),
                                                               display_to="All")
                            print("QQQQQQQ3",allpromo)
                            for f in allpromo:
                                obj.append(model_to_dict(f))
                        except Exception as e:
                            pass
                            print("no promotion for ALL")
            print("final obj list",obj)
            com=Company.objects.get(company_name='All')
            var3=Promotions.objects.filter(company=com,member=company_obj.member,to_date__gte = today.date())

            for pv in var3:
                obj.append(model_to_dict(pv))

            count=None
            if len(obj)>7:
                count=1
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",obj)
            context['object_list'] = obj
            context['group'] = group

            context['count'] = count
            return context
        else:
            lead_u=lead_user.objects.get(user=user)
            lead_obj=Lead.objects.get(pk=lead_u.customer.pk)
            #var3=lead_user.objects.get(user=user)
            #var1 = Lead.objects.get(pk=lead_u.customer.pk)
            address= UserProfile.objects.get(user=lead_obj.member)
            obj=[]
            veh=Lead_Vehicle.objects.filter(lead=lead_obj)
            msg=None
            if veh:
               for vehicle in veh:
                  today=datetime.today()
                  if groupname is "All":
                        var2=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date())
                  else:
                        print("in else group")
                        var2=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to=groupname)
                  for v in var2:
                        obj.append(model_to_dict(v))
                  try:
                      varr2=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to='All')
                      for v12 in varr2:
                          print("in all")
                          obj.append(model_to_dict(v12))
                  except Exception as e:
                      pass
            print(obj)

            com=Company.objects.get(company_name='All')
            #modd=Company_Model.objects.get(model_name='All')
            #mk=Make_Year1.objects.get(make_year='All')
            today = datetime.now().date()
            today_start = datetime.combine(today, time())
            var5=Promotions.objects.filter(company=com,member=lead_obj.member).exclude(to_date__lt=today_start)
            for pv in var5:
                obj.append(model_to_dict(pv))
            context['object_list'] = obj
            context['group'] = group
            context['address'] = address
            return context        
class Promo_List_Mem(AuthRequiredMixin, ListView):
    model= Promotions
    template_name = 'promotion/promotion_list_member.html'
    success_url = reverse_lazy('promotion:server_list_mem')
    
    def get_context_data(self, **kwargs):
        context = super(Promo_List_Mem, self).get_context_data(**kwargs)
        response = TemplateResponse(self.request, self.template_name)
        user = self.request.user
        group=Group.objects.get(user=user)
        today = datetime.now().date()
        today_start = datetime.combine(today, time())
        var2=Promotions.objects.filter(member=user).exclude(to_date__lt=today_start)
        filter=PromotionFilter(self.request.GET, queryset=var2)
        context['filter'] = filter
        context['group'] = group
        context['object_list'] = var2
        return context

class PromotionCreate(AuthRequiredMixin,SuccessMessageMixin, CreateView):
    logger.debug("start of promotion create view")
    logger.info("start of Create view")
    logger.debug("start of Create view")
    model = Promotions
    form_class=PromotionForm
    success_url = reverse_lazy('promotion:server_list_mem')
    success_message = "Promotion successfully created "
    #fields = ['member','company','model_id','price','make_year','image','Service_id','discount', 'description', 'from_date','to_date','coupon_code','display_to']
    
    def get_context_data(self, **kwargs):
        context = super(PromotionCreate, self).get_context_data(**kwargs)
        user = self.request.user
        group=Group.objects.get(user=user)
        context['group'] = group
        return context
    
    def form_valid(self, form):
        user= self.request.user
        today=datetime.today()
        answer=form.cleaned_data['display_to']
        self.object = form.save(commit=False)
        self.object.date_promo = today.date()
        self.object.display_to=answer
        self.object.member=user
        self.object.save()
        now = timezone.now()
        variable=Timeline(comment1="have created a " ,comment2="promotion",action_create=now,user=self.request.user)
        variable.save()
        user= self.request.user
        message=" has created a special offer."
        activity="Create"
        sent_promotion(self.request,self.object.pk,message,activity)
	return super(PromotionCreate, self).form_valid(form)

    

class PromotionUpdate(AuthRequiredMixin,SuccessMessageMixin, UpdateView):
    logger.info("start of Update view")
    logger.debug("start of Update view")
    model = Promotions
    form_class=PromotionForm
    success_url = reverse_lazy('promotion:server_list_mem')
    #fields = ['member','company','price','image','model_id','make_year','Service_id','discount', 'description', 'from_date','to_date','coupon_code']
    success_message = "Promotion successfully updated"
    
    def get_context_data(self, **kwargs):
        context = super(PromotionUpdate, self).get_context_data(**kwargs)
       
        user = self.request.user
        group=Group.objects.get(user=user)
        context['group'] = group
        return context
    
    def form_valid(self, form):
        today=datetime.today()
        self.object = form.save(commit=False)
        self.object.date_update = today.date()
        self.object.save()
        now = timezone.now()
        variable=Timeline(comment1="have updated a" ,comment2=" promotion",action_create=now,user=self.request.user)
        variable.save()
        user= self.request.user
        message=" has updated a special offer."
        activity="Update"
        sent_promotion(self.request,self.object.pk,message,activity)
            	
        return super(PromotionUpdate, self).form_valid(form)

class PromotionDelete(AuthRequiredMixin, DeleteView):
    logger.debug("start of promotion delete view")
    logger.info("start of Update view")
    logger.debug("start of Update view")
    model = Promotions
    success_url = reverse_lazy('promotion:server_list_mem')
    
    def get_context_data(self, **kwargs):
        context = super(PromotionDelete, self).get_context_data(**kwargs) 
        user = self.request.user
        group=Group.objects.get(user=user)
        context['group'] = group
        return context

@login_required(login_url="/registration/login/")
def getmodel(request):
    companyid = request.GET.get('companyid', None)
    queryset1=Company_Model.objects.filter(company_id=companyid)
    modelDict1=[]
    for company in queryset1 :
        shiftData = model_to_dict(company)
        modelDict1.append(shiftData)       
    return JsonResponse(modelDict1, safe=False)

class get_promotion(generics.ListAPIView):
     serializer_class = promotionSerializer
     def get_queryset(self):
         username = self.kwargs['val']
         querySet = Promotions.objects.filter(pk=username)
         return querySet

@login_required(login_url="/registration/login/")    
def promotion_history(request):
    user=request.user
    today=datetime.today()
    group=Group.objects.get(user=user)
    #status = Status.objects.get(status="Job Completed")
    list_promo=[]
    promotions=Promotions.objects.filter(member=request.user,to_date__lt=today.date()).order_by('to_date')
    print("$$$$$$$$$$$$:",promotions)
    for promotion in promotions:
        print("promotion id--",promotion.id)
        cust_request=customer_request.objects.filter(promotion=promotion)
        for cust_request1 in cust_request:
            print("request id---",cust_request1.id)
            list_promo.append(cust_request1)
    filter = promohistoryFilter(request.GET, queryset=promotions)
   # print("customer appointment:",customer_appointment)
    ctx={'promotions':promotions,'group':group,'list_promo':list_promo,'filter':filter}
    return render(request,"promotion/promotion_history.html",ctx)
     

@login_required(login_url="/registration/login/")    
def promotion_reopen(request,pk):
    user=request.user
    group=Group.objects.get(user=user)
    object=Promotions.objects.get(pk=pk)
    promotion_form=PromotionForm(instance=object)
    today=datetime.today()
    if request.method=='POST':
        print(promotion_form.errors)
        print("in post")
        promotion_form=PromotionForm(request.POST,request.FILES)
        if promotion_form.is_valid():
            print("form is valid")
            promotion_obj=promotion_form.save(commit=False)
            promotion_obj.member=request.user
            promotion_obj.date_promo=today.date()
            promotion_obj.save()
            messages.success(request,'Promotion added successfully ')
            message="Created new promotion"
            activity="Create"
            sent_promotion(request,promotion_obj.pk,message,activity)
            return redirect('promotion:server_list_mem')
        else:
            print("in form invalid")
            print(promotion_form.errors)
            return render(request,'promotion/Reopen_promotion.html',{'form':promotion_form,"group":group})
    else:
        return render(request,'promotion/Reopen_promotion.html',{'form':promotion_form,"group":group})

def sent_promotion(request,promo_id,message,activity):
    user=request.user
    promotion=Promotions.objects.get(pk=promo_id)
   # print("promotion object:",promotion)
    notification_sentto=promotion.display_to
    #message="Created new promotion"
    if notification_sentto=='All':
            #print("sent to",notification_sentto)
            status_obj=Status.objects.get(status="Deactivate")
            lead = Lead.objects.filter(~Q(status=status_obj),member= user)
            for lead_obj in lead:
             #   print("in for",lead_obj)
                try:
                    lead_u=lead_user.objects.get(customer=lead_obj)
                except Exception as e:
                    print("lead user matching query does not exist",lead_obj.email)
                    old_user=User.objects.get(username=lead_obj.email)
                    lead_u=lead_user(customer=lead_obj,user=old_user)
                    lead_u.save()
                if promotion.company.company_name=='ALL': 
              #      print("promotion.company.company_name",promotion.company.company_name)
                    notify.send(request.user,recipient=lead_u.user,verb=message,app_name="Promotion",activity="create",object_id=promotion.pk)
                    #notifications for ios
                    try:
                        deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                        #print("devices to which notifications is sent: ",deviceiOS)
                        for deviceiOS1 in deviceiOS:
                            message_sent=deviceiOS1.send_message(message)
                    except Exception as e:
                        print("exception------------------------------------------",e.message)
                    #notifications for ios end
                    #notifications for android
                    try: 
                        device = FCMDevice.objects.filter(user=lead_u.user.pk)
                        #print("devices to which notifications is sent: ",device)
                        for device1 in device:
                            device1.send_message("Promotion",message)
                           # print("message sent")
                    except Exception as e:
                        print("exception------------------------------------------",e.message)
                        #notifications for android end 
                else:
                    try:
#                         print("in notifications sent to all")
#                         print("1111111111111company:",promotion.company)
#                         print("1111111111111model:",promotion.model_id)
#                         print("1111111111makeyear:",promotion.make_year)
#                         print("11111111lead",lead_obj)
                        lead_veh1=Lead_Vehicle.objects.filter(company=promotion.company,model=promotion.model_id,makeyear=promotion.make_year,lead=lead_obj)
                        for lead_veh in lead_veh1:
                            if lead_veh: 
                                notify.send(request.user,recipient=lead_u.user,verb=message,app_name="Promotion",activity="create",object_id=promotion.pk)
                                #notifications for ios
                                try:
                                    deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                                    #print("devices to which notifications is sent: ",deviceiOS)
                                    for deviceiOS1 in deviceiOS:
                                        message_sent=deviceiOS1.send_message(message)
                                except Exception as e:
                                    print("exception------------------------------------------",e.message)
                                #notifications for ios end
                                #notifications for android
                                try: 
                                    device = FCMDevice.objects.filter(user=lead_u.user.pk)
                                    #print("devices to which notifications is sent: ",device)
                                    for device1 in device:
                                        device1.send_message("Promotion",message)
                                       # print("message sent")
                                except Exception as e:
                                    print("exception------------------------------------------",e.message)
                                #notifications for android end 
                    except Exception as e:
                        print("exception--------",e.message)
    elif notification_sentto=='Lead':
#             print("sent to",notification_sentto)
            status_obj=Status.objects.get(status="Lead")
            lead = Lead.objects.filter(status=status_obj,member= user)                        
            for lead_obj in lead:
#                 print("in for")
                try:
                    lead_u=lead_user.objects.get(customer=lead_obj)
                except Exception as e:
                    print("lead user matching query does not exist",lead_obj.email)
                    old_user=User.objects.get(username=lead_obj.email)
                    lead_u=lead_user(customer=lead_obj,user=old_user)
                    lead_u.save()
                if promotion.company.company_name=='All': 
#                     print("promotion.company.company_name",promotion.company.company_name)
                    notify.send(request.user,recipient=lead_u.user,verb=message,app_name="Promotion",activity="create",object_id=promotion.pk)
#                   #notifications for ios
                    try:
                        deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                        #print("devices to which notifications is sent: ",deviceiOS)
                        for deviceiOS1 in deviceiOS:
                            message_sent=deviceiOS1.send_message(message)
                    except Exception as e:
                        print("exception------------------------------------------",e.message)
                    #notifications for ios end
                    #notifications for android
                    try: 
                        device = FCMDevice.objects.filter(user=lead_u.user.pk)
                        #print("devices to which notifications is sent: ",device)
                        for device1 in device:
                            device1.send_message("Promotion",message)
                         #   print("message sent")
                    except Exception as e:
                        print("exception------------------------------------------",e.message)
                        #notifications for android end 
                else:
                    try:
#                         print("in notifications sent to lead")
#                         print("22222company:",promotion.company)
#                         print("22222model:",promotion.model_id)
#                         print("22222makeyear:",promotion.make_year)
#                         print("22222lead",lead_obj)
                        lead_veh1=Lead_Vehicle.objects.filter(company=promotion.company,model=promotion.model_id,makeyear=promotion.make_year,lead=lead_obj)
                        for lead_veh in lead_veh1:
                            if lead_veh: 
                                notify.send(request.user,recipient=lead_u.user,verb=message,app_name="Promotion",activity="create",object_id=promotion.pk)
                                #notifications for ios
                                try:
                                    deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                                    #print("devices to which notifications is sent: ",deviceiOS)
                                    for deviceiOS1 in deviceiOS:
                                        message_sent=deviceiOS1.send_message(message)
                                except Exception as e:
                                    print("exception------------------------------------------",e.message)
                                #notifications for ios end
                                #notifications for android
                                try: 
                                    device = FCMDevice.objects.filter(user=lead_u.user.pk)
                                    #print("devices to which notifications is sent: ",device)
                                    for device1 in device:
                                        device1.send_message("Promotion",message)
                                        #print("message sent")
                                except Exception as e:
                                    print("exception------------------------------------------",e.message)
                            #notifications for android end
                    except Exception as e:
                        print("exception---------",e.message) 
    else:
            #print("sent to",notification_sentto)
            status_obj=Status.objects.get(status="Customer")
            lead = Lead.objects.filter(status=status_obj,member= user)                        
            for lead_obj in lead:
                #print("in for",lead_obj)
                try:
                    lead_u=lead_user.objects.get(customer=lead_obj)
                except Exception as e:
                    print("lead user matching query does not exist",lead_obj.email)
                    old_user=User.objects.get(username=lead_obj.email)
                    lead_u=lead_user(customer=lead_obj,user=old_user)
                    lead_u.save()
                if promotion.company.company_name=='All': 
                    #print("promotion.company.company_name",promotion.company.company_name)
                    notify.send(request.user,recipient=lead_u.user,verb=message,app_name="Promotion",activity="create",object_id=promotion.pk)
#                   #notifications for ios
                    try:
                        deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                        #print("devices to which notifications is sent: ",deviceiOS)
                        for deviceiOS1 in deviceiOS:
                            message_sent=deviceiOS1.send_message(message)
                    except Exception as e:
                        print("exception------------------------------------------",e.message)
                    #notifications for ios end
                    #notifications for android
                    try: 
                        device = FCMDevice.objects.filter(user=lead_u.user.pk)
                        #print("devices to which notifications is sent: ",device)
                        for device1 in device:
                            device1.send_message("Promotion",message)
#                             print("message sent")
                    except Exception as e:
                        print("exception------------------------------------------",e.message)
                        #notifications for android end 
                else:
                    try:
#                         print("in notifications sent to customer")
#                         print("333company:",promotion.company)
#                         print("333model:",promotion.model_id)
#                         print("333makeyear:",promotion.make_year)
#                         print("333lead",lead_obj)
                        lead_veh1=Lead_Vehicle.objects.filter(company=promotion.company,model=promotion.model_id,makeyear=promotion.make_year,lead=lead_obj)
                        for lead_veh in lead_veh1:
                            if lead_veh: 
                                notify.send(request.user,recipient=lead_u.user,verb=message,app_name="Promotion",activity="create",object_id=promotion.pk)
                                #notifications for ios
                                try:
                                    deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
                                    #print("devices to which notifications is sent: ",deviceiOS)
                                    for deviceiOS1 in deviceiOS:
                                        message_sent=deviceiOS1.send_message(message)
                                except Exception as e:
                                    print("exception------------------------------------------",e.message)
                                #notifications for ios end
                                #notifications for android
                                try: 
                                    device = FCMDevice.objects.filter(user=lead_u.user.pk)
                                    #print("devices to which notifications is sent: ",device)
                                    for device1 in device:
                                        device1.send_message("Promotion",message)
                                        print("message sent")
                                except Exception as e:
                                    print("exception------------------------------------------",e.message)
                                #notifications for android end 
                    except Exception as e:
		    	print("exception e---------------",e)	