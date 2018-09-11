from django.contrib import auth
from django.contrib.auth.models import AnonymousUser

from orders.models import ProductInBasket, Order
from products.models import ProductCategory


def context_processor_local(request):
    if auth.get_user(request).username != AnonymousUser.username:
        au_user = auth.get_user(request)
        context_order_user = Order.objects.filter(user=au_user)
    else:
        context_order_user = False


    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    context_category_product = ProductCategory.objects.all()
    context_product_in_basket = ProductInBasket.objects.filter(session_key=session_key, order=None)
    product_in_basket_session = ProductInBasket.objects.filter(session_key=session_key).exclude(order=None)
    context_order_for_no_user = set()
    for elem in product_in_basket_session:
        context_order_for_no_user.add(elem.order)

    return locals()
