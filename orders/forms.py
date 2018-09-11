from django import forms

from .models import *


class BasketForm(forms.ModelForm):

    class Meta:
        model = ProductInBasket
        fields = '__all__'
        # widgets = {'session_key': forms.HiddenInput}

    def __init__(self, *args, **kwargs):
        super(BasketForm, self).__init__(*args, **kwargs)
        self.fields['session_key'].required = False


class AddOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

        widgets = {'User': forms.HiddenInput,
                   # 'status_ord': forms.Select(attrs={'disabled': True}),
                   # 'status_ord': forms.HiddenInput,
                   # 'total_price': forms.NumberInput(attrs={'disabled': True})
                   }

    def __init__(self, *args, **kwargs):
        super(AddOrder, self).__init__(*args, **kwargs)
        self.fields['total_price'].required = False
        self.fields['status_ord'].required = False


class AdmProductInOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'