#from __future__ import unicode_literals
from Registration.models  import *
from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    company_name=models.CharField(max_length=100,null=False,blank=False)

    def __str__(self):
        return str(self.company_name) or u''
    class Meta:
        ordering = ["company_name"]
        db_table='crm_company'
        
        
    
        
class Company_Model(models.Model):
    model_name=models.CharField(max_length=100,null=False,blank=False)
    
    company=models.ForeignKey(Company,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.model_name) or u''
    class Meta:
        ordering = ["model_name"]
        db_table = 'crm_company_model'

class MakeYear(models.Model):
    makeyear=models.IntegerField(null=False,blank=False)
    model=models.ForeignKey(Company_Model,default=None,on_delete=models.CASCADE)
       
    def __str__(self):
        return str(self.makeyear) or u''
    class Meta:
        db_table='crm_makeyear'
        
class Make_Year1(models.Model):
    make_year=models.CharField(max_length=4, null=False,blank=False)
    #model=models.ForeignKey(Company_Model,default=None,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.make_year) or u''
    
    class Meta:
        db_table='crm_make_year1'

    
class Status(models.Model):
    status=models.CharField(max_length=20) 


    def __str__(self):
        return  self.status or u''
    class Meta:
        db_table = 'crm_status'

class Lead(models.Model):
    
    name=models.CharField(max_length=30,blank=False,null=False)
    last_name=models.CharField(max_length=30,blank=False,null=False)
    address=models.CharField(max_length=200,blank=False,null=False)
    licenseid=models.CharField(max_length=20,blank=True,null=True)
    email=models.EmailField(max_length=60,blank=True,null=True)
    phone=models.CharField(blank=True,null=True,max_length=10)
    status=models.ForeignKey(Status,on_delete=models.CASCADE)
    member=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    cred=models.BooleanField()
    image = models.ImageField(blank=True, null=True)
    Emg_no=models.CharField(max_length=10, null=True,blank=True)
    add_by=models.CharField(max_length=12,null=True,blank=True)
    road_side_assistant_num=models.CharField(blank=True,null=True,max_length=20)
    policy_number=models.CharField(blank=True,null=True,max_length=20)
    license_expiry_date = models.DateField(blank=True, null=True)
    area_code=models.CharField(null=True,blank=True,max_length=2)
    postal_code = models.CharField(max_length=4, null=True,blank=True)

    #member=models.ForeignKey
    def __str__(self):
        return self.name or u''
    class Meta:
        db_table = 'crm_lead'

class Lead_Vehicle(models.Model):
    id=models.AutoField(primary_key=True)
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE)
    vehicle_no=models.CharField(max_length=15,null=False,blank=False)
    model=models.ForeignKey(Company_Model,default=None,on_delete=models.CASCADE,null=True,blank=True)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    makeyear=models.ForeignKey(Make_Year1,on_delete=models.CASCADE)
    reg_expiry_date = models.DateField(blank=True, null=True)
    vin_no=models.CharField(max_length=17,null=True,blank=True)
    image=models.ImageField(blank=True,null=True)
    chasis_no=models.CharField(max_length=6,null=True,blank=True)
    def __str__(self):
        return self.vehicle_no or u''
    class Meta:
        db_table = 'crm_lead_vehicle'

class Question(models.Model):
    question=models.CharField(max_length=120,null=False,blank=False)

    def __str__(self):
        return self.question or u''
    class Meta:
        db_table = 'crm_question'
        
class Qualify(models.Model):
    lead=models.ForeignKey(Lead,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.CharField(max_length=3,null=False,blank=False)
    
    class Meta:
        db_table = 'crm_qualify'
        
class lead_user(models.Model):
    customer= models.ForeignKey(Lead, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table="lead_user" 
        
    def __str__(self):
        return self.customer.name or u''

class UploadFile(models.Model):
    file=models.FileField(upload_to="excel")

    class Meta:
        db_table="crm_uploadfile"

class CustCompany(models.Model):
    company_name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    email=models.EmailField(max_length=40)
    phone=models.CharField(blank=True,null=True,max_length=10)
    member=models.ForeignKey(User,on_delete=models.CASCADE)
    person=models.CharField(max_length=100)
    image=models.ImageField(blank=True,null=True)

    def __str__(self):
        return self.company_name or u''
    class Meta:
        db_table = 'crm_custcompany'

        
class Company_Driver(models.Model):
    company=models.ForeignKey(CustCompany,on_delete=models.CASCADE)
    driver=models.ForeignKey(Lead,on_delete=models.CASCADE)

    def __str__(self):
        return "%s is driver of %s" %(self.driver,self.company) or u''
    class Meta:
        db_table = 'crm_Company_Driver'

class CrmCustomerGallery(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    type = models.CharField(max_length=45)
    file = models.FileField(upload_to="gallery")
    date_updated = models.DateField()
    created_date = models.DateField()
    customer = models.ForeignKey(Lead,on_delete=models.CASCADE, db_column='customer', blank=True, null=True)

    class Meta:
        
        db_table = 'crm_customer_gallery'