from django.contrib import admin

from products.models import ProductImage, ProductCategory, Product, Fabric


class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]  # выводит все поля

    class Meta:
        model = ProductImage
admin.site.register(ProductImage, ProductImageAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]  # выводит все поля

    class Meta:
        model = ProductCategory
admin.site.register(ProductCategory, ProductCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = []
    for field in Product._meta.fields:
        if field.name != "description" and field.name != "short_description" and field.name != "created" \
                and field.name != "update":
            list_display.append(field.name)

    inlines = [ProductImageInLine]

    class Meta:
        model = Product
admin.site.register(Product, ProductAdmin)


admin.site.register(Fabric)
