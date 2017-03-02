from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


# Create your models here.
class Timeline(models.Model):
    comment1=models.CharField(max_length=100, null=True)
    comment2=models.CharField(max_length=100, null=True)
    action_create=models.DateTimeField(default=datetime.now, blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'timeline_timeline'

class Member_SMS(models.Model):
    member=models.ForeignKey(User,on_delete=models.CASCADE)
    count=models.IntegerField()
    
    class Meta:
        db_table="timeline_member_sms"
    
    def __str__(self):
        return "%s sent %s messages" %(self.member.first_name,self.count)