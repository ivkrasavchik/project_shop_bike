# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf

from products.models import ProductCategory, ProductImage

from .models import Category
from .forms import Login, UserCreation, UserChange, ProfileChange


# from products.models import *
def alt_login(request):
    args = {}
    args.update(csrf(request))
    args['session_key'] = request.session.session_key
    args['tempText'] = "TEST TEST TEST TEST"+str(args['session_key'])

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'landing/home.html', args)
    return render(request, 'landing/home.html', args)


def alt_register(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        newuser_form = UserCreation(request.POST)
        error_text = ""
        us = request.POST.get('username')
        try:
            us1 = User.objects.get(username=us)
            if us == us1.username:
                error_text += "Такой пользователь уже существует. "
        except User.DoesNotExist:
            if newuser_form.is_valid():
                newuser_form.save()
                newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                            password=newuser_form.cleaned_data['password2'])
                auth.login(request, newuser)
                return HttpResponse(error_text)
            error_text += " Пароль слишком легкий"
            return HttpResponse(error_text)

        return HttpResponse(error_text)

    elif request.GET:
        return render(request, 'landing/home.html', args)
    else:
        return render(request, 'landing/home.html', args)


def home(request):
    args = {}
    args.update(csrf(request))
    if auth.get_user(request).username != AnonymousUser.username:
        args['user'] = auth.get_user(request)
    args['product_image'] = ProductImage.objects.filter(is_main=True, is_active=True, product__status_new=True)
    return render(request, 'landing/home.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required
@transaction.atomic
def update_profile(request):
    args = {}
    args['user'] = auth.get_user(request)
    args['tempText'] = 'Сайт находится в стадии разработки'
    args['users'] = User.objects.all()
    args['category_list'] = Category.objects.all()
    if request.POST:
        args.update(csrf(request))
        if request.POST.get('SearchUser'):
            args['users'] = User.objects.filter(username__contains=request.POST.get('SearchUser'))
    return render(request, 'account/accounts.html', args)


# (Accounts)<-- Change user data (js:change_profile_view)
@login_required
@transaction.atomic
def profile_view(request):
    args = {}
    args.update(csrf(request))

    if request.method == "GET":
        user = User.objects.get(pk=request.GET['user_id'])
        args['form'] = UserChange(request.GET, instance=user)
        args['form2'] = ProfileChange(request.GET)
        args['username'] = request.GET['username']
        user.profile.phone = request.GET['phone']
        user.profile.spare_phone = request.GET['spare_phone']
        user.profile.address_delivery = request.GET['address_delivery']
        args['category'] = request.GET['category']
        for category in Category.objects.all():
            if category.cat == args['category']:
                user.profile.category = category

        user.profile.discount = request.GET['discount']
        user.profile.short_description = request.GET['short_description']
        args['first_name'] = request.GET['first_name']
        args['is_active'] = request.GET['is_active']
        args['is_staff'] = request.GET['is_staff']

        if args['form'].is_valid():
            args['form'].save()

            return redirect('/')

        return HttpResponse('ok', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')


def temp_link(request):
    args = {}
    args['tempText'] = "Гори асфальт"
    return render(request, 'temp.html', args)



# def home(request):
#     args = {}
#     args.update(csrf(request))
#     args['user'] = auth.get_user(request)
#     args['tempText'] = 'Сайт находится в стадии разработки'
#     args['form'] = Login()
#     print(args['user'])
#     if request.POST:
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             print("вьюха -> login: ", username, password)
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             args['login_error'] = "Пользователь не найден"
#             print("вьюха -> login: ", username, password)
#             return render_to_response('landing/home.html', args)
#     else:
#         return render_to_response('landing/home.html', args)


# def home(request):
#     args = {}
#     args.update(csrf(request))
#     args['user'] = auth.get_user(request)
#     args['tempText'] = 'Сайт находится в стадии разработки'
#     print(args['user'])
#     if request.POST:
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             print("вьюха -> login: ", username, password)
#             auth.login(request, user)
#             return redirect('/')
#
#         else:
#             args['login_error'] = "Пользователь не найден"
#             print("вьюха -> login: ", username, password)
#             return render_to_response('landing/home.html', args)
#
#     else:
#         return render_to_response('landing/home.html', args)

#
# def login(request):
#     args = {}
#     args.update(csrf(request))
#     if request.POST:
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             print("вьюха -> login: ", username, password)
#             auth.login(request, user)
#             return redirect('/')
#
#         else:
#             args['login_error'] = "Пользователь не найден"
#             print("вьюха -> login: ", username, password)
#             return render_to_response('account/login.html', args)
#
#     else:
#         return render_to_response('account/login.html', args)
