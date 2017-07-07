from django import forms
from django.forms import Textarea

from .models import Vendor, Product, Contact, Quotation

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

class QuotationForm(forms.ModelForm):

    POWDER = 'POWDER'
    GRANULAR = 'GRANULAR'
    LIQUID = 'LIQUID'
    PRODUCTTYPE = (
        (POWDER, 'POWDER'),
        (GRANULAR, 'GRANULAR'),
        (LIQUID, 'LIQUID'),
    )

    vendor = forms.IntegerField(widget=forms.HiddenInput())
    vendor_name = forms.CharField()
    # effective_date = forms.DateField(widget=forms.DateInput(attrs={'required': False}))
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    ptype = forms.ChoiceField(widget=forms.RadioSelect, choices=PRODUCTTYPE)
    currency = forms.RadioSelect()

    class Meta:
        model = Quotation
        fields = ['vendor', 'vendor_name', 'product', 'ptype',  'price', 
                'currency', 'payterm', 'effective_date', 'status', 'comments']
        widgets = {
            'comments': Textarea(attrs={'rows': 3}),
        }

class QuotationSimpleForm(forms.Form):
    vendor = forms.IntegerField(widget=forms.HiddenInput())
    quotation = forms.IntegerField(widget=forms.HiddenInput())
    newprice = forms.FloatField()


class QuotationUpdateForm(forms.ModelForm):
    quotation = forms.IntegerField(widget=forms.HiddenInput())
    vendor = forms.IntegerField(widget=forms.HiddenInput())
    vendor_name = forms.CharField()
    product = forms.IntegerField(widget=forms.HiddenInput())
    product_name = forms.CharField()

    oldprice = forms.CharField()
    oldpayterm = forms.CharField()
    # ptype = forms.RadioSelect()

    class Meta:
        model = Quotation
        fields = ['quotation', 'vendor', 'vendor_name', 'product', 'product_name', 
                    'oldprice', 'price', 'currency', 'oldpayterm', 'payterm', 
                    'effective_date', 'status', 'comments']
        widgets = {
            'comments': Textarea(attrs={'rows': 3}),
        }
