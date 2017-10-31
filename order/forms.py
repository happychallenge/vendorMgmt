from django import forms
from django.forms import inlineformset_factory

from products.models import Vendor, Contact
from .models import POrder, POrderItem, PayCondition, Shipping, Material

class PayConditionForm(forms.ModelForm):
    class Meta:
        model = PayCondition
        fields = '__all__'

class POrderForm(forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all())
    contact = forms.ModelChoiceField(queryset=Contact.objects.all())
    class Meta:
        model = POrder
        fields = ['offer_no', 'name', 'vendor', 'contact', 'total_amount', 
                'confirmed', 'fixed', 'paid', 'contract_date']

PayConditionFormSet = inlineformset_factory(POrder, PayCondition, 
            form=PayConditionForm, extra=1)

class POrderItemForm(forms.ModelForm):
    class Meta:
        model = POrderItem
        fields = ['porder', 'product', 'ptype', 'amount', 'unit_price', 
                    'purchase_price', 'packing',  ]

POrderItemFormSet = inlineformset_factory(POrder, POrderItem, 
            form=POrderItemForm, extra=2)


class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['destination', 'shipping_date', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows':2}),
        }

ShippingFormSet = inlineformset_factory(POrder, Shipping, 
            form=ShippingForm, extra=0)

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['invoice', 'packingList', 'billofLading', 'coa', 'fta_co', 'baoguandan']
