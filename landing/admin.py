from django.contrib import admin
from .models import *
from orders.models import Order


class OrderInLine(admin.TabularInline):
    model = Order
    extra = 0


class ProfileAdmin(admin.ModelAdmin):
    customers_list = [field.name for field in Profile._meta.fields]  # выводит все поля
    # inlines = [OrderInLine]

    class Meta:
        model = Profile

admin.site.register(Profile, ProfileAdmin)


class CategoryAdmin(admin.ModelAdmin):
    category_list = [field.name for field in Category._meta.fields]

    class Mete:
        model = Category

admin.site.register(Category, CategoryAdmin)
