from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from orders.models import ProductInBasket
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
    product_image = ProductImage.objects.filter(is_main=True, is_active=True)
    return render(request, 'landing/home.html', locals())

