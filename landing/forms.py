import unicodedata

from django import forms
from django.contrib.auth import forms as ausforfs
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core import validators
from django.forms import CharField, EmailInput

from .models import *


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))


class Login(AuthenticationForm):
    username = UsernameField(
        label="Введите Ваш login",
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'style': 'margin:5px; padding:10px;height:30px;',
                                      'class': 'form-control col-sm-12',
                                      'placeholder': 'Введите Ваш Email'
                                      }),
    )

    password = forms.CharField(
        label="Введите Ваш пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'style': 'margin:5px; padding:10px;height:30px;',
            'class': 'form-control col-sm-8',
            'placeholder': 'Введите Ваш пароль'
        }),
    )
    class Meta:
        model = User
        fields = ('username',)

    # widgets = {
    #     'username': forms.TextInput(attrs={
    #         'style': 'margin:5px; padding:10px;height:30px;',
    #         'class': 'form-control col-sm-8',
    #         'placeholder': 'Введите Ваш login',
    #     })
    # }

    def __init__(self, *args, **kwargs):
        # for field in self.base_fields.values():
        #     field.widget.attrs['placeholder'] = field.label
        super(AuthenticationForm, self).__init__(*args, **kwargs)


class UsernameFieldEmail(CharField):

    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

    widget = EmailInput(attrs={
            'autofocus': True,
            'style': 'margin:5px; padding:10px;height:30px;',
            'class': 'form-control col-sm-12',
            'placeholder': 'Введите Ваш Email'
        })
    default_validators = [validators.EmailValidator(message='Email то липовый')]

    def __init__(self, **kwargs):
        super().__init__(strip=True, **kwargs)


class UserCreation(UserCreationForm):
    error_messages = {
        'password_mismatch': "Поля ввода пароля должны совпадать",
    }

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'style':'margin:5px; padding:10px;height:30px;',
            'class':'form-control col-sm-8',
            'placeholder': 'Введите Ваш пароль'
        }),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={
            'style':'margin:5px; padding:10px;height:30px;',
            'class':'form-control col-sm-8',
            'placeholder': 'Подтвердите пароль'
        }),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameFieldEmail}
        # тут мы очищаем поля подсказок
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }


    def __init__(self, *args, **kwargs):
        # for field in self.base_fields.values():
        #     field.widget.attrs['placeholder'] = field.label
        super(UserCreationForm, self).__init__(*args, **kwargs)


class UserChange(UserChangeForm):
    class Meta:
        model = User
        fields = ("first_name", "is_staff", "is_active", "password")
        # fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        # def clean_password(self):
        #     return ""


class ProfileChange(forms.Form):
    class Meta:
        model = Profile
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
