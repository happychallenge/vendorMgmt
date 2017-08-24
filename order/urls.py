from django.conf.urls import url
from . import views

urlpatterns = [
# VENDOR
    url(r'^$', views.porder_list, name='porder_list'),
    url(r'^(?P<id>\d+)/$', views.porder_detail, name='porder_detail'),
    url(r'^porderadd/$', views.porder_add, name='porder_add'),
    url(r'^porderitemadd/(?P<id>\d+)/$', views.porderitem_add, name='porderitem_add'),
    url(r'^shippingadd/(?P<id>\d+)/$', views.shipping_add, name='shipping_add'),
    url(r'^materialfile/$', views.material_file, name='material_file'),
]