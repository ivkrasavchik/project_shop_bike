from django import forms
from django.forms import Textarea, TextInput, NumberInput

from .models import *


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(),
                                      to_field_name="name", widget=forms.Select())
    fabric = forms.ModelChoiceField(queryset=Fabric.objects.all(), to_field_name="name", widget=forms.Select())

    # sizes = forms.ModelMultipleChoiceField(queryset=ProductSizes.objects.all(), to_field_name="name_size",
    #                                        widget=forms.SelectMultiple())

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'short_description': Textarea(attrs={'placeholder': "Краткое описание"}),
            # 'short_description': Textarea(attrs={'cols': 90, 'rows': 7, 'placeholder': "Краткое описание"}),
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

    # def __init__(self, *args, **kwargs):
    #     super(ProductImageForm, self).__init__(*args, **kwargs)
    #     self.fields['product'].required = False


class AddingFabricForm(forms.ModelForm):

    class Meta:
        model = Fabric
        fields = '__all__'
        widgets = {
                   'short_description': Textarea(attrs={
                        'placeholder': "Краткое описание", 'id': "fabric_short_d"
                   }),
                   'description': Textarea(attrs={
                       'placeholder': "Полное описание", 'id': "fabric_d"
                   }),
                   'name': TextInput(attrs={
                       'placeholder': "Наименование производителя", 'id': "fabric_name"
                   })
        }


class AddProductCatForm(forms.ModelForm):

    class Meta:
        model = ProductCategory
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={
                'placeholder': "Название категории", 'id': "category_name"
            })
        }

