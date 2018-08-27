from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.home),
    # url(r'^login/$', auth_views.login, name='login'),
    # url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^account/$', views.update_profile),
    url(r'^profile/$', views.profile_view),

]
