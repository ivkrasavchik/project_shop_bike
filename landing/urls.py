from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    # url(r'^login/$', auth_views.login, name='login'),
    url(r'^alt_login/$', views.alt_login, name="alt_login"),
    url(r'^alt_register/$', views.alt_register, name="alt_register"),
    url(r'^logout/$', views.logout),
    url(r'^account/$', views.update_profile),
    url(r'^profile/$', views.profile_view),
    url(r'^temp_link/$', views.temp_link, name="temp_link"),

]
