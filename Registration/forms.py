from Registration.models import UserProfile,EBC
from django.contrib.auth.models import User
from django import forms
from CRM.models import *
from captcha.fields import ReCaptchaField

class MonospaceForm(forms.Form):
    def addError(self, message):
  	self._errors[NON_FIELD_ERRORS] = self.error_class([message])
  
class CardForm(MonospaceForm):
  
  last_4_digits = forms.CharField(
    required = True,
    min_length = 4,
    max_length = 4,
    widget = forms.HiddenInput()
 )
  
  stripe_token = forms.CharField(
    required = True,
    widget = forms.HiddenInput()
  )

class UserForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name",widget=forms.TextInput(attrs={'required':'true','class':'form-control col-sm-3','type':'text', 'maxlength':'30','id':'id_first_name'}))
    last_name = forms.CharField(label="Last Name",widget=forms.TextInput(attrs={'required':'true','class':'form-control col-sm-3','type':'text', 'maxlength':'30','id':'id_last_name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'required':'true','class': 'form-control','type':'text', 'id':'id_email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required':'true','class': 'form-control','type':'password','id':'pass1','container': 'body'}))
    confirm_pass = forms.CharField(widget=forms.PasswordInput(attrs={'required':'true','class': 'form-control','type':'password','id':'pass2'}))
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['confirm_pass'].required = True
        
    class Meta:
        model = User
        fields = ('first_name','last_name','email', 'password','confirm_pass')
        
        def clean(self):
            if 'password' in self.cleaned_data and 'confirm_pass' in self.cleaned_data:
    
                if self.cleaned_data['password'] != self.cleaned_data['confirm_pass']:
                    raise forms.ValidationError(_("The two password fields did not match."))
            return self.cleaned_data
        
class UserProfileForm(forms.ModelForm):
     city=(('Australian Capital Territory','Australian Capital Territory'),('New South Wales','New South Wales'),('Northern Territory','Northern Territory'),('Queensland','Queensland'),('South Australia','South Australia'),('Tasmania','Tasmania'),('Victoria','Victoria'),('Western Australia','Western Australia'))     
     country=(('Select Country','Select Country'),('Australia','Australia'))
     phone_no= forms.CharField(label="Phone Number",widget=forms.TextInput(attrs={'class':'form-control ','type':'text','maxlength':'10', 'id':'id_phone_no'}))
     shop_name= forms.CharField(label="Shop name",widget=forms.TextInput(attrs={'class':'form-control ','type':'text','id':'id_shop_name'}))
     shop_address = forms.CharField(label="Shop Address",widget=forms.Textarea(attrs={'rows': 10,'cols': 40,'style': 'height: 7em;','class':'form-control','type':'text','id':'id_shop_address'}))     
     country = forms.ChoiceField(choices=country, widget=forms.Select(attrs={'class':'form-control'}))
     city = forms.ChoiceField(choices =city, widget=forms.Select(attrs={'class':'form-control',}))
     website= forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control ','type':'text','placeholder':'Non-Mandatory'}))
     abn= forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control ','type':'text','id':'id_abn','maxlength':'11'}))
     captcha = ReCaptchaField()
     area_code=forms.CharField(required=False,label="Area code",widget=forms.TextInput(attrs={'class':'form-control ','type':'text','maxlength':'2', 'id':'id_area_code'}))
     #landline_number = forms.CharField(required=False,label="Phone Number",widget=forms.TextInput(attrs={'class':'form-control ','type':'text','maxlength':'8', 'id':'landline_number'}))
     postal_code=forms.CharField(required=True,label="Postal code",widget=forms.TextInput(attrs={'class':'form-control ','type':'text','maxlength':'4', 'id':'id_post_code'}))

     class Meta:
        model = UserProfile
        fields = ('phone_no','shop_name','shop_address','city','country','captcha','website','abn','area_code','postal_code')
        
class UpdateProfileForm(forms.ModelForm):
     first_name = forms.CharField(label="First Name",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text', 'id':'fname','maxlength':'30'}))
     last_name = forms.CharField(label="Last Name",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','id':'lname','maxlength':'30'}))
     city=(('Australian Capital Territory','Australian Capital Territory'),('New South Wales','New South Wales'),('Northern Territory','Northern Territory'),('Queensland','Queensland'),('South Australia','South Australia'),('Tasmania','Tasmania'),('Victoria','Victoria'),('Western Australia','Western Australia'))
     country=(('Select Country','Select Country'),('Australia','Australia'))
     phone_no= forms.CharField(label="Phone Number",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'10','id':'phone_num'}))
     shop_name= forms.CharField(label="Shop name",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'50','id':'shop_name'}))
     shop_address = forms.CharField(label="Shop Address",widget=forms.Textarea(attrs={'rows': 10,'cols': 40,'style': 'height: 7em;','class':'form-control form-text-input input-text input-text','type':'text','id':'id_shop_address'}))     
     country = forms.ChoiceField(choices=country, widget=forms.Select(attrs={'class':'form-control ','id':'country'}))
     city = forms.ChoiceField(choices=city, widget=forms.Select(attrs={'class':'form-control','id':'id_city',}))
     website= forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','placeholder':'Non-Mandatory'}) )
     Emg_no= forms.CharField(required=False,label="Emergency Number",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','placeholder':'Emergency Number','maxlength':'10','id':'id_Emg_no'}))
     area_code=forms.CharField(required=False,label="Area code",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'2', 'id':'id_area_code'}))
     #landline_number = forms.CharField(required=False,label="Phone Number",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'9', 'id':'landline_number'}))
     postal_code=forms.CharField(required=True,label="Postal code",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'4', 'id':'id_post_code'}))
     member_mech_license=forms.CharField(required=False,label="Member Mechanic License",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'45', 'id':'member_mech_license','placeholder':' Mechanic License'}))
     member_ARC_license=forms.CharField(required=False,label="Member ARC License",widget=forms.TextInput(attrs={'class':'form-control form-text-input input-text input-text','type':'text','maxlength':'45', 'id':'member_ARC_license','placeholder':' ARC License '}))
     member_mech_license_expiry_date=forms.DateField(required=False, input_formats=['%d/%m/%Y'],widget=forms.widgets.DateInput(format="%d/%m/%Y",attrs={'format':'%d/%m/%Y','class':'form-control form-text-input input-text input-text','placeholder':' Mechanic License Expiry Date'}))    
     member_ARC_license_expiry_date=forms.DateField(required=False, input_formats=['%d/%m/%Y'],widget=forms.widgets.DateInput(format="%d/%m/%Y",attrs={'format':'%d/%m/%Y','class':'form-control form-text-input input-text input-text','placeholder':' ARC License Expiry Date'}))
     

     class Meta:
        model = UserProfile
        fields = ('first_name','last_name','phone_no','shop_name','shop_address','city','country', 'website','Emg_no','area_code','postal_code','member_mech_license','member_ARC_license','member_mech_license_expiry_date','member_ARC_license_expiry_date')

        

        
class ChangePasswordForm(forms.ModelForm):
    oldPassword=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-text-input input-text input-text','type':'password', 'id':'old_password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-text-input input-text input-text','type':'password', 'id':'new_password', 'container': 'body'}))
    confirm_pass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-text-input input-text input-text','type':'password', 'id':'confirm_password'}))
    class Meta:
        model = User
        fields = ('oldPassword','new_password','confirm_pass')



class User_imageForm(forms.ModelForm):
    user_image = forms.FileField(required= False)
    class Meta:
        model=UserProfile
        fields=('user_image',)
        
class cust_imageForm(forms.ModelForm):
    image = forms.FileField(required= False)
    class Meta:
        model=Lead
        fields=('image',)
    

class EBCForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    name=forms.CharField(label="Name",widget=forms.TextInput(attrs={'class':'form-control','type':'text','maxlength':'20'}))

    class Meta:
        model=EBC
        fields=('email','name')

class company_imageForm(forms.ModelForm):
    image = forms.FileField(required= False)
    class Meta:
        model=CustCompany
        fields=('image',)