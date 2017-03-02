from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template.context import RequestContext
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from Appointment.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Group
from CRM.models import *
import logging
logger = logging.getLogger('Appointment')
logger.addHandler(logging.NullHandler())
from customer.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.template import Context
from datetime import datetime
from promotion.mixin import *
from django.template.response import TemplateResponse
from django.contrib.messages.views import SuccessMessageMixin
from notifications.signals import notify
from .tasks import *
from django.db.models import Q
from.forms import *
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.db.models import Sum
from django.http import JsonResponse
# Create your views here.
from django.forms.models import model_to_dict
from push_notifications.models import  APNSDevice
from fcm_django.models import FCMDevice
from django.forms.models import modelformset_factory
from Timeline.models import *
from django.utils import timezone
from Appointment.filters import *
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
    
class AppointmentList(AuthRequiredMixin, ListView):
    model= MemberAppointment
    template_name = 'Appointment/Appointment_list.html'
    success_url = reverse_lazy('promotion:server_list')
    
    def get_context_data(self, **kwargs):
        context = super(AppointmentList, self).get_context_data(**kwargs)
        response = TemplateResponse(self.request, self.template_name)
        user = self.request.user
        group=Group.objects.get(user=user)
        if group.name == "Member":
            logger.debug("user is member")
            #profile=UserProfile.objects.get(user=user)
            #var2=MemberAppointment.objects.filter(member=profile,)
            status=Status.objects.get(status="Job Completed")
            profile=UserProfile.objects.get(user=user)
            var2=MemberAppointment.objects.filter(~Q(status=status),member=profile)
            today=datetime.today()
            date=today.date()
            filter = AppointmentFilter(self.request.GET, queryset=var2)
            context['filter'] = filter
            context['object_list'] = var2
            context['group'] = group
            #context['today'] = date
            return context
        elif group.name == "Company":
            logger.debug("user is company")
            company_auth=User.objects.get(email=user.email)
            cust_comp=CustCompany.objects.get(email=company_auth.email)
            print("customer company:",cust_comp.email)
            status=Status.objects.get(status="Job Completed")
            comp_dri=Company_Driver.objects.filter(company=cust_comp)
            print("before for")
            for comp_driver in comp_dri:
                print(" after for company driver",comp_driver)
                #status=Status.objects.get(status="Job Completed")
                #var2=MemberAppointment.objects.filter(~Q(status=status),customer=comp_driver.driver)
                var2=MemberAppointment.objects.filter(~Q(status=status),customer__in=[comp_driver.driver for comp_driver in comp_dri ])
                print("sorted member appointment:",var2)
                today=datetime.today()
                date=today.date()
                filter = AppointmentFilter(self.request.GET, queryset=var2)
                context={'filter':filter,'today':date,'group': group,'object_list':var2}
                return context
        else:
            logger.debug("user is customer")
            customer=lead_user.objects.get(user=user)
            var1 = Lead.objects.get(pk=customer.customer.pk)
            address= UserProfile.objects.get(user=var1.member) 
            var2= MemberAppointment.objects.filter(customer=customer.customer)
            today=datetime.today()
            date=today.date()
            cust = Lead.objects.get(pk=customer.customer.pk) 
            filter = AppointmentFilter(self.request.GET, queryset=var2)
            context = {'object_list': var2, 'group': group, 'address': address, 'today': date,'filter':filter}            
            context['object_list'] = var2
            context['group'] = group
            context['today'] = date
            context['address'] = address
            return context
            

class AppointmentCreate(AuthRequiredMixin,SuccessMessageMixin, CreateView):
    logger.debug("start of Appointment create")
    model = MemberAppointment
    success_url = reverse_lazy('Appointment:server_list')
    fields = ['coment',]
    var1 = None
    success_message = "Appointment successfully created and an email reminder has been sent to customer for the same"
       
    def get_context_data(self, **kwargs):
        context = super(AppointmentCreate, self).get_context_data(**kwargs)
        var= customer_request.objects.get(id=self.kwargs['pk'])
        
        var1 = Lead.objects.get(id=var.customer.id)
       
        var2= UserProfile.objects.get(user=var1.member.id)
        user = self.request.user
        group=Group.objects.get(user=user)
        context['req_id'] = self.kwargs['pk']
        context['cust_id'] = var.customer.pk
        context['mem_id'] = var2.id
        context['request_detail'] = var
        context['group'] = group
        return context
        
    def form_valid(self, form, **kwargs):
        user= self.request.user
        detail1 = get_object_or_404(User, pk=user.id)
        detail2 = get_object_or_404(UserProfile, user=detail1)
        cust_detail= customer_request.objects.get(id=self.kwargs['pk'])
        status= Status.objects.get(status="Scheduled")
        print("status:",status)
        cust= Lead.objects.get(pk= cust_detail.customer.id)
        today=datetime.today()
        self.object = form.save(commit=False)
        self.object.request= cust_detail
        self.object.member= detail2
        self.object.customer =cust
        self.object.status =status
        self.object.date_appointment = today.date()
        self.object.date=cust_detail.date
        self.object.from_time=cust_detail.from_time
        self.object.to_time=cust_detail.to_time
        self.object.save()
        cust_detail.status_id = status
        cust_detail.save()
        now = timezone.now()
        variable=Timeline(comment1="have created an ", comment2="Appointment",action_create=now,user=self.request.user)
        variable.save()
#         date=form.cleaned_data['date']
#         from_time=form.cleaned_data['from_time']
#         to_time=form.cleaned_data['to_time']
        ctx={'date': cust_detail.date, 'from_time': cust_detail.from_time, 'to_time': cust_detail.to_time, 'request': cust_detail.description, 'name':detail1.first_name, 'phone':detail2.phone_no, 'shop':detail2.shop_name, 'address':detail2.shop_address}
        data = {}
        l_u=lead_user.objects.get(customer=cust_detail.customer)
        #notify.send(self.request.user, recipient=l_u.user, verb='scheduled an Appointment  ')
        notify.send(self.request.user,recipient=l_u.user,verb="Confirmed your "+str(cust_detail.service_type)+" appointment ",app_name="Appointment",activity="create",object_id=self.object.pk)
        message=str(detail1.first_name)+" "+str(detail1.last_name)+" have scheduled an appointment for your request "+str(cust_detail.service_type.service_type)+" on "+str(cust_detail.date)
        #notifications for ios
        try:        
            deviceiOS = APNSDevice.objects.filter(user=l_u.user.pk)
            print("devices to which notifications is sent: ",deviceiOS)
            message_sent=deviceiOS.send_message(message)
        except Exception as e:
            print("exception------------------------------------------",e.message)
        #notifications for ios end
        #notifications for android
        try: 
            print("user: ",FCMDevice.objects.filter(user=l_u.user.pk))
            device = FCMDevice.objects.filter(user=l_u.user.pk)
            print("devices to which notifications is sent: ",device)
            device.send_message("Appointment",message)
            print("message sent")
        except Exception as e:
            print("exception------------------------------------------",e.message)
         #notifications for android end 
    	send_appt_create_task.delay(str(cust_detail.date),str(cust_detail.from_time),str(cust_detail.to_time),cust_detail.description,detail1.first_name,detail2.phone_no,detail2.shop_name,detail2.shop_address,cust_detail.customer.email,detail1.email,detail2.website)
        return super(AppointmentCreate, self).form_valid(form)    
    
class AppointmentUpdate(AuthRequiredMixin,SuccessMessageMixin, UpdateView):
    logger.debug("start of Appointment update")
    model = MemberAppointment
    template_name = 'Appointment/update_appointment.html'
    form_class = UpdateAppointmentForm
    success_url = reverse_lazy('Appointment:server_list')
    #fields = ['date','from_time', 'to_time','coment']
    success_message = "Appointment successfully updated"
    
    def get_context_data(self, **kwargs):
        context = super(AppointmentUpdate, self).get_context_data(**kwargs)
        var2= MemberAppointment.objects.get(id=self.kwargs['pk'])
        var3=None
        if var2.request:
            var3= customer_request.objects.get(pk = var2.request.id)
        user = self.request.user
        group=Group.objects.get(user=user)
        context['request_detail'] = var3
        context['group'] = group
        return context
    
    def form_valid(self, form):
        print("in form valid")
        user= self.request.user
        detail1 = get_object_or_404(User, pk=user.id)
        detail2 = get_object_or_404(UserProfile, user=detail1)
        detail3 = get_object_or_404(MemberAppointment, pk=self.kwargs['pk'])
        cust_detail=None
        if detail3.request:
            cust_detail= customer_request.objects.get(id=detail3.request.pk)
        today=datetime.today()
        self.object = form.save(commit=False)
        self.object.date_update = today.date()
        self.object.save()
        now = timezone.now()
        variable=Timeline(comment1="have updated an ", comment2="Appointment",action_create=now,user=self.request.user)
        variable.save()
        date=form.cleaned_data['date']
        from_time=form.cleaned_data['from_time']
        to_time=form.cleaned_data['to_time']
        coment=form.cleaned_data['coment']
        #print("----------------------------for tasks")
        print("---------lead name",detail3.customer)
        if cust_detail:
            #print("----------------before sending update task")
            send_appt_update_task.delay(str(date),str(from_time),str(to_time),coment, cust_detail.description,detail3.customer.name,detail2.phone_no,detail2.shop_name,detail2.shop_address,cust_detail.customer.email,detail1.email,detail1.first_name,detail2.website)
            l_u=lead_user.objects.get(customer=cust_detail.customer)
            message=str(detail1.first_name)+" "+str(detail1.last_name)+" have updated appointment for your request "+str(cust_detail.service_type.service_type)+" on "+str(date)
            notify.send(self.request.user,recipient=l_u.user,verb="Updated your "+str(cust_detail.service_type)+" appointment ",app_name="Appointment",activity="update",object_id=self.object.pk)
            try:
                comp_dri=Company_Driver.objects.get(driver=detail3.customer)
                print("Company driver:",comp_dri)
                company_user=User.objects.get(email=comp_dri.company.email) 
                notify.send(user,recipient=company_user,verb=" Updated your appointment of "+str(detail3.customer.name),app_name="Appointment",activity="update",object_id=self.object.pk)
                print("notification sent to company for update appointment:",company_user)
            except Exception as e:
                print("it has an exception:",e)
                pass
        else:
            send_appt_update_task.delay(str(date),str(from_time),str(to_time),coment,"",detail3.customer.name,detail2.phone_no,detail2.shop_name,detail2.shop_address,"",detail1.email,detail1.first_name,detail2.website)
            print("=0=0=0000000",detail3.customer)
            l_u=lead_user.objects.get(customer=detail3.customer)
            message=str(detail1.first_name)+" "+str(detail1.last_name)+" have updated appointment for your request  on "+str(date)
            notify.send(self.request.user,recipient=l_u.user,verb="Updated your appointment ",app_name="Appointment",activity="update",object_id=self.object.pk)    
            try:
                comp_dri=Company_Driver.objects.get(driver=detail3.customer)
                print("Company driver:",comp_dri)
                company_user=User.objects.get(email=comp_dri.company.email) 
                notify.send(user,recipient=company_user,verb=" Updated your appointment of "+str(detail3.customer.name),app_name="Appointment",activity="update",object_id=self.object.pk)
                print("notification sent to company for update appointment:",company_user)
            except Exception as e:
                print("it has an exception:",e)
                pass
         #notifications for ios
        try:
            deviceiOS = APNSDevice.objects.filter(user=l_u.user.pk)
            print("device token",deviceiOS)
            for deviceiOS1 in deviceiOS:
                message_sent=deviceiOS1.send_message(message)
            print("@@@@@@@@@@@@@@@@@",message_sent)
        except Exception as e:
            print("exception------------------------------------------",e.message)
         #notifications for ios end
        #notifications for android
        try: 
            device = FCMDevice.objects.filter(user=l_u.user.pk)
            print("devices to which notifications is sent: ",device)
            for device1 in device:
                device1.send_message("Appointment update",message)
            
            print("message sent")
        except Exception as e:
            print("exception------------------------------------------",e.message)
         #notifications for android end        
        #print("-------------------after sending update task")
        return super(AppointmentUpdate, self).form_valid(form)
    
class AppointmentDelete(AuthRequiredMixin, DeleteView):
    logger.debug("start of Appointment delete")
    model = MemberAppointment
    success_url = reverse_lazy('Appointment:server_list')
    
    def get_context_data(self, **kwargs):
        context = super(AppointmentDelete, self).get_context_data(**kwargs)
        user = self.request.user
        group=Group.objects.get(user=user)
        context['group'] = group
        return context
    
    def delete(self, form, **kwargs):
        user= self.request.user
        var1= UserProfile.objects.get(user=user)
        var= MemberAppointment.objects.get(id=self.kwargs['pk'])
        l_u = lead_user.objects.get(customer=var.customer)
        message=" Sorry for the Inconvenience, the set date and time could not be allocated. Kindly Reschedule or contact your workshop."
        #notifications for ios
        try:
            
            deviceiOS = APNSDevice.objects.filter(user=l_u.user.pk)
            print("device token",deviceiOS)
            message_sent=deviceiOS.send_message(message)
            print("@@@@@@@@@@@@@@@@@",message_sent)
        except Exception as e:
            print("exception------------------------------------------",e.message)
        #notifications for ios end
        #notifications for android
        try: 
            device = FCMDevice.objects.filter(user=l_u.user.pk)
            print("devices to which notifications is sent: ",device)
            device.send_message("Appointment delete",message)
            print("message sent")
        except Exception as e:
            print("exception------------------------------------------",e.message)
         #notifications for android end
        ctx={'shop': var1.shop_name, 'name': user.first_name, 'email': user.username, 'address': var1.shop_address, 'phone': var1.phone_no}
        data = {}
        print("before delay")
        send_appt_delete_task.delay(var1.shop_name,user.first_name,user.username,var1.shop_address,var1.phone_no,var.customer.email,var1.website)
        print("after delay called")
        return super(AppointmentDelete, self).delete(form)

"""class done_appointment(AuthRequiredMixin,SuccessMessageMixin, ListView):
    model = MemberAppointment
    template_name = 'Appointment/Appointment_list.html'
    success_url = reverse_lazy('Appointment:server_list')
    success_message = "Job successfully Completed"
    
    def get_context_data(self, **kwargs):
        context = super(done_appointment, self).get_context_data(**kwargs)
        response = TemplateResponse(self.request, self.template_name)
        var1= MemberAppointment.objects.get(id=self.kwargs['pk'])
        user =self.request.user
        var3= UserProfile.objects.get(user=user)
        group=Group.objects.get(user=user)
        print("app detail for done===", var1.customer.email)
        status= Status.objects.get(status= 'Job Completed')
        var1.status= status
        var1.save()
        profile=UserProfile.objects.get(user=user)
        var2=MemberAppointment.objects.filter(member=profile)
        send_appt_done_task.delay(var3.shop_name,user.first_name,user.username,var3.shop_address,var3.phone_no,var1.customer.email)
        group=Group.objects.get(user=user)
        context['request_detail'] = var3
        context['group'] = group
        context['object_list'] = var2 
        return context"""


@login_required(login_url="/registration/login/")
def done_appointment(request, pk ):
    print("in appointment done",pk)
    today=datetime.today()
    var1= MemberAppointment.objects.get(pk=pk)
    user =request.user
    group=Group.objects.get(user=user)
    if group.name=="Company":
        company_obj=CustCompany.objects.get(email=user.username)
        var3= UserProfile.objects.get(user=company_obj.member)
        appointment_detail=MemberAppointment.objects.get(pk=pk)
        da=var1.service_type
        detail=UpcellAppointment.objects.filter(appointment=pk)
        print("detail detail detail", detail)
        sub_detail=UpcellAppointmentSubService.objects.filter(upcellappointment__in=[sub_details.pk for sub_details in detail])
        print("sub_detail sub_detail sub_detail", sub_detail)
        return render(request, "Appointment/job_done_app.html",{'detail':detail,'sub_detail':sub_detail,'appointment_detail':appointment_detail,'group':group})
    else:
    	var3= UserProfile.objects.get(user=user)
    	appointment_detail=MemberAppointment.objects.get(pk=pk)
    	da=var1.service_type
    	detail=UpcellAppointment.objects.filter(appointment=pk)
    	print("detail detail detail", detail)
    	sub_detail=UpcellAppointmentSubService.objects.filter(upcellappointment__in=[sub_details.pk for sub_details in detail])
    	print("sub_detail sub_detail sub_detail", sub_detail)
    
    	if request.method =='POST':
        	coment= request.POST.get('coment')
        	#print("member coment on done==", coment)
        	#print("app detail for done===", var1.customer.email)
        	status= Status.objects.get(status= 'Job Completed')
        	var1.status= status
        	var1.coment = coment
        	var1.date_update=today
        	var1.save()
        	#print("to sent in email==", var1.coment)
        	profile=UserProfile.objects.get(user=user)
        	var2=MemberAppointment.objects.filter(member=profile)
       		# print("=========================",var1.request.pk)
        	#cust_detail= customer_request.objects.get(id=var1.request.id)
        	l_u=lead_user.objects.get(customer=var1.customer)
        	notify.send(request.user,recipient=l_u.user,verb="Thank you, your vehicle is now ready to be picked up at your earliest convenience.",app_name="Appointment",activity="complete",object_id=var1.pk)
        	try:
            		comp_dri=Company_Driver.objects.get(driver=var1.customer)
            		print("Company driver:",comp_dri)
            		company_user=User.objects.get(email=comp_dri.company.email) 
            		notify.send(user,recipient=company_user,verb="Vehicle of "+str(var1.customer.name)+" is now ready to be picked up.",app_name="Appointment",activity="complete",object_id=var1.pk)
            		#print("notification sent to company for update appointment:",company_user)
        	except Exception as e:
                	print("it has an exception:",e)

        	message="Thank you, your vehicle is now ready to be picked up at your earliest convenience."
                       
        	try:
            		deviceiOS = APNSDevice.objects.filter(user=l_u.user.pk)
            		print("device token",deviceiOS)
            		message_sent=deviceiOS.send_message(message)
            		#print("@@@@@@@@@@@@@@@@@",message_sent)
        	except Exception as e:
            		print("exception------------------------------------------",e.message)
         	#notifications for ios end
        	#notifications for android
        	try: 
            		device = FCMDevice.objects.filter(user=l_u.user.pk)
            		#print("devices to which notifications is sent: ",device)
            		device.send_message("Appointment",message)
            		print("message sent")
        	except Exception as e:
            		print("exception------------------------------------------",e.message)
        	#notifications for android end
        	ctx={'shop': var3.shop_name, 'name': user.first_name, 'email': user.username, 'address': var3.shop_address, 'phone': var3.phone_no, 'coment': var1.coment}
        	data = {}
        	send_appt_done_task.delay(var3.shop_name,user.first_name,user.username,var3.shop_address,var3.phone_no,var1.customer.email,var1.coment,profile.website )
        	return redirect('Appointment:server_list')
    	return render(request, "Appointment/job_done_app.html",{'detail':detail,'sub_detail':sub_detail,'appointment_detail':appointment_detail,'group':group})




def Upcell_app_add(request, appointment_id):
    appointment_id=MemberAppointment.objects.get(pk=appointment_id)
    print("appointment_idappointment_id", appointment_id)
    testform1 = formset_factory(Upcell_appointment_form, extra=1)
    user=request.user
   
    group=Group.objects.get(user=user)
    #sub_service_form = formset_factory(Upcell_sub_service_form, extra=1)
    if request.method == 'POST':
         x= request.POST.get("tot_amount")
         print("XXXXXXX",x)
         upcell = testform1(request.POST, request.FILES)
         print("upcell upcell upcell", upcell)
         for f in upcell.forms:
             print("errorssss", f.errors)
             if f.is_valid():                 
                 f.save()
                 obj=f.save(commit=False)
                 obj.appointment=appointment_id
                 
                 obj.save()
         a=UpcellAppointment.objects.filter(appointment=appointment_id).aggregate(Sum('amount'))
         appointment_id.totalamount=x
         #appointment_id.upcell_status="UpSell Created"
         appointment_id.save()

         l_u=lead_user.objects.get(customer=appointment_id.customer)
         a_user=User.objects.get(pk=l_u.user.pk)
         notify.send(request.user,recipient=a_user,verb=" has requested confirmation for additional items in Appointments.",app_name="Appointment",activity="Add_upsell",object_id=appointment_id.pk)
         try:
            comp_dri=Company_Driver.objects.get(driver=appointment_id.customer)
            print("Company driver:",comp_dri)
            company_user=User.objects.get(email=comp_dri.company.email) 
            notify.send(user,recipient=company_user,verb=" has requested confirmation for additional items in Appointments of "+str(appointment_id.customer.name),app_name="Appointment",activity="Add_upsell",object_id=appointment_id.pk)
            print("notification sent to company for update appointment:",company_user)
         except Exception as e:
                print("it has an exception:",e)
                pass
         message=str(request.user.first_name)+" "+str(request.user.last_name)+" has requested confirmation for additional items in Appointments. "
        #notifications for ios
         try:        
            deviceiOS = APNSDevice.objects.filter(user=a_user.pk)
            print("devices to which notifications is sent: ",deviceiOS)
            for deviceiOS1 in deviceiOS:
                message_sent=deviceiOS1.send_message(message)
         except Exception as e:
            print("exception------------------------------------------",e.message)
        #notifications for ios end
        #notifications for android
         try: 
            print("user: ",FCMDevice.objects.filter(user=a_user.pk))
            device = FCMDevice.objects.filter(user=a_user.pk)
            print("devices to which notifications is sent: ",device)
            for device1 in device:
                device1.send_message("Add upsell",message)
            print("message sent")
         except Exception as e:
            print("exception------------------------------------------",e.message)
         #notifications for android end         
         
         #print("sunmmmmmmmmmmmmmm", a)
             
         print("SAVE SUCCESSFULLY")
         return redirect('/appointment/')
    return render(request,"Appointment/upcell_form.html",{"testform":testform1,'group':group})

def upcell_app_update(request, appointment_id):
    user=request.user
    group=Group.objects.get(user=user)
    appointment_id=MemberAppointment.objects.get(pk=appointment_id)
    detail=UpcellAppointment.objects.filter(appointment=appointment_id)
    sub_detail=UpcellAppointmentSubService.objects.filter(upcellappointment__in=[sub_details.pk for sub_details in detail])
    print("appointment_idappointment_id", sub_detail)
    queryk=UpcellAppointment.objects.filter(appointment=appointment_id.pk)
    testform1 = modelformset_factory(UpcellAppointment, form=Upcell_appointment_form, extra=0)
    #sub_service_form = formset_factory(Upcell_sub_service_form, extra=1)
    formset = testform1(queryset =queryk)
    if request.method == 'POST':
         x= request.POST.get("tot_amount")
         desc1= request.POST.get("form-0-description")
         print("XXXXXXX",x)
         upcell = testform1(request.POST, request.FILES)
         print("upcell upcell upcell", upcell)
         for f in upcell.forms:
             print("errorssss", f.errors)
             
             if f.is_valid():                 
                 f.save()
                 obj=f.save(commit=False)
                 obj.appointment=appointment_id
                 obj.save()
         a=UpcellAppointment.objects.filter(appointment=appointment_id)
         i=0
         for desc in a:
            i=i+1
            if i==1:
                desc.description=desc1
                desc.save()
         appointment_id.amount=x
         appointment_id.save()
         l_u=lead_user.objects.get(customer=appointment_id.customer)
         notify.send(request.user,recipient=l_u.user,verb=" has updated additional items in Appointments.",app_name="Appointment",activity="Update_upsell_member",object_id=appointment_id.pk)
         try:
            comp_dri=Company_Driver.objects.get(driver=appointment_id.customer)
            print("Company driver:",comp_dri)
            company_user=User.objects.get(email=comp_dri.company.email) 
            notify.send(user,recipient=company_user,verb=" has updated additional items in Appointments. of "+str(appointment_id.customer.name),app_name="Appointment",activity="Update_upsell_member",object_id=appointment_id.pk)
            print("notification sent to company for update appointment:",company_user)
         except Exception as e:
                print("it has an exception:",e)
                pass
         message=str(request.user.first_name)+" "+str(request.user.last_name)+" has updated additional items in Appointments."
        #notifications for ios
         try:        
            deviceiOS = APNSDevice.objects.filter(user=l_u.user.pk)
            print("devices to which notifications is sent: ",deviceiOS)
            for deviceiOS1 in deviceiOS:
                message_sent=deviceiOS1.send_message(message)
         except Exception as e:
            print("exception------------------------------------------",e.message)
        #notifications for ios end
        #notifications for android
         try: 
            print("user: ",FCMDevice.objects.filter(user=l_u.user.pk))
            device = FCMDevice.objects.filter(user=l_u.user.pk)
            print("devices to which notifications is sent: ",device)
            for device1 in device:
                device1.send_message("Appointment",message)
            print("message sent")
         except Exception as e:
            print("exception------------------------------------------",e.message)
         #notifications for android end
             
         print("SAVE SUCCESSFULLY")
         return redirect('/appointment/')
    return render(request,"Appointment/update_upsell.html",{"testform":formset,'group':group,'sub_detail':sub_detail})

def customer_upcell_update(request, appointment_id):
    user=request.user
   
    group=Group.objects.get(user=user)
    appointment_id=MemberAppointment.objects.get(pk=appointment_id)
    print("appointment_idappointment_id", appointment_id)
    queryk=UpcellAppointment.objects.filter(appointment=appointment_id.pk)
    testform1 = modelformset_factory(UpcellAppointment, form=Upcell_appointment_form, extra=0)
    #sub_service_form = formset_factory(Upcell_sub_service_form, extra=1)
    formset = testform1(queryset =queryk)
    if request.method == 'POST':
         x= request.POST.get("tot_amount")
         print("XXXXXXX",x)
         upcell = testform1(request.POST, request.FILES)
         print("upcell upcell upcell", upcell)
         for f in upcell.forms:
             print("errorssss", f.errors)
             if f.is_valid():                 
                 f.save()
                 obj=f.save(commit=False)
                 obj.appointment=appointment_id
                 
                 obj.save()
         a=UpcellAppointment.objects.filter(appointment=appointment_id).aggregate(Sum('amount'))
         
         cust_upcell=UpcellAppointment.objects.filter(appointment=appointment_id, accept=1)
         cust_tot=0
         if cust_upcell:
             appointment_id.upcell_status="UpSell Accepted"
         for d in cust_upcell:
             cust_tot=cust_tot+int(d.amount)
             print(cust_tot)
         print("sunmmmmmmmmmmmmmm", cust_tot)
         appointment_id.totalamount=cust_tot
         appointment_id.save()
         l_u=lead_user.objects.get(customer=appointment_id.customer)
         lead_obj=Lead.objects.get(pk=appointment_id.customer.pk)
         notify.send(request.user,recipient=lead_obj.member,verb="Updated an extra effort for appointment",app_name="Appointment",activity="Update_upsell_customer",object_id=appointment_id.pk)    
         print("SAVE SUCCESSFULLY")
         return redirect('/appointment/')
    return render(request,"Appointment/customer_upcell_update.html",{"testform":formset,'group':group})



def member_view_upcell_accepted(request, appointment_id):
    
    user=request.user
   
    group=Group.objects.get(user=user)
    appointment_id=MemberAppointment.objects.get(pk=appointment_id)
    print("appointment_idappointment_id", appointment_id)
    queryk=UpcellAppointment.objects.filter(appointment=appointment_id.pk,accept=1)
    testform1 = modelformset_factory(UpcellAppointment, form=Upcell_appointment_form, extra=0)
    #sub_service_form = formset_factory(Upcell_sub_service_form, extra=1)
    formset = testform1(queryset =queryk)
 
    return render(request,"Appointment/mem_upcell_accpet_view.html",{"testform":formset,'group':group})

def subservice_ajax(request):
    serviceid = request.GET.get('serviceid', None)
    queryset1=SubServiceType.objects.filter(service=serviceid)
    modelDict1=[]
    for service in queryset1 :
        shiftData = model_to_dict(service)
        modelDict1.append(shiftData)       
    return JsonResponse(modelDict1, safe=False)

@login_required(login_url="/registration/login/")
def schedule_appointment(request, pk ):
    user= request.user
    detail1 = get_object_or_404(User, pk=user.id)
    detail2 = get_object_or_404(UserProfile, user=detail1)
    cust_detail= customer_request.objects.get(id=pk)
 
    print("schedule_appointment")
    today=datetime.today()
    cust_request=customer_request.objects.get(pk=pk)
    status=Status.objects.get(status="Scheduled")
    confirm_status=Status.objects.get(status="Confirm")
    appointment=MemberAppointment()
    user=request.user
    var3= UserProfile.objects.get(user=user)
    appointment.customer=cust_request.customer
    appointment.member=var3
    appointment.status=status
    appointment.date=cust_request.date
    appointment.from_time=cust_request.from_time
    appointment.to_time=cust_request.to_time
    appointment.date_appointment=today
    appointment.request=cust_request
    appointment.save()
    cust_request.status=status
    cust_request.save()
    print("request:",cust_request.status)
    print("appointment:",appointment.status)
    lead=Lead.objects.get(pk=cust_request.customer.pk)
    l_u=lead_user.objects.get(customer=lead)
    send_appt_create_task.delay(str(cust_detail.date),str(cust_detail.from_time),str(cust_detail.to_time),cust_detail.description,detail1.first_name,detail2.phone_no,detail2.shop_name,detail2.shop_address,cust_detail.customer.email,detail1.email,detail2.website)
    try:
        comp_dri=Company_Driver.objects.get(driver=lead)
        print("Company driver:",comp_dri)
        company_user=User.objects.get(email=comp_dri.company.email) 
        notify.send(user,recipient=company_user,verb=" have confirmed appointment of "+str(cust_request.customer.name),app_name="Appointment",activity="create",object_id=appointment.pk)
        print("notification sent to company for confirm request and generate appointment:",company_user)
    except Exception as e:
        print("it has an exception:",e)
        pass
    message=str(user.first_name)+" "+str(user.last_name)+" have scheduled an appointment for your request "+str(cust_request.service_type.service_type)+" on "+str(cust_request.date)
        #notifications for ios
    try:        
        deviceiOS = APNSDevice.objects.filter(user=l_u.user.pk)
        print("devices to which notifications is sent: ",deviceiOS)
        for deviceiOS1 in deviceiOS:
            message_sent=deviceiOS1.send_message(message)
    except Exception as e:
        print("exception------------------------------------------",e.message)
    #notifications for ios end
    #notifications for android
    try: 
        print("user: ",FCMDevice.objects.filter(user=l_u.user.pk))
        device = FCMDevice.objects.filter(user=l_u.user.pk)
        print("devices to which notifications is sent: ",device)
        for device1 in device:
            device1.send_message("Appointment",message)
        print("message sent")
    except Exception as e:
        print("exception------------------------------------------",e.message)

    notify.send(user,recipient=l_u.user,verb="Confirmed your "+str(cust_request.service_type)+" appointment ",app_name="Appointment",activity="create",object_id=appointment.pk)

    return redirect('Appointment:server_list')
@login_required(login_url="/registration/login/")    
def member_create_appointment(request):
    user=request.user
    userprofile=UserProfile.objects.get(user=user)
    group=Group.objects.get(user=user)
    if request.method=='POST':
       form=member_appointment(request.POST)
       
      # print form['customer'].value()#['']
       k=Lead.objects.get(pk=form['customer'].value())
       #form['customer'].value=k
       print (form.errors)
       if form.is_valid():
           aa=form.cleaned_data['customer']
           status_obj=Status.objects.get(status="Scheduled")

           obj = MemberAppointment(
               
            service_type=form.cleaned_data['service_type'],
            vehicle=Lead_Vehicle.objects.get(pk=form['vehicle'].value()),
            date=form.cleaned_data['date'],
            from_time=form.cleaned_data['from_time'],
            to_time=form.cleaned_data['to_time'],
            coment=form.cleaned_data['coment'],
            customer= k,
            status=status_obj,
            
            member=userprofile,
            )
           obj.save()
           messages.success(request,"Appointment scheduled successfully for customer")
           l_u=lead_user.objects.get(customer=k)
           notify.send(request.user,recipient=l_u.user,verb="Scheduled an  appointment",app_name="Appointment",activity="schedule",object_id=obj.pk)
           send_appt_create_task.delay(str(obj.date),str(obj.from_time),str(obj.to_time),obj.coment,user.first_name,userprofile.phone_no,userprofile.shop_name,userprofile.shop_address,obj.customer.email,user.email,userprofile.website)
           try:
            comp_dri=Company_Driver.objects.get(driver=k)
            print("Company driver:",comp_dri)
            company_user=User.objects.get(email=comp_dri.company.email) 
            notify.send(user,recipient=company_user,verb="Scheduled an  appointment of "+str(k.name),app_name="Appointment",activity="schedule",object_id=obj.pk)
            print("notification sent to company for update appointment:",company_user)
           except Exception as e:
                print("it has an exception:",e)
                pass
           message=str(request.user.first_name)+" "+str(request.user.last_name)+" Scheduled an  appointment"
        #notifications for ios
           try:        
            deviceiOS = APNSDevice.objects.filter(user=l_u.user.pk)
            print("devices to which notifications is sent: ",deviceiOS)
            for deviceiOS1 in deviceiOS:
                message_sent=deviceiOS1.send_message(message)
           except Exception as e:
            print("exception------------------------------------------",e.message)
        #notifications for ios end
        #notifications for android
           try: 
            print("user: ",FCMDevice.objects.filter(user=l_u.user.pk))
            device = FCMDevice.objects.filter(user=l_u.user.pk)
            print("devices to which notifications is sent: ",device)
            for device1 in device:
                device.send_message("Appointment",message)
            print("message sent")
           except Exception as e:
            print("exception------------------------------------------",e.message)
         #notifications for android end        
           return redirect('/appointment/')
       else:
            print("no valid")
            variable=RequestContext(request,{'form':form,'group':group})
            return render(request,'Appointment/member_appointment_create.html',variable)
    else:
        form=member_appointment()
        variable=RequestContext(request,{'form':form,'group':group})
        return render(request,'Appointment/member_appointment_create.html',variable)

def ajxviews(request):
    current_user = request.user
    status=Status.objects.get(status="Lead")
    status1=Status.objects.get(status="Customer")
    leads=Lead.objects.filter((Q(status=status) | Q(status=status1)),member=current_user).values('pk','name','last_name')
    data=[]
    for l in leads:

        data.append(l)
    return JsonResponse(data,safe=False)

class today_appointment_list(AuthRequiredMixin, ListView):
    model= MemberAppointment
    template_name = 'Appointment/today_appointment_list.html'
    success_url = reverse_lazy('promotion:server_list')
    
    def get_context_data(self, **kwargs):
        context = super(today_appointment_list, self).get_context_data(**kwargs)
        response = TemplateResponse(self.request, self.template_name)
        user = self.request.user
        group=Group.objects.get(user=user)
        if group.name == "Member":
            logger.debug("user is member")
            #profile=UserProfile.objects.get(user=user)
            #var2=MemberAppointment.objects.filter(member=profile,)
            status=Status.objects.get(status="Job Completed")
            profile=UserProfile.objects.get(user=user)
            today=datetime.today()
            date=today.date()
            var2=MemberAppointment.objects.filter(~Q(status=status),member=profile, date=date)
            
            context['object_list'] = var2
            context['group'] = group
            #context['today'] = date
            return context
        else:
            logger.debug("user is customer")
            customer=lead_user.objects.get(user=user)
            var1 = Lead.objects.get(pk=customer.customer.pk)
            address= UserProfile.objects.get(user=var1.member) 
            var2= MemberAppointment.objects.filter(customer=customer.customer)
            today=datetime.today()
            date=today.date()
            cust = Lead.objects.get(pk=customer.customer.pk)
            context = {'object_list': var2, 'group': group, 'address': address, 'today': date}
            context['object_list'] = var2
            context['group'] = group
            context['today'] = date
            context['address'] = address
            return context

def upcell_delete_ajax(request,upcell):
   # upcell_id = request.GET.get('upcellid', None)
    tag_to_delete = get_object_or_404(UpcellAppointment, pk=upcell)
    appointment = get_object_or_404(MemberAppointment, pk=tag_to_delete.appointment.pk)
    tag_to_delete.delete()
    #return HttpResponseRedirect(reverse(upcell_app_update, args=(appointment.pk,)))
    return HttpResponseRedirect(reverse('Appointment:upcell_app_update', args=(appointment.pk,)))


@login_required(login_url="/registration/login/")    
def appointment_history(request):
    user=request.user
    today=datetime.today()
    group=Group.objects.get(user=user)
    user_profile=UserProfile.objects.get(user=user)
    #status = Status.objects.get(status="Job Completed")
    status = Status.objects.get(status="Job Completed")
    customer_appointment=MemberAppointment.objects.filter(member= user_profile,status=status).order_by('-date_update')
    filter = appointmenthistoryFilter(request.GET, queryset=customer_appointment)
   # print("customer appointment:",customer_appointment)
    ctx={'customer_appointment':customer_appointment,'group':group,'filter':filter}
    return render(request,"Appointment/Appointment_history.html",ctx)

def Appointment_History_Detail(request,appointment_id):
    #lead=Lead.objects.get(pk=lead_id)
    user=request.user
    group=Group.objects.get(user=user)
    #print("@@Lead:",lead)
    #status = Status.objects.get(status="Job Completed")
    var3=MemberAppointment.objects.get(pk=appointment_id)
    detail=UpcellAppointment.objects.filter(appointment=var3.pk)
    sub_detail=UpcellAppointmentSubService.objects.filter(upcellappointment__in=[sub_details.pk for sub_details in detail])
    ctx={'var3':var3,'detail':detail,'sub_detail':sub_detail,'group':group}
    return render(request,"Appointment/appointment_history_detail.html",ctx)

def get_vehicle(request):
    customerid = request.GET.get('customerid', None)
    queryset1=Lead_Vehicle.objects.filter(lead=customerid).values('pk','vehicle_no')
    print("queryset1",queryset1)
    modelDict1=[]
    for vehicle in queryset1:
        modelDict1.append(vehicle)       
    return JsonResponse(modelDict1, safe=False)
