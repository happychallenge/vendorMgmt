from django.db import models
from products.models import Product, Vendor

# Create your models here.
class Client(models.Model):
    """docstring for Client"""
    """ 설명 """
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Demand(models.Model):
    """docstring for Demand"""
    """ 설명 """
    YEAR = ( (x, str(x)) for x in range(2017, 2031) )
    MONTH = ( (x, str(x)) for x in range(1, 13) )

    year = models.PositiveIntegerField(choices=YEAR)
    month = models.PositiveIntegerField(choices=MONTH)
    product = models.ForeignKey(Product)
    total_demand = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('product', 'year', 'month'),)

    def __str__(self):
        return "{} {} {}".format(self.product, 
            self.year, self.month)


class DemandClient(models.Model):
    """docstring for DemandClient"""
    """ 설명 """
    demand = models.ForeignKey(Demand)
    client = models.ForeignKey(Client)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('demand', 'client'),)

    def __str__(self):
        return "{} {} {}".format(self.demand, 
            self.client, self.amount)


class Supply(models.Model):
    """docstring for Supply"""
    """ 설명 """

    demand = models.OneToOneField(Demand)
    total_supply = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.demand, 
            self.total_supply)


class SupplyVendor(models.Model):
    """docstring for SupplyItem"""
    """ 설명 """
    supply = models.ForeignKey(Supply)

    vendor = models.ForeignKey(Vendor)
    amount = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, 
            blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('supply', 'vendor'),)
        
    def __str__(self):
        return "{} {}".format(self.vendor, self.amount)

    