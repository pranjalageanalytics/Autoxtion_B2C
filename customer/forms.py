from django import forms
from customer.models import customer_request
from promotion.models import Service
from CRM.models import *
from django.contrib.auth.models import User, Group

class customerForm(forms.ModelForm):
    vehicle=forms.ModelChoiceField(queryset=Lead_Vehicle.objects.all(),widget=forms.Select(attrs={'class':'col-md-3 form-control'}))
    date = forms.DateField(input_formats=['%d/%m/%Y'],required=False, widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    from_time = forms.CharField()
    to_time = forms.CharField()
    #coment = forms.CharField(required= False, max_length=100)
    service_type=forms.ModelChoiceField(queryset=Service.objects.all(),widget=forms.Select(attrs={'class':'col-md-3 form-control'}))   
    description= forms.CharField(widget=forms.Textarea)
    image=forms.ImageField(required=False)
    comment= forms.CharField(widget=forms.Textarea,required=False)     
    class Meta:
        model = customer_request
        fields = ('date','from_time','to_time','service_type','description','image','vehicle','comment')
    def __init__(self, *args, **kwargs):
        self.users = kwargs.pop('users', None)
        print("self.users self.users", self.users)
        super(customerForm, self).__init__(*args, **kwargs)
        group=Group.objects.get(user=self.users)
        try:
            if group.name=="Company":
                company=CustCompany.objects.get(email=self.users.email)
                print("company",company)
                driver1=Company_Driver.objects.filter(company=company)
                print("driver",driver1)
                for driver in driver1:
                    lead1=Lead.objects.get(pk=driver.driver.pk)
                    l_u=lead_user.objects.get(customer=lead1)
                    print("lead vehicle ",Lead_Vehicle.objects.filter(lead=l_u.customer))
                    self.fields['vehicle'].queryset= Lead_Vehicle.objects.filter(lead=l_u.customer)
                    
            else:
                lead_u=lead_user.objects.get(user=self.users)
                print("lead_u", lead_u.customer)
                self.fields['vehicle'].queryset= Lead_Vehicle.objects.filter(lead=lead_u.customer)

        except Exception as e:
            print("exception has occured",e)

        
class UpdatecustomerForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%d/%m/%Y'],required=False, widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    from_time = forms.CharField()
    to_time = forms.CharField()
    #coment = forms.CharField(required= False, max_length=100)
    service_type=forms.ModelChoiceField(queryset=Service.objects.all(),widget=forms.Select(attrs={'class':'col-md-3 form-control'}))   
    description= forms.CharField()
    image=forms.ImageField(required=False)   
    class Meta:
        model = customer_request
        fields = ('date','from_time','to_time','service_type','description','image')
    def __init__(self, *args, **kwargs):
        self.users = kwargs.pop('users', None)
        super(customerForm, self).__init__(*args, **kwargs)
        group=Group.objects.get(user=self.users)
        try:
            if group.name=="Company":
                company=CustCompany.objects.get(email=self.users.email)
                print("company",company)
                driver1=Company_Driver.objects.filter(company=company)
                print("driver",driver1)
                for driver in driver1:
                    lead1=Lead.objects.get(pk=driver.driver.pk)
                    l_u=lead_user.objects.get(customer=lead1)
                    print("lead vehicle ",Lead_Vehicle.objects.filter(lead=l_u.customer))
                    self.fields['vehicle'].queryset= Lead_Vehicle.objects.filter(lead=l_u.customer)
                    
            else:
                lead_u=lead_user.objects.get(user=self.users)
                print("lead_u", lead_u.customer)
                self.fields['vehicle'].queryset= Lead_Vehicle.objects.filter(lead=lead_u.customer)

        except Exception as e:
            print("exception has occured",e)

class customerMemberEditForm(forms.ModelForm):
    vehicle=forms.ModelChoiceField(queryset=Lead_Vehicle.objects.all(),widget=forms.Select(attrs={'class':'col-md-3 form-control'}))
    date = forms.DateField(input_formats=['%d/%m/%Y'],required=False, widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    from_time = forms.CharField()
    to_time = forms.CharField()
    #coment = forms.CharField(required= False, max_length=100)
    service_type=forms.ModelChoiceField(queryset=Service.objects.all(),widget=forms.Select(attrs={'class':'col-md-3 form-control'}))   
    description= forms.CharField(widget=forms.Textarea)
    image=forms.ImageField(required=False)
    comment= forms.CharField(widget=forms.Textarea,required=False)  
   
    class Meta:
        model = customer_request
        fields = ('date','from_time','to_time','service_type','description','image','vehicle','comment')


class customerRequestPromotionForm(forms.ModelForm):
    #vehicle=forms.ModelChoiceField(queryset=Lead_Vehicle.objects.all(),widget=forms.Select(attrs={'class':'col-md-3 form-control'}))
    date = forms.DateField(input_formats=['%d/%m/%Y'],required=False, widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    from_time = forms.CharField()
    to_time = forms.CharField()
    #coment = forms.CharField(required= False, max_length=100)
    service_type=forms.ModelChoiceField(queryset=Service.objects.all(),widget=forms.Select(attrs={'class':'col-md-3 form-control'}))   
    description= forms.CharField(widget=forms.Textarea)
    image=forms.ImageField(required=False)   
    class Meta:
        model = customer_request
        fields = ('date','from_time','to_time','service_type','description','image')

       