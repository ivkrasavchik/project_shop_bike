from django.contrib import admin

from orders.models import StatusOrder, Order

admin.site.register(StatusOrder)
admin.site.register(Order)
