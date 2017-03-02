from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from promotion.models import Service
from CRM.models import *

# Create your models here.

class feedback_question(models.Model):
    question=models.CharField(max_length=200,null=False,blank=False)
    
    def __str__(self):
         return self.question
    
    class Meta:
        db_table = 'feedback_question'
        
class member_question(models.Model):
    question=models.CharField(max_length=200,null=False,blank=False)
    
    def __str__(self):
         return self.question
    
    class Meta:
        db_table = 'member_question'
        
        
class FeedbackSubquestion(models.Model):
    sub_question = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
         return self.sub_question
     
    class Meta:
        managed = False
        db_table = 'feedback_subquestion'
        
        
class feedback(models.Model):
    customer = models.ForeignKey(Lead, models.DO_NOTHING, blank=True, null=True)
    question = models.ForeignKey(feedback_question, models.DO_NOTHING, blank=True, null=True)
    answer = models.CharField(max_length=255, blank=True, null=True)
    sub_question = models.ForeignKey(FeedbackSubquestion, models.DO_NOTHING, db_column='sub_question', blank=True, null=True)
    sub_answer = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    feedback_date = models.DateField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'feedback_feedback'
        
class feedback_member(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.ForeignKey(member_question,on_delete=models.CASCADE)
    answer=models.CharField(max_length=255,null=False,blank=False)
    
    def __str__(self):
         return self.answer
    class Meta:
        db_table = 'feedback_member'
        


# feedback for customer
class Custfeedback(models.Model):
    customer = models.ForeignKey(Lead, models.DO_NOTHING, db_column='customer', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        
        ordering = ['date']
        db_table = 'feedback_custfeedback'


class Custfeedquestion(models.Model):
    feedback_cust = models.ForeignKey(Custfeedback, models.DO_NOTHING, db_column='feedback_cust', blank=True, null=True)
    question = models.ForeignKey(feedback_question, models.DO_NOTHING, db_column='question', blank=True, null=True)
    answer = models.CharField(max_length=45, blank=True, null=True)
    sub_question = models.ForeignKey(FeedbackSubquestion, models.DO_NOTHING, db_column='sub_question', blank=True, null=True)
    sub_answer = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback_custfeedquestion'


class Feedback_Star(models.Model):
    customer=models.ForeignKey(Lead,on_delete=models.CASCADE)
    comment=models.CharField(max_length=300)
    rating=models.IntegerField()
    feedback_date = models.DateField(blank=True, null=True)
    member=models.ForeignKey(User,on_delete=models.CASCADE)
    company=models.ForeignKey(CustCompany,on_delete=models.CASCADE,blank=True,null=True)
    class Meta:
        ordering=['-feedback_date']
        db_table="feedback_feedback_star"
