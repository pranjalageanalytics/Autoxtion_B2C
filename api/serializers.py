from rest_framework import serializers
from  promotion.models import *
from CRM.models import *
from .models import *
from rest_framework import generics
from customer.models import *
from Appointment.models import *
from Feedback.models import *
import re
from Registration.tasks import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
import django_filters
from datetime import datetime
from django.core.validators import RegexValidator
from push_notifications.models import GCMDevice, APNSDevice
from django.contrib.auth.models import  Group
UserModel = get_user_model()
from notifications.signals import notify
from notifications.models import Notification
import StringIO
from PIL import Image
import random
import string
from django.shortcuts import render,get_object_or_404
import stripe
from Appointment.tasks import *
from CRM.tasks import *
#from rest_framework.exceptions import ValidationError
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _


class PostalCodeValidator(RegexValidator):
    regex = r'^[0-9]+$'
    message = 'Invalid Postal Code' 


class deletenotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification

#Promotion Serializer

class sub_serviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubServiceType
        fields = ('service_type_name', )

class upcellacceptSerializer(serializers.ModelSerializer):
    sub_service=sub_serviceSerializer(many=True)
    service = serializers.CharField(source='service.service_type')
    
    class Meta:
        model = UpcellAppointment
        fields=('id','accept','service','image','sub_service','description','amount')
        
    def update(self,instance, validated_data):
        print("########################################3",validated_data['accept'])
        
        upcell = self.context.get("upcell")
        upcell_accept= UpcellAppointment.objects.get(pk=upcell)
        upcell_accept.accept=validated_data['accept']
        upcell_accept.save()
        cust_upcell=UpcellAppointment.objects.get(pk=upcell, accept=1)
        appointment_id=MemberAppointment.objects.get(pk=cust_upcell.appointment.pk)
        if cust_upcell:
             appointment_id.upcell_status="UpSell Accepted"
             appointment_id.save()
        return upcell_accept

        
class promotionallSerializer(serializers.ModelSerializer):
    make_year = serializers.CharField(source='make_year.make_year')
    model = serializers.CharField(source='model_id.model_name')
    company = serializers.CharField(source='company.company_name')
    #series = serializers.CharField(source='series.series')
    #engine = serializers.CharField(source='engine.engine')
    #car_variant = serializers.CharField(source='car_variant.body_type')
    Service = serializers.CharField(source='Service_id.service_type')
    
    class Meta:
        model = Promotions
        fields=('id', 'discount', 'description', 'from_date', 'to_date','coupon_code','price','image','company','model','make_year','member','Service','total_amount')

class promotionsearchSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Promotions
        

class promotionaddSerializer(serializers.ModelSerializer):

    options=(('All','All'),('Lead','Lead'),('Customer','Customer'))
    display_to=serializers.ChoiceField(required=True,choices=options)
    from_date = serializers.DateField(format="%d-%m-%Y", input_formats=None)
    to_date = serializers.DateField(format="%d-%m-%Y", input_formats=None)
       
    class Meta:
        model = Promotions
        fields=('id', 'discount', 'description', 'from_date', 'to_date','coupon_code','price','image','company','model_id','make_year','member','Service_id','total_amount','display_to')
        
#Customer Serializer

class CustomerAccidentRequestSerializer(serializers.ModelSerializer):
    phone_no= serializers.RegexField(regex=r'^[0-9]+$', error_messages= {"invalid" : 'Please enter a valid number'})
    class Meta:
        model=Accident_Request
        fields=('image1','image2','car_detail','location','phone_no')
        
    def create(self, validated_data):
        today=datetime.today()
        request=self.context.get('request')
        customer= lead_user.objects.get(user=request.user)
        accident_req_obj= Accident_Request(
                                           image1= validated_data['image1'],
                                           image2= validated_data['image2'],
                                           car_detail= validated_data['car_detail'],
                                           location= validated_data['location'],
                                           phone_no= validated_data['phone_no'],
                                           customer=customer.customer,
                                           status = Status.objects.get(status="Pending"),
                                           date_request = today.date(),
                                           )
        accident_req_obj.save()
        return accident_req_obj
    
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        phn=data['phone_no']
        mylist = []
        mylist.append(phn)
        phn_1=mylist[0][0]
        print("----------phn_1-----------",str(phn_1))
        
        if phn_1=='0':
            print("___________IN 0000__________")
            if len(phn)> 10 :
                raise serializers.ValidationError("Phone Number cannot be greater 10 digits")
            if len(phn)< 10 :
                raise serializers.ValidationError("Phone Number cannot be less 10 digits")
        if phn_1!='0':
            print("___________IN 1111__________")
            if len(phn)> 9 :
                raise serializers.ValidationError("Phone Number cannot be greater 9 digits")
            if len(phn)< 9 :
                raise serializers.ValidationError("Phone Number cannot be less 9 digits")
    
        return data

class CustomerOutsourceHistorySerializer(serializers.ModelSerializer):
    phone_no= serializers.RegexField(regex=r'^[0-9]+$', error_messages= {"invalid" : 'Please enter a valid number'})
    class Meta:
        model=Customer_Outsource_History
        fields=('member_name','shop_name','date_request','description','price','phone_no')
        
    def create(self, validated_data):
        #today=datetime.today()
        request=self.context.get('request')
        customer= lead_user.objects.get(user=request.user)
        customer_outsource_obj= Customer_Outsource_History(
                                           member_name= validated_data['member_name'],
                                           shop_name= validated_data['shop_name'],
                                           date_request= validated_data['date_request'],
                                           description= validated_data['description'],
                                           phone_no= validated_data['phone_no'],
                                           price= validated_data['price'],
                                           customer=customer.customer,
                                           
                                           )
        customer_outsource_obj.save()
        return customer_outsource_obj
    
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        phn=data['phone_no']
        mylist = []
        mylist.append(phn)
        phn_1=mylist[0][0]
        print("----------phn_1-----------",str(phn_1))
        
        if phn_1=='0':
            print("___________IN 0000__________")
            if len(phn)> 10 :
                raise serializers.ValidationError("Phone Number cannot be greater 10 digits")
            if len(phn)< 10 :
                raise serializers.ValidationError("Phone Number cannot be less 10 digits")
        if phn_1!='0':
            print("___________IN 1111__________")
            if len(phn)> 9 :
                raise serializers.ValidationError("Phone Number cannot be greater 9 digits")
            if len(phn)< 9 :
                raise serializers.ValidationError("Phone Number cannot be less 9 digits")
    
        return data

class CustomerOutsourceListSerializer(serializers.ModelSerializer):
    #phone_no= serializers.RegexField(regex=r'^[0-9]+$', error_messages= {"invalid" : 'Please enter a valid number'})
    class Meta:
        model=Customer_Outsource_History
        fields=('member_name','shop_name','date_request','description','price','phone_no')
      
class CustomerRequestSerializer(serializers.ModelSerializer):
    Service = serializers.CharField(source='service_type.service_type')
    customer = serializers.CharField(source='customer.name')
    promotion = serializers.CharField(source='promotion.coupon_code')
    status = serializers.CharField(source='status.status')
    class Meta:
        model = customer_request
        fields=('id','description','Service','customer','promotion','date','from_time','to_time','status','image')

class CustomerAddRequestSerializer(serializers.ModelSerializer):
    #from_time = serializers.TimeField(format="%H:%M %p")
    #to_time = serializers.TimeField(format="%H:%M %p")
    date = serializers.DateField(format="%d-%m-%Y", input_formats=None)
    class Meta:
        model = customer_request
        fields=('id','service_type','description','image','date','from_time','to_time')
        
     
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['service_type'] is None :
            raise serializers.ValidationError("Service type Field cannot be empty")
        return data
    def create(self, validated_data):
        today=datetime.today()
        request = self.context.get("request")
        customer= lead_user.objects.get(user=request.user)
        var1= customer_request(
                                service_type=validated_data['service_type'],
                                description=validated_data['description'],
                                image=validated_data['image'],
                                customer=customer.customer,
                                date_request=today.date(),
                                #promotion = validated_data['promotion'],
                                date=validated_data['date'],
                                from_time = validated_data['from_time'],
                                to_time = validated_data['to_time'],
                                status = Status.objects.get(status="Pending")
                                )              
       
        var1.save()
        lead=Lead.objects.get(email=request.user)
        lead.status=Status.objects.get(status="Customer")
        lead.save()
        notify.send(request.user,recipient=customer.customer.member,verb="Created new request",app_name="CustomerRequest",activity="create",object_id=var1.pk)

        #notify.send(request.user,recipient=lead.member,verb="Created a new request")
        return var1
    
class CustomerUpdateRequestSerializer(serializers.ModelSerializer):
    #from_time = serializers.TimeField(format="%H:%M %p")
    #to_time = serializers.TimeField(format="%H:%M %p")
    date = serializers.DateField(format="%d-%m-%Y", input_formats=None)
    class Meta:
        model = customer_request
        fields=('id','service_type','description','image','date','from_time','to_time')
    
     
    def validate(self, data):
        # The keys can be missing in partial updates
        if "date" in data :
            today=datetime.today()
            if data["date"] < today.date() :
                raise serializers.ValidationError({
                    "date": "Request date cannot be less than today's date",
                })

        return super(CustomerUpdateRequestSerializer, self).validate(data)
    def update(self, instance, validated_data):
        today=datetime.today()
        request = self.context.get("request")
        customer= lead_user.objects.get(user=request.user)
        cust_request_id=self.context['pk']  
        
        #from_time=validated_data['from_time'].strftime("%H:%M")
        #d = datetime.strptime(from_time, "%H:%M")
        #conv_frm_time= d.strftime("%I:%M %p")  
        #to_time=validated_data['to_time'].strftime("%H:%M")
        #e = datetime.strptime(to_time, "%H:%M")
        #conv_to_time = e.strftime("%I:%M %p")
            
        var=customer_request.objects.get(id=cust_request_id)
        var.service_type=validated_data['service_type']
        var.description=validated_data['description']
        
        var.image=validated_data['image']
        var.customer=customer.customer
        var.date_update=today.date()
        var.date=validated_data['date']
        var.from_time = validated_data['from_time']
        var.to_time = validated_data['to_time']
        var.status = Status.objects.get(status="Pending")                     
        var.save()
        print(var.date_update)
        lead=Lead.objects.get(email=request.user)
        lead.status=Status.objects.get(status="Customer")
        lead.save()
        notify.send(request.user,recipient=lead.member,verb="Updated request",app_name="CustomerRequest",activity="update",object_id=var.pk)
        #notify.send(request.user,recipient=lead.member,verb="have updated request")
        return var

class CustomerAddRequestpromotionSerializer(serializers.ModelSerializer):
     date = serializers.DateField(format="%d-%m-%Y", input_formats=None)
     class Meta:
        model = customer_request
        fields=('id','description','image','date','from_time','to_time')
        
     def validate(self, data):
        # The keys can be missing in partial updates
        if "date" in data :
            promotion_id=self.context['Promotions_pk']  
            promotion=Promotions.objects.get(pk=promotion_id)
            print("@@@@@@@@promotionin validate:",promotion.from_date)

            if data["date"] < promotion.from_date :
                raise serializers.ValidationError({
                    "date": "Request date cannot be less than "+str(promotion.from_date)+" and greater than "+str(promotion.to_date),
                })
                
            if data["date"] > promotion.to_date :
                raise serializers.ValidationError({
                    "date": "Request date cannot be less than " +str(promotion.from_date)+" and greater than "+str(promotion.to_date),
                })

        return super(CustomerAddRequestpromotionSerializer, self).validate(data) 
      
     def create(self, validated_data):
        today=datetime.today()
        request = self.context.get("request")
        customer= lead_user.objects.get(user=request.user)
        promotion_id=self.context['Promotions_pk']  
        promotion=Promotions.objects.get(pk=promotion_id)
        print("@@@@@@@@promotion:",promotion.from_date)
        var1= customer_request(
                                service_type=promotion.Service_id,
                                description=validated_data['description'],
                                image=validated_data['image'],
                                customer=customer.customer,
                                date_request=today.date(),
                                promotion = promotion,
                                status = Status.objects.get(status="Pending"),
                                date = validated_data['date'],
                                from_time = validated_data['from_time'],
                                to_time= validated_data['to_time']
                                )              
       
        var1.save()
        lead=Lead.objects.get(email=request.user)
        lead.status=Status.objects.get(status="Customer")
        lead.save()
        message="Customer Added Request"

        notify.send(request.user,recipient=lead.member,verb="Created new request with promotion",app_name="CustomerRequest",activity="createrequest_promotion",object_id=var1.pk)
        return var1
    
class CustomerUpdateRequestpromotionSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y", input_formats=None)
    class Meta:
        model = customer_request
        fields=('id','description','image','date','from_time','to_time')
    
    def validate(self, data):
        # The keys can be missing in partial updates
        if "date" in data :
            cust_request_id=self.context['pk']
            var=customer_request.objects.get(id=cust_request_id)
            #print("promotion object in validate:",var.promotion)
            promotion=Promotions.objects.get(pk=var.promotion.pk)
           # print("@@@@@@@@promotionin validate:",promotion.from_date)

            if data["date"] < promotion.from_date :
                raise serializers.ValidationError({
                    "date": "Request date cannot be less than "+str(promotion.from_date)+" and greater than "+str(promotion.to_date),
                })
                
            if data["date"] > promotion.to_date :
                raise serializers.ValidationError({
                    "date": "Request date cannot be less than " +str(promotion.from_date)+" and greater than "+str(promotion.to_date),
                })

        return super(CustomerUpdateRequestpromotionSerializer, self).validate(data) 
    
    def update(self, instance, validated_data):
        today=datetime.today()
        request = self.context.get("request")
        customer= lead_user.objects.get(user=request.user)
        cust_request_id=self.context['pk']
        var=customer_request.objects.get(id=cust_request_id)
        var.service_type=var.service_type
        var.description=validated_data['description']
        var.promotion=var.promotion
        var.image=validated_data['image']
        var.customer=customer.customer
        var.date=validated_data['date']
        var.from_time=validated_data['from_time']
        var.to_time=validated_data['to_time']
        var.date_update=today.date()
        var.status = Status.objects.get(status="Pending")              
       
        var.save()
#         print("promotions from time",var.from_time)
#         print("promotions from time",var.to_time)
        print(var.date_update)
        lead=Lead.objects.get(email=request.user)
        lead.status=Status.objects.get(status="Customer")
        lead.save()

        notify.send(request.user,recipient=lead.member,verb="Updated request",app_name="CustomerRequest",activity="update",object_id=var.pk)
        return var

    
class CustomerchangestatusSerializer(serializers.ModelSerializer):  
     #status = serializers.CharField(source='status.status')
     class Meta:
        model = customer_request
        fields=('id','status')
     def update(self, instance, validated_data):
         today=datetime.today()
         cust_request_id=self.context['pk']
         var=customer_request.objects.get(id=cust_request_id)
         var.status = validated_data['status']             
       
         var.save()
         return var

#Appointment Serializer

class AppointmentAllSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.name')
    member = serializers.CharField(source='member.user.first_name')
    request = serializers.CharField(source='request.description')
    status = serializers.CharField(source='status.status')
    Servicetype = serializers.CharField(source='service_type.service_type')
    
    class Meta:
        model = MemberAppointment
        fields=('id','date','from_time','to_time','coment','customer','member','request','status','Servicetype')
        
class AppointmentAddSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = MemberAppointment
        fields=('id','date','from_time','to_time','coment','customer','member','request','status')

class AppointmentSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.name')
    member = serializers.CharField(source='member.user.first_name')
    Request_description = serializers.CharField(source='request.description')
    status = serializers.CharField(source='status.status')
    Request_Servicetype = serializers.CharField(source='request.service_type')
    Servicetype = serializers.CharField(source='service_type.service_type')
    class Meta:
        model = MemberAppointment
        fields=('id','date','from_time','to_time','coment','customer','member','status','Request_description','Request_Servicetype','Servicetype')

class SubServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubServiceType
        fields=('service_type_name',)

class appointment_historySerializer(serializers.ModelSerializer):
    
    request = serializers.CharField(source='request.description')
    Request_Servicetype = serializers.CharField(source='request.service_type')
    service_type = serializers.CharField(source='service_type.service_type')   
    class Meta:
        model = MemberAppointment
        fields=('id','request','date','from_time','to_time','coment','totalamount','coment','Request_Servicetype','service_type')
        #fields=('upcell','id','request','date','from_time','to_time','coment','amount')

class Upcell_historySerializer(serializers.ModelSerializer):
    
    service = serializers.CharField(source='service.service_type')
    sub_service=SubServiceTypeSerializer(read_only=True, many=True)
    
    class Meta:
        model = UpcellAppointment
        fields=('id','service','sub_service','description')

#Feedback Serializer
        
class FeedbackAllSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.name')
    
    class Meta:
        model = Custfeedback
        fields=('id','date','comment','customer')
        

class FeedbackViewSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(source='feedback_cust.comment',read_only=True)
    customer = serializers.CharField(source='feedback_cust.customer.name',read_only=True)
    Date = serializers.CharField(source='feedback_cust.date',read_only=True)
    question = serializers.CharField(source='question.question',read_only=True)
    sub_question = serializers.CharField(source='sub_question.sub_question',read_only=True)
    class Meta:
        model = Custfeedquestion
        fields=('id','customer','Date','comment','question','answer','sub_question','sub_answer')


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Custfeedback
        fields=('comment',)
        

class FeedbackCreateSerializer(serializers.ModelSerializer):
    rating= serializers.RegexField(
            regex=r'^[0-9]+$',
            required=True,
            error_messages= {
                        "invalid" : 'Please enter valid rating',
                        "blank" : "Rating cannot be empty",
            })
    comment = serializers.CharField(
        required=False,
        max_length=300,
        error_messages={
            "max_length": "The text entered exceeds the maximum length ",
        })
    
    class Meta:
        model = Feedback_Star
        fields=('comment','rating',)
        
    def create(self, validated_data):
        print("in feedback create")
        today=datetime.today()
        request = self.context.get("request")
        l_u = lead_user.objects.get(user=request.user)
        print("lead id",l_u.customer)
        feeback = Feedback_Star.objects.create(**validated_data)
        feeback.feedback_date=today.date()
        feeback.member = l_u.customer.member
        feeback.customer= l_u.customer
        feeback.save()
        return feeback

#Master Date Serializer

class AllCarCompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        
class AllCarModelSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.company_name')
    
    class Meta:
        model = Company_Model
        fields=('id','model_name','company')
        
class AllMakeYearSerializer(serializers.ModelSerializer):
    model = serializers.CharField(source='model.model_name')
    makeyear = serializers.CharField(source='makeyear.make_year')
    
    class Meta:
        model = MakeYear
        fields=('id','model','makeyear')
        
        
class AllServiceTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Service
        
class UsercountSerializer(serializers.ModelSerializer):
    user_count = serializers.IntegerField(read_only=True)
    print("!!!!!!!!!@@@@@@@@@@@##############", user_count)
    
    class Meta:
        model = User
        fields=('user_count',)

class view_makeyear_Serializer(serializers.ModelSerializer): 
    
    class Meta:
        model=Make_Year1

#Registration Serializer

class PhoneNumberValidator(RegexValidator):
    regex = r'^[0-9]+$'
    message = 'Invalid Phone Number'

class CustomerDetailSerializer(serializers.ModelSerializer):
    status=serializers.CharField(source='status.status')

    class Meta:
        model = Lead
        fields=('id','name','status')

class RoadSideNumberValidator(RegexValidator):
    regex = r'^[0-9]+$'
    message = 'Invalid Road side assistant number' 

class CustomerUpdateProfileSerializer(serializers.ModelSerializer):
    #date_update = serializers.DateTimeField(read_only=True, default=serializers.CreateOnlyDefault(datetime.today().date()))
    phone= serializers.RegexField(regex=r'^[0-9]+$', error_messages= {"invalid" : 'Please enter a valid number'})
    name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
    road_side_assistant_num = serializers.CharField(
        allow_blank=True,
        min_length=1,
        max_length=30,
       validators=[RoadSideNumberValidator()]
    ) 
    postal_code = serializers.CharField(
        allow_blank=True,
        min_length=4,
        max_length=4,
        error_messages={
            "min_length": "Postal_code must contain 4 digits",
            "max_length": "Postal_code must contain 4 digits",
        },
       validators=[PostalCodeValidator()]
    ) 
    
    class Meta:
        model = Lead
        fields=('name', 'address','licenseid','email','phone','image','last_name','road_side_assistant_num','policy_number','postal_code')
        
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        phn=data['phone']
        regex = r'^[0-9]+$'
        mylist = []
        mylist.append(phn)
        phn_1=mylist[0][0]
        print("----------phn_1-----------",str(phn_1))
        
        if phn== "" :
            raise serializers.ValidationError("Phone Number Field cannot be empty")
        if phn_1=='0':
            print("___________IN 0000__________")
            if len(phn)> 10 :
                raise serializers.ValidationError("Phone Number cannot be greater 10 digits")
            if len(phn)< 10 :
                raise serializers.ValidationError("Phone Number cannot be less 10 digits")
        if phn_1!='0':
            print("___________IN 1111__________")
            if len(phn)> 9 :
                raise serializers.ValidationError("Phone Number cannot be greater 9 digits")
            if len(phn)< 9 :
                raise serializers.ValidationError("Phone Number cannot be less 9 digits")
        
        if data['email']== "" :
            raise serializers.ValidationError("Email Field cannot be empty")
        
        return data
        
class FirstNameValidator(RegexValidator): 
    regex= '^[a-zA-Z]+$'
    message = 'Invalid First Name'
    
class LastNameValidator(RegexValidator): 
    regex= '^[a-zA-Z]+$'
    message = 'Invalid First Name'          
        
class UserSerializer(serializers.ModelSerializer):
    first_name= serializers.CharField(validators=[FirstNameValidator()])
    last_name= serializers.CharField(validators=[LastNameValidator()])    
    
    class Meta:
        model = User
        fields=('first_name', 'last_name')
        

class TodayLoggedinUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields=('first_name', 'email','last_login')
  
        
class Vin_noValidator(RegexValidator):
    regex = '^(?=.*\d)(?=.*[a-zA-Z])(?!.*[\W_\x7B-\xFF])'
    message='Invalid Vin Number'

class Chassis_no(RegexValidator):
    regex = r'^-?[0-9]+$'
    message='Make sure you have entered all Integer letters only'



        
class customer_add_vehicles_Serializer(serializers.ModelSerializer):
    vin_no = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=17,
        min_length=17,
        error_messages={
            "min_length": "Length of VIN number should be 17",
            "max_length": "Length of VIN number should be 17",
        },validators=[Vin_noValidator()]
    )
    chasis_no = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=6,
        min_length=6,
        error_messages={
            "min_length": "Length of Chasis number should be 6",
            "max_length": "Length of Chasis number should be 6",
        },validators=[Chassis_no()]

    ) 
    #image= serializers.ImageField(required=False,allow_empty_file=True,) 
    class Meta:
        model=Lead_Vehicle
        fields=('id','vehicle_no','reg_expiry_date','model','company','makeyear','vin_no','image','chasis_no')
       
        
    def create(self, validated_data):

        request = self.context.get("request")
        user= request.user 
        print("logged in user:",user)   
        cust= lead_user.objects.get(user= user)
        print("lead_user object:",cust)
        lead = Lead.objects.get(pk=cust.customer.id)
        print("lead object:",lead)
        var1= Lead_Vehicle.objects.create(**validated_data)
        var1.lead= lead
        var1.save()
        print("vehicle image:",var1.image)
        return var1
    
    def validate(self, data):
        today=datetime.today()
        #if data['reg_expiry_date']:
            #if data['reg_expiry_date'] < today.date():
             #   raise serializers.ValidationError("Registration expiry date cannot be less than today's date")
        if data['model'] is None:
            raise serializers.ValidationError("Model Field cannot be empty")       
        return data


class customer_viewall_vehicle_Serializer(serializers.ModelSerializer): 
    model=serializers.CharField(source='model.model_name')
    lead=serializers.CharField(source='lead.name')
    company=serializers.CharField(source='company.company_name')
    makeyear=serializers.CharField(source='makeyear.make_year')
    class Meta:
        model=Lead_Vehicle

class Vin_noValidator(RegexValidator):
    regex = '^(?=.*\d)(?=.*[a-zA-Z])(?!.*[\W_\x7B-\xFF])'
    message='Invalid Vin Number'

class Chassis_no(RegexValidator):
    regex = r'^-?[0-9]+$'
    message='Make sure you have entered all Integer letters only'


class customer_vehicles_Serializer(serializers.ModelSerializer):
    chasis_no = serializers.CharField(
        required=False,
        allow_blank= True,
        max_length=6,
        min_length=6,
        error_messages={
            "min_length": "Length of Chasis number should be 6",
            "max_length": "Length of Chasis number should be 6",
        },validators=[Chassis_no()]
    )
    vin_no = serializers.CharField(
        required=False,
        max_length=17,
        min_length=17,
        error_messages={
            "min_length": "Length of VIN number should be 17",
            "max_length": "Length of VIN number should be 17",
        },validators=[Vin_noValidator()]
    )
    class Meta:
        model=Lead_Vehicle
        fields=('vehicle_no','reg_expiry_date','model','company','makeyear','vin_no','image','chasis_no')
    
    def validate(self, data):
         
        today=datetime.today()
        #if data['reg_expiry_date']:
            #if data['reg_expiry_date'] < today.date():
                #raise serializers.ValidationError("Registration expiry date cannot be less than today's date")
        
        if data['model'] is None:
            raise serializers.ValidationError("Model Field cannot be empty") 
        return data
    
    def create(self, validated_data):
        lead_id=self.context['lead_id'] 
       # print("**********************",lead_id) 
        lead_obj=Lead.objects.get(pk=lead_id)
        var1= Lead_Vehicle.objects.create(**validated_data)
        var1.save()
        var1.lead=lead_obj
        var1.save()
       # print("var1",var1)
        return var1

#make year        
class view_makeyear_Serializer(serializers.ModelSerializer): 
    class Meta:
        model=Make_Year1




#business card serializers
class member_view_businesscard_Serializer(serializers.ModelSerializer):
    email=serializers.CharField(source='user.email')
    first_name=serializers.CharField(source='user.first_name')
    last_name=serializers.CharField(source='user.last_name')
    class Meta:
        model=UserProfile
        fields=('first_name','last_name','email','phone_no','shop_name','shop_address','website','city','country','area_code')

class member_send_businesscard_Serializer(serializers.ModelSerializer):
    name =serializers.CharField()
    email = serializers.RegexField(regex=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
        required=True,    
        error_messages={
            "blank":"This field may not be blank",
            "invalid":'Please enter valid email_id'
        }
    )
    
    class Meta:
         model=EBC
         fields=('email','name')
         
    def create(self,validated_data):
          request = self.context.get("request")
          email = validated_data['email']
          name = validated_data['name']
          print("emaillllllllll",email)
          user=request.user
          group=Group.objects.get(user=user)
          today=datetime.today()
          if group.name=='Member':
              member=User.objects.get(id=user.id)
              mem=EBC(name=name,email=email,ebctime=today.date(),send_user=user)
              mem.save()
              ws_member_send_businesscard__mail.delay(str(email),str(user.email),str(name))
              return mem
          else:
               
               print("in else")
               lead=Lead.objects.get(email=user.email)
               member=User.objects.get(id=lead.member.pk)
               
               mem=EBC(name=name,email=email,ebctime=today.date(),send_user=user)
               mem.save()
               ws_member_send_businesscard__mail.delay(str(email),str(lead.member.email),str(name))
               return mem


class customer_addimage_Serializer(serializers.ModelSerializer): 
    
    class Meta:
        model=Lead_Vehicle
        fields=('image',)

class CustomerEmerAddRequestSerializer(serializers.ModelSerializer):
    #from_time = serializers.TimeField(format="%H:%M %p")
    #to_time = serializers.TimeField(format="%H:%M %p")
    date = serializers.DateField(format="%d-%m-%Y", input_formats=None)
    class Meta:
        model = customer_request
        fields=('id','description','image','date','from_time')
        
    def create(self, validated_data):
        today=datetime.today()
        request = self.context.get("request")
        customer= lead_user.objects.get(user=request.user)
        service_break= Service.objects.get(service_type="Breakdown")
        var1= customer_request(
                                service_type=service_break,
                                description=validated_data['description'],
                                image=validated_data['image'],
                                customer=customer.customer,
                                date_request=today.date(),
                                #promotion = validated_data['promotion'],
                                date=validated_data['date'],
                                from_time = validated_data['from_time'],
                               
                                status = Status.objects.get(status="Pending"),
                                emergency_status=1,
                                )              
        
        var1.save()
        lead=Lead.objects.get(email=request.user)
        lead.status=Status.objects.get(status="Customer")
        lead.save()
        
        notify.send(request.user,recipient=lead.member,verb="Created an emergency request",app_name="CustomerRequest",activity="create_emergency_request",object_id=var1.pk)

        #notify.send(request.user,recipient=lead.member,verb="Created a new request")
        return var1

class Userdeatailserializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields= ('first_name','last_name','email')
        
class MemberpostalcodeSerializer(serializers.ModelSerializer):
    user=Userdeatailserializer()
    class Meta:
        model = UserProfile
        fields= ('postal_code','phone_no','shop_name','shop_address','city','country','website','user')

class UserNameValidator(RegexValidator): 
    regex=r'^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$'
    message = 'Invalid User Name'       
class new_user_createSerializer(serializers.ModelSerializer):
    first_name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
    last_name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
    username=serializers.CharField(validators=[UserNameValidator()])
  
   
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        error_messages={
            "blank": "Password cannot be empty",
            #"min_length": "password should be 8 character long",
            
        }
    )
    class Meta:
        model=User
        fields=('username','password','first_name','last_name') 
     
    
            
class AreaCodeValidator(RegexValidator):
    regex = r'^[0-9]+$'
    message = 'Invalid Area Code'

class EmergencyNumberValidator(RegexValidator):
    regex = r'^[0-9]+$'
    message = 'Invalid Emergency Number'     
class WebsiteValidator(RegexValidator):    
     regex =r'^(www.)[a-zA-Z0-9\-]+\.[a-zA-Z]{2,5}[\.]{0,1}' 
     message = 'Invalid Website'   
class AbnValidator(RegexValidator):
    regex = r'^[0-9]+$'
    message = 'Invalid Abn number'
                  
                   
class  registration_member_Serializer(serializers.ModelSerializer):
    city_options=(('New South Wales','New South Wales'),('Victoria','Victoria'),('Queensland','Queensland'),('Western Australia','Western Australia'),('South Australia','South Australia'),('Tasmania','Tasmania'),('Northern Territory','Northern Territory'),('Australian Capital Territory','Australian Capital Territory'))
    city=serializers.ChoiceField(required=True,choices=city_options)
    country_options=(('Select Country','Select Country'),('Australia','Australia'))
    country=serializers.ChoiceField(required=True,choices=country_options)
    user = new_user_createSerializer()
    shop_name = serializers.CharField()
    shop_address = serializers.CharField()
    website = serializers.CharField(allow_blank=True,required=False,validators=[WebsiteValidator()])
    abn = serializers.CharField(
        required=True,
        min_length=11,
        max_length=11,
        error_messages={
            #"blank": "Area code cannot be empty",
            "min_length": "ABN number should consist 11 digits",
        },validators=[AbnValidator()]
    )
   
    
    
    phone_no= serializers.RegexField(regex=r'^[0-9]+$', error_messages= {"invalid" : 'Please enter a valid number'})

    area_code = serializers.CharField(
        required=True,
        min_length=2,
        max_length=2,
        error_messages={
            #"blank": "Area code cannot be empty",
            "min_length": "Area code should consist 2 digits",
        },validators=[AreaCodeValidator()]
    )
   
    postal_code = serializers.CharField(
        required=True,
        min_length=4,
        max_length=4,
        error_messages={
            "blank": "Postal code  cannot be empty",
            "min_length": "postal  code should be 4 digit long",
            "max_length": "postal code should be 4 digit long",
        },validators=[PostalCodeValidator()]
    ) 
                                    
    class Meta:
        model=UserProfile
        fields=('user','phone_no','area_code','shop_name','shop_address','city','country','abn','website','postal_code')
    
    def create(self, validated_data):
        tracks_data = validated_data.pop('user')
        user1 = User.objects.create(**tracks_data)
        user1.email=validated_data['username']
        print(user1.password)
        validated_data['user']=user1
        var1= UserProfile.objects.create(**validated_data)
        user1.groups.add(Group.objects.get(name='Member'))
        var2=Payment(last_4_digits=0000,stripe_id=0,subscribed=False,user=user1)
        var2.save()
        send_member_task.delay(user1.username, user1.password,var1.shop_name,var1.website)
        user1.set_password(user1.password)
        user1.save()
        return var1        
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        print["in validate function"]
        phn=data['phone_no']
        print["!!!!!!@@@@@",phn]
        regex = r'^[0-9]+$'
        mylist = []
        mylist.append(phn)
        phn_1=mylist[0][0]
        print("----------phn_1-----------",str(phn_1))
        
        if phn== "" :
            raise serializers.ValidationError("Phone Number Field cannot be empty")
        if phn_1=='0':
            print("___________IN 0000__________")
            if len(phn)> 10 :
                raise serializers.ValidationError("Phone Number cannot be greater 10 digits")
            if len(phn)< 10 :
                raise serializers.ValidationError("Phone Number cannot be less 10 digits")
        if phn_1!='0':
            print("___________IN 1111__________")
            if len(phn)> 9 :
                raise serializers.ValidationError("Phone Number cannot be greater 9 digits")
            if len(phn)< 9 :
                raise serializers.ValidationError("Phone Number cannot be less 9 digits")
        
       
        return data
 
class MemberUpdateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    shop_name = serializers.CharField()
    shop_address = serializers.CharField()
    city_options=(('New South Wales','New South Wales'),('Victoria','Victoria'),('Queensland','Queensland'),('Western Australia','Western Australia'),('South Australia','South Australia'),('Tasmania','Tasmania'),('Northern Territory','Northern Territory'),('Australian Capital Territory','Australian Capital Territory'))
    city=serializers.ChoiceField(required=True,choices=city_options)
    country_options=(('Select Country','Select Country'),('Australia','Australia'))
    country=serializers.ChoiceField(required=True,choices=country_options)
    phone_no= serializers.RegexField(regex=r'^[0-9]+$', error_messages= {"invalid" : 'Please enter a valid number'})
    website = serializers.CharField(allow_blank=True,required=False,validators=[WebsiteValidator()])
    area_code = serializers.CharField(
        required=True,
        min_length=2,
        max_length=2,
        error_messages={
            #"blank": "Area code cannot be empty",
            "min_length": "Area code should consist 2 digits",
        },validators=[PhoneNumberValidator()]
    )
   
    postal_code = serializers.CharField(
        required=True,
        min_length=4,
        max_length=4,
        error_messages={
            "blank": "Postal code  cannot be empty",
            "min_length": "postal  code should be 4 digit long",
            "max_length": "postal code should be 4 digit long",
        },validators=[PostalCodeValidator()]
    ) 
    Emg_no = serializers.CharField(
        required=False,
        min_length=10,
        max_length=10,
        error_messages={
            
            "min_length": "Emergency number should be 10 digit long",
            "max_length": "Emergency number should be 10 digit long",
        },validators=[EmergencyNumberValidator()]
    )                                   
    
    class Meta:
        model = UserProfile
        fields=('phone_no','shop_name','shop_address','city','country','website','area_code','Emg_no','postal_code','user')
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('user')
        user = instance.user
        
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.shop_name = validated_data.get('shop_name', instance.shop_name)
        instance.shop_address = validated_data.get('shop_address', instance.shop_address)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.website = validated_data.get('website', instance.website)
        instance.area_code = validated_data.get('area_code', instance.area_code)
        instance.Emg_no = validated_data.get('Emg_no', instance.Emg_no)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.save()
        
        user.first_name = profile_data.get(
            'first_name',
            user.first_name
        )
        
        user.last_name = profile_data.get(
            'last_name',
            user.last_name
         )
        user.save()

        return instance
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        print["in validate function"]
        phn=data['phone_no']
        print["!!!!!!@@@@@",phn]
        regex = r'^[0-9]+$'
        mylist = []
        mylist.append(phn)
        phn_1=mylist[0][0]
        print("----------phn_1-----------",str(phn_1))
        
        if phn== "" :
            raise serializers.ValidationError("Phone Number Field cannot be empty")
        if phn_1=='0':
            print("___________IN 0000__________")
            if len(phn)> 10 :
                raise serializers.ValidationError("Phone Number cannot be greater 10 digits")
            if len(phn)< 10 :
                raise serializers.ValidationError("Phone Number cannot be less 10 digits")
        if phn_1!='0':
            print("___________IN 1111__________")
            if len(phn)> 9 :
                raise serializers.ValidationError("Phone Number cannot be greater 9 digits")
            if len(phn)< 9 :
                raise serializers.ValidationError("Phone Number cannot be less 9 digits")
        
       
        return data

        
    
class LeadListSerializer(serializers.ModelSerializer):
    status=serializers.CharField(source='status.status')
    member=serializers.CharField(source='member.email')
    class Meta:
        model = Lead
        fields=('id','name','member','status','last_name','licenseid','address','email','phone','image','Emg_no','road_side_assistant_num','policy_number')
        
             
        
#class  AddLeadSerializer(serializers.ModelSerializer):  
#   name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
#   last_name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
#   phone = serializers.CharField(
#       required=True,
#       min_length=10,
#       max_length=10,
#       error_messages={
#           "blank": "Phone number cannot be empty",
#           "min_length": "phone number should be 10 digit long",
#           "max_length": "phone number should be 10 digit long",
#       },validators=[PhoneNumberValidator()]
#   )
#   email = serializers.RegexField(regex=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
#       required=True,    
#       error_messages={
#           "blank":"This field may not be blank",
#           "invalid":'Please enter valid email_id'
#       }
#   )
    
#   class Meta:
#       model = Lead
#       fields=('id','name','last_name','email','phone')    
     
#   def create(self, validated_data):
#       
#       digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
#        chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
#       p=(digits + "@156"+chars)
#       user = User.objects.create_user(
#           username=validated_data['email'],
#           email=validated_data['email'],
#           password=p
#       )
#       user.groups.add(Group.objects.get(name='Lead'))
#       user.save()
#       request = self.context.get("request")
#       lead=Lead.objects.create(
#                                name=validated_data['name'],
#                                last_name=validated_data['last_name'],
#                                
#                                email=validated_data['email'],
#                                phone=validated_data['phone'],
#                                status = Status.objects.get(status="Lead"),
#                                member=request.user,
#                                )
#       lead.save()
#       var1=lead_user(customer=lead, user=user)
#       var1.save()
#       cust_detail=lead_user.objects.get(user=user.pk)
#       mem_detail=Lead.objects.get(id=cust_detail.customer.id)
#       detail1 = get_object_or_404(User, pk=mem_detail.member.id)
#       detail2 = get_object_or_404(UserProfile, user=detail1)
#       send_lead_task.delay(user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,user.first_name,lead.member.username,detail2.website) 
#       return lead

class  AddLeadSerializer(serializers.ModelSerializer):  
    name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
    last_name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
    phone= serializers.RegexField(allow_blank = True,required = False,regex=r'^[0-9]+$', error_messages= {"invalid" : 'Please enter a valid number'})
    #email=serializers.EmailField(allow_blank=True)
    
    class Meta:
        model = Lead
        fields=('id','name','last_name','email','phone')    
     
    def create(self, validated_data):
        request = self.context.get("request")
        digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
        chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
        p=(digits + "@156"+chars)
        name=validated_data['name']
        last_name=validated_data['last_name']
        email=validated_data['email']
        phone=validated_data['phone']
        user_obj=None
        
        
        if phone :# is not None and email is None:
#             
            if  phone and email :# and phone is None:
                print("1 else")
                raise serializers.ValidationError("please enter either email or phone")
            else :
                print("1st if")
                print(phone)
                
                
                mylist = []
                mylist.append(phone)
                phn_1=mylist[0][0]
               
                if phn_1=='0':
                    print("___________IN 0000__________")
                    if len(phone)> 10 :
                        raise serializers.ValidationError("Phone Number cannot be greater 10 digits")
                    if len(phone)< 10 :
                        raise serializers.ValidationError("Phone Number cannot be less 10 digits")
                if phn_1!='0':
                    print("___________IN 1111__________")
                    if len(phone)> 9 :
                        raise serializers.ValidationError("Phone Number cannot be greater 9 digits")
                    if len(phone)< 9 :
                        raise serializers.ValidationError("Phone Number cannot be less 9 digits")
#                     
                lead=Lead(name=name,last_name=last_name,phone=phone,member=request.user,status=Status.objects.get(status='Lead'))
                lead.save()
    #           
                user_obj = User.objects.create_user(username=phone,
                          password =p,
                          first_name=name,
                          last_name=last_name
                         )
                
		user_obj.groups.add(Group.objects.get(name='Lead'))
        	print("user_obj.password")
        elif email:# is not None and phone is None:
            print("1 elif")
            if email and phone :# and phone is None:
                print("1 else")
                raise serializers.ValidationError("please enter either email or phone")

            else :
                print(email)
                lead=Lead(name=name,last_name=last_name,email=email,member=request.user,status=Status.objects.get(status='Lead'))
                lead.save()
                user_obj = User.objects.create_user(username=email,
                          email=email,
                         password =p,
                         first_name=name,
                          last_name=last_name
                         )
                
        	user_obj.groups.add(Group.objects.get(name='Lead'))
        else:
            print("1 else")
            raise serializers.ValidationError("please enter either email or phone")
        
            
        cust_detail=lead_user(customer=lead,user=user_obj)
        cust_detail.save()
	mem_detail=Lead.objects.get(id=cust_detail.customer.id)
        detail1 = get_object_or_404(User, pk=mem_detail.member.id)
        detail2 = get_object_or_404(UserProfile, user=detail1)
        send_lead_task.delay(user_obj.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,user_obj.first_name,lead.member.username,detail2.website) 
        return lead

class customerSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.status')
    class Meta:
        model = Lead
        fields=('id','name','last_name','address','licenseid','email','phone','image','Emg_no','road_side_assistant_num','policy_number','status') 

class delete_customer_Serializer2(serializers.ModelSerializer):
    class Meta:
        model = Lead  

class MemberDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.first_name')
    class Meta:
        model = UserProfile
        fields=('id','user')      
       
class EmailValidator(RegexValidator): 
    regex=r'^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$'
    message = 'Invalid Email Id'  
    
class  AddCustomerSerializer(serializers.ModelSerializer):  
    name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
    last_name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
    phone= serializers.RegexField(regex=r'^[0-9]+$', error_messages= {"invalid" : 'Please enter a valid number'})
    email=serializers.CharField(validators=[EmailValidator()])
    
    class Meta:
        model = Lead
        fields=('id','name','last_name','licenseid','address','email','phone')    
    def validate(self, data):
            """
            Check that the start is before the stop.
            """
            print["in validate function"]
            phn=data['phone']
            print["!!!!!!@@@@@",phn]
            regex = r'^[0-9]+$'
            mylist = []
            mylist.append(phn)
            phn_1=mylist[0][0]
            print("----------phn_1-----------",str(phn_1))
            
            if phn== "" :
                raise serializers.ValidationError("Phone Number Field cannot be empty")
            if phn_1=='0':
                print("___________IN 0000__________")
                if len(phn)> 10 :
                    raise serializers.ValidationError("Phone Number cannot be greater 10 digits")
                if len(phn)< 10 :
                    raise serializers.ValidationError("Phone Number cannot be less 10 digits")
            if phn_1!='0':
                print("___________IN 1111__________")
                if len(phn)> 9 :
                    raise serializers.ValidationError("Phone Number cannot be greater 9 digits")
                if len(phn)< 9 :
                    raise serializers.ValidationError("Phone Number cannot be less 9 digits")
            
           
            return data  
    def create(self, validated_data):
        
        digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
        chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
        p=(digits + "@156"+chars)
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=p
        )
        user.groups.add(Group.objects.get(name='Customer'))
        user.save()
        request = self.context.get("request")
        lead=Lead.objects.create(
                                 name=validated_data['name'],
                                 last_name=validated_data['last_name'],
                                 licenseid=validated_data['licenseid'],
                                 address=validated_data['address'],
                                 email=validated_data['email'],
                                 phone=validated_data['phone'],
                                 status = Status.objects.get(status="Customer"),
                                 member=request.user,
                                 )
        lead.save()
        var1=lead_user(customer=lead, user=user)
        var1.save()
        cust_detail=lead_user.objects.get(user=user.pk)
        mem_detail=Lead.objects.get(id=cust_detail.customer.id)
        detail1 = get_object_or_404(User, pk=mem_detail.member.id)
        detail2 = get_object_or_404(UserProfile, user=detail1)
        send_lead_task.delay(user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,user.first_name,mem_detail.member.username,detail2.website) 
        return lead  



class VehicleListSerializer(serializers.ModelSerializer):
    
    model=serializers.CharField(source='model.model_name')
    company=serializers.CharField(source='company.company_name')
    makeyear=serializers.CharField(source='makeyear.make_year')
    class Meta:
        model = Lead_Vehicle
        fields=('id','vehicle_no','reg_expiry_date','model','company','makeyear','vin_no','image','chasis_no')

class customerDeregisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields=("email",)
        
    def update(self, instance, validated_data):
        request = self.context.get("request")
        lead_id=self.context['pk']
        querySet = Lead.objects.get(pk=lead_id)
        querySet.status=Status.objects.get(status="Deregister")
        querySet.save()
        l_u=lead_user.objects.get(customer=querySet)
        old_lead=User.objects.get(pk=l_u.user.pk)
        old_lead.is_active=False
        old_lead.save()
        request_obj=customer_request.objects.filter(customer=querySet).delete()
        appointment_obj=MemberAppointment.objects.filter(customer=querySet).delete()
        feedback_obj=Feedback_Star.objects.filter(customer=querySet).delete()

        print(querySet)
        print("now de-registered")
        return querySet 

class CustomerAppointmentListSerializer(serializers.ModelSerializer):

  
    class Meta:
        model = MemberAppointment
        #fields=('id','request','service_type','status','totalamount','upcell_status','date_update','date_appointment')




class customer_historySerializer(serializers.ModelSerializer):
    accept = serializers.CharField(source='upcellappointment.accept')
    appoinment_date = serializers.CharField(source='upcellappointment.appointment.date_appointment')
    request_service_type = serializers.CharField(source='upcellappointment.appointment.request.description')
#     totalamount = serializers.CharField(source='upcellappointment.appointment.totalamount')
    price = serializers.CharField(source='upcellappointment.amount')
     
    job_done_date = serializers.CharField(source='upcellappointment.appointment.date_update')
    status = serializers.CharField(source='upcellappointment.appointment.status.status')
    description = serializers.CharField(source='upcellappointment.description')
    sub_service_type = serializers.CharField(source='subservicetype.service_type_name')
    service_type = serializers.CharField(source='subservicetype.service.service_type')
    class Meta:
        model = UpcellAppointmentSubService
        fields = ('request_service_type','appoinment_date','job_done_date','price','accept','status','description','sub_service_type','service_type')#('id','status','service_type','date_appointment','date_update','totalamount')
        



    
class EditLeadSerializer(serializers.ModelSerializer):
    name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
    last_name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
    phone= serializers.RegexField(allow_blank = True,required = False,regex=r'^[0-9]+$', error_messages= {"invalid" : 'Please enter a valid number'})
    class Meta:
        model = Lead
        fields=('id','name','last_name','email','phone')
    
    def update(self, instance, validated_data):
        print("user in serializzer ---")      
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        
        instance.save()
        return instance
    
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        request = self.context.get("request")
        print["in validate function"]
        phone=data['phone']
        email=data['email']
        name=data['name']
        last_name=data['last_name']
        print["phone in serializer----",phone]
        
        digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
        chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
        p=(digits + "@156"+chars)
        lead= None
        user_obj= None
        
        
        if phone :# is not None and email is None:

            if  phone and email :# and phone is None:
                print("1 else")
                raise serializers.ValidationError("please enter either email or phone")
            else :
                print("1st if")
                print(phone)
                
                
                mylist = []
                mylist.append(phone)
                phn_1=mylist[0][0]
               
                if phn_1=='0':
                    print("___________IN 0000__________")
                    if len(phone)> 10 :
                        raise serializers.ValidationError("Phone Number cannot be greater 10 digits")
                    if len(phone)< 10 :
                        raise serializers.ValidationError("Phone Number cannot be less 10 digits")
                if phn_1!='0':
                    print("___________IN 1111__________")
                    if len(phone)> 9 :
                        raise serializers.ValidationError("Phone Number cannot be greater 9 digits")
                    if len(phone)< 9 :
                        raise serializers.ValidationError("Phone Number cannot be less 9 digits")
                lead=Lead(name=name,last_name=last_name,phone=phone,member=request.user,status=Status.objects.get(status='Lead'))
                lead.save()
                user_obj = User.objects.create_user(username=phone,
                          password =p,
                          first_name=name,
                          last_name=last_name
                         )
                

        
        elif email:# is not None and phone is None:
            print("1 elif")
            if email and phone :# and phone is None:
                print("1 else")
                raise serializers.ValidationError("please enter either email or phone")
            else :
                print(email)
                lead=Lead(name=name,last_name=last_name,email=email,member=request.user,status=Status.objects.get(status='Lead'))
                lead.save()
                user_obj = User.objects.create_user(username=email,
                          email=email,
                         password =p,
                         first_name=name,
                          last_name=last_name
                         )
                
        
        else:
            print("1 else")
            raise serializers.ValidationError("please enter either email or phone")
            
        cust_detail=lead_user(customer=lead,user=user_obj)
        cust_detail.save()
        #send_lead_task.delay(user_obj.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,user_obj.first_name,lead.member.username,detail2.website) 
        return data

class PotentialleadSerializer(serializers.ModelSerializer):
    email=serializers.CharField(required=True,validators=[EmailValidator()])
    name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, 
                                 error_messages= {"invalid" : 'Please enter a valid name'})

    class Meta:
        model = EBC
        fields=("email","name")  

    def create(self, validated_data):  
        request = self.context.get("request")
        user=request.user
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",str(user.id))
        group=Group.objects.get(user=user)
        mail_id=validated_data['email']
        name=validated_data['name']
        today=datetime.today()
        ebc=EBC(email=mail_id,name=name,ebctime=today.date(),send_user=user)
        ebc.save()
        print("currently loggedin user",user.email,mail_id)
        if group.name=="Member": 
            send_vcf_email_task.delay(mail_id,user.email,name,user.id)
            print(name)
            print(user.email)
            print(mail_id)
            return ebc

class FeedbackSerializer(serializers.ModelSerializer):
     class Meta:
        model = Feedback_Star


##### member app starts

class reschedule_request_Serializer(serializers.ModelSerializer):
    #from_time = serializers.TimeField(format="%H:%M %p")
    #to_time = serializers.TimeField(format="%H:%M %p")
    date = serializers.DateField(format="%d-%m-%Y", input_formats=None)
    class Meta:
        model = customer_request
        fields=('id','service_type','status','description','image','date','from_time','to_time')
     
      
#     def validate(self, data):
#         # The keys can be missing in partial updates
#         if "date" in data :
#             today=datetime.today()
#             if data["date"] < today.date() :
#                 raise serializers.ValidationError({
#                     "date": "Request date cannot be less than today's date",
#                 })
#  
#         return super(CustomerUpdateRequestSerializer, self).validate(data)
    def update(self, instance, validated_data):
        today=datetime.today()
        request = self.context.get("request")
        
        cust_request_id=self.context['pk']  
         
        #from_time=validated_data['from_time'].strftime("%H:%M")
        #d = datetime.strptime(from_time, "%H:%M")
        #conv_frm_time= d.strftime("%I:%M %p")  
        #to_time=validated_data['to_time'].strftime("%H:%M")
        #e = datetime.strptime(to_time, "%H:%M")
        #conv_to_time = e.strftime("%I:%M %p")
             
        var=customer_request.objects.get(id=cust_request_id)
        customer = Lead.objects.get(id = var.customer.pk)
         
        var.service_type=validated_data['service_type']
        var.description=validated_data['description']
         
        var.image=validated_data['image']
        var.customer=customer
        var.date_update=today.date()
        var.date=validated_data['date']
        var.from_time = validated_data['from_time']
        var.to_time = validated_data['to_time']
        var.status = Status.objects.get(status="Pending")                     
        var.save()
#         lead=Lead.objects.get(email=request.user)
#         lead.status=Status.objects.get(status="Customer")
#         lead.save()
        #notify.send(request.user,recipient=lead.member,verb="Updated request",app_name="CustomerRequest",activity="update",object_id=var.pk)
        #notify.send(request.user,recipient=lead.member,verb="have updated request")
        return var
        



class regenerate_login_credentials_Serializer(serializers.ModelSerializer):
     email=serializers.EmailField()
     class Meta: 
         model = Lead
  
         fields = ('id','email')
         
     def update(self, instance, validated_data):
         print("user in serializzer ---",validated_data.get('email'))      
         instance.email = validated_data.get('email', instance.email)
         
         instance.status = Status.objects.get(status="Lead")
 #         
         email = instance.email
         
         lead_user3 = lead_user.objects.filter(customer = Lead.objects.filter(email =email )).values('user')
         print("in lead user ---",lead_user3)
     
         instance.save()
         return instance
     def validate(self, data):
         """
         Check that the start is before the stop.
         """
         request = self.context.get("request")
                  
         email=data['email']
         
         digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
         chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
         p=(digits + "@156"+chars)
         lead= None
         user_obj= None
         
         email_obj = User.objects.filter(email=request.data['email'])
         email_len = len(email_obj)
         
         
#          if email_len > 1:
#              msg = _('Account already exists for same user credentials')
#              raise exceptions.ValidationError(msg)
 #         
         if email_len == 1:# is not None and phone is None:
            pk =self.context['pk']  
            lead=Lead.objects.get(pk=pk)
            username = User.objects.filter(username = email)
#             if username:
#                 messages =_("email already exists")
#                 raise exceptions.ValidationError(messages)
            
            l_u=lead_user.objects.get(customer=lead)
            user= User.objects.get(pk=l_u.user.pk)
            lead.email=email
            lead.save()
            digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
            chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
            p=(digits + "@156"+chars)
            print(p)
            user.username=lead.email
            user.set_password(p)
            user.save()
            
            detail1 = get_object_or_404(User, pk=lead.member.id)
            detail2 = get_object_or_404(UserProfile, user=detail1)
            send_new_credentials.delay(user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,user.first_name,lead.member.username,detail2.website)
            group=Group.objects.get(user=user)
            print("group",group.name)
            messages =_("New password has been generated successfully")
            raise exceptions.ValidationError(messages)
         #send_lead_task.delay(user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,user.first_name,lead.member.username,detail2.website) 
         if email_len == 0:
            email_obj = User.objects.filter(email=request.data['email']) 
            #msg = _('Email already exists for same user credentials')
            #raise serializers.ValidationError("Email already exists ")
            pk =self.context['pk']  
            lead_obj = Lead.objects.get(pk = pk)
            
            l_u=lead_user.objects.get(customer=lead_obj)
            user= User.objects.get(pk=l_u.user.pk)
            lead_obj.email=email
            lead_obj.save()
            digits = "".join( [random.choice(string.digits) for i in xrange(4)] )
            chars = "".join( [random.choice(string.letters) for i in xrange(4)] )
            p=(digits + "@156"+chars)
            
            user.username=lead_obj.email
            user.set_password(p)
            user.save()
            
            detail1 = get_object_or_404(User, pk=lead_obj.member.id)
            detail2 = get_object_or_404(UserProfile, user=detail1)
            send_new_credentials.delay(user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead_obj.email,user.first_name,lead_obj.member.username,detail2.website)
            group=Group.objects.get(user=user)
            
            msg = _('New password has been generated successfully')
            raise exceptions.ValidationError(msg) 
             
         return data


class Schedule_Appointment_Serializers(serializers.ModelSerializer):
    class Meta:
        model = MemberAppointment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password=serializers.CharField(max_length=128,style={'input_type': 'password'})
    username = serializers.CharField(allow_blank = True,required = False,validators=[UserNameValidator()])
    class Meta:
        model = User
        fields = ('username','password')
            
class  LeadSerializer(serializers.ModelSerializer):  
    name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
    last_name= serializers.RegexField(regex=r'^[a-zA-Z -.\'\_]+$', required=True, error_messages= {"invalid" : 'Please enter a valid name'})
    phone= serializers.RegexField(allow_blank = True,required = False,regex=r'^[0-9]+$', error_messages= {"invalid" : 'Please enter a valid number'})
   # email=serializers.EmailField(allow_blank=True)
    class Meta:
        model = Lead
        fields=('name','last_name','phone')     
  
    
class  external_customer_registrationSerializer(serializers.ModelSerializer):  

    customer  = LeadSerializer()
    user = UserSerializer()
    class Meta:
        model = lead_user
        fields=('customer','user')    
     
    def create(self, validated_data):
        request = self.context.get("request")
        print("user in ext_cust",request.user)
        customer= validated_data.pop('customer')
        user= validated_data.pop('user')
        print("name",customer['name'])
        name=customer['name']
        print("in name----",name) 
        last_name=customer['last_name']
        print("in lastname",last_name)
        email=user['username']
        print("in email",email)
        phone=customer['phone']
        print("in phone",phone)
        password=user['password']
        print("in pwd",password)
        user_obj=None
             
        if  phone and email :
            print("both mail n phone")
            if( User.objects.filter(email = email) or User.objects.filter(username = email)):
                    print("in email--",email)
                    raise serializers.ValidationError("email already exists")
            else:
                mylist = []
                mylist.append(phone)
                phn_1=mylist[0][0]
                print(" phn_1",mylist)
                if phn_1=='0':
                    print("___________IN 0000__________",phn_1)
                    if len(phone)> 10 :
                        raise serializers.ValidationError("Phone Number cannot be greater 10 digits")
                    if len(phone)< 10 :
                        raise serializers.ValidationError("Phone Number cannot be less 10 digits")
                    
                    lead=Lead(name=name,last_name=last_name,phone=phone,email=email,member=None,status=Status.objects.get(status='External_Customer'))
                    lead.save()
                   
                    user_obj = User(username=email,
                              #password =password,
                              email=email,
                              first_name=name,
                              last_name=last_name
                             )
                    user_obj.set_password(password)
                    user_obj.save()
                   # user_obj.set_password(p)
                    user_obj.groups.add(Group.objects.get(name='External_Customer'))
            
                    
                if phn_1!='0':
                    print("___________IN 1111__________",phn_1)
                    if len(phone)> 9 :
                        
                        raise serializers.ValidationError("Phone Number cannot be greater 9 digits")
                    if len(phone)< 9 :
                        raise serializers.ValidationError("Phone Number cannot be less 9 digits")
                    
                    code = "+61"
                    
                    a = str(code + phone)
                    print("phone with code",a) 
                    lead=Lead(name=name,last_name=last_name,email=email,phone=phone,member=None,status=Status.objects.get(status='External_Customer'))
                    lead.save()
                   
                    user_obj = User(username=email,
                                    email=email,
                              #password =password,
                              first_name=name,
                              last_name=last_name
                             )
                    user_obj.set_password(password)
                    user_obj.save()
                    user_obj.groups.add(Group.objects.get(name='External_Customer'))
                    print("password---",user_obj.password)
                
                
        elif phone :
                print("1st if")
                print(phone)
                
                
                mylist = []
                mylist.append(phone)
                phn_1=mylist[0][0]
                print(" phn_1",mylist)
                if phn_1=='0':
                    print("___________IN 0000__________",phn_1)
                    if len(phone)> 10 :
                        raise serializers.ValidationError("Phone Number cannot be greater 10 digits")
                    if len(phone)< 10 :
                        raise serializers.ValidationError("Phone Number cannot be less 10 digits")
                    
                    lead=Lead(name=name,last_name=last_name,phone=phone,member=None,status=Status.objects.get(status='External_Customer'))
                    lead.save()
                   
                    user_obj = User.objects.create_user(username=phone,
                              #password =password,
                              email=email,
                              first_name=name,
                              last_name=last_name
                             )
                    user_obj.set_password(password)
                   
                    user_obj.groups.add(Group.objects.get(name='External_Customer'))
            
                    
                if phn_1!='0':
                    print("___________IN 1111__________",phn_1)
                    if len(phone)> 9 :
                        
                        raise serializers.ValidationError("Phone Number cannot be greater 9 digits")
                    if len(phone)< 9 :
                        raise serializers.ValidationError("Phone Number cannot be less 9 digits")
                    
                    code = "+61"
                    
                    a = str(code + phone)
                    print("phone with code",a) 
                    lead=Lead(name=name,last_name=last_name,phone=phone,member=None,status=Status.objects.get(status='External_Customer'))
                    lead.save()
                   
                    user_obj = User.objects.create_user(username=a,
                              #password =password,
                              email=email,
                              first_name=name,
                              last_name=last_name
                             )
                    user_obj.set_password(password)
                    user_obj.groups.add(Group.objects.get(name='External_Customer'))
                    print("password---",user_obj.password)
        
        elif email:
            if( User.objects.filter(email = email) or User.objects.filter(username = email)):
                    print("in email--",email)
                    raise serializers.ValidationError("email already exists")
            else:
            
                print(email)
                lead=Lead(name=name,last_name=last_name,email=email,member=None,status=Status.objects.get(status='External_Customer'))
                lead.save()
                email_obj = User.objects.filter(email = email) or User.objects.filter(username = email)            
                     
                user_obj = User.objects.create_user(username=email,
                          email=email,
                         password =password,
                         first_name=name,
                          last_name=last_name
                         )
                
                
                user_obj.groups.add(Group.objects.get(name='External_Customer'))
                print("password---",user_obj.password)
        else:
            print("1 else")
            raise serializers.ValidationError("please enter either email or phone")
        
            
        cust_detail=lead_user(customer=lead,user=user_obj)
        cust_detail.save()
        print("pwd in lead---",cust_detail.user.password)
        msg = ("Successfully Registered!")
        #send_lead_task.delay(user.username,detail1.first_name,p,detail2.phone_no,detail2.shop_name,detail2.shop_address,lead.email,user.first_name,lead.member.username,detail2.website) 
        return cust_detail
    
    
class promotionReopenSerializer(serializers.ModelSerializer):
    options=(('All','All'),('Lead','Lead'),('Customer','Customer'))
    display_to=serializers.ChoiceField(required=True,choices=options)
    from_date = serializers.DateField(format="%d-%m-%Y", input_formats=None)
    to_date = serializers.DateField(format="%d-%m-%Y", input_formats=None)
    

    class Meta:
        model = Promotions
        fields=('id', 'discount', 'description', 'from_date', 'to_date','price','image','company','model_id','make_year','Service_id','total_amount','display_to','member')
        
    def create(self, validated_data):
        today=datetime.today()
        request = self.context.get("request")
        #pk = self.context.get("pk")
        user= request.user
        #querySet = Promotions.objects.filter(member= user)
        promotion_id=self.context['pk']  
        promotion=Promotions.objects.get(pk=promotion_id)
                
        var  = Promotions(
                          discount=validated_data['discount'],
                          price=validated_data['price'],
                          total_amount = validated_data['total_amount'],
                          date_promo=today,
                          description = promotion.description,
                          from_date = promotion.from_date,
                          to_date = promotion.to_date,
                          company = promotion.company,
                          model_id = promotion.model_id,
                          make_year = promotion.make_year,
                          Service_id = promotion.Service_id,
                          display_to = promotion.display_to,
                          member = user,
                          )
        var.save()
        print("in promo reopn---",var)
        return var
        


class crm_customer_gallery_serializer(serializers.ModelSerializer):
    options=(('Miscellaneous','Miscellaneous'),('Warranty','Warranty'),('Images','Images'))
    type=serializers.ChoiceField(required=True,choices=options)
    class Meta:
        model = CrmCustomerGallery
        fields = ('name','description','type','file')
        
    def create(self, validated_data):
        request = self.context.get("request")
        user= request.user
        print("user in gallery",user)
        today=datetime.today()
        lead = Lead.objects.get(email=user)
        #lead = CrmCustomerGallery.objects.filter(customer = user.pk)
        print("lead in gallery--",lead)
        lead_obj = CrmCustomerGallery(
                                      name=validated_data['name'],
                                      description=validated_data['description'],
                                      type=validated_data['type'],
                                      file=validated_data['file'],
                                      created_date=today,
                                      date_updated=today,
                                      customer=lead
                                    
                                      )
        lead_obj.save()
        return lead_obj
    
    
    
class list_customer_gallery_serializer(serializers.ModelSerializer):
#     options=(('Miscellaneous','Miscellaneous'),('Warranty','Warranty'),('Images','Images'))
#     type=serializers.ChoiceField(required=True,choices=options)
    class Meta:
        model = CrmCustomerGallery
        fields = ('id','name','description','type','file','created_date','date_updated')


 
class list_expence_type_serializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseType
        
        
class expence_details_serializer(serializers.ModelSerializer):
    options=(('Cash','Cash'),('Cheque','Cheque'),('Card','Card'))
    payment_type=serializers.ChoiceField(required=True,choices=options)
    options=(('Inclusive','Inclusive'),('Exclusive','Exclusive'))
    tax=serializers.ChoiceField(required=True,choices=options)
    class Meta:
        model = ExpenseDetails
        fields = ('payment_type','date','total','tax')
        
        
        
class expence_subdetails_serializer(serializers.ModelSerializer):
    #expense_details = expence_details_serializer()
    #expense_type = serializers.CharField(source = 'expense_type.expense_type')
    options=(('Cash','Cash'),('Cheque','Cheque'),('Card','Card'))
    payment_type=serializers.ChoiceField(required=True,choices=options)
    options=(('Inclusive','Inclusive'),('Exclusive','Exclusive'))
    tax=serializers.ChoiceField(required=True,choices=options)
    
    class Meta:
        model = ExpenseDetails
        fields = ('payment_type','date','total','tax','expense_type','image','description')
        
    def create(self, validated_data):
        request = self.context.get("request")
        print("user---",request.user)
        lead_user_obj= lead_user.objects.get(user=request.user)
        print("--------",lead_user_obj)
        lead_obj=Lead.objects.get(pk=lead_user_obj.customer.pk)
        print("--------",lead_obj)
#         tracks_data = validated_data.pop('expense_details')
        expense_type = validated_data['expense_type']
        
        expense_type_obj = ExpenseType.objects.get(expense_type=expense_type)
        print("expense_type_obj",expense_type_obj)
        image = validated_data['image']
        description = validated_data['description']
       # customer = customer.customer,
        payment_type = validated_data['payment_type']
#         date = today,
        total = validated_data['total']
        tax = validated_data['tax']
        print("************************************",validated_data['tax'])
        today=datetime.today()
        
        expense_details_obj = ExpenseDetails.objects.create(        
                expense_type = expense_type_obj,
                image = image,
                description = description,
                customer = lead_obj,
                payment_type = payment_type,
                date = today.date(),
                total = total,
                tax =tax)
        
        expense_details_obj.save()
        print("expense_details_obj.save()--",expense_details_obj.save())                                               
                                                                 
        
        return expense_details_obj#.save()
class list_of_expence_details_serializer(serializers.ModelSerializer):
    #expense_details = expence_details_serializer()
    expense_type = serializers.CharField(source = 'expense_type.expense_type')
    class Meta:
        model = ExpenseDetails