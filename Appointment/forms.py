from django import forms
from Appointment.models import *
from promotion.models import *
from django.contrib.admin.widgets import FilteredSelectMultiple

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    from_time = forms.CharField()
    to_time = forms.CharField()
    coment = forms.CharField(required= False, max_length=100)
    
    class Meta:
        model = MemberAppointment
        fields = ('date','from_time','to_time','coment')
        
class UpdateAppointmentForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    from_time = forms.CharField()
    to_time = forms.CharField()
    coment = forms.CharField(required= False, max_length=100)
    vehicle=forms.ModelChoiceField(queryset=Lead_Vehicle.objects.all(),required=False,widget=forms.Select(attrs={'class':'col-md-3 form-control'}))

    
    class Meta:
        model = MemberAppointment
        fields = ('date','from_time','to_time', 'coment','vehicle')

    
class Upcell_appointment_form(forms.ModelForm):
    #sub_service = forms.ModelMultipleChoiceField(queryset=SubServiceType.objects.all(),required= True, widget=FilteredSelectMultiple("verbose name", is_stacked=False))
    sub_service = forms.ModelMultipleChoiceField(queryset=SubServiceType.objects.all(),required=False, widget=forms.CheckboxSelectMultiple())
    service=forms.ModelChoiceField(queryset=Service.objects.all(),required= True, widget=forms.Select(attrs={'class':'col-md-1 form-control service_type'}))
    amount = forms.FloatField(required= False, widget=forms.TextInput(attrs={'class':'form-control tot_amount'}))
    total = forms.FloatField(required= False)
    description=forms.CharField(required= False, max_length=255, widget=forms.Textarea(attrs={'class':'form-control desc_text'}))
    accept = forms.BooleanField(required=False)
    image=forms.ImageField(required=False)
    
    class Meta:
        model = UpcellAppointment
        fields = ('sub_service','service','amount','total','description','accept','image')

class member_appointment(forms.Form):
    vehicle=forms.ModelChoiceField(queryset=Lead_Vehicle.objects.all(),required=False,widget=forms.Select(attrs={'class':'col-md-3 form-control'}))
    customer=forms.ModelChoiceField(queryset=Lead.objects.all(),required=False,widget=forms.Select(attrs={'class':'col-md-3 form-control'}))
    service_type=forms.ModelChoiceField(queryset=Service.objects.all(),widget=forms.Select(attrs={'class':'col-md-3 form-control'}))
    date = forms.DateField(input_formats=['%d/%m/%Y'],required=False, widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    from_time = forms.CharField()
    to_time = forms.CharField()
    
#     date_appointment=forms.CharField(widget=forms.TextInput(attrs={'class':'col-md-3 form-control'}))
#     date_update=forms.CharField(widget=forms.TextInput(attrs={'class':'col-md-3 form-control'}))
    coment = forms.CharField(required= False, max_length=100,widget=forms.TextInput(attrs={'class':'col-md-3 form-control'}))
       
    
    class Meta:
        model = MemberAppointment
        fields = ('customer','date','from_time','to_time','service_type','coment','vehicle')