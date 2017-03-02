from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.i18n import i18n_patterns
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework import routers
from django.contrib.auth.views import password_reset
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet

router = routers.DefaultRouter()
#router.register(r'v1/rest/customer_upcell', views.acceptupcell,{'appointment_id'})
router.register(r'device/apns', APNSDeviceAuthorizedViewSet)
router.register(r'device/gcm', GCMDeviceAuthorizedViewSet)
router.register(r'devices', FCMDeviceAuthorizedViewSet)
urlpatterns =[

#promotions
    url(r'^v1/rest/member_all_promotions/$',  views.member_all_promotions.as_view()),
    url(r'^v1/rest/member_update_delete_promotion/(?P<pk>.+)/$',  views.member_update_delete_promotion.as_view()),
    url(r'^v1/rest/member_add_promotion/$',  views.member_add_promotion.as_view()),
    url(r'^v1/rest/customer_all_promotions/$',  views.customer_all_promotions.as_view()),
    url(r'^v1/rest/customer_5_promotions/$',  views.customer_5_promotions.as_view()),
    url(r'^v1/rest/search_promotion/$',  views.search_promotion.as_view()),
    
#Service Request
    url(r'^v1/rest/member_all_request/$',  views.member_all_request.as_view()),
    url(r'^v1/rest/customer_all_request/$',  views.customer_all_request.as_view()),
    #url(r'^v1/rest/customer_add_request/$',  views.customer_add_request.as_view()),
    #url(r'^v1/rest/customer_update_delete_request/(?P<pk>.+)/$',  views.customer_update_delete_request.as_view()),
    url(r'^v1/rest/customer_emer_request/$',  views.customer_emer_request.as_view()),
    url(r'^v1/rest/customer_add_emer_request/$',  views.customer_add_emer_request.as_view()),

    url(r'^v1/rest/customer_accident_request_list/$',  views.customer_accident_request_list.as_view()),
    url(r'^v1/rest/customer_add_request/$',  views.customer_add_request.as_view()),
    url(r'^v1/rest/customer_update_delete_request/(?P<pk>.+)/$',  views.customer_update_delete_request.as_view()),
    url(r'^v1/rest/customer_add_request_with_promotion/(?P<Promotions_pk>.+)$',  views.customer_add_requestwithpromotion.as_view()),
    url(r'^v1/rest/customer_update_delete_request_with_promotion/(?P<pk>.+)/$',  views.customer_update_delete_requestwithpromotion.as_view()),
    url(r'^v1/rest/customer_change_status/(?P<pk>.+)/$',  views.customer_change_status.as_view()),

    url(r'^v1/rest/customer_accident_request/$',  views.customer_accident_request.as_view()),
    url(r'^v1/rest/customer_create_outsource_history/$', views.customer_create_outsource_history.as_view()),
    url(r'^v1/rest/customer_outsource_history_list/$', views.customer_outsource_history_list.as_view()),
    
    
#Appointment
    url(r'^v1/rest/member_all_appointment/$',  views.member_all_appointment.as_view()),
    url(r'^v1/rest/customer_all_appointment/$',  views.customer_all_appointment.as_view()),
    url(r'^v1/rest/member_add_appointment/$',  views.member_add_appointment.as_view()),
    url(r'^v1/rest/member_update_delete_appointment/(?P<pk>.+)/$',  views.member_update_delete_appointment.as_view()),
    url(r'^v1/rest/customer_appointment/(?P<pk>.+)/$',  views.customer_appointment.as_view()),
    url(r'^v1/rest/cust_appointment_history/$',  views.cust_appointment_history.as_view()),
    url(r'^v1/rest/cust_upcell_history/(?P<appointment_pk>.+)/$',  views.cust_upcell_history.as_view()),
    url(r'^v1/rest/customer_accept_upcell/(?P<pk>.+)$',  views.customer_accept_upcell.as_view()),
    url(r'^v1/rest/customer_upcell/(?P<appointment_id>.+)$',  views.acceptupcell.as_view()),
 
#Feed Back
    url(r'^v1/rest/member_all_feedback/$',  views.member_all_feedback.as_view()),
    url(r'^v1/rest/member_view_feedback/(?P<Custfeedback_pk>.+)/view/$',  views.member_view_feedback.as_view()),
    url(r'^v1/rest/customer_create_feedback/$',  views.customer_create_feedback.as_view()),
    
#Master data
    url(r'^v1/rest/get_all_CarCompany/$',  views.get_all_CarCompany.as_view()),
    url(r'^v1/rest/get_all_CarModel/(?P<Company_pk>.+)/$',  views.get_all_CarModel.as_view()),
    url(r'^v1/rest/get_all_MakeYear/(?P<Company_model_pk>.+)/$',  views.get_all_MakeYear.as_view()),
    #url(r'^v1/rest/get_all_Series/(?P<Company_model_pk>.+)/$',  views.get_all_Series.as_view()),
    #url(r'^v1/rest/get_all_Engine/(?P<Series_pk>.+)/$',  views.get_all_Engine.as_view()),
    url(r'^v1/rest/get_all_ServiceType/$',  views.get_all_ServiceType.as_view()),
    url(r'v1/rest/view_make_year/$',views.view_make_year.as_view()),
    
#Registration
    url(r'^v1/rest/customer_update_profile/(?P<pk>.+)/$',  views.customer_update_profile.as_view()),
    url(r'^v1/rest/member_update_profile/(?P<pk>.+)/$',  views.member_update_profile.as_view()),
    url(r'^v1/rest/get_cust_detail/$',  views.get_cust_detail.as_view()),
    #url(r'^v1/rest/recoverpassword/$', password_reset.views.recover, name='password_reset_recover'),
    url(r'^v1/rest/member_postal_code/(?P<postal_code>.+)/$',  views.member_postal_code.as_view()),

#businesscard
    url(r'^v1/rest/member_view_businesscard/(?P<pk>.+)/$',views.member_view_businesscard.as_view()),
    url(r'^v1/rest/customer_view_businesscard/$',views.customer_view_businesscard.as_view()),  
    url(r'^v1/rest/member_send_businesscard/(?P<email>.+)$',views.member_send_businesscard.as_view()),  
    url(r'^v1/rest/customer_send_businesscard/$',views.customer_send_businesscard.as_view()),
    
#CRM    
    url(r'^v1/rest/users/count/$', views.UserCountView.as_view(), name='users-count'),
    url(r'^v1/rest/users/count1/$', views.UserCount1View.as_view()),
    url(r'^v1/rest/number_of_leads/$', views.number_of_leads.as_view()),
    url(r'^v1/rest/number_of_customer/$', views.number_of_customer.as_view()),
    url(r'^v1/rest/number_of_today_appointment/$', views.number_of_today_appointment.as_view()),
    url(r'^v1/rest/number_of_request/$', views.number_of_request.as_view()),
    url(r'^v1/rest/today_loggedin_customer/$', views.today_loggedin_customer.as_view()),
    url(r'^v1/rest/customer_add_vehicles/$',views.customer_add_vehicles.as_view()),
    url(r'v1/rest/customer_view_all_vehicle/$',views.customer_view_all_vehicle.as_view()),
    url(r'^v1/rest/customer_edit_vehicle/(?P<pk>.+)/$',views.customer_edit_vehicle.as_view()),
    url(r'^v1/rest/customer_add_image/(?P<pk>.+)/$',views.customer_add_image.as_view()), 

#push_notifications
    url(r'^notify/', views.notifyMessage),     
    url(r'^thanks/', views.thanks),

#make_year
    url(r'v1/rest/view_make_year/$',views.view_make_year.as_view()), 
    url(r'^', include(router.urls)),
    url(r'^v1/rest/delete_notification/(?P<pk>.+)/$',  views.delete_notification.as_view()),
    url(r'^v1/rest/delete_all_notification/$',  views.delete_all_notification.as_view()),

#for Member
#Dashboard
    url(r'^v1/rest/top_5_customer/$', views.top_5_customer.as_view()),

#member_registration    
    url(r'^v1/rest/registration_member/$',views.registration_member.as_view()),
    url(r'^v1/rest/get_member_detail/$',  views.get_member_detail.as_view()), 

    
#CRM       
    url(r'^v1/rest/lead_list/$', views.lead_list.as_view()),
    url(r'^v1/rest/add_lead/$', views.add_lead.as_view()),
    url(r'^v1/rest/member_edit_lead/(?P<pk>.+)/$',views.member_edit_lead.as_view()),
    url(r'^v1/rest/customer_list/$', views.customer_list.as_view()),
    url(r'^v1/rest/delete_customer/(?P<pk>.+)/$',  views.delete_customer_S.as_view()),
    url(r'^v1/rest/add_customer/$', views.add_customer.as_view()),
    url(r'^v1/rest/edit_customer/(?P<pk>.+)/$',views.edit_customer.as_view()),
    url(r'^v1/rest/member_add_vehicles/(?P<lead_id>.+)/$',views.member_add_vehicles.as_view()),
    url(r'^v1/rest/member_edit_vehicles/(?P<pk>.+)/$',views.member_edit_vehicles.as_view()),
    url(r'^v1/rest/member_list_vehicles/(?P<Lead_pk>.+)/$',views.member_list_vehicles.as_view()),
#customer
    url(r'^v1/rest/customer_history_details/(?P<appointment_id>.+)/$', views.customer_history.as_view()),
    url(r'^v1/rest/CustomerAppointmentList/(?P<pk>.+)/$', views.CustomerAppointmentList.as_view()),

#customer de-register
    url(r'^v1/rest/customer_deregister/(?P<pk>.+)/$',views.customer_deregister.as_view()),
 
#member generate potentail lead
    url(r'^v1/rest/member_potentail_lead/$',views.member_potentail_lead.as_view()), 
    url(r'^v1/rest/Ebc_history/$',views.Ebc_history.as_view()), 
#feedback
    url(r'^v1/rest/feedback_list/$',views.feedback_list.as_view()), 

#member app starts

url(r'v1/rest/regenerate_login_credentials/(?P<pk>.+)/$',views.regenerate_login_credentials.as_view()),
url(r'^v1/rest/reschedule_request/(?P<pk>.+)$',views.reschedule_request.as_view()),
url(r'^v1/rest/schedule_appointment/(?P<pk>.+)$',views.Schedule_Appointment.as_view()),

#member app ends

#customer registration
url(r'^v1/rest/promotion_re-open/(?P<pk>.+)/$',  views.promotion_re_open.as_view()),
url(r'^v1/rest/external_customer_registration/$',views.external_customer_registration.as_view()),

url(r'^v1/rest/upload_customer_gallery/$',  views.upload_customer_gallery.as_view()),
url(r'^v1/rest/list_customer_gallery/(?P<type>.+)/$',  views.list_customer_gallery.as_view()),
url(r'^v1/rest/expences_list/$',  views.list_expence_type.as_view()),
url(r'^v1/rest/expence_details/$',  views.expence_details.as_view()),
url(r'^v1/rest/list_of_expence_details/$',  views.list_of_expence_details.as_view()),
url(r'^v1/rest/search_member_postal_code/(?P<postal_code>.+)/$',  views.search_member_postal_code.as_view({'get': 'list'})),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)