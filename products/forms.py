from django import forms
from django.forms import Textarea
from django.utils.html import mark_safe
from django.template import Template

from .models import Vendor, Product, Contact, Quotation, Sourcing

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html = Template("""<img src='$link'/>""")
        return mark_safe(html.render(link=value))


class ContactForm(forms.ModelForm):
    # picture = forms.ImageField(widget=PictureWidget)

    class Meta:
        model = Contact
        fields = [ 'user', 'vendor', 'cn_name', 'en_name', 'role', 'picture', 
                'email', 'mobile', 'fixed', 'wechat', 'qq']

class QuotationProductForm(forms.ModelForm):

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


# For views.sourcing_productadd
class SourcingProductForm(forms.ModelForm):

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

# 제품을 선택하도록 함 
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    ptype = forms.ChoiceField(widget=forms.RadioSelect, choices=PRODUCTTYPE)

    class Meta:
        model = Sourcing
        fields = ['vendor', 'vendor_name', 'product', 'ptype',  'buying_price', 
                'payterm', 'effective_date', 'status', 'comments']
        widgets = {
            'comments': Textarea(attrs={'rows': 3}),
        }

class SourcingPriceForm(forms.ModelForm):

    vendor = forms.IntegerField(widget=forms.HiddenInput())
    vendor_name = forms.CharField()
    product = forms.IntegerField(widget=forms.HiddenInput())
    product_name = forms.CharField()
    ptype = forms.CharField()

    class Meta:
        model = Sourcing
        fields = [ 'vendor', 'vendor_name', 'product', 'product_name', 'ptype',  
                'buying_price', 'payterm', 'effective_date', 'status', 'comments']
        widgets = {
            'comments': Textarea(attrs={'rows': 3}),
        }


class SourcingSimpleForm(forms.Form):
    vendor = forms.IntegerField(widget=forms.HiddenInput())
    sourcing = forms.IntegerField(widget=forms.HiddenInput())
    newprice = forms.FloatField()

