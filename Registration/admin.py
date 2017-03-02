from django.contrib import admin
from Registration.models import UserProfile, UserLogin

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__email','phone_no','shop_name','shop_address','city','website')
    list_filter = ('city',)
    list_display = ('user','phone_no','shop_name','shop_address','city','country','website','abn')
    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserLogin)
