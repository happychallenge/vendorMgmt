from django.conf.urls import url
from . import views

urlpatterns = [
# VENDOR
    url(r'^$', views.event_list, name='event_list'),
    url(r'^timetable/$', views.event_timetable, name='event_timetable'),
]