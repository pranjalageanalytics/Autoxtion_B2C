from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views
from django.core.urlresolvers import reverse_lazy,reverse

app_name = 'Registration'

urlpatterns = [
    url(r'^login/$', views.login,name='login'),

    url(r'^member_login/$', views.member_login,name='member_login'),
    url(r'^customer_login/$', views.customer_login,name='customer_login'),

    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page':'/registration/login'}),
    url(r'^register/$', views.register, name='register'),
    url(r'^updatedetails/(?P<user_id>[0-9]+)', views.updatedetails, name='updatedetails'),
    url(r'^success/$', views.success, name='success'),
    url(r'^EBC/(?P<user_id>[0-9]+)', views.businesscard, name='businesscard'),
    url(r'^EBC_cust/(?P<user_id>[0-9]+)', views.businesscard_cust, name='businesscard_cust'),
    url(r'^FAQ/$', views.faq,name='faq'),
    url(r'^enroll/$', views.enroll,name='enroll'),
    url(r'^usermanual/$',views.pdfopen,name='pdfopen'),
    url(r'^payment/$',views.payment),
    url(r'^newpayment/$',views.newpayment),
    url(r'^unsubscribe/$',views.unsubscribe),
    url(r'^subscribe/$',views.subscribe,name="subscribe"),
    url(r'^resubscribe/$',views.resubscribe),
    url(r'^demologin/$',views.demologin,name='demologin'),  
    url(r'^get_vcard/$',views.getVcard,name='sendebc'),
    url(r'^get_vcard1/$',views.getVcard1,name='sendcard'),
    url(r'^user_image/(?P<user_id>[0-9]+)', views.user_image, name='user_image'),
    url(r'^user_header_image/$',views.user_header_image, name='user_header_image'),
    url(r'^Contct_us/$', views.contact,name='contact'),
    url(r'^Video_tutorial/$', views.Video_tutorial,name='Video_tutorial'),
    url(r'^member_agree/$', views.member_agree,name='member_agree'),
    url(r'^member_agree2/$', views.member_agree2,name='member_agree2'),
    url(r'^unlink_member/$', views.unlink_member,name='unlink_member'),
]
    