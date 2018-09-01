from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render


@login_required
@transaction.atomic
def adm_orders(request):
    args = {}
    args['test'] = "Ща всех порвем"

    return render(request, 'orders/orders.html', args)
