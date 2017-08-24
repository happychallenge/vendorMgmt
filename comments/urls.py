from django.conf.urls import url
from . import views

urlpatterns = [

# COMMENT    
    url(r'^ajaxadd/(?P<vendor_id>\d+)/$', views.ajax_comment_add, name='ajax_comment_add'),
    url(r'^ajaxupdate/(?P<comment_id>\d+)/$', views.ajax_comment_update, name='ajax_comment_update'),
]
