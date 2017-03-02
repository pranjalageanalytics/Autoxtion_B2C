from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime 
from CRM.models import *

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone_no= models.CharField(max_length=10,null=True)
    shop_name=models.CharField(max_length=244, null=True)
    shop_address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=20,null=True)
    country=models.CharField(max_length=20,null=True)
    abn=models.CharField(max_length=11)
    website = models.CharField(max_length=200, blank=True, null=True)
    #last_4_digits = models.CharField(max_length=4, default=False)
    #stripe_id = models.CharField(max_length=255, default=False)
    #subscribed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    Emg_no=models.CharField(max_length=10, null=True,blank=True)
    payment_date = models.DateTimeField(default=datetime.now, blank=True)
    area_code=models.CharField(null=True,blank=True,max_length=2)
    #landline_number= models.CharField(null=True,blank=True,max_length=9)
    status=models.ForeignKey(Status,blank=True,null=True)
    unsubscribe_date=models.DateField(blank=True,null=True)
    user_image = models.ImageField(upload_to='user_image')
    flag = models.BooleanField(default=False)
    postal_code=models.CharField(blank=True,null=True,max_length=4)
    billing_address=models.CharField(blank=True,null=True,max_length=45)
    member_mech_license=models.CharField(blank=True,null=True,max_length=45)
    member_mech_license_expiry_date=models.DateField(blank=True, null=True)
    member_ARC_license=models.CharField(blank=True,null=True,max_length=45)
    member_ARC_license_expiry_date=models.DateField(blank=True, null=True)

    def __str__(self):
         return self.user.first_name
    
    class Meta:
        db_table = 'registration_userprofile'
        
class UserLogin(models.Model):
    user = models.ForeignKey(User) 
    timestamp = models.DateTimeField()
    
    class Meta:
        db_table = 'registration_userlogin'

class Payment(models.Model):
    user = models.OneToOneField(User)
    last_4_digits = models.CharField(max_length=4,blank=True, null=True, default=False)
    stripe_id = models.CharField(max_length=255, blank=True, null=True,default=False)
    subscribed = models.BooleanField(default=False)  
    
    class Meta:
        db_table = "registration_payment"


class EBC(models.Model):
    email=models.EmailField(max_length=20,blank=True,null=True)
    name=models.CharField(max_length=20,blank=True,null=True)
    ebctime=models.DateField()  
    send_user=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        db_table='registration_ebc'