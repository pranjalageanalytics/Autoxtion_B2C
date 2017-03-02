import django_filters
from Feedback.models import *

class FeedbackFilter(django_filters.FilterSet):
    feedback_date = django_filters.DateFromToRangeFilter()
    month_CHOICES = (('','Select month'),(1, 'January'),(2, 'February'),(3, 'March'),(4, 'April'),(5, 'May'),(6, 'June'),(7, 'July'),(8, 'August'),(9, 'September'),(10, 'October'),(11, 'November'),(12, 'December'),)
    month = django_filters.ChoiceFilter(name='feedback_date__month',choices=month_CHOICES)
    
    class Meta:
        model = feedback
        #exclude = ['Service_id', 'model_id','make_year','display_to','image','company','price','coupon_code','member','to_date','date_promo','discount','description']
        fields = ['feedback_date','month']