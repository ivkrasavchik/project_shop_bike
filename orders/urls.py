from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'add_order/$', views.add_order, name="add_order"),
    url(r'^$', views.adm_orders, name="adm_orders"),
    url(r'user_orders/(?P<elem_id>\w+)/$', views.user_orders, name="user_orders"),
    url(r'delfrombasket/(?P<elem_id>\w+)/$', views.del_from_basket, name="delfrombasket"),
    url(r'order_list/$', views.order_list, name="order_list"),
    url(r'order_items/$', views.order_items, name="order_items"),
    url(r'adm_ord_prod_items/$', views.adm_ord_prod_items, name="adm_ord_prod_items"),
    # url(r'foto_add/$', views.add_img, name="add_img"),
]
