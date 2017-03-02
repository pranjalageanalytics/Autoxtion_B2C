from django import forms
from .models import *
from django.forms.widgets import Widget
from django.db.models.query import QuerySet



class LeadForm(forms.ModelForm):
    id=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'id','type':'hidden','class':'form-control'}))
    name=forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    address=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text'}))
    licenseid=forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'type':'email','class':'form-control form-text-input input-text input-text'}))
    phone=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'10' }))
    Emg_no= forms.CharField(required=False,label="Emergency Number",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','placeholder':'Emergency Number','maxlength':'10','id':'id_Emg_no'}))
    road_side_assistant_num= forms.CharField(required=False,label="Road Side Assistant Number",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','placeholder':'Road Side Assistant Number','maxlength':'10','id':'id_roadsides_no'}))
    policy_number= forms.CharField(required=False,label="Policy Number",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','placeholder':'Policy Number','maxlength':'10','id':'id_policy_no'}))
    license_expiry_date = forms.DateField(required=False, input_formats=['%d/%m/%Y'],widget=forms.widgets.DateInput(format="%d/%m/%Y",attrs={'format':'%d/%m/%Y','class':'id_date form-control form-text-input input-text input-text','placeholder':'License expiry-date'}))
    area_code=forms.CharField(required=False,label="Area code",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'2', 'id':'id_area_code'}))
    postal_code = forms.CharField(required=False,label="Postal Code",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'4','id':'id_postal_code'}))

    class Meta:
        model=Lead
        fields={"id","name","last_name","address","licenseid","email","phone","Emg_no","road_side_assistant_num","policy_number","license_expiry_date","area_code","postal_code"}


        
        
class LeadVehicle_Form(forms.ModelForm):
    vehicle_no=forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'vehicle_no col-md-1 form-control'}))
    company=forms.ModelChoiceField(queryset=Company.objects.all(),widget=forms.Select(attrs={'class':'company col-md-1 form-control'}))
    model=forms.ModelChoiceField(queryset=Company_Model.objects.all(),widget=forms.Select(attrs={'class':'model col-md-1 form-control'}))    
    makeyear=forms.ModelChoiceField(queryset=Make_Year1.objects.all().order_by('make_year'),widget=forms.Select(attrs={'class':'makeyear col-md-1 form-control'}))
    reg_expiry_date=forms.DateField(required=False, input_formats=['%d/%m/%Y'],widget=forms.widgets.DateInput(format="%d/%m/%Y",attrs={'format':'%d/%m/%Y','class':'id_date form-control','placeholder':'Registration expiry date'}))    
    vin_no=forms.CharField(label="VIN Number",required=False,widget=forms.TextInput(attrs={'class':'form-control vin_box','maxlength':'17',}))
    #chasis_no=forms.CharField(label="Chasis Number",required=False,widget=forms.TextInput(attrs={'class':'form-control ','maxlength':'6'}))
    chasis_no=forms.CharField(label="Chasis Number",required=False,widget=forms.TextInput(attrs={'class':'chasis_no form-control ','maxlength':'6'}))
    class Meta:
        model=Lead_Vehicle
        fields={"vehicle_no","model","company","makeyear", "reg_expiry_date","vin_no","chasis_no",}
        exclude={"lead"}
        

        
class QualifyForm(forms.ModelForm):
    choice=(('No','No'),('Yes','Yes'))
    question=forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'col-md-1 form-control','readonly':'readonly'}))
    answer=forms.ChoiceField(required=False,choices=choice,widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model=Qualify
        exclude={"lead","question"}
        
        
        
        
class Vehicle_Form(forms.ModelForm):
    vehicle_no=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter vehicle number','type':'text','class':'col-md-1 form-control'}))
    company=forms.ModelChoiceField(queryset=Company.objects.all(),widget=forms.Select(attrs={'class':'col-md-1 form-control','id':'id_form-0-company'}))
    model=forms.ModelChoiceField(queryset=Company_Model.objects.all(),widget=forms.Select(attrs={'class':'col-md-1 form-control','id':'id_form-0-model'}))    
    makeyear=forms.ModelChoiceField(queryset=Make_Year1.objects.all().order_by('make_year'),widget=forms.Select(attrs={'class':'col-md-1 form-control','id':'id_form-0-makeyear'}))
    reg_expiry_date=forms.DateField(required=False, input_formats=['%d/%m/%Y'],widget=forms.widgets.DateInput(format="%d/%m/%Y",attrs={'format':'%d/%m/%Y','class':'form-control','placeholder':'Registration expiry date'}))    
    vin_no=forms.CharField(label="VIN Number",required=False,widget=forms.TextInput(attrs={'class':'form-control vin_box','maxlength':'17',}))
    chasis_no=forms.CharField(label="Chasis Number",required=False,widget=forms.TextInput(attrs={'class':'form-control ','maxlength':'6'}))
    
    class Meta:
        model=Lead_Vehicle
        fields={"vehicle_no","model","company","makeyear", "reg_expiry_date","vin_no","chasis_no",}
        exclude={"lead"}



class ExcelForm(forms.ModelForm):
    class Meta:
        model=UploadFile
        fields=["file"]

class CustomerForm(forms.ModelForm):
    id=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'id','type':'hidden','class':'form-control'}))
    name=forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    address=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text'}))
    licenseid=forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'type':'email','class':'form-control form-text-input input-text input-text'}))
    phone=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'10' }))
    Emg_no= forms.CharField(required=False,label="Emergency Number",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','placeholder':'Emergency Number','maxlength':'10','id':'id_Emg_no'}))
    #member=forms.ModelChoiceField(required=True,queryset=User.objects.filter(username="charlee@yopmail.com"),widget=forms.Select(attrs={'class':'form-control ',}))
    road_side_assistant_num= forms.CharField(required=False,label="Road Side Assistant Number",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','placeholder':'Road Side Assistant Number','maxlength':'20','id':'id_roadsides_no'}))
    policy_number= forms.CharField(required=False,label="Policy Number",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','placeholder':'Policy Number','maxlength':'20','id':'id_policy_no'}))
    license_expiry_date = forms.DateField(required=False, input_formats=['%d/%m/%Y'],widget=forms.widgets.DateInput(format="%d/%m/%Y",attrs={'format':'%d/%m/%Y','class':'form-control form-text-input input-text input-text','placeholder':'License expiry-date'}))
    area_code=forms.CharField(required=False,label="Area code",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'2', 'id':'id_area_code'}))
    postal_code = forms.CharField(required=False,label="Postal Code",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'4','id':'id_postal_code'}))

    class Meta:
        model=Lead
        fields={"id","name","address","licenseid","email","phone","Emg_no","last_name","road_side_assistant_num","policy_number","license_expiry_date","area_code","postal_code"}

class CompanyForm(forms.Form):
    company_name=forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    address=forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control form-text-input input-text input-text','cols':'10','rows':'5'}))
    email=forms.EmailField(required=False,widget=forms.TextInput(attrs={'type':'email','class':'email form-control form-text-input input-text input-text'}))
    phone=forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'10' }))
    person=forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    class Meta:
        #model=CustCompany
        fields={"company_name","address","email","phone","person"}

class CompanyVehicleForm(forms.Form):
    #email=forms.EmailField(widget=forms.TextInput(attrs={'type':'email','class':'form-control form-text-input input-text input-text'}))
    name=forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'form-control f_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'last_name form-control'}))
    address=forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    licenseid=forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'type':'email','class':'email form-control'}))
    phone=forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control phone_no','type':'text','maxlength':'10' }))
    Emg_no= forms.CharField(required=False,label="Emergency Number",widget=forms.TextInput(attrs={'class':'form-control ','type':'text','placeholder':'Emergency Number','maxlength':'10','id':'id_Emg_no'}))
# vehicle field
    vehicle_no=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter vehicle number','type':'text','class':'vehicle_no col-md-1 form-control'}))
    company=forms.ModelChoiceField(queryset=Company.objects.all(),widget=forms.Select(attrs={'class':'company col-md-1 form-control','id':'id_form-0-company'}))
    model=forms.ModelChoiceField(queryset=Company_Model.objects.all(),widget=forms.Select(attrs={'class':'model col-md-1 form-control','id':'id_form-0-model'}))
    makeyear=forms.ModelChoiceField(queryset=Make_Year1.objects.all().order_by('make_year'),widget=forms.Select(attrs={'class':'makeyear col-md-1 form-control','id':'id_form-0-makeyear'}))
    reg_expiry_date=forms.DateField(required=False, input_formats=['%d/%m/%Y'],widget=forms.widgets.DateInput(format="%d/%m/%Y",attrs={'format':'%d/%m/%Y','class':'id_date class_date form-control','placeholder':'Registration expiry date'}))
    vin_no=forms.CharField(label="VIN Number",required=False,widget=forms.TextInput(attrs={'class':'form-control vin_box','maxlength':'17'}))
    #chasis_no=forms.CharField(label="Chasis Number",required=False,widget=forms.TextInput(attrs={'class':'form-control ','maxlength':'6'}))
    chasis_no=forms.CharField(label="Chasis Number",required=False,widget=forms.TextInput(attrs={'class':'chasis_no form-control ','maxlength':'6'}))
    class Meta:
        #model=CompanyVehicle
        fields={"Emg_no","phone","email","vehicle_no","company","model","makeyear","reg_expiry_date","vin_no","chasis_no","name","last_name","address","licenseid"}

        

class CompanyUpdateForm(forms.ModelForm):
    company_name=forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    address=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control form-text-input input-text input-text','cols':'10','rows':'5'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'type':'email','class':'email form-control form-text-input input-text input-text'}))
    phone=forms.CharField(widget=forms.TextInput(attrs={'class':'phone form-control form-text-input input-text input-text','type':'text','maxlength':'10' }))
    person=forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    class Meta:
        model=CustCompany
        fields={"company_name","address","email","phone","person"}

class DriverForm(forms.ModelForm):
    
    name=forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'f_name form-control form-text-input input-text input-text'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'last_name form-control form-text-input input-text input-text'}))
    address=forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text'}))
    licenseid=forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'type':'email','class':'email form-control form-text-input input-text input-text'}))
    phone=forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'phone_no form-control form-text-input input-text input-text','type':'text','maxlength':'10' }))
    license_expiry_date = forms.DateField(required=False, input_formats=['%d/%m/%Y'],widget=forms.widgets.DateInput(format="%d/%m/%Y",attrs={'format':'%d/%m/%Y','class':'form-control form-text-input input-text input-text','placeholder':'License expiry-date'}))


    class Meta:
        model=Lead
        fields={"name","last_name","address","licenseid","email","phone",'license_expiry_date'}

class CustForm(forms.ModelForm):
    company_name=forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    address=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control form-text-input input-text input-text','cols':'10','rows':'5'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'type':'email','class':'form-control form-text-input input-text input-text'}))
    phone=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'10' }))
    person=forms.CharField(widget=forms.TextInput(attrs={'type':'text','class':'form-control form-text-input input-text input-text'}))
    class Meta:
        model=CustCompany
        fields={"company_name","address","email","phone","person"}