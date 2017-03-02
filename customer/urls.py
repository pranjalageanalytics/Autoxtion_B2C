from django.conf.urls import url, include
from django.contrib import admin
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
              
   url(r'^$', views.RequestList.as_view(), name='server_list'),
   #url(r'^$', views.CustomerRequestList, name='server_list'),
   url(r'^new_req/$', views.RequestnewCreate.as_view(), name='server_new_req'),
   url(r'^new/(?P<pk>\d+)$', views.RequestCreate.as_view(), name='server_new'),
   url(r'^edit/(?P<pk>\d+)$', views.RequestUpdate.as_view(), name='server_edit'),
   url(r'^delete/(?P<pk>\d+)$', views.RequestDelete.as_view(), name='server_delete'),
   url(r'^get_lead/',views.get_lead),
   #url(r'^get_promo/(?P<requestid>\d+)$',views.get_promo.as_view()),
   url(r'^memberedit/(?P<pk>\d+)$',views.MemberEditRequest.as_view(), name='member_edit_request'),
   url(r'^confirm/(?P<customer_request_id>[0-9]+)/$',views.ConfirmRequest, name='confirm_request'),
   url(r'^accept/(?P<customer_request_id>[0-9]+)/$',views.AcceptRequest, name='accept_request'),


   url(r'^customer_history/$', views.customer_history.as_view(), name='customer_history'),
   url(r'^EmergencyRequestList/$', views.EmergencyRequestList.as_view(), name='EmergencyRequestList'),
   url(r'^Add_emergency_req/$', views.Add_emergency_req.as_view(), name='Add_emergency_req'),
   url(r'^edit_emergency_req/(?P<pk>\d+)$', views.edit_emergency_req.as_view(), name='edit_emergency_req'),
   url(r'^membereditemergency/(?P<pk>\d+)$',views.MemberEditRequestEmergency.as_view(), name='member_edit_emergency'),
   url(r'^delete_emergency_req/(?P<pk>\d+)$', views.delete_emergency_req.as_view(), name='delete_emergency_req'),
   url(r'^emer_confirm/(?P<customer_request_id>[0-9]+)/$',views.Emer_ConfirmRequest, name='emer_confirm_request'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])