from django.conf.urls import url, include
from django.contrib import admin
from . import views
 
 
urlpatterns = [
 
#url(r'^$', views.FeedbackList, name='server_list'),
#url(r'^new$', views.FeedbackCreate.as_view(), name='server_new'),
url(r'^get_lead/',views.get_lead),
url(r'^new/$',views.FeedbackCreate, name='server_new'),
#url(r'^viewfeed/(?P<feed_id>[0-9]+)/$', views.viewfeedback, name='viewfeedback'),
url(r'^get_feeds/',views.get_feeds,name="get_feeds"),
url(r'^view_feed/',views.view_feed,name="view_feed"),
url(r'^new$', views.FeedbackCreate, name='server_new'),

]