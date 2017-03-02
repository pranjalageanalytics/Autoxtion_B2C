from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.AppointmentList.as_view(), name='server_list'),
    url(r'^new/(?P<pk>\d+)$', views.AppointmentCreate.as_view(), name='server_new'),
    url(r'^edit/(?P<pk>\d+)$', views.AppointmentUpdate.as_view(), name='server_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.AppointmentDelete.as_view(), name='server_delete'),
    url(r'^app_done/(?P<pk>\d+)$', views.done_appointment, name='server_done'),

    url(r'^upcell_app_add/(?P<appointment_id>\d+)$', views.Upcell_app_add, name='upcell_app_add'),
    url(r'^upcell_app_update/(?P<appointment_id>\d+)$', views.upcell_app_update, name='upcell_app_update'),
    url(r'^customer_upcell_update/(?P<appointment_id>\d+)$', views.customer_upcell_update, name='customer_upcell_update'),
    url(r'^member_view_upcell_accepted/(?P<appointment_id>\d+)$', views.member_view_upcell_accepted, name='member_view_upcell_accepted'),
    url(r'^upcell_delete_ajax/(?P<upcell>\d+)$',views.upcell_delete_ajax, name='upcell_delete_ajax'),
    url(r'^appointment_history/$', views.appointment_history, name='appointment_history'),
    url(r'^subservice_ajax/$',views.subservice_ajax, name='subservice_ajax'),  
    url(r'^schedule_appointment/(?P<pk>\d+)$',views.schedule_appointment, name='schedule_appointment'),
    url(r'^create/$', views.member_create_appointment, name='member_create_appointment'),
    url(r'^get_leads/$',views.ajxviews,name='get_leads'),
    url(r'^today_appointment_list/$', views.today_appointment_list.as_view(), name='today_appointment_list'),
    url(r'^appointment_history_detail/(?P<appointment_id>[0-9]+)/$', views.Appointment_History_Detail, name='appointment_history_detail'),
    url(r'^get_vehicle/$', views.get_vehicle, name='get_vehicle'),
]