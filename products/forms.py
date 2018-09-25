from django import forms
from django.forms import Textarea, TextInput, NumberInput

from .models import *


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(),
                                      to_field_name="name", widget=forms.Select())
    fabric = forms.ModelChoiceField(queryset=Fabric.objects.all(), to_field_name="name", widget=forms.Select())

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'short_description': Textarea(attrs={'cols': 90, 'rows': 7, 'placeholder': "Краткое описание"}),
            'description': Textarea(attrs={'cols': 90, 'rows': 10, 'placeholder': "Полное описание"}),
            'article': TextInput(attrs={'size': 7, 'placeholder': "Артикул"}),
            'name': TextInput(attrs={'cols': 20, 'rows': 1, 'placeholder': "Имя"}),
            'year_model': TextInput(attrs={'size': 5, 'placeholder': "Год выпуска"}),
            'price': NumberInput(attrs={'size': 10, 'placeholder': "Цена"}),
            'discount': NumberInput(attrs={'size': 4, 'placeholder': "%"}),
        }


class ProductImageForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), to_field_name="name", widget=forms.Select())

    class Meta:
        model = ProductImage
        fields = '__all__'
