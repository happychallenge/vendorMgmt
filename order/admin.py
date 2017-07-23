from django.contrib import admin

from .models import Customer, POrder, POrderItem, PayCondition, Shipping
from .models import SalesOrder, SalesOrderItem
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    class Meta:
        model = Customer
    list_display = ['en_name', 'address']


class POrderItemInline(admin.TabularInline):
    model = POrderItem
    raw_id_fields = [ 'quotation', 'product']

class PayConditionInline(admin.TabularInline):
    model = PayCondition

class ShippingInline(admin.TabularInline):
    model = Shipping

@admin.register(POrder)
class POrderAdmin(admin.ModelAdmin):
    class Meta:
        model = POrder
    list_display = ['offer_no', 'name', 'vendor', 'contact', 'total_amount']
    inlines = [
        POrderItemInline, PayConditionInline, ShippingInline
    ]


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

