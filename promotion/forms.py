from django import forms
from CRM.models import *
from promotion.models import *

from django.db.models.query import QuerySet

 
 
 
class PromotionForm(forms.ModelForm):
    options=(('All','All'),('Lead','Lead'),('Customer','Customer'))
    company=forms.ModelChoiceField(queryset=Company.objects.all(),widget=forms.Select(attrs={'class':'col-md-1 form-control'}))
    model_id=forms.ModelChoiceField(queryset=Company_Model.objects.all(),widget=forms.Select(attrs={'class':'col-md-1 form-control'}))    
    make_year=forms.ModelChoiceField(queryset=Make_Year1.objects.all().order_by('make_year'),widget=forms.Select(attrs={'class':'col-md-1 form-control'}))
    #series=forms.ModelChoiceField(required= False,queryset=Series.objects.all(),widget=forms.Select(attrs={'class':'col-md-1 form-control'}))
    #engine=forms.ModelChoiceField(required= False,queryset=Engine.objects.all(),widget=forms.Select(attrs={'class':'col-md-1 form-control'}))
    #car_variant=forms.ModelChoiceField(required= False,queryset=Car_Variant.objects.all(),widget=forms.Select(attrs={'class':'col-md-1 form-control'}))
    Service_id=forms.ModelChoiceField(queryset=Service.objects.all(),widget=forms.Select(attrs={'class':'col-md-1 form-control'}))
    price=forms.CharField(required= False, max_length= 5)
    discount=forms.CharField(required= False, max_length= 2)
    description=forms.CharField(required= False, max_length= 100)
    from_date= forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    to_date= forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.widgets.DateInput(format="%d/%m/%Y"))
    image=forms.ImageField(required= False)
    coupon_code=forms.CharField(required= False)
    display_to=forms.ChoiceField(choices =options, widget=forms.Select(attrs={'class':'form-control',}))
    total_amount=forms.CharField(required= False, max_length= 5)    
    class Meta:
        model = Promotions
        fields = ('company','model_id','make_year','Service_id','price','discount','description','from_date','to_date','image','coupon_code','display_to','total_amount',)
    