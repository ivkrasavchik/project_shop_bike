import simplejson as simplejson
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
import json
from django.contrib.auth.models import AnonymousUser
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.urls import reverse

from orders.forms import AddOrder
from orders.models import ProductInBasket, Order, StatusOrder
from products.models import ProductImage


@login_required
@transaction.atomic
def adm_orders(request):
    args = {}
    args['test'] = "Ща всех порвем"
    return render(request, 'orders/orders.html', args)


def del_from_basket(request, elem_id):
    position = ProductInBasket.objects.get(id=elem_id)
    position.delete()
    # product_image = ProductImage.objects.filter(is_main=True, is_active=True)
    return render(request, 'landing/home.html', locals())


def add_order(request):
    args = {}
    args.update(csrf(request))
    session_key = request.session.session_key
    product_image = ProductImage.objects.filter(is_main=True, is_active=True)
    product_in_orders = ProductInBasket.objects.filter(session_key=session_key, order=None)
    amount = 0
    for elem in product_in_orders:
        amount += elem.price_per_item * elem.nmb

    form = AddOrder()
    if request.POST:
        form = AddOrder(request.POST)
        status = StatusOrder.objects.get(status_name="created")

        if form.is_valid():
            nf = form.save(commit=False)
            nf.status_ord = status
            nf.total_price = amount
            if auth.get_user(request).username != AnonymousUser.username:
                nf.user = auth.get_user(request)
            nf.save()

            for elem in product_in_orders:
                elem.order = nf
                # elem.session_key += "1"
                elem.save(force_update=True)

            return redirect("/",)
    return render(request, 'orders/add_order.html', locals())


def user_orders(request, elem_id):

    product_in_users_order = ProductInBasket.objects.filter(order_id=elem_id).values()

    status = Order.objects.get(id=elem_id)

    for elem in product_in_users_order:
        img_qs = ProductImage.objects.filter(product_id=elem['product_id'], is_main=True)#.values()
        # print(img_qs)
        for el in img_qs:
            elem['image'] = el.image.url
            elem['product_name'] = el.product.name
            elem['price'] = el.product.price
            # print(elem)
    return render(request, 'orders/user_orders.html', locals())


def order_list(request):
    args = {}
    args.update(csrf(request))
    orders_user = Order.objects.filter(user=request.POST.get('user_id')).values_list(
        'id', 'total_price', 'status_ord__status_name', 'created', 'data_completed')
    json_orders_user = json.dumps(list(orders_user), cls=DjangoJSONEncoder)
    return JsonResponse(json_orders_user, safe=False)


def order_items(request):
    args = {}
    args.update(csrf(request))
    orders_itm = ProductInBasket.objects.filter(order_id=request.POST.get('ord_id')).values_list(
        'product__article', 'product__name', 'sizes', 'nmb', 'price_per_item')
    json_orders_user = json.dumps(list(orders_itm), cls=DjangoJSONEncoder)
    return JsonResponse(json_orders_user, safe=False)


def adm_ord_prod_items(request):
    args = {}
    args.update(csrf(request))
    prod_itm = ProductImage.objects.filter(product__article=request.POST.get('prod_id')).values_list(
        'image', 'product__price', 'product__discount', 'product__category__name'
    )
    json_orders_user = json.dumps(list(prod_itm), cls=DjangoJSONEncoder)
    return JsonResponse(json_orders_user, safe=False)