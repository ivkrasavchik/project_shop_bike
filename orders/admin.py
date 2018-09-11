from django.contrib import admin

from orders.models import ProductInBasket, StatusOrder, Order


class ProductInBasketInLine(admin.TabularInline):
    model = ProductInBasket
    extra = 0


class AdmOrder(admin.ModelAdmin):
    inlines = [ProductInBasketInLine]

    class Meta:
        model = Order


admin.site.register(StatusOrder)
admin.site.register(Order, AdmOrder)
admin.site.register(ProductInBasket)
