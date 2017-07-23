from django.conf.urls import url
from . import views

urlpatterns = [
# VENDOR
    url(r'^demandsupply/$', views.product_demandsupply_list, name='product_demandsupply_list'),
    url(r'^demandsupply/(?P<id>\d+)/(?P<year_month>.+)/$', 
            views.product_demandsupply_detail, name='product_demandsupply_detail'),
    url(r'^demand/add/$', views.client_demand_add, name='client_demand_add'),
    url(r'^supply/add/$', views.vendor_supply_add, name='vendor_supply_add'),
]