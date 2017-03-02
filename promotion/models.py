from __future__ import unicode_literals

from django.db import models
from CRM.models import *
from django.contrib.auth.models import User
from Registration.models import UserProfile

from django.db import models
from .models import *

# Create your models here.
    
class Service(models.Model):
    service_type= models.CharField(max_length=244)
    
    def __str__(self):
        return self.service_type
    
    class Meta:
        db_table="promotion_service"

       
class Promotions(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    model_id=models.ForeignKey(Company_Model,on_delete=models.CASCADE)
    make_year=models.ForeignKey(Make_Year1,on_delete=models.CASCADE)
    member=models.ForeignKey(User,on_delete=models.CASCADE)
    Service_id= models.ForeignKey(Service,on_delete=models.CASCADE)
    discount= models.IntegerField(blank=True, null=True)
    description= models.CharField(max_length=244, blank=True, null=True)
    from_date= models.DateField()
    to_date= models.DateField()
    coupon_code=models.CharField(max_length=12,blank=True, null=True)
    price= models.CharField(max_length=11, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    date_promo = models.DateField(blank=True, null=True)
    date_update = models.DateField(blank=True, null=True)
    display_to = models.CharField(max_length=20,blank=True, null=True)
    total_amount=models.IntegerField(blank=True, null=True)    
    def __str__(self):
        return self.description
    
    class Meta:
        db_table="promotion_promotions"
