from django.conf.urls import url, include
from django.contrib import admin
from . import views
urlpatterns = [

    url(r'^$',views.index,name="index"),
    url(r'addlead/$',views.addlead,name="addlead"),
    #url(r'addlead/$',views.addlead.as_view(),name="addlead"),
    url(r'^edit/(?P<lead_id>[0-9]+)/$', views.edit_lead, name='edit_lead'),
    url(r'^change_status/(?P<lead_id>[0-9]+)/$', views.change_status, name='change_status'),
    url(r'^get_models/$', views.get_models),
    url(r'^get_mod/$', views.get_mod),
    url(r'^get_make_year/$', views.get_make_year),
    #url(r'^qualify_lead/$', views.qualify_lead,name="qualify_lead"),
    url(r'^crmcust/$', views.customer_index, name='customer_index'),
    url(r'^deleteVehicle/$',views.deleteVehicle,name="deleteVehicle"),
    url(r'^index2/(?P<d>[0-9]+)/$', views.index2,name="index2"),
    url(r'^customer_index2/(?P<d>[0-9]+)/$', views.customer_index2,name="cindex2"),
    url(r'^existing_cust/$', views.existing_cust,name="existing_cust"),
    url(r'^addVehicle/$', views.addVehicle,name="addVehicle"),
    url(r'^editVehicle/$', views.editVehicle,name="editVehicle"),
    url(r'^deleteVehicleCust/$',views.deleteVehicleCust,name="deleteVehicleCust"),
    url(r'^excelsheetimport/$',views.excelsheet,name="excelsheet"),
    url(r'^view_history/(?P<lead_id>[0-9]+)/$', views.view_history, name='view_history'),
    url(r'^customerRegistration/$', views.customer_registration, name='customer_registration'),  
    url(r'^customerdel/$', views.customer_delete,name="customerdel"), 
    url(r'^get_customerlist/(?P<user_id>[0-9]+)/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/$',  views.get_customer.as_view()),
    url(r'^get_leadlist/(?P<user_id>[0-9]+)/(?P<from_dt>\d{4}-\d{2}-\d{2})/(?P<to_dt>\d{4}-\d{2}-\d{2})/$',  views.get_leadlist.as_view()),
    url(r'^add/(?P<mem_detail>[0-9]+)$',views.add),
    url(r'^downloadExcelTemplate',views.downloadDemoTemplate,name="downloadexceltemplate"),
    url(r'^generate_credentials/$', views.generateCredentials,name="generateCredentials"),
    url(r'addCompany/$',views.addCompany,name="addCompany"),
    url(r'UpdateCompany/(?P<company_id>[0-9]+)/$',views.UpdateCompany,name="UpdateCompany"),
    url(r'^driver_delete_ajax/(?P<vehicle_id>\d+)$',views.driver_delete_ajax, name='driver_delete_ajax'),
    url(r'^edit_drivers/$',views.edit_drivers, name='edit_drivers'),
    url(r'^company_list/$', views.company_index, name='company_index'),

]