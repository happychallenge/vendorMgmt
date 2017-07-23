from django.conf.urls import url
from . import views

urlpatterns = [
# VENDOR
    url(r'^orderadd/$', views.porder_add, name='porder_add'),
    url(r'^orderitemadd/(?P<id>\d+)/$', views.porderitem_add, name='porderitem_add'),
    # url(r'^demandsupply/$', views.product_demandsupply_list, name='product_demandsupply_list'),
    # url(r'^demandsupply/(?P<id>\d+)/(?P<year_month>.+)/$', 
    #         views.product_demandsupply_detail, name='product_demandsupply_detail'),
]