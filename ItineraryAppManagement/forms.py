from django import forms
from .models import Order
from phonenumber_field.formfields import PhoneNumberField

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields = [ 'email','phone','countryphone_code']
