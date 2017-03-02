from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework import routers

from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
#app_name = 'promotion
from rest_framework.urlpatterns import format_suffix_patterns
#router = routers.SimpleRouter()

#router.register(r'get_promotion', views.get_promotion.as_view())
#router.register(r'get_services', views.NewPromoList)


urlpatterns = [
              
   url(r'^$', views.PromotionList.as_view(), name='server_list'),
   url(r'^all$', views.PromotionListall.as_view(), name='server_list_all'),
   url(r'^list$', views.Promo_List_Mem.as_view(), name='server_list_mem'),
   #url(r'^new$', views.PromotionCreate.as_view(), name='server_new'),
   url(r'^new_all$', views.PromotionCreate.as_view(), name='server_new'),
   #url(r'^detail/(?P<pk>\d+)$', views.ServerDetail.as_view(), name='server_detail'),
   url(r'^edit/(?P<pk>\d+)$', views.PromotionUpdate.as_view(), name='server_edit'),
   url(r'^delete/(?P<pk>\d+)$', views.PromotionDelete.as_view(), name='server_delete'),
   url(r'^test/$',views.getmodel, name='test'),
   url(r'^get_promotion/(?P<val>.+)/$',  views.get_promotion.as_view()),
   url(r'^promotion_history/$', views.promotion_history, name='promotion_history'),
   url(r'^promotion_reopen/(?P<pk>\d+)$', views.promotion_reopen, name='promotion_reopen'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])