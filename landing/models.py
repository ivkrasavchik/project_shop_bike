# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    cat = models.CharField(max_length=24, verbose_name="Категория клиента")
    discount = models.DecimalField(max_digits=3, blank=True, null=True, decimal_places=1)

    class Meta:
        # django само определяет единственное и множественное число, но можно переопределить
        verbose_name = "Категория клиента"  # приомзносимое имя в единственном числе
        verbose_name_plural = "Категории клиентов"  # приомзносимое имя во множественном числе

    def __str__(self):  # настройка презинтации модели вадминке
        # return "%s %s" % (self.cat, self.discount)
        return self.cat


class Profile(models.Model):
    user = models.OneToOneField(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=False, null=False, default="User", verbose_name="Имя")
    phone = models.CharField(max_length=15, blank=False, null=False, default="+375", verbose_name="Телефон")
    spare_phone = models.CharField(max_length=15, blank=True, verbose_name="Доп. телефон")
    address_delivery = models.TextField(max_length=128, verbose_name="Адрес доставки", default="Уточнять при заказе")
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.DO_NOTHING,
                                 default=None, db_constraint=False)
    discount = models.IntegerField(default=0, verbose_name="Скидка")
    short_description = models.TextField(max_length=128, blank=True, verbose_name="Дополнительная информация")


    class Meta:
        # django само определяет единственное и множественное число, но можно переопределить
        verbose_name = "Клиент"  # приомзносимое имя в единственном числе
        verbose_name_plural = "Клиенты"  # приомзносимое имя во множественном числе

    def __str__(self):  # настройка презинтации модели вадминке
        return "%s " % self.user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
