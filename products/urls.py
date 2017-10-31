from django.conf.urls import url
from . import views, views_quote

urlpatterns = [
# VENDOR
    url(r'^vendors/$', views.vendor_list, name='vendor_list'),
    url(r'^vendors/(?P<id>\d+)/$', views.vendor_detail, name='vendor_detail'),
    url(r'^vendors/add/$', views.vendor_add, name='vendor_add'),
    url(r'^vendors/update/(?P<id>\d+)/$', views.vendor_update, name='vendor_update'),

# PRODUCT
    url(r'^proudct/$', views.product_list, name='product_list'),
    url(r'^proudct/(?P<id>\d+)/$', views.product_detail, name='product_detail'),
    url(r'^product/add/$', views.product_add, name='product_add'),
    url(r'^products/update/(?P<id>\d+)/$', views.product_update, name='product_update'),

# CONTACT
    url(r'^contact/$', views.contact_list, name='contact_list'),
    url(r'^contact/add/(?P<vendor_id>\d+)/$', views.contact_add, name='contact_add'),
    url(r'^contact/update/(?P<id>\d+)/$', views.contact_update, name='contact_update'),

# QUOTATION
    url(r'^quotation/productadd/$', views_quote.quotation_productadd, name='quotation_productadd'),
    url(r'^quotation/simpleadd/$', views_quote.quotation_simpleadd, name='quotation_simpleadd'),
    url(r'^quotation/update/$', views_quote.quotation_update, name='quotation_update'),
    url(r'^quotation/ajax_add/$', views_quote.ajax_quotation_add, name='ajax_quotation_add'),

# SOURCING
    url(r'^sourcing/$', views.sourcingvendor_list, name='sourcingvendor_list'),
    url(r'^sourcing/(?P<id>\d+)/$', views.sourcingvendor_detail, name='sourcingvendor_detail'),
    url(r'^sourcing/priceadd/$', views.sourcing_priceadd, name='sourcing_priceadd'),
    url(r'^sourcing/productadd/$', views.sourcing_productadd, name='sourcing_productadd'),
    url(r'^sourcing/vendoradd/(?P<product_id>\d+)/$', views.sourcing_vendoradd, name='sourcing_vendoradd'),
    url(r'^sourcing/simpleadd/$', views.sourcing_simpleadd, name='sourcing_simpleadd'),
    # url(r'^sourcing/update/(?P<id>\d+)/$', views.vendor_update, name='vendor_update'),

# PRODUCT
    url(r'^sourcingproudct/$', views.sourcingproduct_list, name='sourcingproduct_list'),
    url(r'^sourcingproudct/(?P<id>\d+)/$', views.sourcingproduct_detail, name='sourcingproduct_detail'),
    # url(r'^product/add/$', views.product_add, name='product_add'),
    # url(r'^products/update/(?P<id>\d+)/$', views.product_update, name='product_update'),

]
