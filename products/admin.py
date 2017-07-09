from django.contrib import admin

# Register your models here.
from .models import Vendor, Tag, Contact, Category, Product, VendorProduct, Quotation


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    class Meta:
        model = Vendor
    list_display = ['id', 'cn_name', 'en_name', 'companytype', 'status']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    class Meta:
        model = Tag
    list_display = ['tag', ]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    class Meta:
        model = Contact
    list_display = ['cn_name', 'vendor', 'role', 'mobile', 'email',  'wechat', 'qq']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category
    list_display = ['cn_name', 'en_name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product
    list_display = ['cn_name', 'en_name', 'category']

@admin.register(VendorProduct)
class VendorProductAdmin(admin.ModelAdmin):
    class Meta:
        model = VendorProduct
    list_display = ['id', 'vendor', 'product', 'ptype', 'created_at']
    list_select_related = ('vendor', 'product')
    search_fields = [ 'vendor__en_name', 'product__en_name' ]

def update_quote_invalid(modeladmin, request, queryset):
    queryset.update(status='I')
update_quote_invalid.short_description = 'Update Quotaion In-Valid'

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    class Meta:
        model = Quotation
    list_display = ['vendorproduct', 'price', 'currency', 'quote_date', 'effective_date', 'status']
    actions = [ update_quote_invalid ]
    search_fields = [ 'vendorproduct__vendor__en_name', 'vendorproduct__product__en_name']



# def update_exchange_rate(modeladmin, request, queryset):
#     exchange_rate = get_exchange_rate()
#     queryset.update(exchange_rate=exchange_rate)
# update_exchange_rate.short_description = 'Update Exchange Rate'


# def get_exchange_rate():
#     html = requests.get('http://hq.sinajs.cn/rn=1494394971815list=fx_susdcny').text
#     matched = re.search(r'(?<=\d{2}:\d{2}:\d{2},)(\d\.\d*)', html)
#     if matched:
#         exchange_rate = matched.group(0)
#     else:
#         exchange_rate = None

#     return exchange_rate


# @admin.register(ExchangeRate)
# class ExchangeRateAdmin(admin.ModelAdmin):
#     class Meta:
#         model = ExchangeRate
#     list_display = ['date', 'exchange_rate', 'created_at']
#     actions = [ update_exchange_rate ]
