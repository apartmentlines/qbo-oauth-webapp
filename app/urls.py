from django.urls import re_path
from django.views.generic.base import RedirectView
from . import views

app_name = 'app'

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^oauth/?$', views.oauth, name='oauth'),
    re_path(r'^callback/?$', views.callback, name='callback'),
    re_path(r'^connected/?$', views.connected, name='connected'),
    re_path(r'^qbo_request/?$', views.qbo_request, name='qbo_request'),
    re_path(r'^revoke/?$', views.revoke, name='revoke'),
    re_path(r'^refresh/?$', views.refresh, name='refresh'),
]
