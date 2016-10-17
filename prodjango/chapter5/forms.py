from django import forms
from chapter5 import widgets


class ProductEntry(forms.Form):
    sku = forms.IntegerField(label='SKU')
    description = forms.CharField(widget=forms.Textarea())
    price = forms.DecimalField(decimal_places=2, widget=widgets.PriceInput())
    tax = forms.IntegerField(widget=widgets.PercentInput())
