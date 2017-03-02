
from rest_framework import serializers
from  promotion.models import *
from CRM.models import *


class promSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.company_name',read_only=True)
    model_name = serializers.CharField(source='model_id.model_name',read_only=True)
    makeyear = serializers.CharField(source='make_year.make_year',read_only=True)
    #description = serializers.CharField(source='MakeYear.company',read_only=True)
    #discount = serializers.CharField(source='MakeYear.company',read_only=True)
    #from_date = serializers.CharField(source='MakeYear.company',read_only=True)
    #to_date = serializers.CharField(source='MakeYear.company',read_only=True)
    #coupon_code = serializers.CharField(source='MakeYear.company',read_only=True)
    #image = serializers.CharField(source='MakeYear.company',read_only=True)
    service_id = serializers.CharField(source='Service_id.service_type',read_only=True)
    
    class Meta:
        model = Promotions
        fields=('service_id','company','model_name','makeyear','description', 'discount','from_date', 'to_date','coupon_code','image')
        