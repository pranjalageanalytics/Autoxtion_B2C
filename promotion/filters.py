import django_filters
from promotion.models import *

class PromotionFilter(django_filters.FilterSet):
    date_promo = django_filters.DateFromToRangeFilter()
    month_CHOICES = (('','Select month'),(1, 'January'),(2, 'February'),(3, 'March'),(4, 'April'),(5, 'May'),(6, 'June'),(7, 'July'),(8, 'August'),(9, 'September'),(10, 'October'),(11, 'November'),(12, 'December'),)
    month = django_filters.ChoiceFilter(name='date_promo__month',choices=month_CHOICES)
    
    class Meta:
        model = Promotions
        #exclude = ['Service_id', 'model_id','make_year','display_to','image','company','price','coupon_code','member','to_date','date_promo','discount','description']
        fields = ['date_promo','month']

class promohistoryFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='iexact')
    #date_request__gt = django_filters.DateFilter(name='date_request')
    from_date = django_filters.DateFromToRangeFilter()
    month_CHOICES = (('','Select month'),(1, 'January'),(2, 'February'),(3, 'March'),(4, 'April'),(5, 'May'),(6, 'June'),(7, 'July'),(8, 'August'),(9, 'September'),(10, 'October'),(11, 'November'),(12, 'December'),)
    month = django_filters.ChoiceFilter(name='from_date__month',choices=month_CHOICES)
   
    class Meta:
        model = Promotions
        fields = ['month','from_date']