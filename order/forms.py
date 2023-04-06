from django import forms
from order.models import *

class OrderForm(forms.Form):
    addressId =  forms.ChoiceField(widget=forms.Select)


""" class OrderForm(forms.ModelForm): 
    class Meta:
        model = Order
        fields = [
            'first_name',
            'last_name',
            'email',
            'address',
            'phone',
            'city',
            'country'
        ] """