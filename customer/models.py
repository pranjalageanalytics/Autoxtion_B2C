from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
from promotion.models import Service
from CRM.models import Lead
from promotion.models import * 

# Create your models here.

"""class customer(models.Model):
    customer=models.OneToOneField(User)
    member= models.ForeignKey(User, on_delete=models.CASCADE)
    #group= models.ForeignKey(Group, on_delete=models.CASCADE)"""
    
class customer_request(models.Model):
    vehicle= models.ForeignKey(Lead_Vehicle, on_delete=models.CASCADE)
    service_type= models.ForeignKey(Service, on_delete=models.CASCADE)
    description=models.TextField()
    customer=models.ForeignKey(Lead, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotions, models.DO_NOTHING, blank=True, null=True)
    date_request = models.DateField(blank=True, null=True)
    date_update = models.DateField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    date = models.DateField(blank=True,null=True)
    from_time = models.CharField(max_length=11)
    to_time = models.CharField(max_length=11)
    status = models.ForeignKey(Status, models.DO_NOTHING, blank=True, null=True)
    emergency_status = models.BooleanField()
    comment=models.CharField(blank=True, null=True,max_length=300)

    def __str__(self):
         return self.description

    class Meta:
        db_table="customer_request"
        
class Accident_Request(models.Model):
    image1= models.ImageField(blank= True, null= True)
    image2= models.ImageField(blank=True, null=True)
    car_detail= models.CharField(max_length= 100, blank=True, null=True)
    location= models.CharField(max_length=100, blank= True, null=True)
    phone_no = models.CharField(max_length=10, blank= True, null=True)
    customer=models.ForeignKey(Lead, on_delete=models.CASCADE)
    date_request = models.DateField(blank=True, null=True)
    date_update = models.DateField(blank=True, null=True)
    status = models.ForeignKey(Status, models.DO_NOTHING, blank=True, null=True)
    
    def __str__(self):
        return self.location
    
    class Meta:
        db_table="customer_accident_request"

class Customer_Outsource_History(models.Model):
    member_name= models.CharField(max_length= 45, blank=True, null=True)
    shop_name= models.CharField(max_length=45, blank= True, null=True)
    phone_no = models.CharField(max_length=10, blank= True, null=True)
    date_request = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=100, blank= True, null=True)
    price = models.CharField(max_length=10, blank= True, null=True)
    customer=models.ForeignKey(Lead, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.description
    
    class Meta:
        db_table="customer_outsource_history"

        
class ExpenseType(models.Model):
    expense_type = models.CharField(db_column='expense _type', max_length=45)  # Field renamed to remove unsuitable characters.
    image = models.ImageField()

    class Meta:
        managed = False
        db_table = 'customer_expense _type'
	verbose_name_plural = 'ExpenseType'
        
    def __str__(self):
        return self.expense_type

class ExpenseDetails(models.Model):
    customer = models.ForeignKey(Lead,on_delete=models.CASCADE,blank=True, null=True)
    payment_type = models.CharField(max_length=45)
    date = models.DateField()
    total = models.IntegerField()
    tax = models.CharField(max_length=45)
    expense_type = models.ForeignKey(ExpenseType,on_delete=models.CASCADE,  db_column='expense_type')
    image = models.ImageField(blank=True, null=True)
    description = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'customer_expense_details'
    def __str__(self):
        return "%s" % self.id

