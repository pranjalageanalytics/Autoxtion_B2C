from __future__ import unicode_literals
from django.db import models
from CRM.models import Lead, Status
from customer.models import customer_request
from Registration.models import UserProfile
from promotion.models import *

# Create your models here.

class MemberAppointment(models.Model):
    vehicle= models.ForeignKey(Lead_Vehicle, on_delete=models.CASCADE)
    customer = models.ForeignKey(Lead, models.DO_NOTHING, blank=True, null=True)
    member = models.ForeignKey(UserProfile, models.DO_NOTHING, blank=True, null=True)
    request = models.ForeignKey(customer_request, models.DO_NOTHING, blank=True, null=True)
    status = models.ForeignKey(Status, models.DO_NOTHING, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    from_time= models.CharField(max_length=11)
    to_time= models.CharField(max_length=11)
    date_appointment = models.DateField(blank=True, null=True)
    date_update = models.DateField(blank=True, null=True)
    coment= models.CharField(max_length=255, blank=True, null=True)
    totalamount= models.FloatField(max_length=45, blank=True, null=True)
    service_type=models.ForeignKey(Service,models.DO_NOTHING, blank=True, null=True)
    upcell_status= models.CharField(max_length=45, blank=True, null=True)

   
    class Meta:
        managed = False
        db_table = 'member_appointment'

class SubServiceType(models.Model):
 
    service_type_name = models.CharField(max_length=45, blank=True, null=True)
    service = models.ForeignKey(Service, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sub_service_type'
        
    def __str__(self):
        return self.service_type_name
        
class UpcellAppointment(models.Model):
    
    appointment = models.ForeignKey(MemberAppointment,blank=True, null=True)
    service = models.ForeignKey(Service)
    sub_service = models.ManyToManyField(SubServiceType)
    amount = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    description= models.CharField(max_length=255, blank=True, null=True)
    accept = models.BooleanField()
    image= models.ImageField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'upcell_appointment'


class UpcellAppointmentSubService(models.Model):
    upcellappointment = models.ForeignKey(UpcellAppointment, blank=True, null=True)
    subservicetype = models.ForeignKey(SubServiceType, blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'upcell_appointment_sub_service'
