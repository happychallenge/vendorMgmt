"""ChemCmpy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
# from django.contrib.auth import views as login_views

from authentication import views as signup_views

urlpatterns = [
    url('^$', lambda r: redirect('/event'), name='home'),
    url(r'^xmlyoon/', admin.site.urls),
    url(r'^chemical/', include('products.urls', namespace='chemical')),
    url(r'^allocation/', include('allocation.urls', namespace='allocation')),
    url(r'^authentication/', include('authentication.urls', namespace='authentication')),
    url(r'^order/', include('order.urls', namespace='order')),
    url(r'^event/', include('event.urls', namespace='event')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^todos/', include('todos.urls', namespace='todos')),

    url(r'^signup/$', signup_views.signup, name='signup'),
    url(r'^login', signup_views.login, name='login'),
    url(r'^logout', signup_views.logout, name='logout'),
]

if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns = [
    #     url(r'^__debug__/', include(debug_toolbar.urls)),
    # ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)