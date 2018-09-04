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
