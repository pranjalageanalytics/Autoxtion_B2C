from django.contrib import admin
from Feedback.models import *
# Register your models here.
admin.site.register(feedback)
admin.site.register(feedback_question)
admin.site.register(member_question)
admin.site.register(feedback_member)
admin.site.register(FeedbackSubquestion)
admin.site.register(Custfeedback)
admin.site.register(Custfeedquestion)