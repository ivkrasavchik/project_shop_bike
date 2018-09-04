from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^product_save/$', views.adm_product_save, name="product_save"),
    url(r'^adm_img/$', views.adm_product_img),
    url(r'^$', views.adm_products, name="adm_products"),
    url(r'product/(?P<product_id>\w+)/$', views.product, name="product"),
    url(r'product_by_category/(?P<category_id>\w+)/$', views.product_by_category, name="product_by_category"),
]
