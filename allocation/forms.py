from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet

from .models import Demand, DemandClient, Supply, SupplyVendor


class DemandForm(forms.ModelForm):
    class Meta:
        model = Demand
        fields = ['product', 'year', 'month', 'total_demand']


class DemandClientForm(forms.ModelForm):
    class Meta:
        model = DemandClient
        exclude = ()

DemandClientFormSet5 = inlineformset_factory(Demand, DemandClient, 
            form=DemandClientForm, extra=5)
DemandClientFormSet = inlineformset_factory(Demand, DemandClient, 
            form=DemandClientForm, extra=0)


class BaseSupplyFormSet(BaseInlineFormSet):
    def clean(self):
        super(BaseSupplyFormSet, self).clean()

        for form in self.forms:
            unit_price = form.cleaned_data.get('unit_price', 0)
            amount = form.cleaned_data.get('amount', 0)
            if unit_price and amount:
                form.cleaned_data['purchase_price'] = unit_price * amount
        return self.cleaned_data

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['demand', 'total_supply']


class SupplyVendorForm(forms.ModelForm):
    class Meta:
        model = SupplyVendor
        fields = ['supply', 'vendor', 'amount', 'unit_price', 'purchase_price']
        # widgets = {
        #     'purchase_price': forms.HiddenInput(),
        # }

SupplyVendorFormSet5 = inlineformset_factory(Supply, SupplyVendor, 
        form=SupplyVendorForm, formset=BaseSupplyFormSet, extra=5)
SupplyVendorFormSet = inlineformset_factory(Supply, SupplyVendor, 
        form=SupplyVendorForm, formset=BaseSupplyFormSet, extra=0)