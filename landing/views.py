# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.template.context_processors import csrf
from django.views.generic import FormView, View
from django.contrib.auth.forms import UserCreationForm

from products.models import ProductCategory, Product, ProductImage
from . import models
from .models import Category
from .forms import Login, UserCreation, UserChange, ProfileChange


# from products.models import *


def home(request):

    args = {}
    args.update(csrf(request))
    session_key = request.session.session_key
    # args['user'] = auth.get_user(request)
    args['tempText'] = 'Сайт находится в стадии разработки'
    # args['form'] = Login()
    # args['form2'] = UserCreation()
    args['category_product'] = ProductCategory.objects.all()
    # args['product_image'] = ProductImage.objects.filter(is_main=True, is_active=True)
    user = auth.get_user(request)
    product_image = ProductImage.objects.filter(is_main=True, is_active=True)
    form = Login()
    form2 = UserCreation()

    if request.POST:  # and args['form'].is_valid():
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if password2:
            newuser_form = UserCreation(request.POST)
            if newuser_form.is_valid():
                print("вьюха -> Pass2 Valid: ", username, password2)
                newuser_form.save()
                newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                            password=newuser_form.cleaned_data['password2'])
                auth.login(request, newuser)

                return redirect('/')
                # return HttpResponse('ok', content_type='text/html')
            else:
                args['form'] = newuser_form

                return HttpResponse(args)  # , content_type='text/html')
                # return redirect('/')
                # return render_to_response('landing/home.html', args)
        else:
            print("вьюха -> UUUU: ", username, password2)
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                print("вьюха -> login: ", username, password)
                auth.login(request, user)
                return redirect('/')
            else:
                # if username:
                #     print("вьюха -> login:  NONONOONONONONONONONONONO")
                args['login_error'] = "Вход не выполнен"
                print("вьюха -> login: ", username, password)
                return redirect('/')
                # return render_to_response('landing/home.html', args)
    elif request.GET:
        error_text = ""
        newuser_form = UserCreation(request.GET)
        us = request.GET['username']
        try:
            us1 = User.objects.get(username=us)
            print(us, us1)
            if us == us1.username:
                error_text += "Такой пользователь уже существует. "
        except User.DoesNotExist:
            # pass
            # # error_text = "ok"
            # # password = request.GET['password']
            # password1 = request.GET['password1']
            # password2 = request.GET['password2']

            if newuser_form.is_valid():
                # print("вьюха -> login:  GgggggGGGGGGGGGGggggg", request.GET['username'])
                newuser_form.save()
                newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                            password=newuser_form.cleaned_data['password2'])
                auth.login(request, newuser)
                # return redirect('/')
                return HttpResponse(error_text)
            error_text += " Пароль слишком легкий"
            return HttpResponse(error_text)

        return HttpResponse(error_text)
    else:

        # return render_to_response('landing/home.html', args)
        return render(request, 'landing/home.html', locals())
        # return render_to_response('wrapper.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required
@transaction.atomic
def update_profile(request):
    args = {}
    args.update(csrf(request))
    args['user'] = auth.get_user(request)
    args['tempText'] = 'Сайт находится в стадии разработки'
    args['users'] = User.objects.all()
    args['category_list'] = Category.objects.all()

    # for elem in args['users']:
    #     print(elem.profile.__dict__)

    return render(request, 'account/accounts.html', args)
    # return render_to_response('account/accounts.html', args)
    # return redirect('/')

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
