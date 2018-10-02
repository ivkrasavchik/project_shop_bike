import simplejson as simplejson
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
import json
from django.contrib.auth.models import AnonymousUser, User
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf

from orders.forms import AddOrder, OrderAdmOrders
from orders.models import ProductInBasket, Order, StatusOrder
from products.models import ProductImage, ProductSizes, Product

from decimal import Decimal


# (Orders) < --Sends data to js to output products according to the selected order (js:AddProductToOrder())
@login_required
@transaction.atomic
def adding_product_in_order(request):
    args = {}
    if request.POST:
        args.update(csrf(request))
        price_per_item = Decimal(request.POST.get('price_per_item'))
        nmb = Decimal(request.POST.get('nmb'))
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        size = request.POST.get('size')
        if request.POST.get('order_ord'):
            sessionkey = request.session.session_key
            order = Order.objects.get(id=request.POST.get('order_ord'))
            prod_in_bask = ProductInBasket()
            prod_in_bask.order = order
            prod_in_bask.product = product
            prod_in_bask.nmb = nmb
            prod_in_bask.price_per_item = price_per_item
            prod_in_bask.sizes = size
            prod_in_bask.session_key = str(auth.get_user(request).username) + sessionkey
            prod_in_bask.save(auth.models.User.username)
            order.total_price = order.total_price + (price_per_item * nmb)
            order.save(force_update=True)
            products = ProductImage.objects.filter(product__productinbasket__order=order, is_main=True).values(
                'image', 'product__article', 'product__name', 'product__productinbasket__sizes',
                'product__productinbasket__nmb', 'product__productinbasket__price_per_item', 'product__productinbasket',
                'product__price'
            )
            json_orders_user = json.dumps(list(products), cls=DjangoJSONEncoder)
            return JsonResponse(json_orders_user, safe=False)
    return JsonResponse(False, safe=False)


# (Orders) < --(js:sessionfalse())
@login_required
@transaction.atomic
def session_false(request):
    args = {}
    args.update(csrf(request))
    request.session['pk'] = False
    return HttpResponse('OK')


# (Orders) < --Displays the main order page. Processes a query from a form for data filtering
@login_required
@transaction.atomic
def adm_orders(request):
    # request.session['pk'] = False
    args = {}
    args['orders'] = Order.objects.filter(status_ord__status_name="created")
    # args['orders'] = Order.objects.all()
    args['order_form'] = OrderAdmOrders()
    args['users'] = User.objects.all()
    args['status_ord'] = StatusOrder.objects.all()
    args['products'] = ProductImage.objects.filter(is_main=True, is_active=True)
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
            args['orders'] = Order.objects.filter(customer_name__contains=name, created__gte=create, status_ord__status_name=status)
        elif phone and create and status:
            args['orders'] = Order.objects.filter(customer_phone__contains=phone, created__gte=create, status_ord__status_name=status)
        elif user and status:
            args['orders'] = Order.objects.filter(user__username=user, status_ord__status_name=status)
        elif name and status:
            args['orders'] = Order.objects.filter(customer_name__contains=name, status_ord__status_name=status)
        elif phone and status:
            args['orders'] = Order.objects.filter(customer_phone__contains=phone, status_ord__status_name=status)
        elif user and create:
            args['orders'] = Order.objects.filter(user__username=user, created__gte=create)
        elif name and create:
            args['orders'] = Order.objects.filter(customer_name__contains=name, created__gte=create)
        elif phone and create:
            args['orders'] = Order.objects.filter(customer_phone__contains=phone, created__gte=create)

        elif user:
            args['orders'] = Order.objects.filter(user__username=user)
        elif name:
            args['orders'] = Order.objects.filter(customer_name__contains=name)
        elif phone:
            args['orders'] = Order.objects.filter(customer_phone__contains=phone)
        elif create:
            args['orders'] = Order.objects.filter(created__gte=create)
        elif completed:
            args['orders'] = Order.objects.filter(data_completed__gte=completed)
        elif status:
            args['orders'] = Order.objects.filter(status_ord__status_name=status)
        else:
            args['orders'] = Order.objects.all()
    return render(request, 'orders/orders.html', args)


# (Orders) < --Filter products according to the received query from js to add to the order (js:ProductFind)
@login_required
@transaction.atomic
def ord_find_product(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        if request.POST.get('product'):
            position = request.POST.get('product')
            product = ProductImage.objects.filter(product_id=position, is_main=True, is_active=True).values(
                'image', 'product', 'product__price', 'product__sizes__name_size', 'product__article',
                'product__category__name', 'product__name', 'product__fabric__name', 'product__year_model',
                'product__discount'
            )
            json_orders_user = json.dumps(list(product), cls=DjangoJSONEncoder)
            return JsonResponse(json_orders_user, safe=False)
        elif request.POST.get('article'):
            position = request.POST.get('article')
            product = ProductImage.objects.filter(product__article__contains=position, is_main=True, is_active=True).values(
                'image', 'product', 'product__price', 'product__article',
                'product__category__name', 'product__name', 'product__fabric__name', 'product__year_model',
                'product__discount'
            )
            json_orders_user = json.dumps(list(product), cls=DjangoJSONEncoder)
            return JsonResponse(json_orders_user, safe=False)
        elif request.POST.get('prod'):
            position = request.POST.get('prod')
            product = ProductImage.objects.filter(product__name__contains=position , is_main=True, is_active=True).values(
                'image', 'product', 'product__price', 'product__article',
                'product__category__name', 'product__name', 'product__fabric__name', 'product__year_model',
                'product__discount'
            )
            json_orders_user = json.dumps(list(product), cls=DjangoJSONEncoder)
            return JsonResponse(json_orders_user, safe=False)
        else:
            product = ProductImage.objects.filter(is_main=True, is_active=True).values(
                'image', 'product', 'product__price', 'product__article',
                'product__category__name', 'product__name', 'product__fabric__name', 'product__year_model',
                'product__discount'
            )
            json_orders_user = json.dumps(list(product), cls=DjangoJSONEncoder)
            return JsonResponse(json_orders_user, safe=False)
    return JsonResponse(False, safe=False)


# (Orders) < -- Sends in js the available sizes for the selected product (js: SelectedIdProduct)
@login_required
@transaction.atomic
def size_for_product(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        if request.POST.get('prod_id'):
            prod = request.POST.get('prod_id')
            sizes = ProductSizes.objects.filter(product=prod).values('name_size')

            json_orders_user = json.dumps(list(sizes), cls=DjangoJSONEncoder)
            return JsonResponse(json_orders_user, safe=False)
        return JsonResponse(False, safe=False)


# (Orders) < -- Sends in js description for the selected product (js: SelectedIdProduct)
@login_required
@transaction.atomic
def description_for_product(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        if request.POST.get('prod_id'):
            prod = request.POST.get('prod_id')
            description = Product.objects.get(id=prod).description
            # json_orders_user = json.dumps(list(description), cls=DjangoJSONEncoder)
            # return JsonResponse(json_orders_user, safe=False)
            return HttpResponse(description)
        return JsonResponse(False, safe=False)


# (Orders) < -- Sends data to js to fill in the attributes of the order form (js: ord_filter)
@login_required
@transaction.atomic
def ord_editing(request):
    args = {}
    args.update(csrf(request))
    orders_user = Order.objects.filter(id=request.POST.get('order')).values_list(
        'user', 'total_price', 'customer_name', 'customer_phone', 'status_ord', 'data_completed',
        'customer_address', 'comments', 'id', 'created')
    json_orders_user = json.dumps(list(orders_user), cls=DjangoJSONEncoder)
    return JsonResponse(json_orders_user, safe=False)


# (Orders) < -- recount total_price in order according to the base price of the product (js:OrderRecount)
@login_required
@transaction.atomic
def order_recount(request):
    products = False
    if request.POST:
        if request.POST.get('order_ord'):
            order = Order.objects.get(id=request.POST.get('order_ord'))
            products = ProductInBasket.objects.filter(order=order)
            sum = 0
            for elem in products:
                sum += elem.price_per_item * elem.nmb
            if sum == 0:
                for elem in products:
                    sum += elem.product.price * elem.nmb
            return JsonResponse(sum, safe=False)
        return JsonResponse(products, safe=False)


# (Orders) < -- Saves a changed query or creates a new one.(orders.html)
@login_required
@transaction.atomic
def ord_editing_save(request):
    args = {}
    args.update(csrf(request))
    # print(request.session['pk'])
    if request.POST:
        if request.POST.get('order_id'):  # and type(request.POST.get('order_id')) == int:
            order = Order.objects.get(id=request.POST.get('order_id'))
            order_form = OrderAdmOrders(request.POST, instance=order)
            if order_form.is_valid():
                order_form.save()
        elif request.POST.get('customer_name') and request.POST.get('customer_phone'):
            order_form = OrderAdmOrders(request.POST)
            if order_form.is_valid():
                order = order_form.save()
                pk = order.id
                args['pk'] = order.id
                request.session['pk'] = order.id
                print(request.session['pk'])
        #         return redirect('/orders/')
        return redirect('/orders/')
    print("render_to_response")
    return render_to_response('orders/orders.html', args)
    # return render(request, 'orders/orders.html', args)


# (Orders) < -- Deletes the selected order
@login_required
@transaction.atomic
def ord_editing_del(request):
    args = {}
    args.update(csrf(request))
    if request.POST and request.POST.get('order_id_del'):
        order = Order.objects.get(id=request.POST.get('order_id_del'))
        order.delete()
    return redirect('/orders/')


# (Orders) < -- Displays a list of products in the selected order(js:AddBlockListShow)
@login_required
@transaction.atomic
def ord_editing_list(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        if request.POST.get('order_ord'):
            order = Order.objects.get(id=request.POST.get('order_ord'))
            products = ProductImage.objects.filter(product__productinbasket__order=order, is_main=True).values(
                'image', 'product__article', 'product__name', 'product__productinbasket__sizes',
                'product__productinbasket__nmb', 'product__productinbasket__price_per_item', 'product__productinbasket',
                'product__price'
            )

            json_orders_user = json.dumps(list(products), cls=DjangoJSONEncoder)
            return JsonResponse(json_orders_user, safe=False)
        return JsonResponse(False, safe=False)


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
            'product__productinbasket__nmb', 'product__productinbasket__price_per_item', 'product__productinbasket',
            'product__price'
        )
        position = ProductInBasket.objects.get(id=product)
        price = position.price_per_item * position.nmb
        balance = order.total_price - price
        if balance < 0:
            balance = 0
        order.total_price = balance
        order.save(force_update=True)
        position.delete()

        json_orders_user = json.dumps(list(products), cls=DjangoJSONEncoder)
        return JsonResponse(json_orders_user, safe=False)
    return JsonResponse(products, safe=False)


def ord_edit_product(request):
    args = {}
    args.update(csrf(request))
    products = False
    if request.POST:
        product = request.POST.get('product')
        price_per_item = request.POST.get('price')
        nmb = request.POST.get('nmb')
        sizes = request.POST.get('size')
        position = ProductInBasket.objects.get(id=product)
        order = Order.objects.get(productinbasket=product)

        old_price = position.price_per_item * position.nmb
        new_price = Decimal(price_per_item) * Decimal(nmb)
        current_sum = order.total_price - old_price

        balance = current_sum + new_price
        if balance < 0:
            balance = 0
        order.total_price = balance
        order.save(force_update=True)
        position.price_per_item = price_per_item
        position.nmb = nmb
        position.sizes = sizes
        position.save(force_update=True)
        products = ProductImage.objects.filter(product__productinbasket__order=order, is_main=True).values(
            'image', 'product__article', 'product__name', 'product__productinbasket__sizes',
            'product__productinbasket__nmb', 'product__productinbasket__price_per_item', 'product__productinbasket',
            'product__price'
        )
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


# (Account) <--Sends data to display all orders of the selected user (js:profile_view)
@login_required
@transaction.atomic
def order_list(request):
    args = {}
    args.update(csrf(request))
    orders_user = Order.objects.filter(user=request.POST.get('user_id')).values_list(
        'id', 'total_price', 'status_ord__status_name', 'created', 'data_completed')
    json_orders_user = json.dumps(list(orders_user), cls=DjangoJSONEncoder)
    return JsonResponse(json_orders_user, safe=False)


# (Account) <--Sends data to display all product of the selected orders (js:AdmOrderItem)
@login_required
@transaction.atomic
def order_items(request):
    args = {}
    args.update(csrf(request))
    orders_itm = ProductInBasket.objects.filter(order_id=request.POST.get('ord_id')).values_list(
        'product__article', 'product__name', 'sizes', 'nmb', 'price_per_item')
    json_orders_user = json.dumps(list(orders_itm), cls=DjangoJSONEncoder)
    return JsonResponse(json_orders_user, safe=False)


# (Account) <--Sends data to display Displaying info about selected product (js:AdmOrdProdItem)
def adm_ord_prod_items(request):
    args = {}
    args.update(csrf(request))
    prod_itm = ProductImage.objects.filter(is_main=True, product__article=request.POST.get('prod_id')).values_list(
        'image', 'product__price', 'product__discount', 'product__category__name'
    )
    json_orders_user = json.dumps(list(prod_itm), cls=DjangoJSONEncoder)
    return JsonResponse(json_orders_user, safe=False)