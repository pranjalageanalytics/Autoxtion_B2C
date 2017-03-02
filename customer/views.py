from django.shortcuts import render, render_to_response, get_object_or_404,redirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from customer.models import customer_request
from django.core.urlresolvers import reverse_lazy
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from CRM.models import *
from django.contrib.auth.models import User, Group
from django.http.response import JsonResponse
from promotion.models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
logger = logging.getLogger('Appointment')
logger.addHandler(logging.NullHandler())
from promotion.mixin import *
from django.contrib.messages.views import SuccessMessageMixin
from django.template.response import TemplateResponse
from notifications.signals import notify 
from customer.forms import *
from .forms import *
from Appointment.models import *
from Timeline.models import *
from django.utils import timezone
from customer.filters import *
import time
from push_notifications.models import GCMDevice, APNSDevice
from fcm_django.models import FCMDevice
from django.db.models import Q



class RequestList(AuthRequiredMixin, ListView):
    model= Promotions
    template_name = 'customer/request_list.html'
    success_url = reverse_lazy('promotion:server_list')
    
    def get_context_data(self, **kwargs):
        context = super(RequestList, self).get_context_data(**kwargs)
        response = TemplateResponse(self.request, self.template_name)
        user = self.request.user
        group=Group.objects.get(user=user)
        today=datetime.today()
        status_schedule=Status.objects.get(status="Scheduled")
        if group.name == "Member":
            logger.debug("user is from member group")
            var1 = Lead.objects.filter(member=user)
            var3=customer_request.objects.filter(~Q(status=status_schedule),customer__in=var1,emergency_status=None,date__gte = today.date())
            filter = CustomerRequestFilter(self.request.GET, queryset=var3)
            context = {'object_list': var3, 'group':group,'filter':filter}
            #context = {'object_list': var3, 'group':group}
            return context
        elif group.name=="Company":
            logger.debug("user is from company group")
            company_auth=User.objects.get(email=user.email)
            cust_comp=CustCompany.objects.get(email=company_auth.email)
            print("customer company:",cust_comp.email)
            comp_dri=Company_Driver.objects.filter(company=cust_comp)
            print("before for")
            for comp_driver in comp_dri:
                print(" after for company driver",comp_driver)
                #var3= customer_request.objects.filter(customer=comp_driver.driver,status=status_pending,date__gte = today.date(),emergency_status=None)
                var3= customer_request.objects.filter(customer__in=[comp_driver.driver for comp_driver in comp_dri ],status=status_pending,date__gte = today.date(),emergency_status=None)
                print("requests filtered",var3)
                filter = CustomerRequestFilter(self.request.GET, queryset=var3)
                context = {'object_list': var3, 'group':group,'filter':filter}
                return context
        elif group.name == "Lead":
	    filter=None
            logger.debug("user is from customer group")
            customer=lead_user.objects.get(user=user)
            cust = Lead.objects.get(pk=customer.customer.pk)
            address= UserProfile.objects.get(user=cust.member) 
            var3= customer_request.objects.filter(~Q(status=status_schedule),customer=customer.customer,date__gte = today.date(),emergency_status=None)
            count= len(var3)
            print("number of request for lead==", count)
            if count == 0:
                print("cannlot convert to cust")
            else:
                cust.status= Status.objects.get(status= 'Customer')
                cust.save()
                print("cust status=====",cust.status.pk)
                server1_group = User.groups.through.objects.get(user=user)
                server1_group.group=Group.objects.get(name='Customer')
                server1_group.save()
                filter = CustomerRequestFilter(self.request.GET, queryset=var3)
            context = {'object_list': var3, 'group':group,'address':address,'filter':filter}
           # context = {'object_list': var3, 'group':group,'address':address}
            return context
        
        else:
            logger.debug("user is from customer group")
            customer=lead_user.objects.get(user=user)
            cust = Lead.objects.get(pk=customer.customer.pk)
            address= UserProfile.objects.get(user=cust.member) 
            var3= customer_request.objects.filter(~Q(status=status_schedule),customer=customer.customer).exclude(status_id__in=[7])
            filter = CustomerRequestFilter(self.request.GET, queryset=var3)
            context = {'object_list': var3, 'group':group,'address':address,'filter':filter}
           # context = {'object_list': var3, 'group':group,'address':address}
            return context
    
class RequestnewCreate(AuthRequiredMixin,SuccessMessageMixin, CreateView):
    logger.debug("start of create new request list view")
    model = customer_request
    #template_name = 'customer_request1_form.html'
    form_class = customerForm
    success_url = reverse_lazy('customer:server_list')
   # fields = ['id','customer','description','service_type','date_request','date','from_time','to_time','status','image']
    success_message = "Service Request successfully created "
    
    def get_context_data(self, **kwargs):
        print("inside request get")
        context = super(RequestnewCreate, self).get_context_data(**kwargs)
        #response = TemplateResponse(self.request, self.template_name)
        id2=self.request.POST.get("promo_id")
        user = self.request.user
        today=datetime.today()
        print("todays date is====", today.date())
        group=Group.objects.get(user=user)
        lead_u=lead_user.objects.get(user=user)
        #request1=
        #request1 = get_object_or_404(customer_request, customer=lead_u)
        #print(" get request1111====", request1)
        lead=Lead.objects.get(pk=lead_u.customer.pk)
        address= UserProfile.objects.get(user=lead.member) 
        context['group'] = group
        context['promo'] = id2
        context['address'] = address
        context['date'] = today.date()
        return context
    def get_form_kwargs(self):
        kwargs = super(RequestnewCreate, self).get_form_kwargs()
 
        kwargs['users'] = self.request.user
        print("!!!!!!!!!!!!",kwargs )
        return kwargs


    def form_invalid(self, form):
        print("for INVALID")
        #context = super(RequestnewCreate, self).get_context_data(**kwargs)
        context = super(RequestnewCreate, self).form_invalid(form)
        context['service_type'] = "errorr"
        return context

    def form_valid(self, form):
        user=self.request.user
        cust1= lead_user.objects.get(user= user.id)
        cust= Lead.objects.get(pk= cust1.customer.pk)
        print("customer_id:",cust.pk)
        today=datetime.today()
        print(self.request.POST.get("service_type"))
        print(today.date())
        service_obj=Service.objects.get(pk=self.request.POST.get("service_type"))
        print(service_obj)
        
        lastcustreq=customer_request.objects.filter(date_request=today.date(),customer=cust,service_type=service_obj)
        print(lastcustreq)
        qlen=len(lastcustreq)
        print("---------",qlen)
        if qlen>0:
            print("can not add request")
            print(lastcustreq[qlen-1])
            form.add_error("service_type",'You have already made a request today for same service type')
            return self.form_invalid(form)
            #return redirect(RequestList)
        else:
            today=datetime.today()
            status=Status.objects.get(status="Pending")
            self.object = form.save(commit=False)
            self.object.date_request = today.date()
            self.object.status=status
            #self.object.image=form.cleaned_data('image')
            self.object.save()
            self.object.customer=cust
            print("customer_id:",cust.pk)
            self.object.save()
            now = timezone.now()
            variable=Timeline(comment1="have created a", comment2="Request",action_create=now,user=self.request.user)
            variable.save()
            lead_u=lead_user.objects.get(user=user)
            lead=Lead.objects.get(pk=lead_u.customer.pk)
            status_lead=Status.objects.get(status="Customer")
            lead.status=status_lead
            lead.save()
            #notify.send(self.request.user,recipient=lead.member,verb="Created a new request")
            notify.send(self.request.user,recipient=lead.member,verb="Created new request",app_name="CustomerRequest",activity="create",object_id=self.object.pk)
            try:
                comp_dri=Company_Driver.objects.get(driver=lead)
                print("Company driver:",comp_dri)
                company_user=User.objects.get(email=comp_dri.company.email) 
                notify.send(self.request.user,recipient=company_user,verb="Created new request",app_name="CustomerRequest",activity="create",object_id=self.object.pk)
                print("notification sent to company",company_user)
            except:
                pass
            return super(RequestnewCreate, self).form_valid(form)
    
class RequestCreate(AuthRequiredMixin,SuccessMessageMixin, CreateView):
    logger.debug("start of create request with promotion id ")
    model = customer_request
   # form_class = UpdatecustomerForm
    #form_class = customerForm
    form_class = customerRequestPromotionForm
	
    template_name="customer/customer_request_promotionform.html"
    success_url = reverse_lazy('customer:server_list')
   # fields = ['promotion','customer','description','service_type','image','date','from_time','to_time']
    success_message = "Service Request successfully created "
    
    def get_context_data(self, **kwargs):
        context = super(RequestCreate, self).get_context_data(**kwargs)
        var= Promotions.objects.get(id=self.kwargs['pk'])
        promo= Promotions.objects.get(pk = var.id)
        user = self.request.user
        group=Group.objects.get(user=user)
        lead_u=lead_user.objects.get(user=user)
        lead=Lead.objects.get(pk=lead_u.customer.pk)
        address= UserProfile.objects.get(user=lead.member)
        context['address'] = address
        context['group'] = group
        context['promo'] = var.id
        context['promo_detail'] = promo
        return context
    
    def form_valid(self, form):
        print("form is valid")
        today=datetime.today()
        user = self.request.user
        lead_u=lead_user.objects.get(user=user)
        lead=Lead.objects.get(pk=lead_u.customer.pk)
        status_lead=Status.objects.get(status="Customer")
        lead.status=status_lead
        lead.save()
        status=Status.objects.get(status="Pending")
        var= Promotions.objects.get(id=self.kwargs['pk'])
        self.object = form.save(commit=False)
        self.object.date_request = today.date()
        self.object.promotion=var
        self.object.status=status
        self.object.customer=lead
        self.object.save()
        print("form saved: ",self.object.pk)
        print(" date:",self.object.date)
        now = timezone.now()
        variable=Timeline(comment1="have created a", comment2="Request",action_create=now,user=self.request.user)
        variable.save()
        
      
        #notify.send(self.request.user,recipient=lead.member,verb="Created a new request")
        notify.send(self.request.user,recipient=lead.member,verb="Created new request with promotion",app_name="CustomerRequest",activity="createrequest_promotion",object_id=self.object.pk)
        try:
                comp_dri=Company_Driver.objects.get(driver=lead)
                print("Company driver:",comp_dri)
                company_user=User.objects.get(email=comp_dri.company.email) 
                notify.send(self.request.user,recipient=company_user,verb="Created new request with promotion",app_name="CustomerRequest",activity="createrequest_promotion",object_id=self.object.pk)
                print("notification sent to company for request across promotion",company_user)
        except:
                pass
       
        return super(RequestCreate, self).form_valid(form)    
    
class RequestUpdate(AuthRequiredMixin,SuccessMessageMixin, UpdateView):
    logger.debug("start of update request view")
    model = customer_request
    form_class = customerForm
    success_url = reverse_lazy('customer:server_list')
   # fields = ['service_type','description', 'date_update','date','from_time','to_time','image']
    template_name="customer/customer_updaterequest_form.html"
    success_message = "Service Request successfully updated"
    
    def get_context_data(self, **kwargs):
        context = super(RequestUpdate, self).get_context_data(**kwargs)
        group=Group.objects.get(user=self.request.user)
        context['group'] = group
        return context

    def get_form_kwargs(self):
        kwargs = super(RequestUpdate, self).get_form_kwargs()
 
        kwargs['users'] = self.request.user
        print("!!!!!!!!!!!!",kwargs )
        return kwargs

    
    def form_valid(self, form):
        today=datetime.today()
        self.object = form.save(commit=False)
        self.object.date_update = today.date()
        self.object.save()
        now = timezone.now()
        variable=Timeline(comment1="have updated a", comment2=" Request",action_create=now,user=self.request.user)
        variable.save()
        id_request=self.kwargs['pk']
        cust_request=customer_request.objects.get(id=id_request)
        lead_u=lead_user.objects.get(customer=cust_request.customer.pk)
       # print(lead_u.user)
        lead=Lead.objects.get(pk=lead_u.customer.pk)
        #notify.send(self.request.user,recipient=lead.member,verb="Customer has edited your request for "+str(cust_request.service_type)+" .Please confirm")
        notify.send(self.request.user,recipient=lead.member,verb="Updated request",app_name="CustomerRequest",activity="update",object_id=self.object.pk)  
        try:
            comp_dri=Company_Driver.objects.get(driver=lead)
            print("Company driver:",comp_dri)
            company_user=User.objects.get(email=comp_dri.company.email) 
            notify.send(self.request.user,recipient=company_user,verb="Updated request",app_name="CustomerRequest",activity="update",object_id=self.object.pk)
            print("notification sent to company for update_request",company_user)
        except:
                pass
     
        return super(RequestUpdate, self).form_valid(form)

class RequestDelete(AuthRequiredMixin, DeleteView):
    logger.debug("start of delete request view")
    logger.debug("start of create request with promotion id list view")
    model = customer_request
    success_url = reverse_lazy('customer:server_list')
    
    def get_context_data(self, **kwargs):
        context = super(RequestDelete, self).get_context_data(**kwargs)
        
        user = self.request.user
        group=Group.objects.get(user=user)
        
        var3=lead_user.objects.get(user=user)
        var1 = Lead.objects.get(pk=var3.customer.pk)
        address= UserProfile.objects.get(user=var1.member) 
        context['address'] = address
        context['group'] = group
        return context
        
def get_lead(request):
    user=request.user
    l=lead_user.objects.get(user=user)
    data=model_to_dict(l)
    print("data in lead",data)
    return JsonResponse(data)

class MemberEditRequest(AuthRequiredMixin,SuccessMessageMixin, UpdateView):
    logger.debug("start of update request view")
    model = customer_request
    form_class= customerMemberEditForm
    success_url = reverse_lazy('customer:server_list')
    #fields = ['service_type','description', 'date_update','date','from_time','to_time','image']
    success_message = "Service Request successfully updated"
    template_name="customer/member_request_form.html"
    
    def get_context_data(self, **kwargs):
        context = super(MemberEditRequest, self).get_context_data(**kwargs)
        group=Group.objects.get(user=self.request.user)
        flag=None
        if self.object.comment:
            flag=1
        else:
            flag=2
        context['group'] = group
        context['flag'] = flag
        return context
    
    def form_valid(self, form):
        print("form is valid")
        id_request=self.kwargs['pk']
        print("@@@@@@@@@@@@@2",id_request)
        today=datetime.today()
        self.object = form.save(commit=False)
        self.object.date_update = today.date()
        self.object.status=Status.objects.get(status="Reschedule")
        self.object.save()
        user = self.request.user
        cust_request=customer_request.objects.get(id=id_request)
        print(cust_request.customer.pk)
        
        lead_u=lead_user.objects.get(customer=cust_request.customer.pk)
        print(lead_u.user)
        #notify.send(self.request.user,recipient=lead_u.user,verb="Member has edited your request for "+str(cust_request.service_type)+" .Please confirm")
        notify.send(self.request.user,recipient=lead_u.user,verb=" has rescheduled your request.",app_name="CustomerRequest",activity="update",object_id=self.object.pk)
        try:
            comp_dri=Company_Driver.objects.get(driver=cust_request.customer)
            print("Company driver:",comp_dri)
            company_user=User.objects.get(email=comp_dri.company.email) 
            notify.send(self.request.user,recipient=company_user,verb=" Rescheduled request of "+str(lead_u.user.first_name),app_name="CustomerRequest",activity="update",object_id=self.object.pk)
            print("notification sent to company for update_request of your driver",company_user)
        except:
            pass
        message=str(user.first_name)+" "+str(user.last_name)+" Rescheduled your request"
        #notifications for ios
        try:        
            deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
            print("devices to which notifications is sent: ",deviceiOS)
            for deviceiOS1 in deviceiOS:
                message_sent=deviceiOS1.send_message(message)
        except Exception as e:
            print("exception------------------------------------------",e.message)
        #notifications for ios end
        #notifications for android
        try: 
            print("user: ",FCMDevice.objects.filter(user=lead_u.user.pk))
            device = FCMDevice.objects.filter(user=lead_u.user.pk)
            print("devices to which notifications is sent: ",device)
            for device1 in device:
                device1.send_message("Request Edit",message)
            print("message sent")
        except Exception as e:
            print("exception------------------------------------------",e.message)
         #notifications for android end


        return super(MemberEditRequest, self).form_valid(form)

def AcceptRequest(request,customer_request_id):
    print("---------------------------------ConfirmRequest------------------------------")
    today=datetime.today()
    cust_request=customer_request.objects.get(id=customer_request_id)
    confirm_status=Status.objects.get(status="Confirm")
    cust_request.status=confirm_status
    cust_request.save()
    lead_u=lead_user.objects.get(customer=cust_request.customer.pk)
    print(lead_u.user)
    lead=Lead.objects.get(pk=lead_u.customer.pk)
    notify.send(request.user,recipient=lead.member,verb=" has accepted rescheduled request detail. ",app_name="CustomerRequest",activity="accept",object_id=cust_request.pk)
    
    try:
        comp_dri=Company_Driver.objects.get(driver=lead)
        print("Company driver:",comp_dri)
        company_user=User.objects.get(email=comp_dri.company.email) 
        notify.send(request.user,recipient=company_user,verb=" Accepted request of "+str(lead.member.first_name)+" "+str(lead.member.last_name),app_name="CustomerRequest",activity="accept",object_id=cust_request.pk)
        print("notification sent to company for request for your driver",company_user)
    except:
        pass   
    return redirect('/customer/')


def ConfirmRequest(request,customer_request_id):
    print("---------------------------------ConfirmRequest------------------------------")
    today=datetime.today()
    cust_request=customer_request.objects.get(id=customer_request_id)
    status=Status.objects.get(status="Scheduled")
    confirm_status=Status.objects.get(status="Confirm")
    appointment=MemberAppointment()
    user=request.user
    var3= UserProfile.objects.get(user=cust_request.customer.member)
    appointment.customer=cust_request.customer
    appointment.member=var3
    appointment.status=status
    appointment.date=cust_request.date
    appointment.from_time=cust_request.from_time
    appointment.to_time=cust_request.to_time
    appointment.date_appointment=today
    appointment.request=cust_request
    appointment.save()
    cust_request.status=confirm_status
    cust_request.save()
    print("request:",cust_request.status)
    print("appointment:",appointment.status)
    
    lead_u=lead_user.objects.get(customer=cust_request.customer.pk)
    lead=Lead.objects.get(pk=lead_u.customer.pk)
    notify.send(request.user,recipient=lead.member,verb="Confirmed your "+str(cust_request.service_type)+" appointment ",app_name="Appointment",activity="create",object_id=appointment.pk)
    try:
        comp_dri=Company_Driver.objects.get(driver=lead)
        print("Company driver:",comp_dri)
        company_user=User.objects.get(email=comp_dri.company.email) 
        notify.send(request.user,recipient=company_user,verb=" have confirmed request of "+str(cust_request.customer.name)+" and scheduled an appointment",app_name="Appointment",activity="create",object_id=appointment.pk)
        print("notification sent to company for confirm request and generate appointment:",company_user)
    except Exception as e:
        print("it has an exception:",e)
        pass
   
    return redirect('/appointment/')

class customer_history(AuthRequiredMixin, ListView):
    model= MemberAppointment
    template_name = 'customer/customer_history.html'
    success_url = reverse_lazy('promotion:server_list')
    
    def get_context_data(self, **kwargs):
        context = super(customer_history, self).get_context_data(**kwargs)
        response = TemplateResponse(self.request, self.template_name)
        status1=Status.objects.get(status="Job Completed")
        user = self.request.user
        print("user", user)
        customerGroup=Group.objects.get(user=user)
	group=customerGroup
	#print("---------------------------",customerGroup.name)
        if customerGroup.name=="Company":
            print("in company")
            dict_final=[]
            dict1=[]
            var3_final=[]
            detail_final=[]
            sub_final=[]
            company_obj=CustCompany.objects.get(email=user.email)
            driver_list=Company_Driver.objects.filter(company=company_obj)
            for driver in driver_list:
                #lead_obj=Lead.objects.get(pk=driver.driver.pk)
                cust = Lead.objects.get(pk=driver.driver.pk)
                #print("--------------------------cust", cust)
                var3= MemberAppointment.objects.filter(customer=driver.driver,status=status1)

                for app in var3:
                    var3_final.append(app)
                    dict2=[]
                    dict1.append(app)
                    upcell=UpcellAppointment.objects.filter(appointment=app.pk)
                    dict2.append(upcell)
                    dict1.append(dict2)
                    dict3=[]
                    for sub in upcell:
                        sub_det=UpcellAppointmentSubService.objects.filter(upcellappointment=sub.pk)
                        dict3.append(sub_det)
                        dict_final.append(dict3)
                    #dict_final.append(dict1)
                #print("dict1dict1dict1", len(dict1))
                dict_final.append(dict1)



                detail=UpcellAppointment.objects.filter(appointment__in=[app_details.pk for app_details in var3])
                for d in detail:
                    detail_final.append(d)
                sub_detail=UpcellAppointmentSubService.objects.filter(upcellappointment__in=[sub_details.pk for sub_details in detail])
                for s in sub_detail:
                    sub_final.append(s)
            context = {'var3':var3_final,'detail':detail_final,'sub_detail':sub_final,'zipped_data':zip(var3_final,detail_final,sub_final),'parent':dict_final,'customerGroup':group}
            return context
	else:
            customer=lead_user.objects.get(user=user)
            cust = Lead.objects.get(pk=customer.customer.pk)
            print("cust", cust)
            dict1=[]
            detail=[]
	    sub_detail=[]
            dict1=[]
	    #print("**************************************",customerGroup.name)
            var3= MemberAppointment.objects.filter(customer=customer.customer,status=status1)
            for app in var3:
            	dict2=[]
            	dict1.append(app)
            	upcell=UpcellAppointment.objects.filter(appointment=app.pk)  
            	dict2.append(upcell)
            	dict1.append(dict2)
            	dict3=[]
            	for sub in upcell:
                	sub_det=UpcellAppointmentSubService.objects.filter(upcellappointment=sub.pk)
                	dict3.append(sub_det)
                	dict1.append(dict3)
        	print("dict1dict1dict1", dict1)
        
    
        	detail=UpcellAppointment.objects.filter(appointment__in=[app_details.pk for app_details in var3])
        	sub_detail=UpcellAppointmentSubService.objects.filter(upcellappointment__in=[sub_details.pk for sub_details in detail])
        
        	#print("***************************",customerGroup.name)
                context = {'var3':var3,'detail':detail,'sub_detail':sub_detail,'zipped_data':zip(var3,detail,sub_detail),'parent':dict1,'customerGroup':group}
		#context={'var3':var3,'customerGroup':group}
                print("----------------------------",group.name)
                return context
     

class EmergencyRequestList(AuthRequiredMixin, ListView):
    model= Promotions
    template_name = 'customer/customer_emergency_request.html'
    success_url = reverse_lazy('promotion:EmergencyRequestList')
    
    def get_context_data(self, **kwargs):
        context = super(EmergencyRequestList, self).get_context_data(**kwargs)
        response = TemplateResponse(self.request, self.template_name)
        user = self.request.user
        group=Group.objects.get(user=user)
        if group.name == "Member":
            logger.debug("user is from member group")
            var1 = Lead.objects.filter(member=user)
            var3=customer_request.objects.filter(customer__in=var1,emergency_status=1)
            context = {'object_list': var3, 'group':group}
            return context
        
        elif group.name == "Lead":
            logger.debug("user is from customer group")
            customer=lead_user.objects.get(user=user)
            cust = Lead.objects.get(pk=customer.customer.pk)
            address= UserProfile.objects.get(user=cust.member) 
            var3= customer_request.objects.filter(customer=customer.customer, emergency_status=1)
            count= len(var3)
            print("number of request for lead==", count)
            if count == 0:
                print("cannlot convert to cust")
            else:
                cust.status= Status.objects.get(status= 'Customer')
                cust.save()
                print("cust status=====",cust.status.pk)
                server1_group = User.groups.through.objects.get(user=user)
                server1_group.group=Group.objects.get(name='Customer')
                server1_group.save()
            context = {'object_list': var3, 'group':group,'address':address}
            return context
        elif group.name=="Company":
            logger.debug("user is from company group")
            company_auth=User.objects.get(email=user.email)
            cust_comp=CustCompany.objects.get(email=company_auth.email)
            print("customer company:",cust_comp.email)
            comp_dri=Company_Driver.objects.filter(company=cust_comp)
            print("before for")
            for comp_driver in comp_dri:
                print(" after for company driver",comp_driver)
                #status=Status.objects.get(status="Job Completed")
                #var3=customer_request.objects.filter(customer=comp_driver.driver,emergency_status=1)
                var3=customer_request.objects.filter(customer__in=[comp_driver.driver for comp_driver in comp_dri ],emergency_status=1)
                print("sorted customer request:",var3)   
                context = {'object_list': var3, 'group':group}
                return context
        else:
            logger.debug("user is from customer group")
            customer=lead_user.objects.get(user=user)
            cust = Lead.objects.get(pk=customer.customer.pk)
            address= UserProfile.objects.get(user=cust.member) 
            var3= customer_request.objects.filter(customer=customer.customer, emergency_status=1)
            context = {'object_list': var3, 'group':group,'address':address}
            return context
    
class Add_emergency_req(AuthRequiredMixin,SuccessMessageMixin, CreateView):
    logger.debug("start of create new request list view")
    model = customer_request
    template_name = 'customer/emergency_request_form.html'
    #form_class = customerForm
    success_url = reverse_lazy('customer:EmergencyRequestList')
    fields = ['description','image']
    success_message = "Emergency Service Request successfully created "
    
    def get_context_data(self, **kwargs):
        print("inside request get")
        context = super(Add_emergency_req, self).get_context_data(**kwargs)
        #response = TemplateResponse(self.request, self.template_name)
        id2=self.request.POST.get("promo_id")
        user = self.request.user
        today=datetime.today()
        print("todays date is====", today.date())
        group=Group.objects.get(user=user)
        lead_u=lead_user.objects.get(user=user)
        #request1=
        #request1 = get_object_or_404(customer_request, customer=lead_u)
        #print(" get request1111====", request1)
        lead=Lead.objects.get(pk=lead_u.customer.pk)
        address= UserProfile.objects.get(user=lead.member) 
        context['group'] = group
        context['promo'] = id2
        context['address'] = address
        context['date'] = today.date()
        return context
    
    def form_valid(self, form):
        user=self.request.user
        cust1= lead_user.objects.get(user= user.id)
        cust= Lead.objects.get(pk= cust1.customer.pk)
        print("customer_id:",cust.pk)
        service_break=Service.objects.get(service_type="Breakdown")
        today=datetime.today()
        status=Status.objects.get(status="Pending")
        self.object = form.save(commit=False)
        self.object.date_request = today.date()
        self.object.date = today.date()
        print("_____________________________________",time.strftime("%I:%M %p"))
        self.object.from_time = time.strftime("%I:%M %p")
        self.object.service_type = service_break
        self.object.emergency_status=1
        self.object.status=status
        #self.object.image=form.cleaned_data('image')
        self.object.save()
        self.object.customer=cust
        print("customer_id:",cust.pk)
        self.object.save()
        lead_u=lead_user.objects.get(user=user)
        lead=Lead.objects.get(pk=lead_u.customer.pk) 
        #notify.send(self.request.user,recipient=lead.member,verb="Created a new request")
        notify.send(self.request.user,recipient=lead.member,verb="Created emergency request",app_name="CustomerRequest",activity="create_emergency_request",object_id=self.object.pk,emergency_status=1)

        try:
            comp_dri=Company_Driver.objects.get(driver=lead)
            print("Company driver:",comp_dri)
            company_user=User.objects.get(email=comp_dri.company.email) 
            notify.send(self.request.user,recipient=company_user,verb="Created emergency request",app_name="CustomerRequest",activity="create_emergency_request",object_id=self.object.pk,emergency_status=1)
            print("notification sent to company for create_emergency_request",company_user)
        except:
                pass
	return super(Add_emergency_req, self).form_valid(form)
    
class edit_emergency_req(AuthRequiredMixin,SuccessMessageMixin, UpdateView):
    logger.debug("start of update request view")
    model = customer_request
    #form_class = customerForm
    success_url = reverse_lazy('customer:EmergencyRequestList')
    fields = ['description','image']
    template_name = 'customer/emergency_request_form.html'
    success_message = "Service Request successfully updated"
    
    def get_context_data(self, **kwargs):
        context = super(edit_emergency_req, self).get_context_data(**kwargs)
        group=Group.objects.get(user=self.request.user)
        context['group'] = group
        return context
    
    def form_valid(self, form):
        today=datetime.today()
        self.object = form.save(commit=False)
        self.object.date_update = today.date()
        self.object.date = today.date()
        print("_____________________________________",time.strftime("%I:%M %p"))
        self.object.from_time = time.strftime("%I:%M %p")
        self.object.save()
        id_request=self.kwargs['pk']
        cust_request=customer_request.objects.get(id=id_request)
        lead_u=lead_user.objects.get(customer=cust_request.customer.pk)
       # print(lead_u.user)
	    #notify.send(self.request.user,recipient=lead.member,verb="Customer has edited your request for "+str(cust_request.service_type)+" .Please confirm")
       # notify.send(self.request.user,recipient=lead.member,verb="Updated emergency request",app_name="CustomerRequest",activity="update_emergency_request",object_id=self.object.pk,emergency_status==1) 
        lead=Lead.objects.get(pk=lead_u.customer.pk)
        notify.send(self.request.user,recipient=lead.member,verb="Customer has edited your request for "+str(cust_request.service_type)+" .Please confirm")
        try:
            comp_dri=Company_Driver.objects.get(driver=lead)
            print("Company driver:",comp_dri)
            company_user=User.objects.get(email=comp_dri.company.email) 
            notify.send(self.request.user,recipient=company_user,verb="Customer has edited your request for "+str(cust_request.service_type),app_name="CustomerRequest",activity="update_emergency_request",object_id=self.object.pk,emergency_status=1)
            print("notification sent to company for update_emergency_request",company_user)
        except:
                pass
        return super(edit_emergency_req, self).form_valid(form)

class MemberEditRequestEmergency(AuthRequiredMixin,SuccessMessageMixin, UpdateView):
    logger.debug("start of update request view")
    model = customer_request
    #form_class= customerForm
    success_url = reverse_lazy('customer:EmergencyRequestList')
    fields = ['description','date','from_time','image']
    success_message = "Service Request successfully updated"
    template_name="customer/member_emer_request_form.html"
    
    def get_context_data(self, **kwargs):
        context = super(MemberEditRequestEmergency, self).get_context_data(**kwargs)
        group=Group.objects.get(user=self.request.user)
        context['group'] = group
        return context
    
    def form_valid(self, form):
        print("form is valid")
        id_request=self.kwargs['pk']
        print("@@@@@@@@@@@@@2",id_request)
        today=datetime.today()
        self.object = form.save(commit=False)
        self.object.date_update = today.date()
        self.object.save()
        user = self.request.user
        cust_request=customer_request.objects.get(id=id_request)
        print(cust_request.customer.pk)
        
        lead_u=lead_user.objects.get(customer=cust_request.customer.pk)
        print(lead_u.user)
        message=str(user.first_name)+" "+str(user.last_name)+" Updated your emergency request"
        #notifications for ios
        try:        
            deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
            print("devices to which notifications is sent: ",deviceiOS)
            for deviceiOS1 in deviceiOS:
                message_sent=deviceiOS1.send_message(message)
        except Exception as e:
            print("exception------------------------------------------",e.message)
        #notifications for ios end
        #notifications for android
        try: 
            print("user: ",FCMDevice.objects.filter(user=lead_u.user.pk))
            device = FCMDevice.objects.filter(user=lead_u.user.pk)
            print("devices to which notifications is sent: ",device)
            for device1 in device:
                device1.send_message("Request Edit",message)
            print("message sent")
        except Exception as e:
            print("exception------------------------------------------",e.message)
         #notifications for android end
        notify.send(self.request.user,recipient=lead_u.user,verb="Member has edited your request for "+str(cust_request.service_type)+" .Please confirm")
        try:
            comp_dri=Company_Driver.objects.get(driver=cust_request.customer)
            print("Company driver:",comp_dri)
            company_user=User.objects.get(email=comp_dri.company.email)
            print("company user:",company_user) 
            notify.send(self.request.user,recipient=company_user,verb="Member has edited your request of "+str(cust_request.customer.name)+" for "+str(cust_request.service_type),app_name="CustomerRequest",activity="member_edit_emergency",object_id=self.object.pk,emergency_status=1)
            print("notification sent to company for update_request of your driver",company_user)
        except:
            pass
        return super(MemberEditRequest, self).form_valid(form)

class delete_emergency_req(AuthRequiredMixin, DeleteView):
    logger.debug("start of delete request view")
    logger.debug("start of create request with promotion id list view")
    model = customer_request
    success_url = reverse_lazy('customer:EmergencyRequestList')
    
    def get_context_data(self, **kwargs):
        context = super(delete_emergency_req, self).get_context_data(**kwargs)
        
        user = self.request.user
        group=Group.objects.get(user=user)
        
        var3=lead_user.objects.get(user=user)
        var1 = Lead.objects.get(pk=var3.customer.pk)
        address= UserProfile.objects.get(user=var1.member) 
        context['address'] = address
        context['group'] = group
        return context

def Emer_ConfirmRequest(request,customer_request_id):
    today=datetime.today()
    cust_request=customer_request.objects.get(id=customer_request_id)
    status=Status.objects.get(status="Scheduled")
    confirm_status=Status.objects.get(status="Confirm")
    appointment=MemberAppointment()
    user=request.user
    var3= UserProfile.objects.get(user=cust_request.customer.member)
    appointment.customer=cust_request.customer
    appointment.member=var3
    appointment.status=status
    appointment.date=cust_request.date
    appointment.from_time=cust_request.from_time
    appointment.to_time=cust_request.to_time
    appointment.date_appointment=today
    appointment.request=cust_request
    appointment.save()
    cust_request.status=confirm_status
    cust_request.emergency_status=1
    cust_request.save()
    print("request:",cust_request.status)
    print("appointment:",appointment.status)
    lead_u=lead_user.objects.get(customer=cust_request.customer.pk)
    group=Group.objects.get(user=request.user)
    lead=Lead.objects.get(pk=lead_u.customer.pk)
    
    message=str(user.first_name)+" "+str(user.last_name)+" have scheduled an appointment for your request "+str(cust_request.service_type)+" on "+str(cust_request.date)
        #notifications for ios
    try:        
            deviceiOS = APNSDevice.objects.filter(user=lead_u.user.pk)
            print("devices to which notifications is sent: ",deviceiOS)
            for deviceiOS1 in deviceiOS:
               message_sent=deviceiOS1.send_message(message)
    except Exception as e:
            print("exception------------------------------------------",e.message)
        #notifications for ios end
        #notifications for android
    try: 
            print("user: ",FCMDevice.objects.filter(user=lead_u.user.pk))
            device = FCMDevice.objects.filter(user=lead_u.user.pk)
            print("devices to which notifications is sent: ",device)
            for devices in device:
                devices.send_message("Appointment",message)
            print("message sent")
    except Exception as e:
            print("exception------------------------------------------",e.message)
         #notifications for android end

    notify.send(request.user,recipient=lead_u.user,verb="Confirmed and scheduled your "+str(cust_request.service_type)+" appointment ",app_name="Appointment",activity="create",object_id=appointment.pk,emergency_status=1)
    try:
        comp_dri=Company_Driver.objects.get(driver=cust_request.customer)
        print("Company driver:",comp_dri)
        print("company user:",User.objects.get(email=comp_dri.company.email) )
        company_user=User.objects.get(email=comp_dri.company.email) 
        notify.send(request.user,recipient=company_user,verb=" have confirmed request of "+str(cust_request.customer.name)+" and scheduled an appointment",app_name="Appointment",activity="create",object_id=appointment.pk,emergency_status=1)
        print("notification sent to company for confirm and schedule driver request",company_user)
    except Exception as e:
        print("it has an exception",e)
        pass

    return redirect('/appointment/') 
  
