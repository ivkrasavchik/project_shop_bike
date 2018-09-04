from orders.models import ProductInBasket
from products.models import ProductCategory


def context_processor_local(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    context_category_product = ProductCategory.objects.all()
    context_product_in_basket = ProductInBasket.objects.filter(session_key=session_key)

    return locals()