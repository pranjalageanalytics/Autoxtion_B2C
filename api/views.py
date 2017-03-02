from django.shortcuts import render,HttpResponse
from CRM.models import *
from Appointment.models import *
from rest_framework import generics
from django.contrib.gis.serializers.geojson import Serializer
from .serializers import *
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from fcm_django.models import FCMDevice
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from Registration.tasks import *
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from Feedback.models import *
import itertools
from django.db.models import Q
#Promotion API
from notifications.models import Notification
from rest_framework.permissions import*
from datetime import datetime,time
from customer.models import *

class delete_all_notification(APIView   ):
    serializer_class = deletenotificationSerializer
    queryset = Notification.objects.all()
    def delete(self, request, format=None):
        user=self.request.user
        print("USSSEEERRRR",user.pk)
        notification_del=Notification.objects.filter(recipient=user)
        for notify in notification_del:
            notify.delete()
        
        #snippet = self.get_object(pk)
        #snippet.delete()
        return Response("content deleted")


#Promotion API
class delete_notification(generics.DestroyAPIView):
    serializer_class = deletenotificationSerializer
    queryset = Notification.objects.all()
#     def get_serializer_context(self):
#         print(self.request.user)
#         return {"upcell":self.kwargs['pk'],}


class customer_accept_upcell(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = upcellacceptSerializer
    queryset = UpcellAppointment.objects.all()
    def get_serializer_context(self):
        print(self.request.user)
        return {"upcell":self.kwargs['pk'],}

class acceptupcell(generics.ListAPIView):
    serializer_class = upcellacceptSerializer
    def get_queryset(self):
        appointmentid=self.kwargs['appointment_id']
        #appointmentid= self.request.query_params.get('appointment_id')
        print("appointment_id", appointmentid)
        upcell_detail=UpcellAppointment.objects.filter(appointment=appointmentid)
        return upcell_detail


#Member add promotion
class member_update_delete_promotion(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = promotionaddSerializer
    def get_queryset(self):
        user=self.request.user
        querySet = Promotions.objects.filter(member= user)
        return querySet  

#member edit delete promotion
class member_add_promotion(generics.CreateAPIView):
    serializer_class = promotionaddSerializer
    querySet = Promotions.objects.all()
    

#All promotions for Member   
class member_all_promotions(generics.ListAPIView):
    serializer_class = promotionallSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields =['id', 'discount', 'description','from_date','to_date','coupon_code','price','model_id__model_name', "company__company_name" ,]
    def get_queryset(self):
        user=self.request.user
        today = datetime.now().date()
        today_start = datetime.combine(today, time())
        querySet = Promotions.objects.filter(~Q(to_date__lt=today_start),member= user)
        return querySet
    
#All promotions for Customer   
class customer_all_promotions(generics.ListAPIView):
    serializer_class = promotionallSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields =['id', 'discount', 'description','from_date','to_date','coupon_code','price','model_id__model_name', "company__company_name" ,]
    def get_queryset(self):
        user = self.request.user
        lead_u=lead_user.objects.get(user=user)
        
        lead_obj=Lead.objects.get(pk=lead_u.customer.pk)
        
        group=Group.objects.get(user=user)
        groupname=group.name
        #var3=lead_user.objects.get(user=user)   
        #var1 = Lead.objects.get(pk=var3.customer.pk)
        address= UserProfile.objects.get(user=lead_obj.member)
        print("-------------address",address.shop_name)    
        obj=[]
        veh=Lead_Vehicle.objects.filter(lead=lead_obj) 
        today=datetime.today()
        msg=None
        print(groupname)
        if groupname=="Customer" or groupname=="E_Customer":
            print("IN CUSTOMER or E_customer")
            if veh:
    
                for vehicle in veh:
                    if groupname != "All":
                         
                        var2=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to="Customer")              
                        obj.append(list(itertools.chain(var2)))
                    try:
                        allpromo=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to="All")
                        obj.append(list(itertools.chain(allpromo)))
                    
                    except Exception as e:
                        pass
                        print("no promotion for ALL")
                   
            com=Company.objects.get(company_name='All')
            var3=Promotions.objects.filter(company=com,member=lead_obj.member,to_date__gte = today.date())
        
            #for pv in var3:
            obj.append(list(itertools.chain(var3)))
            cnt=0
            k=[]
            for r in obj:
               if len(r)!=0:
                for s in r:
                    print (s)
                    k.append(s)
            print("KKKKKKKKKKKKKKKK",k)
            return k
        
        if groupname=="Lead":
            print("IN LEAD")
            if veh:
    
                for vehicle in veh:
                    if groupname != "All": 
                        var2=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to="Lead")              
                        obj.append(list(itertools.chain(var2)))
                    try:
                        allpromo=Promotions.objects.filter(member=lead_obj.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date(),display_to="All")
                        obj.append(list(itertools.chain(allpromo)))
                    
                    except Exception as e:
                        pass
                        print("no promotion for ALL")
                   
            com=Company.objects.get(company_name='All')
            var3=Promotions.objects.filter(company=com,member=lead_obj.member,to_date__gte = today.date())
        
            #for pv in var3:
            obj.append(list(itertools.chain(var3)))
            cnt=0
            k=[]
            for r in obj:
               if len(r)!=0:
                for s in r:
                    print (s)
                    k.append(s)
            return k

#Top 5 promotions for Customer   
class customer_5_promotions(generics.ListAPIView):
    serializer_class = promotionallSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields =['id', 'discount', 'description','from_date','to_date','coupon_code','price','model_id__model_name', "company__company_name" ,]
    def get_queryset(self):
        user=self.request.user
        var3=lead_user.objects.get(user=user)
        var1 = Lead.objects.get(pk=var3.customer.pk)
        veh=Lead_Vehicle.objects.filter(lead=var1)
        result=[]
        if veh:
            for vehicle in veh: 
                today=datetime.today()
                querySet=Promotions.objects.filter(member=var1.member,company=vehicle.company,model_id=vehicle.model,make_year=vehicle.makeyear, to_date__gte = today.date()).order_by('-id')[0:8]
                print(querySet)
                result.append(list(itertools.chain(querySet)))
        com=Company.objects.get(company_name='All')
        var5=Promotions.objects.filter(company=com,member=var1.member)
        result.append(list(itertools.chain(var5)))        
        cnt=0
        k=[]
        for r in result:
           if len(r)!=0:
            for s in r:
                print (s)
                k.append(s)
        return k
# Service Request API

#Member all Service Request
class member_all_request(generics.ListAPIView):
    serializer_class = CustomerRequestSerializer
    def get_queryset(self):
        user=self.request.user
        today=datetime.today()
        status_pending=Status.objects.get(status="Pending")
        var1 = Lead.objects.filter(member=user)
        querySet = customer_request.objects.filter(customer__in=var1,emergency_status=None,date__gte = today.date(),status=status_pending)

        return querySet

class search_promotion(generics.ListAPIView):
    serializer_class = promotionallSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields =["Service_id__service_type",'id', 'discount', 'description','from_date','to_date','coupon_code','price','model_id__model_name', "company__company_name" ,'make_year__make_year']
    def get_queryset(self):
         user=self.request.user
         querySet = Promotions.objects.filter(member=user)
         return querySet
    
#customer all Service Request
class customer_all_request(generics.ListAPIView):
    serializer_class = CustomerRequestSerializer
    def get_queryset(self):
        today=datetime.today()
        print(today)
        #self.object.date_request = todays.date()
        user=self.request.user
        customer=lead_user.objects.get(user=user)
        querySet = customer_request.objects.filter(emergency_status=None,customer=customer.customer.pk,date__gte= today.date())
        print(querySet)
       # print(date_request)
        return querySet

class customer_accident_request(generics.CreateAPIView):
    serializer_class = CustomerAccidentRequestSerializer
    queryset = Accident_Request.objects.all()
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,}

class customer_create_outsource_history(generics.CreateAPIView):
    serializer_class = CustomerOutsourceHistorySerializer
    queryset = Customer_Outsource_History.objects.all()
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,}  

class customer_outsource_history_list(generics.ListAPIView):
    serializer_class = CustomerOutsourceListSerializer
    def get_queryset(self):
        today=datetime.today()
        print(today)
        #self.object.date_request = todays.date()
        user=self.request.user
        customer=lead_user.objects.get(user=user)
        querySet = Customer_Outsource_History.objects.filter(customer=customer.customer.pk)
        print(querySet)
       # print(date_request)
        return querySet
    
class customer_add_request(generics.CreateAPIView):
    serializer_class = CustomerAddRequestSerializer
    queryset = customer_request.objects.all()
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,}

    
class customer_update_delete_request(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerUpdateRequestSerializer
    def get_queryset(self):
        user=self.request.user
        customer=lead_user.objects.get(user=user)
        querySet = customer_request.objects.filter(customer=customer.customer.pk)
        return querySet
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,"pk":self.kwargs['pk']}
    



class customer_add_requestwithpromotion(generics.CreateAPIView):
    queryset = customer_request.objects.all()
    serializer_class = CustomerAddRequestpromotionSerializer
    def get_serializer_context(self):
        return {"request":self.request,"Promotions_pk":self.kwargs['Promotions_pk']}
    
class customer_update_delete_requestwithpromotion(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerUpdateRequestpromotionSerializer
    def get_queryset(self):
        user=self.request.user
        customer=lead_user.objects.get(user=user)
        querySet = customer_request.objects.filter(customer=customer.customer.pk)
        return querySet
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,"pk":self.kwargs['pk']}

class customer_change_status(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerchangestatusSerializer
    def get_queryset(self):
        user=self.request.user
        customer=lead_user.objects.get(user=user)
        querySet = customer_request.objects.filter(customer=customer.customer.pk)
        return querySet
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,"pk":self.kwargs['pk']}



# Appointment API

#Member all Appointment
class member_all_appointment(generics.ListAPIView):
    serializer_class = AppointmentAllSerializer
    def get_queryset(self):
        user=self.request.user
        status=Status.objects.get(status="Job Completed")
        profile=UserProfile.objects.get(user=user)
        querySet = MemberAppointment.objects.filter(~Q(status=status),member=profile)
        return querySet

#Customer all Appointment
class customer_all_appointment(generics.ListAPIView):
    serializer_class = AppointmentAllSerializer
    def get_queryset(self):
        user=self.request.user
        customer=lead_user.objects.get(user=user)
        querySet = MemberAppointment.objects.filter(customer=customer.customer)
        return querySet

#Member Add Appointment  
class member_add_appointment(generics.CreateAPIView):
    serializer_class = AppointmentAddSerializer
    queryset = MemberAppointment.objects.all()

#Member Update Appointment   
class member_update_delete_appointment(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentAddSerializer
    def get_queryset(self):
        user=self.request.user
        profile=UserProfile.objects.get(user=user)
        querySet = MemberAppointment.objects.filter(member=profile)
        return querySet

class customer_appointment(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    def get_queryset(self):
        user=self.request.user
        pk = self.kwargs['pk']
        querySet = MemberAppointment.objects.filter(pk=pk)
        return querySet

    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,"pk":self.kwargs['pk']}


class cust_appointment_history(generics.ListAPIView):
    serializer_class = appointment_historySerializer
    #filter_backends = (filters.SearchFilter,)
    #search_fields =['id', 'discount', 'description','from_date','to_date','coupon_code','price','model_id__model_name', "company__company_name" ,]
    def get_queryset(self):
        status1=Status.objects.get(status="Job Completed")
        user = self.request.user
        print("user", user)
        group=Group.objects.get(user=user)
        customer=lead_user.objects.get(user=user)
        cust = Lead.objects.get(pk=customer.customer.pk)
        print("cust", cust)
        dict1=[]
        var3= MemberAppointment.objects.filter(customer=customer.customer,status=status1)
        
        return var3

class cust_upcell_history(generics.ListAPIView):
    serializer_class = Upcell_historySerializer
    #filter_backends = (filters.SearchFilter,)
    #search_fields =['id', 'discount', 'description','from_date','to_date','coupon_code','price','model_id__model_name', "company__company_name" ,]
    def get_queryset(self):
        appointmentid=company=self.kwargs.get('appointment_pk')
        upcell=UpcellAppointment.objects.filter(appointment=appointmentid,accept=1)

        return upcell





#Feedback

#All Feedback of Member
class member_all_feedback(generics.ListAPIView):
    serializer_class = FeedbackAllSerializer
    def get_queryset(self):
        user=self.request.user
        customer=Lead.objects.filter(member=user)
        queryset=Custfeedback.objects.filter(customer__in=customer)
        print(queryset)
        return queryset

#view Feedback    
class member_view_feedback(generics.ListAPIView):
    queryset = Custfeedquestion.objects.all()
    serializer_class = FeedbackViewSerializer
    def get_queryset(self):
        
        user=self.request.user
        customer=Lead.objects.filter(member=user)
        cust_feedback=Custfeedback.objects.filter(pk=self.kwargs.get('Custfeedback_pk'), customer__in=customer)
        return self.queryset.filter(feedback_cust=cust_feedback)
        

#Customer create Feedback       
class customer_create_feedback(generics.CreateAPIView):
    serializer_class = FeedbackCreateSerializer
    queryset = Feedback_Star.objects.all()
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request}
#Master data

#Get All Company
class get_all_CarCompany(generics.ListAPIView):
    serializer_class = AllCarCompanySerializer
    queryset = Company.objects.all().exclude(company_name="All")

#Get models according to Car company
class get_all_CarModel(generics.ListAPIView):
    queryset = Company_Model.objects.all()
    serializer_class = AllCarModelSerializer
    def get_queryset(self):
        return self.queryset.filter(company=self.kwargs.get('Company_pk'))

#Get makeyear according to Car models
class get_all_MakeYear(generics.ListAPIView):
    queryset = MakeYear.objects.all()
    serializer_class = AllMakeYearSerializer
    def get_queryset(self):
        return self.queryset.filter(model=self.kwargs.get('Company_model_pk'))

#get all Service type   
class get_all_ServiceType(generics.ListAPIView):
    serializer_class = AllServiceTypeSerializer
    queryset = Service.objects.all()

#view make year
class view_make_year(generics.ListAPIView):
    serializer_class = view_makeyear_Serializer
    queryset=Make_Year1.objects.all().exclude(make_year="All")

#Registration

#Customer Update Profile
class customer_update_profile(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerUpdateProfileSerializer
    def get_queryset(self):
        user=self.request.user
        customer=lead_user.objects.get(user=user)
        querySet = Lead.objects.filter(pk=customer.customer.pk)
        return querySet
    
#Member Update Profile
class member_update_profile(generics.RetrieveUpdateAPIView):
    serializer_class = MemberUpdateProfileSerializer
    def get_queryset(self):
        user=self.request.user
        #customer=lead_user.objects.get(user=user)
        querySet = UserProfile.objects.filter(user= user)
        return querySet

class get_cust_detail(generics.ListAPIView):
    serializer_class = CustomerDetailSerializer
    def get_queryset(self):
        user=self.request.user
        customer=lead_user.objects.get(user=user)
        querySet = Lead.objects.filter(pk=customer.customer.id)
        return querySet


class member_view_businesscard(generics.RetrieveAPIView):
    serializer_class = member_view_businesscard_Serializer
    def get_queryset(self):
      user=self.request.user
      print(user)
      queryset= UserProfile.objects.filter(user=user)
      print(queryset)
      return queryset

class customer_view_businesscard(generics.ListAPIView):
    serializer_class = member_view_businesscard_Serializer
    def get_queryset(self):
        user=self.request.user   
        lead=Lead.objects.get(email=user.email)
        queryset= UserProfile.objects.filter(user=lead.member.pk)
        return queryset


    
#CRM

#Number of User
class UserCount1View(generics.ListAPIView):
    renderer_classes = (JSONRenderer, )
    #serializer_class = UsercountSerializer

    def get(self, request, format=None):
        user_count = User.objects.filter(is_active=True).count()
        #print("&&&&&&&&&&&&&&&&&&&", user_count)
        content = {'user_count': user_count}
        return Response(content)
    
class UserCountView(generics.ListAPIView):
    #renderer_classes = (JSONRenderer, )
    serializer_class = UsercountSerializer

    def get_queryset(self):
        user_count = User.objects.filter(is_active=True).count()
        #user_count = User.objects.annotate(user_count=Count('username')).count()
        print("&&&&&&&&&&&&&&&&&&&", user_count)
        content = {'user_count': user_count}
        return str(user_count)

#Number of Leads    
class number_of_leads(generics.ListAPIView):
    renderer_classes = (JSONRenderer, )
    #serializer_class = UsercountSerializer

    def get(self, request, format=None):
        user=self.request.user
        s=Status.objects.get(status="Lead")
        lead_count = Lead.objects.filter(member=user,status=s).count()
        content = {'lead_count': lead_count}
        return Response(content)
    
#Number of Customer
class number_of_customer(generics.ListAPIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        user=self.request.user
        s=Status.objects.get(status="Customer")
        Customer_count = Lead.objects.filter(member=user,status=s).count()
        content = {'Customer_count': Customer_count}
        return Response(content)

#Number of Todays Appointment    
class number_of_today_appointment(generics.ListAPIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        user=self.request.user
        profile=UserProfile.objects.get(user=user)
        today=datetime.today()
        Appointment_count = MemberAppointment.objects.filter(member=profile, date=today).count()
        content = {'Appointment_count': Appointment_count}
        return Response(content)

#Number of Service Request
class number_of_request(generics.ListAPIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        user=self.request.user
        today=datetime.today()
        status_pending=Status.objects.get(status="Pending")
        var1 = Lead.objects.filter(member=user)
        request_count=customer_request.objects.filter(customer__in=var1,emergency_status=None,date__gte = today.date(),status=status_pending).count()
        content = {'request_count': request_count}
        return Response(content)

#Number of today's loggedin users
class today_loggedin_customer(generics.ListAPIView):
    serializer_class = TodayLoggedinUserSerializer
    def get_queryset(self):
        user=self.request.user
        s=Status.objects.get(status="Customer")
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
                today=datetime.today()
                if y == today.date():
                    cust_arr.append(cust)
        return cust_arr
    
#customer add vehicles
#Customer Add Vehical    
class customer_add_vehicles(generics.CreateAPIView):
    serializer_class = customer_add_vehicles_Serializer
    queryset = Lead_Vehicle.objects.all()

    def get_serializer_context(self):
        print(self.request.user)
        return {"request":self.request,}

#Customer View All_Vehical

class customer_view_all_vehicle(generics.ListAPIView):
    serializer_class = customer_viewall_vehicle_Serializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'vehicle_no','reg_expiry_date','vin_no','model__model_name','company__company_name')
    def get_queryset(self):
         
        user=self.request.user
        lead = Lead.objects.filter(email = user)
        queryset = Lead_Vehicle.objects.filter(lead__in = lead)
        return queryset
#Customer Edit Vehical

class customer_edit_vehicle(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = customer_add_vehicles_Serializer
    def get_queryset(self):
        user=self.request.user
        lead = Lead.objects.filter(email = user)
        print("customer:",lead)
        queryset = Lead_Vehicle.objects.filter(lead__in = lead)
        return queryset



#view make year
class view_make_year(generics.ListAPIView):
    serializer_class = view_makeyear_Serializer
    queryset=Make_Year1.objects.all().exclude(make_year="All")


#send business card
class member_send_businesscard(generics.ListAPIView):
    serializer_class = member_send_businesscard_Serializer
    def get_queryset(self):
        user=self.request.user
        email=self.kwargs['email']
        name=self.kwargs["name"]        
        #print("name is", name)          
        today=datetime.today()
        ebc=EBC(email=email,name=name,ebctime=today.date())
        ebc.save()
       # lead=Lead.objects.filter(email=email,member=user)
        #print("-------",lead)     
        if ebc is not None:
            ws_member_send_businesscard__mail.delay(str(email),str(user.email),str(name))
            print("delay has been called")
            return ebc
        else:
            return "Please enter valid email id"

class customer_send_businesscard(generics.CreateAPIView):
    serializer_class = member_send_businesscard_Serializer
    queryset=None





def notifyMessage(request):
    user= request.user
    message = "hello this from local ip, message for andriod device"
    try: 
        device = FCMDevice.objects.all()
        device.send_message("Local server", "hello this from local ip, message for andriod device")
        print ("----------------------------------------" , device)
        print("message sent")
        print ("end of gcm")
        
    except Exception as e:
        print("exception------------------------------------------",e.message)
        
    return HttpResponseRedirect('/api/thanks/')
    
def thanks(request):
     return render(request, 'thanks.html')


class customer_add_image(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = customer_addimage_Serializer
    def get_queryset(self):
        user=self.request.user
        lead = Lead.objects.filter(email = user)
        
        queryset = Lead_Vehicle.objects.filter(lead__in = lead)
        return queryset


class customer_emer_request(generics.ListAPIView):
    serializer_class = CustomerRequestSerializer
    def get_queryset(self):
        today=datetime.today()
        print("today today",today)
        #self.object.date_request = todays.date()
        user=self.request.user
        print("USER", user)
        customer=lead_user.objects.get(user=user)
        print("customer customer",customer.customer.pk)
        querySet = customer_request.objects.filter(customer=customer.customer.pk,date_request__gte= today.date(),emergency_status=1)
        print("querySet querySet querySet",querySet)
       # print(date_request)
        return querySet
    
class customer_add_emer_request(generics.CreateAPIView):
    serializer_class = CustomerEmerAddRequestSerializer
    queryset = customer_request.objects.all()
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,}

class member_postal_code(generics.ListAPIView):
    serializer_class = MemberpostalcodeSerializer   
    def get_queryset(self):
         postal_code=self.kwargs["postal_code"] 
         user_pro=UserProfile.objects.filter(postal_code=postal_code)
        # print("user profile",user_pro)
         return user_pro
class registration_member(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = registration_member_Serializer
    queryset=UserProfile.objects.all()
      
    
class lead_list(generics.ListAPIView):
    serializer_class = LeadListSerializer
    def get_queryset(self):
      
        user=self.request.user
       # group=Group.objects.get(user=request.user)
        status=Status.objects.get(status="Lead")
        querySet = Lead.objects.filter(status=status,member=user)
        print(querySet)
       # print(date_request)
        return querySet    
    
    
class add_lead(generics.CreateAPIView):
    serializer_class = AddLeadSerializer
    def get_queryset(self):
        queryset=Lead.objects.all()
        return queryset  
    
#class member_edit_lead(generics.RetrieveUpdateAPIView):
#    serializer_class = AddLeadSerializer
#    def get_queryset(self):
#        user=self.request.user
#        queryset = Lead.objects.filter(member= user)
#        return queryset

class member_edit_lead(generics.RetrieveUpdateAPIView):
    serializer_class = EditLeadSerializer
    def get_queryset(self):
        user=self.request.user
        print("user in edit_lead view----",user)
        queryset = Lead.objects.filter(member= user)
        return queryset
    def get_serializer_context(self):
        print self.request.user
        return {"request":self.request,"pk":self.kwargs['pk']}  
      

class customer_list(generics.ListAPIView):
    serializer_class = customerSerializer

    def get_queryset(self):
        user=self.request.user
        status1=Status.objects.filter(status="Customer" )
        status2=Status.objects.filter(status="Deactivate" )
    
        list1=Lead.objects.filter(member=user)
        list=list1.filter(Q(status=status1) | Q(status=status2))  
        return list

class top_5_customer(generics.ListAPIView):
    serializer_class = customerSerializer

    def get_queryset(self):
        customer = Lead.objects.filter(member=self.request.user)
        list2=[]
        for custt in customer:
            request1=customer_request.objects.filter(customer=custt)
            list2.append(request1)
        cnt=0
        cust_request_list=[]
        for cust_req in list2:
           if len(cust_req)!=0:
            for s in cust_req:
                cust_request_list.append(s)
        cust_req_obj=customer_request.objects.filter(id__in=[cust_req.id for cust_req in cust_request_list]).order_by('-customer')
        groupnames = set()
        for cust in cust_req_obj:
            for item in cust_req_obj:
              if cust.customer not in groupnames:
        
                groupnames.add(cust.customer)
            
        return groupnames

class get_member_detail(generics.ListAPIView):
    serializer_class = MemberDetailSerializer
    def get_queryset(self):
        user=self.request.user
        member_id=UserProfile.objects.filter(user=user)
        return member_id

class customer_accident_request_list(generics.ListAPIView):
    serializer_class = CustomerAccidentRequestSerializer
    #queryset = Accident_Request.objects.all()
    def get_queryset(self):
        user=self.request.user
        customer=lead_user.objects.get(user=user)
        querySet = Accident_Request.objects.filter(customer=customer.customer.pk)
        print(querySet)
       # print(date_request)
        return querySet
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,}

class delete_customer_S(generics.ListAPIView):
    serializer_class = delete_customer_Serializer2

    def get_queryset(self):
            
            pk = self.kwargs['pk']
            lead_obj = Lead.objects.get(pk=pk)
            
            print(" customer delete---",lead_obj)
            status=Status.objects.get(status='Inacitve')
            lead_obj.status = status
            lead_obj.save()
            lead_u = lead_user.objects.filter(customer=lead_obj)
            print("lead_user----",lead_u)

            lead_u.is_active=False
            list1=[]
            list1.append(lead_obj)
            print list1
            return list1

class add_customer(generics.CreateAPIView):
    #permission_classes = (AllowAny,)
    serializer_class = AddCustomerSerializer
    queryset=Lead.objects.all()
    
class edit_customer(generics.RetrieveUpdateAPIView):
    serializer_class = AddCustomerSerializer
    def get_queryset(self):
        user=self.request.user
        queryset = Lead.objects.filter(member= user)
        return queryset      

class member_add_vehicles(generics.CreateAPIView):
    serializer_class = customer_vehicles_Serializer
    queryset=Lead_Vehicle.objects.all()
        
    def get_serializer_context(self):
        print("-------------------",self.kwargs['lead_id'])
        return {"request":self.request,"lead_id":self.kwargs['lead_id']}

class member_edit_vehicles(generics.RetrieveUpdateAPIView):
    serializer_class = customer_vehicles_Serializer
    def get_queryset(self):
        queryset=Lead_Vehicle.objects.all()
        return queryset      
    
def get_serializer_context(self):
        print self.request.user
        return {"request":self.request,"pk":self.kwargs['pk']}    
      
    
class member_list_vehicles(generics.ListAPIView):
    serializer_class = VehicleListSerializer
    def get_queryset(self):
        Lead_pk = self.kwargs['Lead_pk']
        #print("Lead_pk---",Lead_pk)
        Lead_obj= Lead.objects.get(id=Lead_pk)
       # print("Lead_obj---",Lead_obj)
        today=datetime.today()
        user=self.request.user
        querySet = Lead_Vehicle.objects.filter(lead_id=Lead_obj)
        return querySet 

class customer_deregister(generics.RetrieveUpdateAPIView):
    serializer_class = customerDeregisterSerializer
    def get_queryset(self):
        pk=self.kwargs["pk"]
        querySet = Lead.objects.filter(pk=pk)
        print("view",querySet)
        return querySet
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,"pk":self.kwargs['pk']}    

class customer_history(generics.ListAPIView): 
    serializer_class = customer_historySerializer
    def get_queryset(self):
        appointment_id = self.kwargs['appointment_id']
        print("appointment_id-----",appointment_id)
        up = UpcellAppointment.objects.filter(appointment=appointment_id)
        print("up---",up)
        up1 = []
        for f in up:
                 
            q = UpcellAppointmentSubService.objects.filter(upcellappointment=f)
            for k in q:
                        up1.append (k)
                        print ("up1 : ",set(up1))
        return up1   
    
                   
class CustomerAppointmentList(generics.ListAPIView):
    serializer_class = CustomerAppointmentListSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        print("pk-----",pk)
        status=Status.objects.get(status='Job Completed')
        appointment_obj = MemberAppointment.objects.filter(customer=pk,status=status)
        print(" customer in history---",appointment_obj)
        return appointment_obj
    
class member_potentail_lead(generics.CreateAPIView):
    serializer_class = PotentialleadSerializer
    queryset = EBC.objects.all()
    
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,}
    
class Ebc_history(generics.ListAPIView):
    serializer_class = PotentialleadSerializer
    def get_queryset(self):
        user=self.request.user
        queryset=EBC.objects.filter(send_user=user).order_by('-ebctime')
        return queryset
    
class feedback_list(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    def get_queryset(self):
        user=self.request.user
        queryset=Feedback_Star.objects.filter(member=user).order_by('-feedback_date')
        return queryset

#member app starts

class reschedule_request(generics.RetrieveUpdateAPIView):
    serializer_class = reschedule_request_Serializer
    queryset = customer_request.objects.all()
    def get_serializer_context(self):
        #print self.request.user
        return {"request":self.request,"pk":self.kwargs['pk']} 


class regenerate_login_credentials(generics.RetrieveUpdateAPIView):
    serializer_class = regenerate_login_credentials_Serializer
    def get_queryset(self):
      #lead_id = self.kwargs['pk']
      #queryset=Lead.objects.get(pk=lead_id)
      queryset=Lead.objects.all()
 
      return queryset  
  
    def get_serializer_context(self):

        return {"request":self.request,"pk":self.kwargs['pk']}


class Schedule_Appointment(generics.ListAPIView):
    serializer_class = Schedule_Appointment_Serializers
    
    def get_queryset(self):
        request_id = self.kwargs['pk']

        Req_obj= customer_request.objects.get(id=request_id)

        today=datetime.today()
        user=self.request.user
        lead_obj = Lead.objects.get(id = Req_obj.customer.pk)

        User_Profile_obj = UserProfile.objects.get(user=user)

        status= Status.objects.get(status="Scheduled")

        
        
    #for i in User_Profile_obj:
        #MemberAppointment.objects.create(
        member_obj = MemberAppointment(   request = Req_obj,
                                  customer = lead_obj,
                                  member = User_Profile_obj,
                                  date_appointment = today.date(),
                                  status = status,
                                  date=Req_obj.date,
                                  from_time=Req_obj.from_time,
                                  to_time=Req_obj.to_time,
                                                          )
    
        member_obj.save()
        statusOfRequest= Status.objects.get(status="Scheduled")

        Req_obj.status = statusOfRequest
        Req_obj.save()
        return MemberAppointment.objects.filter(request=request_id)


class external_customer_registration(generics.CreateAPIView):
    serializer_class = external_customer_registrationSerializer
    queryset=lead_user.objects.all()

class promotion_re_open(generics.CreateAPIView):
    serializer_class = promotionReopenSerializer
    def get_queryset(self):
        user=self.request.user
        querySet = Promotions.objects.filter(member= user)
        return querySet  
    def get_serializer_context(self):
        return {"request":self.request,"pk":self.kwargs['pk']}
    

class upload_customer_gallery(generics.ListCreateAPIView):
    serializer_class = crm_customer_gallery_serializer
    def get_queryset(self):
        user=self.request.user
        lead = CrmCustomerGallery.objects.filter(customer = user.pk)
        return lead
        
        
class list_customer_gallery(generics.ListAPIView):
    serializer_class = list_customer_gallery_serializer
    def get_queryset(self):
        user=self.request.user
        lead_obj = Lead.objects.get(email = user)
        type = self.kwargs["type"]
        lead_gallery_obj = CrmCustomerGallery.objects.filter(customer = lead_obj,type = type)
	return lead_gallery_obj
        

class list_expence_type(generics.ListAPIView):
    serializer_class = list_expence_type_serializer
    queryset = ExpenseType.objects.all().order_by('expense_type')
    
    
class expence_details(generics.CreateAPIView):
    serializer_class = expence_subdetails_serializer
    #queryset = ExpenseSubdetails.objects.all()
    queryset = ExpenseDetails.objects.all()

class list_of_expence_details(generics.ListAPIView):
    serializer_class = list_of_expence_details_serializer
    def get_queryset(self):
        user=self.request.user
        lead_obj = Lead.objects.get(email = user)
        expense_details = ExpenseDetails.objects.filter(customer = lead_obj)
#         list1 = []
#         for expense in expense_details:
#             ExpenseSubdetails_obj = ExpenseSubdetails.objects.get(expense_details = expense)
#             list1.append(ExpenseSubdetails_obj)
        return expense_details


class search_member_postal_code(viewsets.ModelViewSet):
    serializer_class = MemberpostalcodeSerializer   
    def get_queryset(self):
         user=self.request.user
         today=datetime.today()
            
         postal_code=self.kwargs["postal_code"] 
         list1 = []
         user_pro=UserProfile.objects.filter(postal_code=postal_code)
         if len(user_pro)>0:
              obj=SearchMember.objects.create(email=user.email,status='Member available',postal_code=postal_code,date=today.date())
              
         else:
             obj=SearchMember.objects.create(email=user.email,status='Member not available',postal_code=postal_code,date=today.date())
             #obj.save()
         return user_pro