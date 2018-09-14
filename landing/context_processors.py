from django.contrib import auth
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.context_processors import csrf

from landing.forms import Login, UserCreation
from orders.models import ProductInBasket, Order
from products.models import ProductCategory


def context_processor_local(request):
    args = {}
    if auth.get_user(request).username != AnonymousUser.username:
        args['au_user'] = auth.get_user(request)
        args['context_order_user'] = Order.objects.filter(user=args['au_user'])
    else:
        args['context_order_user'] = False

    args['session_key'] = request.session.session_key
    if not args['session_key']:
        request.session.cycle_key()

    args['cont_form'] = Login()
    args['cont_form2'] = UserCreation()
    args['context_category_product'] = ProductCategory.objects.all()
    args['context_product_in_basket'] = ProductInBasket.objects.filter(session_key=args['session_key'], order=None)
    args['product_in_basket_session'] = ProductInBasket.objects.filter(session_key=args['session_key']).exclude(order=None)
    args['context_order_for_no_user'] = set()
    for elem in args['product_in_basket_session']:
        args['context_order_for_no_user'].add(elem.order)

    return args
    # return locals()
