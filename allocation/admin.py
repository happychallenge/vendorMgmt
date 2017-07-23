from django.contrib import admin

from .models import Client, Demand, DemandClient, Supply, SupplyVendor

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    class Meta:
        model = Client
    list_display = [ 'name' ]


class DemandClientInline(admin.TabularInline):
    model = DemandClient
    raw_id_fields = ['client']


@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    class Meta:
        model = Demand
        ordering = [ ('year', 'month', 'product'), ]
    list_display = [ 'id', 'product', 'year', 'month', 'total_demand', 'created_at']
    search_fields = [ 'product__en_name' ]
    inlines = [
        DemandClientInline
    ]

class SupplyVendorInline(admin.TabularInline):
    model = SupplyVendor
    raw_id_fields = ['vendor']


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    class Meta:
        model = Supply
    list_display = [ 'id', 'demand', 'total_supply', 'created_at']
    search_fields = [ 'demand__product__en_name']
    inlines = [
        SupplyVendorInline
    ]

