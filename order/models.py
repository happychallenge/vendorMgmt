from django.db import models
from django.urls import reverse
from products.models import Vendor, Product, Contact, Quotation

# Create your models here.
class Customer(models.Model):
    """docstring for Customer"""
    """ 설명 """
    en_name = models.CharField(max_length=30, verbose_name='ENGLISH NAME')
    address = models.CharField(max_length=100, verbose_name='ENGLISH ADDRESS')
    tel = models.CharField(max_length=30)
    fax = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.en_name


# GP Purchase Order 
class POrder(models.Model):
    """docstring for POrder"""
    """ 설명 """
    offer_no = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    vendor = models.ForeignKey(Vendor)
    contact = models.ForeignKey(Contact)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    fixed = models.BooleanField(default=False)
    contract_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-contract_date", )

    def __str__(self):
        return self.name


POWDER = 'POWDER'
GRANULAR = 'GRANULAR'
LIQUID = 'LIQUID'
TYPE = (
    (POWDER, 'POWDER'),
    (GRANULAR, 'GRANULAR'),
    (LIQUID, 'LIQUID'),
)

CARTON = 'CARTON'
BAG = 'BAG'
DRUM = 'DRUM'
CYLINDER = 'CYLINDER'
EXTRA = 'EXTRA'
PACKINGTYPE = (
    (CARTON, 'CARTON'),
    (BAG, 'BAG'),
    (DRUM, 'DRUM'),
    (CYLINDER, 'CYLINDER'),
    (EXTRA, 'EXTRA'),
)

class Packing(models.Model):
    """docstring for Packing"""
    """ 설명 """
    product = models.ForeignKey(Product, related_name='packingproduct')
    ptype = models.CharField(max_length=10, choices=TYPE, default=POWDER)
    num = models.PositiveIntegerField()
    packing_type = models.CharField(max_length=10, 
            choices=PACKINGTYPE, default=BAG)
    unit_weight = models.IntegerField()
    pallet_weight = models.IntegerField(default=500)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ( 'product', 'ptype', 'num' )

    def __str__(self):
        return "{} {} {} {}".format(self.product, self.ptype, 
            self.packing_type, self.unit_weight)


class POrderItem(models.Model):
    """docstring for POrderItem"""
    """ 설명 """
    porder = models.ForeignKey(POrder)
    product = models.ForeignKey(Product)
    ptype = models.CharField(max_length=10, choices=TYPE, default=POWDER)
    amount = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    packing = models.ForeignKey(Packing, null=True, blank=True )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('porder', 'product', 'ptype'),)

    def __str__(self):
        return "POrder Item : {}".format(self.id)



class PayCondition(models.Model):
    """docstring for Delivery"""
    """ 설명 """
    CIF = 'CIF'
    FOB = 'FOB'
    PRICETERM = (
        (CIF, 'CIF'),
        (FOB, 'FOB'),
    )

    CASH = 'CASH'
    THIRTY = '30%PREPAY, 70%LATER'
    TT30 = 'T/T 30 DAYS'
    TT45 = 'T/T 45 DAYS'
    TT60 = 'T/T 60 DAYS'
    TT90 = 'T/T 90 DAYS'
    PAYTERM = (
        (CASH, 'CASH'),
        (THIRTY, '30%PREPAY, 70%LATER'),
        (TT30, 'T/T 30 DAYS'),
        (TT45, 'T/T 45 DAYS'),
        (TT60, 'T/T 60 DAYS'),
        (TT90, 'T/T 90 DAYS'),
    )

    porder = models.OneToOneField(POrder, on_delete=models.CASCADE)
    price_term = models.CharField(max_length=3, choices=PRICETERM, default=CIF)
    pay_term = models.CharField(max_length=20, choices=PAYTERM)

    def __str__(self):
        return "PayTerm {}".format(self.id)


# ShengPeng TiangGang  Sales Order 
class SalesOrder(models.Model):
    """docstring for SalesOrder"""
    """ 설명 """
    SALESCONTRACT = 10
    PURCHASECONTRACT = 20
    INVOICE_PACKINGLIST = 30
    SHIPMENT = 40
    EXPORT_DOCUMENT = 50
    MOMEYRECEIVED = 80
    TAXREFUND = 100
    
    PROGRESS = (
        (SALESCONTRACT, 'SALESCONTRACT'),
        (PURCHASECONTRACT, 'PURCHASECONTRACT'),
        (INVOICE_PACKINGLIST, 'INVOICE_PACKINGLIST'),
        (SHIPMENT, 'SHIPMENT'),
        (EXPORT_DOCUMENT, 'EXPORT_DOCUMENT'),
        (MOMEYRECEIVED, 'MOMEYRECEIVED'),
        (TAXREFUND, 'TAXREFUND'),
    )

    porder = models.ForeignKey(POrder, null=True, blank=True)
    progress = models.IntegerField(default=SALESCONTRACT, choices=PROGRESS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.porder)


class SalesOrderItem(models.Model):
    """docstring for SalesOrderItem"""
    """ 설명 """
    sales_order = models.ForeignKey(SalesOrder)
    sales_order_item = models.ForeignKey(POrderItem)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('sales_order', 'sales_order_item'),)

    def __str__(self):
        return "{} | {}".format(self.sales_order, self.sales_order_item)
    

class Shipping(models.Model):
    """docstring for Shipping"""
    """ 설명 """
    INCHEON = 'INCHEON'
    PUSAN = 'PUSAN'
    GUANGYANG = 'GUANGYANG'
    DESTINATION = (
        (INCHEON, 'INCHEON'),
        (PUSAN, 'PUSAN'),
        (GUANGYANG, 'GUANGYANG'),
    )

    porder = models.ForeignKey(POrder)
    sales_order = models.ForeignKey(SalesOrder, blank=True, null=True)
    destination = models.CharField(max_length=10, default=PUSAN, choices=DESTINATION)
    shipping_date = models.DateField(blank=True, null=True)
    comments = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Shipping {}".format(self.id)

