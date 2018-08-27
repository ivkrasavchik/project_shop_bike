from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^product_save/$', views.adm_product_save, name="product_save"),
    url(r'^adm_img/$', views.adm_product_img),
    url(r'^$', views.adm_products, name="adm_products"),
    # url(r'foto_add/$', views.add_img, name="add_img"),
]
