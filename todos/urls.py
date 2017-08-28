from django.conf.urls import url
from . import views

urlpatterns = [
# VENDOR
    url(r'^$', views.todo_list, name='todo_list'),
    url(r'^add/$', views.ajax_todo_add, name='ajax_todo_add'),
    url(r'^detail/(?P<id>\d+)/$', views.todo_detail, name='todo_detail'),
]