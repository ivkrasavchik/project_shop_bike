from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    customers_list = [field.name for field in Profile._meta.fields]  # выводит все поля

    class Meta:
        model = Profile

admin.site.register(Profile, ProfileAdmin)


class CategoryAdmin(admin.ModelAdmin):
    category_list = [field.name for field in Category._meta.fields]

    class Mete:
        model = Category

admin.site.register(Category, CategoryAdmin)
