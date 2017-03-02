from rest_framework import serializers
from CRM.models import *

class GetCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Lead