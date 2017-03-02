from django.conf.urls import url

from . import views

app_name = 'password_reset'
urlpatterns = [
    url(r'^recover/(?P<signature>.+)/$', views.recover_done,
        name='password_reset_sent'),
    url(r'^recover/$', views.recover, name='password_reset_recover'),
    url(r'^reset/done/$', views.reset_done, name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.reset,
        name='password_reset_reset'),
    url(r'^password_change/(?P<user_id>[0-9]+)', views.password_change, name='password_change'),
    #url(r'^password_change_done/$', views.password_change_done, name='password_change_done'),
]