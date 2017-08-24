from django.db import models

from order.models import POrder
# Create your models here.
class Event(models.Model):
    """docstring for Event"""
    """ 설명 """

    CONTRACT = 'CONTRACT'
    SHIPPING = 'SHIPPING'
    PAYMENT = 'PAYMENT'
    TAXREFUND = 'TAXREFUND'
    TYPE = (
        (CONTRACT, 'CONTRACT'),
        (SHIPPING, 'SHIPPING'),
        (PAYMENT, 'PAYMENT'),
        (TAXREFUND, 'TAXREFUND'),
    )

    name = models.CharField(max_length=50)
    num = models.PositiveIntegerField()
    porder = models.ForeignKey(POrder, blank=True, null=True)
    etype = models.CharField(max_length=10, choices=TYPE)
    event_date = models.DateField()

    money = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=1, default='$')
    rmb = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cost(models.Model):
    PROFIT = 'PROFIT'
    COST = 'COST'
    CATEGORY = (
        (PROFIT, 'PROFIT'),
        (COST, 'COST'),
    )

    PURCHASE = 'PURCHASE'
    LOGISTICS = 'LOGISTICS'
    POSTING = 'POSTING'
    SALES = 'SALES'
    TAXREFUND = 'TAXREFUND'
    EXTRA = 'EXTRA'
    CTYPE = (
        (PURCHASE, 'PURCHASE'),
        (LOGISTICS, 'LOGISTICS'),
        (POSTING, 'POSTING'),
        (SALES, 'SALES'),
        (TAXREFUND, 'TAXREFUND'),
        (EXTRA, 'EXTRA'),
    )

    porder = models.ForeignKey(POrder)
    category = models.CharField(max_length=10, choices=CATEGORY)
    ctype = models.CharField(max_length=50, choices=CTYPE)
    cost = models.IntegerField()
    receipt = models.BooleanField(default=True)
    happen_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.porder, self.ctype )
