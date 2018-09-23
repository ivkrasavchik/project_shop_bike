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
    url(r'ord_editing/$', views.ord_editing, name="ord_editing"),
    url(r'ord_editing_save/$', views.ord_editing_save, name="ord_editing_save"),
    url(r'ord_editing_del/$', views.ord_editing_del, name="ord_editing_del"),
    url(r'ord_editing_list/$', views.ord_editing_list, name="ord_editing_list"),
    url(r'ord_del_product/$', views.ord_del_product, name="ord_del_product"),
    url(r'ord_edit_product/$', views.ord_edit_product, name="ord_edit_product"),
    url(r'order_recount/$', views.order_recount, name="order_recount"),
    url(r'ord_find_product/$', views.ord_find_product, name="ord_find_product"),
    url(r'size_for_product/$', views.size_for_product, name="size_for_product"),
    url(r'description_for_product/$', views.description_for_product, name="description_for_product"),
    url(r'adding_product_in_order/$', views.adding_product_in_order, name="adding_product_in_order"),
    url(r'sessionFalse/$', views.session_false, name="sessionFalse"),
    # url(r'foto_add/$', views.add_img, name="add_img"),
]
