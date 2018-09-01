from json import JSONDecodeError

from django.contrib.auth.decorators import login_required
from django.core.serializers import json
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.utils.datastructures import MultiValueDictKeyError

from .forms import ProductImageForm, ProductForm
from products.models import *
# import requests
import json


@login_required
@transaction.atomic
def adm_products(request):
    args = dict()
    args.update(csrf(request))

    args['products'] = Product.objects.all()

    args['form1'] = ProductForm(request.POST or None)
    args['form2'] = ProductImageForm()

    if request.method == "GET":

        try:
            article = request.GET['article']
            if Product.objects.filter(article=article).exists():
                print("наш запрос изменение", request)
                product = Product.objects.get(article=article)
                args['form1'] = ProductForm(request.GET, instance=product)
                if args['form1'].is_valid():
                    args['form1'].save()
                    dumps = json.dumps("OK")
                    return HttpResponse(dumps)
            else:
                print("наш запрос создание", request)
                args['form1'] = ProductForm(request.GET)
                if args['form1'].is_valid():
                    print("NEW_____NEW_____NEW")
                    args['form1'].save()
                    dumps = json.dumps("OK")
                    return HttpResponse(dumps)

        except MultiValueDictKeyError:
            print("U_______________MultiValueDictKeyError")
        except:
            print("U_______________XZ___KeyError")

    if request.POST:
        print("_______________POST________________")
        # args['form2'] = ProductImageForm()
        args['form2'] = ProductImageForm(request.POST, request.FILES)
        if args['form2'].is_valid():
            print("NEW_____IMAGE_____NEW")
            args['form2'].save()
            return redirect('/admin_product')
    return render(request, 'products/product.html', args)


@login_required
@transaction.atomic
def adm_product_img(request):
    args = dict()
    products_img_list = []
    name = request.GET['name']

    for img in ProductImage.objects.filter(product__name=name):
        products_img_list.append([img.image.url, img.is_main, img.is_active, img.id])
        print("UUUUUUUUUUUUU", img.product.name, "url", img.image.url, "is_main", img.is_main, "is_activ", img.is_active, "id", img.id)

    args['products_img_list'] = products_img_list
    dumps = json.dumps(args)
    return HttpResponse(dumps)


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
                            print("image_id____________________image_id__", json_data_elem[dic][id], "type elem ->", type(json_data_elem[dic][id]), end="\n")
                            fotka = ProductImage.objects.get(id=int(id))
                            fotka.is_main = json_data_elem[dic][id][0]
                            fotka.is_active = json_data_elem[dic][id][1]
                            fotka.save()

                    else:
                        print("test____________________test", json_data_elem[dic], "type elem ->", type(json_data_elem[dic]), end="\n")
    #                         print("FFFFFFFFFFFFFFFFFFFFFFFFFFFF", json_data)
    #                 return HttpResponse("ok")
    #             except JSONDecodeError:
    #                 print("FFFFFFFFFFFFFFFFFFFFFFFFFFFF", elem)
    #                 # return HttpResponse("ok")
    #         else:
    #             print("else____________________else", list_img, "type list_img ->", type(list_img), end="\n")
    #     return HttpResponse("ok")
    #
    # print("YYYYYYYYYYYYYYYY")
    dumps = json.dumps("OK")
    return HttpResponse(dumps)


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'products/us_product.html', locals())