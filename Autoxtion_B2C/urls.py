"""Autoxtion_B2C URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
#from django import views
from Registration import views
import promotion.urls
import customer.urls
import Feedback.urls
import Appointment.urls
import api.urls
from django.conf import settings
import notifications.urls 

#handler404 = 'Registration.views.custom_404'

#if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
 #   urlpatterns += patterns('',
  #          url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
   # )


urlpatterns = [
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', admin.site.urls),
    url(r'^registration/', include('Registration.urls')),
    url(r'^email/', include('password_reset.urls')),
    url(r'^CRM/',include('CRM.urls',namespace='CRM')),
    url(r'^promotion/', include(promotion.urls, namespace='promotion')),
    url(r'^customer/', include(customer.urls, namespace='customer')),
    url(r'^feedback/', include(Feedback.urls, namespace='Feedback')),
    url(r'^appointment/', include(Appointment.urls, namespace='Appointment')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^api/', include(api.urls, namespace='api')),
    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
