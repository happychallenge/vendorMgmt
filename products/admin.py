from django.contrib import admin

# Register your models here.
from .models import Vendor, Tag, Contact, Category, Product, VendorProduct
from .models import Quotation, Sourcing, Packing, Location
from allocation.models import Demand, Supply

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    class Meta:
        model = Location
    list_display = ['en_name', 'cn_name']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    class Meta:
        model = Vendor
    list_display = ['id', 'cn_name', 'en_name', 'simple_name', 'companytype', 'status']
    list_editable = ['en_name','simple_name']
    search_fields = ['en_name', 'cn_name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    class Meta:
        model = Tag
    list_display = ['tag', ]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    class Meta:
        model = Contact
    list_display = ['cn_name', 'en_name', 'vendor', 'role', 'mobile', 'email',  'wechat', 'qq']
    search_fields = ['cn_name', 'en_name', 'vendor__en_anme', 'vendor__cn_name']
    list_editable = [ 'en_name' ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category
    list_display = ['cn_name', 'en_name']


##############################
# Quotation
##############################
from datetime import date
def make_demand_plan(modeladmin, request, queryset):
    today = date.today()
    year = today.year
    for product in queryset:
        for yy in range(year, year+2):
            for month in range(1, 13):
                obj, created = Demand.objects.get_or_create(
                    product=product, year=yy, month=month
                )

                obj, created = Supply.objects.get_or_create(
                    demand = obj
                )
make_demand_plan.short_description = 'Make DEMAND & SUPPLY Planning'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product
    list_display = [ 'id', 'cn_name', 'en_name', 'category']
    actions = [make_demand_plan]



@admin.register(VendorProduct)
class VendorProductAdmin(admin.ModelAdmin):
    class Meta:
        model = VendorProduct
    list_display = ['id', 'vendor', 'product', 'ptype', 'created_at']
    list_select_related = ('vendor', 'product')
    search_fields = [ 'vendor__en_name', 'product__en_name' ]


##############################
# Quotation
##############################
def update_quote_invalid(modeladmin, request, queryset):
    queryset.update(status='I')
update_quote_invalid.short_description = 'Update Quotaion In-Valid'

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    class Meta:
        model = Quotation
    list_display = ['id', 'vendorproduct', 'price', 'currency', 'quote_date', 'effective_date', 'status']
    actions = [ update_quote_invalid ]
    search_fields = [ 'vendorproduct__vendor__en_name', 'vendorproduct__product__en_name']


##############################
# Sourcing
##############################
def update_usd_price(modeladmin, request, queryset):
    for sourcing in queryset:
        rate_taxrefund = sourcing.vendorproduct.product.rate_taxrefund/100
        buying_price = sourcing.buying_price
        usd_price = (buying_price - 
                            (buying_price/1.17*rate_taxrefund))/6.70
        sourcing.usd_price = usd_price
        sourcing.save()
update_usd_price.short_description = 'GET USD PRICE'

@admin.register(Sourcing)
class SourcingAdmin(admin.ModelAdmin):
    class Meta:
        model = Sourcing
    list_display = ['vendorproduct', 'buying_price', 'usd_price', 'sales_price',
                'quote_date', 'effective_date', 'status']
    actions = [ update_quote_invalid, update_usd_price ]
    search_fields = [ 'vendorproduct__vendor__en_name', 'vendorproduct__product__en_name']




@admin.register(Packing)
class PackingAdmin(admin.ModelAdmin):
    class Meta:
        model = Packing
    list_display = ['product', 'ptype', 'packing_type', 'unit_weight', 'pallet_weight']


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
