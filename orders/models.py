from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class StatusOrder(models.Model):  # модели принято называть в ед. числе
    status_name = models.CharField(max_length=24)
    status_is_actual = models.BooleanField(default=True)

    class Meta:
        # django само определяет единственное и множественное число, но можно переопределить
        verbose_name = "Статус заказа"  # приомзносимое имя в единственном числе
        verbose_name_plural = "Статусы заказа"  # приомзносимое имя во множественном числе

    def __str__(self):  # настройка презинтации модели вадминке
        return "Статус  %s" % self.status_name


class Order(models.Model):  # модели принято называть в ед. числе
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # total price for all products in order
    customer_name = models.CharField(max_length=64, blank=False, verbose_name="Как звать?")
    # customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=48, blank=False, verbose_name="Мобила для связи")
    customer_address = models.CharField(max_length=128, blank=True, null=True, verbose_name="Куда везти?")
    comments = models.TextField(max_length=256, blank=True, verbose_name="Что еще нам стоит знать?")
    status_ord = models.ForeignKey(StatusOrder, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        # django само определяет единственное и множественное число, но можно переопределить
        verbose_name = "Заказ"  # приомзносимое имя в единственном числе
        verbose_name_plural = "Заказы"  # приомзносимое имя во множественном числе

    def __str__(self):  # настройка презинтации модели вадминке
        return "Заказ  %s %s" % (self.id, self.status_ord.status_name)


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    nmb = models.PositiveSmallIntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # price*nmb

    class Meta:
        verbose_name = "Товар в корзине"  # приомзносимое имя в единственном числе
        verbose_name_plural = "Товары в корзине"  # приомзносимое имя во множественном числе

    def save(self, *args, **kwargs):
        self.price_per_item = self.product.price
        self.total_price = int(self.nmb) * self.price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)