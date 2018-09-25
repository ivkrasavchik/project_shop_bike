from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^product_save/$', views.adm_product_save, name="product_save"),
    url(r'^adm_img/$', views.adm_product_img),
    url(r'^$', views.adm_products, name="adm_products"),
    url(r'product/(?P<product_id>\w+)/$', views.product, name="product"),
    url(r'product_by_category/(?P<category_id>\w+)/$', views.product_by_category, name="product_by_category"),
    url(r'all_product/$', views.all_product, name="all_product"),
    url(r'^brands/$', views.brands, name="brands"),
    url(r'^brand/(?P<brand_id>\w+)/$', views.brand, name="brand"),
    url(r'^baraholka/$', views.baraholka, name="baraholka"),
    url(r'^adm_products_img_add/$', views.adm_products_img_add, name="adm_products_img_add"),
    url(r'^image_product_del/$', views.image_product_del, name="image_product_del"),
]
