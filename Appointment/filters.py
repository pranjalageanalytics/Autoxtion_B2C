import django_filters
from Appointment.models import *

class AppointmentFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='iexact')
    #date_request__gt = django_filters.DateFilter(name='date_request')
    date = django_filters.DateFromToRangeFilter()
    month_CHOICES = (('','Select month'),(1, 'January'),(2, 'February'),(3, 'March'),(4, 'April'),(5, 'May'),(6, 'June'),(7, 'July'),(8, 'August'),(9, 'September'),(10, 'October'),(11, 'November'),(12, 'December'),)    
    month = django_filters.ChoiceFilter(name='date__month',choices=month_CHOICES)

    class Meta:
        model = MemberAppointment
        fields = ['status','date']

class appointmenthistoryFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='iexact')
    #date_request__gt = django_filters.DateFilter(name='date_request')
    date_update = django_filters.DateFromToRangeFilter()
    month_CHOICES = (('','Select month'),(1, 'January'),(2, 'February'),(3, 'March'),(4, 'April'),(5, 'May'),(6, 'June'),(7, 'July'),(8, 'August'),(9, 'September'),(10, 'October'),(11, 'November'),(12, 'December'),)
    month = django_filters.ChoiceFilter(name='date_update__month',choices=month_CHOICES)
   
    class Meta:
        model = MemberAppointment
        fields = ['status','date_update']   