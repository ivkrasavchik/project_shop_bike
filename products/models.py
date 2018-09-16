from django.db import models


class Fabric(models.Model):
    name = models.CharField(max_length=64)
    short_description = models.TextField(max_length=256, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    logo = models.ImageField(upload_to='logo/', blank=True)

    class Meta:
        # django само определяет единственное и множественное число, но можно переопределить
        verbose_name = "Фабрика"  # приомзносимое имя в единственном числе
        verbose_name_plural = "Фабрики"  # приомзносимое имя во множественном числе

    def __str__(self):  # настройка презинтации модели вадминке
        return "%s" % self.name

    def __unicode__(self):
        return self.logo.url


class ProductCategory(models.Model):
    name = models.CharField(max_length=64)
    is_activ = models.BooleanField(default=True)

    class Meta:
        # django само определяет единственное и множественное число, но можно переопределить
        verbose_name = "Категория товара"  # приомзносимое имя в единственном числе
        verbose_name_plural = "Категория товаров"  # приомзносимое имя во множественном числе

    def __str__(self):  # настройка презинтации модели вадминке
        return "%s" % self.name


class ProductSizes(models.Model):
    name_size = models.CharField(max_length=5)

    class Meta:
        verbose_name = "Размер"  # приомзносимое имя в единственном числе
        verbose_name_plural = "Размеры"  # приомзносимое имя во множественном числе

    def __str__(self):  # настройка презинтации модели вадминке
        return "%s" % self.name_size


class Product(models.Model):  # модели принято называть в ед. числе
    name = models.CharField(max_length=64, unique=True)
    article = models.CharField(max_length=7, default="артикул", unique=True)
    # purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Цена закупки
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # allowance = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=20)  # торговая надбавка
    discount = models.IntegerField(default=0)
    category = models.ForeignKey(ProductCategory, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    short_description = models.TextField(max_length=128, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    prod_active = models.BooleanField(default=True)
    year_model = models.CharField(max_length=10, default="2018")
    status_new = models.BooleanField(default=True)
    status_sale = models.BooleanField(default=True)
    second_hands = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=True, auto_now=False)
    fabric = models.ForeignKey(Fabric, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    sizes = models.ManyToManyField(ProductSizes, blank=True, null=True, default=None)

    class Meta:
        # django само определяет единственное и множественное число, но можно переопределить
        verbose_name = "Товар"  # приомзносимое имя в единственном числе
        verbose_name_plural = "Товары"  # приомзносимое имя во множественном числе

    def __str__(self):  # настройка презинтации модели вадминке
        return "%s %s" % (self.price, self.name)


class ProductImage(models.Model):  # модели принято называть в ед. числе
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        # django само определяет единственное и множественное число, но можно переопределить
        verbose_name = "Фото"  # приомзносимое имя в единственном числе
        verbose_name_plural = "Фотографии"  # приомзносимое имя во множественном числе

    def __str__(self):  # настройка презинтации модели вадминке
        return "%s" % self.id

    def __unicode__(self):
        return self.image.url



