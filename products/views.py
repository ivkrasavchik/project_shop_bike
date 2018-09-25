from json import JSONDecodeError

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.serializers import json
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.utils.datastructures import MultiValueDictKeyError

from landing.forms import Login, UserCreation
from orders.forms import BasketForm
from .forms import ProductImageForm, ProductForm
from products.models import *
# import requests
import json


# adm_product (product.html)
@login_required
@transaction.atomic
def adm_products(request):
    args = dict()
    args.update(csrf(request))

    args['products'] = Product.objects.all()

    args['form1'] = ProductForm(request.POST or None)
    args['form2'] = ProductImageForm()

    # if request.method == "GET":
    if request.POST:
        try:
            article = request.POST.get('article')
            if Product.objects.filter(article=article).exists():

                product = Product.objects.get(article=article)
                args['form1'] = ProductForm(request.POST, instance=product)
                print("наш запрос изменение", request)
                if args['form1'].is_valid():
                    print("Valid = True")
                    args['form1'].save()
                    return redirect('/admin_product')
            else:
                print("наш запрос создание", request)
                args['form1'] = ProductForm(request.POST)
                if args['form1'].is_valid():
                    print("NEW_____NEW_____NEW")
                    args['form1'].save()
                    dumps = json.dumps("OK")
                    return HttpResponse(dumps)

        except MultiValueDictKeyError:
            print("U_______________MultiValueDictKeyError")
        except:
            print("U_______________XZ___KeyError")
            return redirect('/admin_product')
    return render(request, 'products/product.html', args)


@login_required
@transaction.atomic
def adm_products_img_add(request):
    args = dict()
    args.update(csrf(request))
    if request.POST:
        print("_______________POST________________")
        # args['form2'] = ProductImageForm()
        args['form2'] = ProductImageForm(request.POST, request.FILES)
        if args['form2'].is_valid():
            print("NEW_____IMAGE_____NEW")
            args['form2'].save()
            return redirect('/admin_product')
    return redirect('/admin_product')


# sends js data to the output of pictures for the selected product (js:AutoProductList)
@login_required
@transaction.atomic
def adm_product_img(request):
    args = dict()
    # args.update(csrf(request))
    products_img_list = []
    if request.POST:
        name = request.POST.get('name')
        for img in ProductImage.objects.filter(product__name=name):
            products_img_list.append([img.image.url, img.is_main, img.is_active, img.id])

        args['products_img_list'] = products_img_list
        dumps = json.dumps(args)
        return HttpResponse(dumps)


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
