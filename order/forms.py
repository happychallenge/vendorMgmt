from django import forms
from django.forms import inlineformset_factory

from .models import POrder, POrderItem

class POrderForm(forms.ModelForm):
    class Meta:
        model = POrder
        fields = ['offer_no', 'name', 'vendor', 'contact', 'total_amount', 'paid']

class POrderItemForm(forms.ModelForm):
    class Meta:
        model = POrderItem
        fields = ['porder', 'product', 'quotation', 'ptype', 'amount', 'unit_price', 
                    'purchase_price', 'packing_type', 'unit_weight', 'pallet_weight' ]

POrderItemFormSet = inlineformset_factory(POrder, POrderItem, 
            form=POrderItemForm, extra=3)