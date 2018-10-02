from json import JSONDecodeError

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.utils.datastructures import MultiValueDictKeyError

from landing.forms import Login, UserCreation
from orders.forms import BasketForm
from .forms import ProductImageForm, ProductForm, AddingFabricForm, AddProductCatForm
from products.models import *
# import requests
import json


# adm_product (product.html)
@login_required
@transaction.atomic
def adding_fabric(request):
    args = dict()
    args.update(csrf(request))
    if request.POST and request.FILES:

        form = AddingFabricForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    elif request.POST:
        form = AddingFabricForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('/admin_product')


# adm_product (product.html)
@login_required
@transaction.atomic
def adding_product_cat(request):
    args = dict()
    args.update(csrf(request))
    if request.POST:
        form = AddProductCatForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('/admin_product')


# adm_product (product.html)
@login_required
@transaction.atomic
def adm_products(request):
    args = dict()
    args.update(csrf(request))

    args['products'] = Product.objects.all()

    args['form1'] = ProductForm(request.POST or None)
    args['form2'] = ProductImageForm()
    args['form3'] = AddingFabricForm()
    args['form4'] = AddProductCatForm()

    # if request.method == "GET":
    if request.POST:
        if request.POST.get('SearchProduct'):
            args['products'] = Product.objects.filter(article__contains=request.POST.get('SearchProduct'))
            if len(args['products']) == 0:
                args['products'] = Product.objects.filter(name__contains=request.POST.get('SearchProduct'))
                if len(args['products']) == 0:
                    args['products'] = Product.objects.all()
        else:
            try:
                article = request.POST.get('article')
                if Product.objects.filter(article=article).exists():

                    product = Product.objects.get(article=article)
                    args['form1'] = ProductForm(request.POST, instance=product)
                    print("наш запрос изменение", request)
                    if args['form1'].is_valid():
                        print("TUT TUT TUT", request.POST.get('sizes'))
                        nf = args['form1'].save(commit=False)
                        nf.save(force_update=True)
                        args['form1'].save_m2m()
                        return redirect('/admin_product')
                else:
                    print("наш запрос создание", request)
                    args['form1'] = ProductForm(request.POST)

                    if args['form1'].is_valid():
                        nf = args['form1'].save(commit=False)
                        nf.save()
                        args['form1'].save_m2m()
                        return redirect('/admin_product')

            except MultiValueDictKeyError:
                print("U_______________MultiValueDictKeyError")
            except:
                print("U_______________XZ___KeyError")
                return redirect('/admin_product')
    return render(request, 'products/product.html', args)


# adm_product (product.html)
@login_required
@transaction.atomic
def adm_new_products(request):
    args = dict()
    args.update(csrf(request))
    if request.POST and request.POST.get('article'):
        products = ProductImage.objects.filter(product__article=request.POST.get('article')).values(
            'id', 'product_id', 'product__article', 'product__category__name', 'product__name', 'product__fabric__name',
            'product__price', 'product__discount', 'product__year_model', 'product__prod_active', 'product__status_new',
            'product__status_sale', 'product__second_hands', 'product__short_description', 'product__description',
            'is_active', 'is_main', 'image'
        )
        if len(products) == 0:
            product = Product.objects.get(article=request.POST.get('article'))

            products = [
                {'product_id': product.id, 'product__name': product.name, 'product__article': product.article,
                 'product__category__name': product.category.name, 'product__fabric__name': product.fabric.name,
                 'product__price': product.price, 'product__discount': product.discount,
                 'product__year_model': product.year_model, 'product__prod_active': product.prod_active,
                 'product__status_new': product.status_new, 'product__status_sale': product.status_sale,
                 'product__second_hands': product.second_hands, 'product__short_description': product.short_description,
                 'product__description': product.description,
                 }
            ]
        json_orders_user = json.dumps(list(products), cls=DjangoJSONEncoder)
        return JsonResponse(json_orders_user, safe=False)
    return JsonResponse(False, safe=False)


# adm_product (product.html)
@login_required
@transaction.atomic
def adm_sizes_for_new_products(request):
    args = dict()
    args.update(csrf(request))
    if request.POST and request.POST.get('article'):
        sizes = ProductSizes.objects.filter(product__article=request.POST.get('article')).values('id', 'name_size')
        json_orders_user = json.dumps(list(sizes), cls=DjangoJSONEncoder)
        return JsonResponse(json_orders_user, safe=False)
    return JsonResponse(False, safe=False)


@login_required
@transaction.atomic
def adm_products_img_add(request):
    args = dict()
    args.update(csrf(request))
    if request.POST:
        # args['form2'] = ProductImageForm()
        args['form2'] = ProductImageForm(request.POST, request.FILES)
        if args['form2'].is_valid():
            args['form2'].save()
            # return render(request, 'products/product.html', args)
            return redirect('/admin_product')
    return redirect('/admin_product')


# sends js data to the output of pictures for the selected product (js:AutoProductList)
# @login_required
# @transaction.atomic
# def adm_product_img(request):
#     args = dict()
#     # args.update(csrf(request))
#     products_img_list = []
#     if request.POST:
#         name = request.POST.get('name')
#         for img in ProductImage.objects.filter(product__name=name):
#             products_img_list.append([img.image.url, img.is_main, img.is_active, img.id])
#
#         args['products_img_list'] = products_img_list
#         dumps = json.dumps(args)
#         return HttpResponse(dumps)


@login_required
@transaction.atomic
def image_product_del(request):
    args = dict()
    if request.POST:
        args.update(csrf(request))
        img = request.POST.get('img_for_del')
        del_img = ProductImage.objects.get(id=img)
        del_img.delete()
        print("удаление image_product_del")

    return redirect('/admin_product')


@login_required
@transaction.atomic
def adm_product_save(request):
    if request.method == "GET":
        json_data = request.GET
        list_img = {}
        for elem in json_data:
            if elem != "_":
                # json_data_elem = eval(elem) #  не воспринимает true & false
                # try:
                json_data_elem = json.loads(elem)
                for dic in json_data_elem:
                    if dic == "image_id":
                        for id in json_data_elem[dic]:
                            # print("image_id____________________image_id__", json_data_elem[dic][id],
                            #       "type elem ->", type(json_data_elem[dic][id]), end="\n")
                            fotka = ProductImage.objects.get(id=int(id))
                            fotka.is_main = json_data_elem[dic][id][0]
                            fotka.is_active = json_data_elem[dic][id][1]
                            fotka.save()

                    # else:
                    #     print("test____________________test", json_data_elem[dic],
                    #           "type elem ->", type(json_data_elem[dic]), end="\n")

    dumps = json.dumps("OK")
    return HttpResponse(dumps)


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    # prod1 = product.productinbasket_set.values('price_per_item')
    if auth.get_user(request).username != AnonymousUser.username:
        user = auth.get_user(request)

    # else:
    #     user = False

    pr_img = ProductImage.objects.filter(product=product_id)
    # form = BasketForm(request.POST, instance=product)
    form = BasketForm(request.POST)
    if request.POST:
        form = BasketForm(request.POST)
        data = request.POST
        price_per_item = data.get('price_per_item')
        if form.is_valid():
            obj = form.save(commit=False)
            obj.session_key = request.session.session_key
            obj.product = product
            obj.price_per_item = price_per_item
            obj.save()
            return redirect("/admin_product/product/" + str(product_id))

    return render(request, 'products/us_product.html', locals())


def product_by_category(request, category_id):
    product_image = ProductImage.objects.filter(is_main=True, is_active=True, product__category=category_id,
                                                product__second_hands=False)
    return render(request, 'products/products_by_category.html', locals())


def all_product(request):
    product_image = ProductImage.objects.filter(is_main=True, is_active=True, product__second_hands=False)
    return render(request, 'products/products_by_category.html', locals())


def baraholka(request):
    product_image = ProductImage.objects.filter(is_main=True, is_active=True, product__second_hands=True)
    return render(request, 'products/products_by_category.html', locals())


def brands(request):
    args = {}
    args['brands'] = Fabric.objects.all()
    return render(request, 'products/brands.html', args)


def brand(request, brand_id):
    fabric = Fabric.objects.filter(id=brand_id)
    return render(request, 'products/brand.html', locals())
