from django.contrib import admin

from .models import Customer, POrder, POrderItem, PayCondition, Shipping
from .models import SalesOrder, SalesOrderItem, Packing, Shipping, Material
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    class Meta:
        model = Customer
    list_display = ['en_name', 'address']


class POrderItemInline(admin.TabularInline):
    model = POrderItem
    raw_id_fields = [ 'product']

class PayConditionInline(admin.TabularInline):
    model = PayCondition

class ShippingInline(admin.TabularInline):
    model = Shipping

@admin.register(POrder)
class POrderAdmin(admin.ModelAdmin):
    class Meta:
        model = POrder
    list_display = [ 'id', 'offer_no', 'name', 'vendor', 'contact', 'total_amount', 'get_payterm']
    list_display_links = [ 'offer_no', 'name', 'vendor' ]
    inlines = [
        PayConditionInline, POrderItemInline, ShippingInline
    ]

    def get_payterm(self, obj):
        return obj.paycondition.pay_term


class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    raw_id_fields = [ 'sales_order', 'sales_order_item']

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    class Meta:
        model = SalesOrder
    list_display = ['porder', 'progress']
    inlines = [
        SalesOrderItemInline
    ]


@admin.register(Packing)
class PackingAdmin(admin.ModelAdmin):
    class Meta:
        model = Packing
    list_display = ['product', 'ptype', 'num', 'packing_type', 'unit_weight', 'pallet_weight']


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    class Meta:
        model = Shipping
    list_display = ['id', 'porder', 'destination', 'shipping_date', 'comments']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    class Meta:
        model = Material
    list_display = ['shipping', 'invoice', 'packingList', 'billofLading']

