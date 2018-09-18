import simplejson as simplejson
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
import json
from django.contrib.auth.models import AnonymousUser, User
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf

from orders.forms import AddOrder, OrderAdmOrders
from orders.models import ProductInBasket, Order, StatusOrder
from products.models import ProductImage


@login_required
@transaction.atomic
def adm_orders(request):
    args = {}
    args['orders'] = Order.objects.all()
    args['order_form'] = OrderAdmOrders()
    args['users'] = User.objects.all()
    args['status_ord'] = StatusOrder.objects.all()
    args['all_cust_name'] = set()
    for elem in args['orders'].values_list('customer_name'):
        args['all_cust_name'].add(elem[0])

    if request.POST:
        args.update(csrf(request))
        id_ord = request.POST.get('nord')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        create = request.POST.get('create')
        completed = request.POST.get('completed')
        user = request.POST.get('user')
        status = request.POST.get('status')

        if id_ord:
            args['orders'] = Order.objects.filter(id=id_ord)
        elif user and create and status:
            args['orders'] = Order.objects.filter(user__username=user, created__gte=create, status_ord__status_name=status)
        elif name and create and status:
            args['orders'] = Order.objects.filter(customer_name=name, created__gte=create, status_ord__status_name=status)
        elif phone and create and status:
            args['orders'] = Order.objects.filter(customer_phone=phone, created__gte=create, status_ord__status_name=status)
        elif user and status:
            args['orders'] = Order.objects.filter(user__username=user, status_ord__status_name=status)
        elif name and status:
            args['orders'] = Order.objects.filter(customer_name=name, status_ord__status_name=status)
        elif phone and status:
            args['orders'] = Order.objects.filter(customer_phone=phone, status_ord__status_name=status)
        elif user and create:
            args['orders'] = Order.objects.filter(user__username=user, created__gte=create)
        elif name and create:
            args['orders'] = Order.objects.filter(customer_name=name, created__gte=create)
        elif phone and create:
            args['orders'] = Order.objects.filter(customer_phone=phone, created__gte=create)

        elif user:
            args['orders'] = Order.objects.filter(user__username=user)
        elif name:
            args['orders'] = Order.objects.filter(customer_name=name)
        elif phone:
            args['orders'] = Order.objects.filter(customer_phone__contains=phone)
        elif create:
            args['orders'] = Order.objects.filter(created__gte=create)
        elif completed:
            args['orders'] = Order.objects.filter(data_completed__gte=completed)
        elif status:
            args['orders'] = Order.objects.filter(status_ord__status_name=status)

    return render(request, 'orders/orders.html', args)


def ord_editing(request):
    args = {}
    args.update(csrf(request))
    orders_user = Order.objects.filter(id=request.POST.get('order')).values_list(
        'user', 'total_price', 'customer_name', 'customer_phone', 'status_ord', 'data_completed',
        'customer_address', 'comments', 'id')
    json_orders_user = json.dumps(list(orders_user), cls=DjangoJSONEncoder)
    return JsonResponse(json_orders_user, safe=False)


@login_required
@transaction.atomic
def ord_editing_save(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        order = Order.objects.get(id=request.POST.get('order_id'))
        order_form = OrderAdmOrders(request.POST, instance=order)
        if order_form.is_valid():
            order_form.save()

        return redirect('/orders/')
    return render(request, 'orders/orders.html', args)


@login_required
@transaction.atomic
def ord_editing_del(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        order = Order.objects.get(id=request.POST.get('order_id_del'))
        order.delete()
    return redirect('/orders/')


@login_required
@transaction.atomic
def ord_editing_list(request):
    args = {}
    args.update(csrf(request))
    products = False
    if request.POST:
        if request.POST.get('order_ord'):
            order = Order.objects.get(id=request.POST.get('order_ord'))
            products = ProductImage.objects.filter(product__productinbasket__order=order, is_main=True).values(
                'image', 'product__article', 'product__name', 'product__productinbasket__sizes',
                'product__productinbasket__nmb', 'product__productinbasket__price_per_item', 'product__productinbasket'
            )
            json_orders_user = json.dumps(list(products), cls=DjangoJSONEncoder)
            return JsonResponse(json_orders_user, safe=False)
        return JsonResponse(products, safe=False)


def del_from_basket(request, elem_id):
    position = ProductInBasket.objects.get(id=elem_id)
    position.delete()
    return render(request, 'landing/home.html', locals())


def ord_del_product(request):
    args = {}
    args.update(csrf(request))
    products = False
    if request.POST:
        product = request.POST.get('product')
        order = Order.objects.get(productinbasket=product)
        products = ProductImage.objects.filter(product__productinbasket__order=order, is_main=True).values(
            'image', 'product__article', 'product__name', 'product__productinbasket__sizes',
            'product__productinbasket__nmb', 'product__productinbasket__price_per_item', 'product__productinbasket'
        )
        position = ProductInBasket.objects.get(id=product)
        price = position.price_per_item * position.nmb
        balance = order.total_price - price
        if balance < 0:
            balance = 0
        order.total_price = balance
        order.save(force_update=True)
        position.delete()
        print("BAX BAX BAX BAX BAX BAX", balance, price, position.price_per_item, position.nmb)
        json_orders_user = json.dumps(list(products), cls=DjangoJSONEncoder)
        return JsonResponse(json_orders_user, safe=False)
    return JsonResponse(products, safe=False)


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
        img_qs = ProductImage.objects.filter(product_id=elem['product_id'], is_main=True)  # .values()
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