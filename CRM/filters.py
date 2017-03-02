import django_filters
from CRM.models import *
from customer.models import *

class LeadFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    
    
#     user = django_filters.BooleanFilter(method='filter_published')
# 
#     def filter_published(self, queryset, name, value):
#         # construct the full lookup expression.
#         request = self.context.get("request")
#         print("@@@@@@@@@@",request.POST.get("date_appointment_0"))
#         return queryset.filter(**{lookup: False})
# 
#         # alternatively, it may not be necessary to construct the lookup.
#         return queryset.filter(published_on__isnull=False)
    
    class Meta:
        model = Lead
        fields = ['name','email','member__date_joined']
        
class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Lead
        fields = ['name', 'last_name','status','email']
        
