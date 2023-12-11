from django import forms
from .models import Order, OrderProduct, Payment


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "phone_number", "email",
                  "address_line", "departament", "city", "number_dui"]
