from django import forms
from .models import *
from django.forms.widgets import Widget


class FeedbackFormCust(forms.ModelForm):
    question=forms.ModelChoiceField(required=False,queryset=feedback_question.objects.all(),widget=forms.Select(attrs={'type':'text','class':'col-md-3 form-control'}))
    answer=forms.ChoiceField(choices=(('Yes', 'Yes'), ('No', 'No')),widget=forms.Select(attrs={'class':'form-control col-sm-3 viewOnlyAccess classActivityType'}))    
    sub_question=forms.ModelChoiceField(required=False,queryset=FeedbackSubquestion.objects.all(),widget=forms.Select(attrs={'type':'text','class':'col-md-1 form-control'}))
    sub_answer=forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    
    class Meta:
        model=Custfeedquestion
        fields = ('question','answer','sub_question','sub_answer')
        
class FeedbackForm(forms.ModelForm):
    question=forms.ModelChoiceField(required=False,queryset=member_question.objects.all(),widget=forms.Select(attrs={'type':'text','class':'col-md-1 form-control'}))
    answer=forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control','required':'required'}))
    
    class Meta:
        model=feedback_member
        fields = ('question','answer')
 
class FeedbackFormCust2(forms.ModelForm):
    question=forms.ModelChoiceField(queryset=feedback_question.objects.all(),widget=forms.Select(attrs={'type':'text','class':'col-md-3 form-control'}))
    answer=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control col-sm-3 viewOnlyAccess classActivityType'}))    
    sub_question=forms.ModelChoiceField(required=False,queryset=FeedbackSubquestion.objects.all(),widget=forms.Select(attrs={'type':'text','class':'col-md-1 form-control'}))
    sub_answer=forms.CharField(required=False,widget=forms.TextInput(attrs={'type':'text','class':'form-control'}))
    
    class Meta:
        model=feedback
        fields = ('question','answer','sub_question','sub_answer')       


class showrating(forms.Form):
    customer=forms.CharField(widget=forms.TextInput(),required=False)
    comment=forms.CharField(widget=forms.TextInput(),required=False)
    rating=forms.CharField(widget=forms.HiddenInput(),required=False)
    feedback_date=forms.CharField(widget=forms.TextInput(),required=False)
    class Meta:
        model=Feedback_Star
        fields={'customer','comment','rating','feedback_date'}